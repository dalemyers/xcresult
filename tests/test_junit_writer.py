"""Test JUnit writer functionality."""

import os
import sys
import tempfile
from lxml import etree as ET

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.junit_writer import JunitWriter

# pylint: enable=wrong-import-position


def test_junit_writer_success():
    """Test JUnit writer with successful tests."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)
        writer.write()

        assert os.path.exists(output_path)

        # Parse and validate the XML
        tree = ET.parse(output_path)
        root = tree.getroot()
        assert root.tag == "testsuites"


def test_junit_writer_with_failures():
    """Test JUnit writer with test failures."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestFailure.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)
        writer.write()

        assert os.path.exists(output_path)

        # Parse and validate the XML
        tree = ET.parse(output_path)
        root = tree.getroot()
        assert root.tag == "testsuites"

        # Check for failures
        failures = root.xpath("//failure")
        assert len(failures) > 0


def test_junit_writer_with_skipped():
    """Test JUnit writer with skipped tests."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)
        writer.write()

        assert os.path.exists(output_path)


def test_junit_writer_with_attachments():
    """Test JUnit writer with attachments export."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        attachments_path = os.path.join(temp_dir, "attachments")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path, attachments_path)
        writer.write()

        assert os.path.exists(output_path)


def test_junit_writer_with_prefix():
    """Test JUnit writer with test class prefix."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path, test_class_prefix="MyPrefix")
        writer.write()

        assert os.path.exists(output_path)

        # Parse and validate the XML
        tree = ET.parse(output_path)
        # Check that at least one testcase has the prefix
        testcases = tree.xpath("//testcase")
        if testcases:
            classname = testcases[0].get("classname")
            assert classname is not None
            assert "MyPrefix." in classname


def test_junit_writer_with_suffix():
    """Test JUnit writer with test class suffix."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path, test_class_suffix="MySuffix")
        writer.write()

        assert os.path.exists(output_path)

        # Parse and validate the XML
        tree = ET.parse(output_path)
        # Check that at least one testcase has the suffix
        testcases = tree.xpath("//testcase")
        if testcases:
            classname = testcases[0].get("classname")
            assert classname is not None
            assert ".MySuffix" in classname


def test_junit_writer_with_prefix_and_suffix():
    """Test JUnit writer with both prefix and suffix."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(
            bundle,
            output_path,
            test_class_prefix="MyPrefix",
            test_class_suffix="MySuffix",
        )
        writer.write()

        assert os.path.exists(output_path)


def test_generate_test_case_success():
    """Test generating a test case for a successful test."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)

        # Create a mock test
        suite = ET.Element("testsuite")
        test = xcresult.ActionTestMetadata()
        test.identifier = "TestClass/testMethod"
        test.name = "testMethod"
        test.duration = 1.5
        test.testStatus = "Success"

        tests, failures, skipped = writer.generate_test_case(suite, test)
        assert tests == 1
        assert failures == 0
        assert skipped == 0


def test_generate_test_case_skipped():
    """Test generating a test case for a skipped test."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)

        suite = ET.Element("testsuite")
        test = xcresult.ActionTestMetadata()
        test.identifier = "TestClass/testMethod"
        test.name = "testMethod"
        test.duration = 0.0
        test.testStatus = "Skipped"

        tests, failures, skipped = writer.generate_test_case(suite, test)
        assert tests == 1
        assert failures == 0
        assert skipped == 1


def test_generate_test_case_failure_no_summary_ref():
    """Test generating a test case for a failed test with no summary ref."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)

        suite = ET.Element("testsuite")
        test = xcresult.ActionTestMetadata()
        test.identifier = "TestClass/testMethod"
        test.name = "testMethod"
        test.duration = 1.5
        test.testStatus = "Failed"
        test.summaryRef = None

        tests, failures, skipped = writer.generate_test_case(suite, test)
        assert tests == 1
        assert failures == 1
        assert skipped == 0


