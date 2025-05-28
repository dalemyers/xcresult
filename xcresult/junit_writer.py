"""Junit writer for writing out the results of tests."""

# pylint: disable=c-extension-no-member

import os
from typing import cast
from lxml import etree as ET

from xcresult.model import (
    ActionTestMetadata,
    ActionTestSummary,
    ActionTestableSummary,
    ActionTestPlanRunSummaries,
)
from xcresult.xcresult_base import XcresultsBase
from xcresult.xcresulttool import deserialize


class JunitWriter:
    """Junit writer for writing out the results of tests."""

    results: XcresultsBase
    junit_path: str
    export_attachments_path: str | None
    test_class_prefix: str | None
    test_class_suffix: str | None

    def __init__(
        self,
        results: XcresultsBase,
        junit_path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
    ) -> None:
        self.results = results
        self.junit_path = junit_path
        self.export_attachments_path = export_attachments_path
        self.test_class_prefix = test_class_prefix
        self.test_class_suffix = test_class_suffix

    def generate_test_case(
        self,
        suite: ET.Element,  # type: ignore
        test: ActionTestMetadata,
    ) -> tuple[int, int, int]:
        """Generate the XML for a test case.

        :param suite: The suite to add the test case to
        :param test: The test to generate the XML for

        :returns: A tuple of the number of tests, failures and skipped tests
        """

        test_case = ET.SubElement(suite, "testcase")
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
            cdata.append(f"[[ATTACHMENT|{coverage_relative_path}]]")

        system_out = ET.SubElement(test_case, "system-out")
        system_out.text = ET.CDATA("\n" + "\n".join(cdata) + "\n")

        return 1, 1, 0

    def generate_test_suite(
        self,
        root: ET.Element,  # type: ignore
        summary: ActionTestableSummary,
        configuration_name: str,
    ) -> tuple[int, int, int]:
        """Generate the test suite."""

        for test in summary.tests:
            suite = ET.SubElement(root, "testsuite")
            suite.set("name", f"{summary.name}/{test.identifier}" or "Unknown Suite")

            # We get an identifiable, but that "protocol" isn't guaranteed to have a duration
            suite.set("time", str(getattr(test, "duration", 0)))

            properties = ET.SubElement(suite, "properties")
            configuration = ET.SubElement(properties, "property")
            configuration.set("name", "Configuration")
            configuration.set("value", configuration_name)

            all_tests = summary.all_tests()

            total_tests = 0
            total_failures = 0
            total_skipped = 0

            for test in all_tests:
                if not isinstance(test, ActionTestMetadata):
                    raise TypeError(f"Expected ActionTestMetadata, got {type(test)}")

                test_count, failure_count, skipped_count = self.generate_test_case(suite, test)
                total_tests += test_count
                total_failures += failure_count
                total_skipped += skipped_count

            suite.set("tests", str(total_tests))
            suite.set("failures", str(total_failures))
            suite.set("skipped", str(total_skipped))

        return total_tests, total_failures, total_skipped

    def write(self) -> None:
        """Get the test results."""

        if self.export_attachments_path:
            self.results.export_test_attachments(self.export_attachments_path)

        root = ET.Element("testsuites")

        action_results = [
            r.actionResult
            for r in self.results.actions_invocation_record.actions
            if r.actionResult is not None
        ]

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
                    test_count, failure_count, skipped_count = self.generate_test_suite(
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
