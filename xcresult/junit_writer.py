"""Junit writer for writing out the results of tests."""

# pylint: disable=c-extension-no-member

import os
from typing import cast
from lxml import etree as ET

from xcresult.model import (
    ActionTestMetadata,
    ActionTestSummary,
    ActionTestSummaryIdentifiableObject,
    ActionTestableSummary,
    ActionTestPlanRunSummaries,
)
from xcresult.xcresult_base import XcresultsBase
from xcresult.xcresulttool import deserialize

# lxml exposes its element type only via the underscore-prefixed name.
Element = ET._Element  # pylint: disable=protected-access  # pyright: ignore[reportPrivateUsage]


class JunitWriter:
    """Junit writer for writing out the results of tests."""

    results: XcresultsBase
    junit_path: str
    export_attachments_path: str | None
    test_class_prefix: str | None
    test_class_suffix: str | None
    collapse_retries: bool

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        results: XcresultsBase,
        junit_path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
        collapse_retries: bool = False,
    ) -> None:
        self.results = results
        self.junit_path = junit_path
        self.export_attachments_path = export_attachments_path
        self.test_class_prefix = test_class_prefix
        self.test_class_suffix = test_class_suffix
        self.collapse_retries = collapse_retries

    # pylint: enable=too-many-positional-arguments

    def _collapse_retries(
        self,
        tests: list[ActionTestSummaryIdentifiableObject],
    ) -> list[ActionTestSummaryIdentifiableObject]:
        """Collapse retry attempts of the same test into one representative.

        Under ``xcodebuild ... -retry-tests-on-failure`` a test that fails and is
        retried appears as multiple leaves sharing one ``identifier``. Emitting a
        ``<testcase>`` per attempt inflates the totals and duplicates the test.
        This keeps a single representative per identifier: a successful attempt if
        any passed (a flaky pass), otherwise a failing attempt, otherwise the
        first attempt (e.g. all skipped). First-seen order is preserved.

        Leaves without an identifier cannot be matched to their retries, so each
        is kept as its own entry.

        :param tests: The flattened test leaves for a single suite.

        :returns: One representative test per distinct identifier.
        """

        order: list[str] = []
        groups: dict[str, list[ActionTestSummaryIdentifiableObject]] = {}

        for test in tests:
            # Key un-identified leaves by object identity so they never merge.
            key = test.identifier if test.identifier is not None else f"\x00{id(test)}"
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(test)

        representatives: list[ActionTestSummaryIdentifiableObject] = []
        for key in order:
            attempts = groups[key]
            # A pass on any attempt wins (flaky pass); otherwise the first real
            # failure; otherwise the first attempt (covers an all-skipped group).
            chosen = next(
                (t for t in attempts if getattr(t, "testStatus", None) == "Success"),
                None,
            )
            if chosen is None:
                chosen = next(
                    (t for t in attempts if getattr(t, "testStatus", None) != "Skipped"),
                    None,
                )
            if chosen is None:
                chosen = attempts[0]
            representatives.append(chosen)

        return representatives

    def generate_test_case(
        self,
        suite: Element,
        test: ActionTestMetadata,
    ) -> tuple[int, int, int]:
        """Generate the XML for a test case.

        :param suite: The suite to add the test case to
        :param test: The test to generate the XML for

        :returns: A tuple of the number of tests, failures and skipped tests
        """

        test_case = ET.SubElement(suite, "testcase")  # type: ignore[arg-type]
        test_case_identifier = test.identifier or "Unknown Test"
        test_case_identifier = test_case_identifier.split("/", maxsplit=1)[0]

        if self.test_class_prefix:
            test_case_identifier = f"{self.test_class_prefix}.{test_case_identifier}"

        if self.test_class_suffix:
            test_case_identifier = f"{test_case_identifier}.{self.test_class_suffix}"

        test_case.set("classname", test_case_identifier)
        test_case.set("name", test.name or "Unknown Test")
        test_case.set("time", str(test.duration))

        if test.testStatus == "Success":
            return 1, 0, 0

        if test.testStatus == "Skipped":
            _ = ET.SubElement(test_case, "skipped")
            return 1, 0, 1

        if test.summaryRef is None:
            failure_element = ET.SubElement(test_case, "failure")
            failure_element.set("message", "Unknown failure due to missing summary ref.")
            return 1, 1, 0

        base_failure = cast(ActionTestSummary, deserialize(self.results.get(test.summaryRef.id)))

        for failure in base_failure.failureSummaries:
            if (
                failure.sourceCodeContext is None
                or failure.sourceCodeContext.location is None
                or failure.sourceCodeContext.location.filePath is None
            ):
                line = "Unknown location"
            else:
                line = failure.sourceCodeContext.location.filePath
                line += f"#EndingLineNumber={failure.sourceCodeContext.location.lineNumber}&"
                line += f"StartingLineNumber={failure.sourceCodeContext.location.lineNumber}"
            failure_element = ET.SubElement(test_case, "failure")
            failure_element.set("message", f"{failure.message} ({line})")

        if not self.export_attachments_path:
            return 1, 1, 0

        assert (
            test.identifierURL is not None
        ), f"Test identifier URL is None for test {test_case_identifier}. Unable to export attachments."

        test_attachments_relative_path = test.identifierURL.replace("test://com.apple.xcode/", "")
        test_attachments_path = os.path.join(
            self.export_attachments_path, test_attachments_relative_path
        )

        cdata = []

        for attachment_name in os.listdir(test_attachments_path):
            attachment_path = os.path.join(test_attachments_path, attachment_name)
            coverage_relative_path = os.path.relpath(
                attachment_path, os.path.dirname(self.junit_path)
            )
            cdata.append(f"[[ATTACHMENT|{coverage_relative_path}]]")  # type: ignore[arg-type]

        system_out = ET.SubElement(test_case, "system-out")
        system_out.text = ET.CDATA("\n" + "\n".join(cdata) + "\n")  # type: ignore[arg-type]

        return 1, 1, 0

    def generate_test_suite(
        self,
        root: Element,
        summary: ActionTestableSummary,
        configuration_name: str,
    ) -> tuple[int, int, int]:
        """Generate the test suite."""

        total_tests = 0
        total_failures = 0
        total_skipped = 0

        for test in summary.tests:
            suite = ET.SubElement(root, "testsuite")  # type: ignore[arg-type]
            suite.set("name", f"{summary.name}/{test.identifier}" or "Unknown Suite")

            # We get an identifiable, but that "protocol" isn't guaranteed to have a duration
            suite.set("time", str(getattr(test, "duration", 0)))

            properties = ET.SubElement(suite, "properties")
            configuration = ET.SubElement(properties, "property")
            configuration.set("name", "Configuration")
            configuration.set("value", configuration_name)

            suite_total_tests = 0
            suite_total_failures = 0
            suite_total_skipped = 0

            # `summary.tests` is typed as the base identifiable object (generated
            # model); the runtime elements are groups/metadata that implement
            # all_subtests.
            subtests = cast(
                list[ActionTestSummaryIdentifiableObject],
                test.all_subtests(),  # type: ignore[attr-defined]
            )
            if self.collapse_retries:
                subtests = self._collapse_retries(subtests)

            for subtest in subtests:
                if not isinstance(subtest, ActionTestMetadata):
                    raise TypeError(f"Expected ActionTestMetadata, got {type(subtest)}")

                test_count, failure_count, skipped_count = self.generate_test_case(suite, subtest)
                suite_total_tests += test_count
                suite_total_failures += failure_count
                suite_total_skipped += skipped_count

            suite.set("tests", str(suite_total_tests))
            suite.set("failures", str(suite_total_failures))
            suite.set("skipped", str(suite_total_skipped))

            total_tests += suite_total_tests
            total_failures += suite_total_failures
            total_skipped += suite_total_skipped

        return total_tests, total_failures, total_skipped

    def write(self) -> None:
        """Get the test results."""

        if self.export_attachments_path:
            self.results.export_test_attachments(self.export_attachments_path)

        root = ET.Element("testsuites")

        action_results = [r.actionResult for r in self.results.actions_invocation_record.actions]

        test_refs = [ar.testsRef for ar in action_results if ar.testsRef is not None]
        test_identifiers = [tr.id for tr in test_refs]

        summaries = [
            cast(
                ActionTestPlanRunSummaries,
                deserialize(self.results.get(test_identifier)),
            )
            for test_identifier in test_identifiers
        ]

        total_tests = 0
        total_failures = 0
        total_skipped = 0

        for summary in summaries:
            for run_summary in summary.summaries:
                for testable_summary in run_summary.testableSummaries:
                    test_count, failure_count, skipped_count = self.generate_test_suite(  # type: ignore[arg-type]
                        root,
                        testable_summary,
                        run_summary.name or "Unknown Configuration",
                    )
                    total_tests += test_count
                    total_failures += failure_count
                    total_skipped += skipped_count

        root.set("tests", str(total_tests))
        root.set("failures", str(total_failures))
        root.set("skipped", str(total_skipped))

        tree = ET.ElementTree(root)

        ET.indent(tree, space="    ", level=0)

        with open(self.junit_path, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)