def test_generate_test_suite():
    """Test generating a test suite."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)

        root = ET.Element("testsuites")

        # Get a real testable summary
        if bundle.actions_invocation_record.actions:
            action = bundle.actions_invocation_record.actions[0]
            if action.actionResult.testsRef:
                from xcresult.xcresulttool import get_test_plan_run_summaries

                summaries = get_test_plan_run_summaries(
                    test_data_path, action.actionResult.testsRef.id
                )
                if summaries.summaries and summaries.summaries[0].testableSummaries:
                    testable = summaries.summaries[0].testableSummaries[0]
                    tests, failures, skipped = writer.generate_test_suite(
                        root, testable, "Test Configuration"
                    )
                    assert tests >= 0
                    assert failures >= 0
                    assert skipped >= 0


def test_junit_writer_build_failure():
    """Test JUnit writer with build failure."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestBuildFailure.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        try:
            writer = JunitWriter(bundle, output_path)
            writer.write()
            assert os.path.exists(output_path)
        except (TypeError, AttributeError):
            # If there are no test results in the bundle, this is expected
            pass


def test_junit_suite_counts_match_actual_tests():
    """Test that each test suite's counts match the actual test cases in that suite.

    This test would have caught a bug where each suite was counting ALL tests
    instead of just its own tests, because the code was using summary.all_tests()
    instead of test.all_subtests().
    """
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)
        writer.write()

        assert os.path.exists(output_path)

        # Parse the XML
        tree = ET.parse(output_path)
        root = tree.getroot()
        assert root.tag == "testsuites"

        # Get all test suites
        suites = root.findall("testsuite")

        # Verify each suite's counts match the actual test cases in that suite
        total_tests_from_suites = 0
        total_failures_from_suites = 0
        total_skipped_from_suites = 0

        for suite in suites:
            # Get the declared counts from the suite attributes
            declared_tests = int(suite.get("tests", "0"))
            declared_failures = int(suite.get("failures", "0"))
            declared_skipped = int(suite.get("skipped", "0"))

            # Count the actual test cases in this suite
            testcases = suite.findall("testcase")
            actual_tests = len(testcases)
            actual_failures = len(suite.findall(".//failure"))
            actual_skipped = len(suite.findall(".//skipped"))

            # Each suite should report only its own test counts
            assert declared_tests == actual_tests, (
                f"Suite '{suite.get('name')}' declares {declared_tests} tests "
                f"but contains {actual_tests} test cases"
            )
            assert declared_failures == actual_failures, (
                f"Suite '{suite.get('name')}' declares {declared_failures} failures "
                f"but contains {actual_failures} failure elements"
            )
            assert declared_skipped == actual_skipped, (
                f"Suite '{suite.get('name')}' declares {declared_skipped} skipped "
                f"but contains {actual_skipped} skipped elements"
            )

            total_tests_from_suites += declared_tests
            total_failures_from_suites += declared_failures
            total_skipped_from_suites += declared_skipped

        # Verify the root testsuites totals match the sum of all suites
        root_tests = int(root.get("tests", "0"))
        root_failures = int(root.get("failures", "0"))
        root_skipped = int(root.get("skipped", "0"))

        assert (
            root_tests == total_tests_from_suites
        ), f"Root declares {root_tests} tests but suites sum to {total_tests_from_suites}"
        assert (
            root_failures == total_failures_from_suites
        ), f"Root declares {root_failures} failures but suites sum to {total_failures_from_suites}"
        assert (
            root_skipped == total_skipped_from_suites
        ), f"Root declares {root_skipped} skipped but suites sum to {total_skipped_from_suites}"


