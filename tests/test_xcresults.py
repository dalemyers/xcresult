"""Test Xcresults class."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.exceptions import MissingPropertyException

# pylint: enable=wrong-import-position


def test_xcresults_init_absolute_path():
    """Test Xcresults initialization with absolute path."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )
    bundle = xcresult.Xcresults(test_data_path)
    assert bundle.path == test_data_path


def test_xcresults_init_relative_path():
    """Test Xcresults initialization with relative path."""
    cwd = os.getcwd()
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )
    rel_path = os.path.relpath(test_data_path, cwd)
    bundle = xcresult.Xcresults(rel_path)
    assert bundle.path == os.path.join(cwd, rel_path)


def test_actions_invocation_record_caching():
    """Test that actions invocation record is cached."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )
    bundle = xcresult.Xcresults(test_data_path)

    # First call
    record1 = bundle.actions_invocation_record
    # Second call should return the same cached object
    record2 = bundle.actions_invocation_record

    assert record1 is record2


def test_get():
    """Test the get method."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )
    bundle = xcresult.Xcresults(test_data_path)

    # Get an identifier from the bundle
    if bundle.actions_invocation_record.actions:
        action = bundle.actions_invocation_record.actions[0]
        if action.actionResult.testsRef:
            test_id = action.actionResult.testsRef.id
            result = bundle.get(test_id)
            assert isinstance(result, dict)


def test_export_attachment():
    """Test the export_attachment method."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestFailure.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Try to find an attachment to export
        if bundle.actions_invocation_record.actions:
            action = bundle.actions_invocation_record.actions[0]
            if action.actionResult.testsRef:
                from xcresult.xcresulttool import (
                    get_test_plan_run_summaries,
                    get_action_test_summary,
                )

                summaries = get_test_plan_run_summaries(
                    test_data_path, action.actionResult.testsRef.id
                )
                if summaries.summaries and summaries.summaries[0].testableSummaries:
                    testable = summaries.summaries[0].testableSummaries[0]
                    all_tests = testable.all_tests()
                    for test in all_tests:
                        if (
                            isinstance(test, xcresult.ActionTestMetadata)
                            and test.summaryRef
                        ):
                            summary = get_action_test_summary(
                                test_data_path, test.summaryRef.id
                            )
                            if summary.activitySummaries:
                                for activity in summary.activitySummaries:
                                    if activity.attachments:
                                        for attachment in activity.attachments:
                                            if attachment.payloadRef:
                                                output_path = os.path.join(
                                                    temp_dir,
                                                    attachment.filename or "test",
                                                )
                                                bundle.export_attachment(
                                                    attachment.payloadRef.id,
                                                    "file",
                                                    output_path,
                                                )
                                                return


def test_export_test_attachments_no_actions():
    """Test export_test_attachments with no actions."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        # Mock the actions to be None
        bundle._actions_invocation_record = xcresult.ActionsInvocationRecord()
        bundle._actions_invocation_record.actions = None

        try:
            bundle.export_test_attachments(temp_dir)
            assert False, "Should have raised MissingPropertyException"
        except MissingPropertyException:
            pass


def test_export_test_attachments_no_test_ref():
    """Test export_test_attachments with no test ref."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        # This should handle the case where testsRef is None
        # The code logs and continues, so this should succeed
        bundle.export_test_attachments(temp_dir)


def test_write_junit():
    """Test writing JUnit output."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)
        bundle.write_junit(output_path)
        assert os.path.exists(output_path)


def test_write_junit_with_attachments():
    """Test writing JUnit output with attachments."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        attachments_path = os.path.join(temp_dir, "attachments")
        bundle = xcresult.Xcresults(test_data_path)
        bundle.write_junit(output_path, attachments_path)
        assert os.path.exists(output_path)


def test_write_junit_with_prefix_suffix():
    """Test writing JUnit output with test class prefix and suffix."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)
        bundle.write_junit(
            output_path, test_class_prefix="prefix", test_class_suffix="suffix"
        )
        assert os.path.exists(output_path)
