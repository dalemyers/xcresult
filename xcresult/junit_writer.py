"""Junit writer for writing out the results of tests."""

from typing import cast
import xml.etree.ElementTree as ET

from xcresult.exceptions import XcresultException
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

    def __init__(self, results: XcresultsBase) -> None:
        self.results = results

    def generate_test_case(
        self,
        suite: ET.Element,
        test: ActionTestMetadata,
    ) -> tuple[int, int, int]:
        """Generate the XML for a test case.

        :param suite: The suite to add the test case to
        :param test: The test to generate the XML for

        :returns: A tuple of the number of tests, failures and skipped tests
        """

        test_case = ET.SubElement(suite, "testcase")
        test_case_identifier = test.identifier or "Unknown Test"
        test_case.set("classname", test_case_identifier.split("/", maxsplit=1)[0])
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

        return 1, 1, 0

    def generate_test_suite(
        self,
        root: ET.Element,
        summary: ActionTestableSummary,
        configuration_name: str,
    ) -> tuple[int, int, int]:
        """Generate the test suite."""
        suite = ET.SubElement(root, "testsuite")
        suite.set("name", summary.name or "Unknown Suite")

        if len(summary.tests) != 1:
            raise XcresultException(
                "Only one test per testable summary is supported. Please file a bug with your xcresult if you encounter this issue."
            )

        # We get an identifiable, but that "protocol" isn't guaranteed to have a duration
        suite.set("time", str(getattr(summary.tests[0], "duration", 0)))

        properties = ET.SubElement(suite, "properties")
        configuration = ET.SubElement(properties, "property")
        configuration.set("name", "Configuration")
        configuration.set("value", configuration_name)

        total_tests = 0
        total_failures = 0
        total_skipped = 0

        all_tests = summary.all_tests()

        for test in all_tests:
            test_count, failure_count, skipped_count = self.generate_test_case(suite, test)
            total_tests += test_count
            total_failures += failure_count
            total_skipped += skipped_count

        suite.set("tests", str(total_tests))
        suite.set("failures", str(total_failures))
        suite.set("skipped", str(total_skipped))

        return total_tests, total_failures, total_skipped

    def write(self, path: str) -> None:
        """Get the test results."""

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
                        root, testable_summary, run_summary.name or "Unknown Configuration"
                    )
                    total_tests += test_count
                    total_failures += failure_count
                    total_skipped += skipped_count

        root.set("tests", str(total_tests))
        root.set("failures", str(total_failures))
        root.set("skipped", str(total_skipped))

        tree = ET.ElementTree(root)

        ET.indent(tree, space="    ", level=0)

        with open(path, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