def test_generate_test_suite_with_multiple_test_groups():
    """Test generating test suites with multiple test groups.

    This test explicitly checks the bug where summary.all_tests() was being
    called instead of test.all_subtests(), which would cause each suite to
    count ALL tests instead of just its own tests.
    """
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)

        root = ET.Element("testsuites")

        # Create a mock summary with multiple test groups
        mock_summary = xcresult.ActionTestableSummary()
        mock_summary.name = "MockTestTarget"

        # Create first test group with 2 tests
        test_group1 = xcresult.ActionTestSummaryGroup()
        test_group1.identifier = "TestSuite1"

        test1 = xcresult.ActionTestMetadata()
        test1.identifier = "TestSuite1/test1"
        test1.name = "test1"
        test1.duration = 1.0
        test1.testStatus = "Success"

        test2 = xcresult.ActionTestMetadata()
        test2.identifier = "TestSuite1/test2"
        test2.name = "test2"
        test2.duration = 1.0
        test2.testStatus = "Success"

        test_group1.subtests = [test1, test2]

        # Create second test group with 3 tests
        test_group2 = xcresult.ActionTestSummaryGroup()
        test_group2.identifier = "TestSuite2"

        test3 = xcresult.ActionTestMetadata()
        test3.identifier = "TestSuite2/test3"
        test3.name = "test3"
        test3.duration = 1.0
        test3.testStatus = "Success"

        test4 = xcresult.ActionTestMetadata()
        test4.identifier = "TestSuite2/test4"
        test4.name = "test4"
        test4.duration = 1.0
        test4.testStatus = "Failed"
        test4.summaryRef = None

        test5 = xcresult.ActionTestMetadata()
        test5.identifier = "TestSuite2/test5"
        test5.name = "test5"
        test5.duration = 1.0
        test5.testStatus = "Skipped"

        test_group2.subtests = [test3, test4, test5]

        mock_summary.tests = [test_group1, test_group2]

        # Generate the test suites
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, mock_summary, "Test Configuration"
        )

        # With the bug (using summary.all_tests()), each suite would count all 5 tests
        # The bug would cause:
        # - Suite 1: 5 tests, 1 failure, 1 skipped
        # - Suite 2: 5 tests, 1 failure, 1 skipped
        # - Total: 10 tests, 2 failures, 2 skipped
        #
        # With the fix (using test.all_subtests()), we should get:
        # - Suite 1: 2 tests, 0 failures, 0 skipped
        # - Suite 2: 3 tests, 1 failure, 1 skipped
        # - Total: 5 tests, 1 failure, 1 skipped

        # Check the totals returned by generate_test_suite
        assert total_tests == 5, f"Expected 5 total tests, got {total_tests}"
        assert total_failures == 1, f"Expected 1 total failure, got {total_failures}"
        assert total_skipped == 1, f"Expected 1 total skipped, got {total_skipped}"

        # Parse and verify individual suite counts
        suites = root.findall("testsuite")
        assert len(suites) == 2, f"Expected 2 suites, got {len(suites)}"

        # Check suite 1 (TestSuite1)
        suite1 = suites[0]
        suite1_tests = int(suite1.get("tests", "0"))
        suite1_failures = int(suite1.get("failures", "0"))
        suite1_skipped = int(suite1.get("skipped", "0"))
        assert suite1_tests == 2, (
            f"Suite 1 should have 2 tests, got {suite1_tests}. "
            "Bug: using summary.all_tests() instead of test.all_subtests()"
        )
        assert suite1_failures == 0, f"Suite 1 should have 0 failures, got {suite1_failures}"
        assert suite1_skipped == 0, f"Suite 1 should have 0 skipped, got {suite1_skipped}"

        # Check suite 2 (TestSuite2)
        suite2 = suites[1]
        suite2_tests = int(suite2.get("tests", "0"))
        suite2_failures = int(suite2.get("failures", "0"))
        suite2_skipped = int(suite2.get("skipped", "0"))
        assert suite2_tests == 3, (
            f"Suite 2 should have 3 tests, got {suite2_tests}. "
            "Bug: using summary.all_tests() instead of test.all_subtests()"
        )
        assert suite2_failures == 1, f"Suite 2 should have 1 failure, got {suite2_failures}"
        assert suite2_skipped == 1, f"Suite 2 should have 1 skipped, got {suite2_skipped}"


