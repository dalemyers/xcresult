"""Junit writer for writing out the results of tests."""

# pylint: disable=c-extension-no-member

import os
from typing import Callable, cast
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

# A predicate used to decide whether a single test should appear in the report.
# It receives a test leaf and must return ``True`` to keep it or ``False`` to
# omit it entirely (it is then excluded from the emitted XML and from all
# tests/failures/skipped counts). Both ``identifier`` (e.g. "Class/testMethod()")
# and ``name`` are available on the supplied object for matching.
TestFilter = Callable[[ActionTestSummaryIdentifiableObject], bool]


class JunitWriter:
    """Junit writer for writing out the results of tests."""

    results: XcresultsBase
    junit_path: str
    export_attachments_path: str | None
    test_class_prefix: str | None
    test_class_suffix: str | None
    collapse_retries: bool
    test_filter: TestFilter | None

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        results: XcresultsBase,
        junit_path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
        collapse_retries: bool = False,
        test_filter: TestFilter | None = None,
    ) -> None:
        self.results = results
        self.junit_path = junit_path
        self.export_attachments_path = export_attachments_path
        self.test_class_prefix = test_class_prefix
        self.test_class_suffix = test_class_suffix
        self.collapse_retries = collapse_retries
        self.test_filter = test_filter

    # pylint: enable=too-many-positional-arguments

    def _collapse_retry_indices(
        self,
        tests: list[ActionTestSummaryIdentifiableObject],
    ) -> set[int]:
        """Collapse retry attempts of the same test down to one representative.

        Under ``xcodebuild ... -retry-tests-on-failure`` a test that fails and is
        retried appears as multiple leaves sharing one ``identifier``. Emitting a
        ``<testcase>`` per attempt inflates the totals and duplicates the test.
        This keeps a single representative per identifier: a successful attempt if
        any passed (a flaky pass), otherwise a failing attempt, otherwise the
        first attempt (e.g. all skipped).

        Leaves without an identifier cannot be matched to their retries, so each
        is kept as its own entry.

        Positions are returned rather than the leaves themselves so that the
        caller can tell which of several equal (or even identical) leaves was
        picked, without relying on object identity.

        :param tests: The flattened test leaves for a single testable summary.

        :returns: The indices into ``tests`` of the leaves to keep, one per
            distinct identifier.
        """

        order: list[str] = []
        attempts_by_key: dict[str, list[int]] = {}

        for index, test in enumerate(tests):
            # Key un-identified leaves by position so they never merge.
            key = test.identifier if test.identifier is not None else f"\x00{index}"
            if key not in attempts_by_key:
                attempts_by_key[key] = []
                order.append(key)
            attempts_by_key[key].append(index)

        retained: set[int] = set()
        for key in order:
            attempts = attempts_by_key[key]
            # A pass on any attempt wins (flaky pass); otherwise the first real
            # failure; otherwise the first attempt (covers an all-skipped group).
            chosen = next(
                (i for i in attempts if getattr(tests[i], "testStatus", None) == "Success"),
                None,
            )
            if chosen is None:
                chosen = next(
                    (i for i in attempts if getattr(tests[i], "testStatus", None) != "Skipped"),
                    None,
                )
            if chosen is None:
                chosen = attempts[0]
            retained.add(chosen)

        return retained

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
        """Generate the test suite.

        A ``<testsuite>`` is emitted per top level group in the testable summary,
        except for groups which contribute no test cases at all (either because
        they were empty, or because collapsing and filtering removed every leaf).

        :param root: The ``<testsuites>`` element to add the suites to
        :param summary: The testable summary to generate the suites for
        :param configuration_name: The name of the configuration the tests ran in

        :returns: A tuple of the number of tests, failures and skipped tests
        """

        total_tests = 0
        total_failures = 0
        total_skipped = 0

        # Flatten every top level group up front. `summary.tests` is typed as the
        # base identifiable object (generated model); the runtime elements are
        # groups/metadata that implement all_subtests.
        groups = list(summary.tests or [])
        group_subtests = [
            cast(
                list[ActionTestSummaryIdentifiableObject],
                group.all_subtests(),  # type: ignore[attr-defined]
            )
            for group in groups
        ]

        # Retries have to be collapsed across the whole testable summary rather
        # than per top level group. `xcodebuild ... -retry-tests-on-failure`
        # records the initial run and the retries in *separate* groups ("All
        # tests" and "Selected tests"), and starts another group whenever the
        # test host crashes. Collapsing per group would leave the stale first
        # attempt behind, so a test that crashed once and then passed on every
        # retry would still be reported as a failure. Survivors are tracked by
        # their position in the flattened list, so each one stays in the group it
        # actually ran in.
        retained_indices: set[int] | None = None
        if self.collapse_retries:
            retained_indices = self._collapse_retry_indices(
                [subtest for subtests in group_subtests for subtest in subtests]
            )

        group_start = 0

        for test, group_leaves in zip(groups, group_subtests):
            subtests = group_leaves
            if retained_indices is not None:
                subtests = [
                    subtest
                    for index, subtest in enumerate(group_leaves, start=group_start)
                    if index in retained_indices
                ]
            group_start += len(group_leaves)

            # Drop any tests the caller asked to exclude. Doing it here keeps the
            # emitted XML and the suite/root counts consistent without a second
            # pass over the document.
            if self.test_filter is not None:
                subtests = [subtest for subtest in subtests if self.test_filter(subtest)]

            # Collapsing moves a test into the group its winning attempt ran in,
            # which can empty out a retry group entirely. Emitting a suite with no
            # test cases in it would just be noise, so skip it.
            if not subtests:
                continue

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
