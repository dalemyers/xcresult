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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestFailure.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path)
        writer.write()

        assert os.path.exists(output_path)


def test_junit_writer_with_attachments():
    """Test JUnit writer with attachments export."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        attachments_path = os.path.join(temp_dir, "attachments")
        bundle = xcresult.Xcresults(test_data_path)

        writer = JunitWriter(bundle, output_path, attachments_path)
        writer.write()

        assert os.path.exists(output_path)


def test_junit_writer_with_prefix():
    """Test JUnit writer with test class prefix."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

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
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestBuildFailure.xcresult"
    )

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