def _retry_meta(identifier: str, name: str, status: str) -> "xcresult.ActionTestMetadata":
    """Build a leaf test result for the retry fixtures."""
    meta = xcresult.ActionTestMetadata()
    meta.identifier = identifier
    meta.name = name
    meta.duration = 1.0
    meta.testStatus = status
    # summaryRef None keeps generate_test_case from touching the bundle.
    meta.summaryRef = None
    return meta


def _retry_summary() -> "xcresult.ActionTestableSummary":
    """A testable whose suite holds retried tests (duplicate identifiers).

    Mirrors ``-retry-tests-on-failure``: ``flaky()`` fails then passes (a flaky
    pass), ``fails()`` fails twice (never passes), plus a clean pass and a skip.
    Distinct tests: 4 (1 pass, 1 flaky-pass, 1 fail, 1 skip). Raw leaves: 6.
    """
    summary = xcresult.ActionTestableSummary()
    summary.name = "MockTarget"

    group = xcresult.ActionTestSummaryGroup()
    group.identifier = "FlakySuite"
    group.subtests = [
        _retry_meta("FlakySuite/flaky()", "flaky()", "Failed"),
        _retry_meta("FlakySuite/flaky()", "flaky()", "Success"),
        _retry_meta("FlakySuite/passes()", "passes()", "Success"),
        _retry_meta("FlakySuite/fails()", "fails()", "Failed"),
        _retry_meta("FlakySuite/fails()", "fails()", "Failed"),
        _retry_meta("FlakySuite/skips()", "skips()", "Skipped"),
    ]
    summary.tests = [group]
    return summary


def test_collapse_retries_off_counts_every_attempt():
    """Default behavior (collapse_retries=False) emits one testcase per attempt."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        writer = JunitWriter(bundle, os.path.join(temp_dir, "junit.xml"))

        root = ET.Element("testsuites")
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, _retry_summary(), "Test Configuration"
        )

        # 6 raw leaves: failed flaky attempt + 2 failed fails() attempts = 3 failures.
        assert total_tests == 6, f"Expected 6 (every attempt), got {total_tests}"
        assert total_failures == 3, f"Expected 3 failures, got {total_failures}"
        assert total_skipped == 1, f"Expected 1 skipped, got {total_skipped}"

        # flaky() appears twice (once per attempt) when not collapsing.
        flaky_cases = root.xpath("//testcase[@name='flaky()']")
        assert len(flaky_cases) == 2, f"Expected 2 flaky() cases, got {len(flaky_cases)}"


def test_collapse_retries_on_merges_attempts():
    """collapse_retries=True keeps one testcase per identifier with the final result."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        writer = JunitWriter(bundle, os.path.join(temp_dir, "junit.xml"), collapse_retries=True)

        root = ET.Element("testsuites")
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, _retry_summary(), "Test Configuration"
        )

        # 4 distinct tests: passes(), flaky() (passed on retry), fails(), skips().
        assert total_tests == 4, f"Expected 4 distinct tests, got {total_tests}"
        assert total_failures == 1, f"Expected 1 failure (fails()), got {total_failures}"
        assert total_skipped == 1, f"Expected 1 skipped, got {total_skipped}"

        # flaky() collapses to a single PASSING testcase (no <failure> child).
        flaky_cases = root.xpath("//testcase[@name='flaky()']")
        assert len(flaky_cases) == 1, f"Expected 1 flaky() case, got {len(flaky_cases)}"
        assert not flaky_cases[0].findall("failure"), "flaky() should collapse to a pass"

        # fails() collapses to a single FAILING testcase.
        fails_cases = root.xpath("//testcase[@name='fails()']")
        assert len(fails_cases) == 1, f"Expected 1 fails() case, got {len(fails_cases)}"
        assert fails_cases[0].findall("failure"), "fails() should remain a failure"


def test_collapse_retries_keeps_anon_tests_separate():
    """Leaves without an identifier are never merged together when collapsing."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        writer = JunitWriter(bundle, os.path.join(temp_dir, "junit.xml"), collapse_retries=True)

        summary = xcresult.ActionTestableSummary()
        summary.name = "MockTarget"
        group = xcresult.ActionTestSummaryGroup()
        group.identifier = "Suite"
        first = _retry_meta("", "anon-a", "Success")
        first.identifier = None
        second = _retry_meta("", "anon-b", "Success")
        second.identifier = None
        group.subtests = [first, second]
        summary.tests = [group]

        root = ET.Element("testsuites")
        total_tests, _, _ = writer.generate_test_suite(root, summary, "Test Configuration")

        assert total_tests == 2, f"Un-identified leaves must not merge, got {total_tests}"


def test_test_filter_excludes_matching_tests():
    """A test_filter returning False drops the test from XML and from the counts."""
    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(
            os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
        )

        # Exclude the two flaky leaves (failed flaky attempt + both fails() attempts).
        def keep(test: "xcresult.ActionTestSummaryIdentifiableObject") -> bool:
            return (test.name or "") not in {"flaky()", "fails()"}

        writer = JunitWriter(bundle, os.path.join(temp_dir, "junit.xml"), test_filter=keep)

        root = ET.Element("testsuites")
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, _retry_summary(), "Test Configuration"
        )

        # Started with 6 leaves (3 failures, 1 skip). Dropping flaky() (2 leaves)
        # and fails() (2 leaves) leaves passes() + skips() = 2 tests, 0 failures.
        assert total_tests == 2, f"Expected 2 remaining, got {total_tests}"
        assert total_failures == 0, f"Expected 0 failures after filtering, got {total_failures}"
        assert total_skipped == 1, f"Expected 1 skipped, got {total_skipped}"

        assert not root.xpath("//testcase[@name='flaky()']")
        assert not root.xpath("//testcase[@name='fails()']")
        assert root.xpath("//testcase[@name='passes()']")


def test_test_filter_none_keeps_everything():
    """Omitting test_filter is equivalent to keeping every test (default behavior)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(
            os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
        )
        writer = JunitWriter(bundle, os.path.join(temp_dir, "junit.xml"), test_filter=None)

        root = ET.Element("testsuites")
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, _retry_summary(), "Test Configuration"
        )

        assert total_tests == 6, f"Expected all 6 leaves, got {total_tests}"
        assert total_failures == 3, f"Expected 3 failures, got {total_failures}"
        assert total_skipped == 1, f"Expected 1 skipped, got {total_skipped}"


def test_test_filter_composes_with_collapse_retries():
    """Filtering runs after collapsing, so excluded identifiers drop post-merge."""
    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(
            os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
        )

        def keep(test: "xcresult.ActionTestSummaryIdentifiableObject") -> bool:
            return (test.name or "") != "fails()"

        writer = JunitWriter(
            bundle,
            os.path.join(temp_dir, "junit.xml"),
            collapse_retries=True,
            test_filter=keep,
        )

        root = ET.Element("testsuites")
        total_tests, total_failures, total_skipped = writer.generate_test_suite(
            root, _retry_summary(), "Test Configuration"
        )

        # Collapsed distinct tests: passes(), flaky() (flaky pass), fails(), skips() = 4.
        # Dropping fails() leaves 3 tests, and the only failure is gone.
        assert total_tests == 3, f"Expected 3 after collapse+filter, got {total_tests}"
        assert total_failures == 0, f"Expected 0 failures, got {total_failures}"
        assert total_skipped == 1, f"Expected 1 skipped, got {total_skipped}"
        assert not root.xpath("//testcase[@name='fails()']")
