"""Test xcresulttool functionality."""

# pylint: disable=duplicate-code
# pylint: disable=invalid-name

import datetime
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.xcresulttool import (
    deserialize,
    get,
    get_actions_invocation_record,
    get_test_plan_run_summaries,
    get_action_test_summary,
    export_attachment,
    export_action_test_summary_group,
)
from xcresult.exceptions import UnsupportedTypeException

# pylint: enable=wrong-import-position


def _first_attachment(bundle: xcresult.Xcresults, test_data_path: str) -> tuple[str, str] | None:
    """Return the name and payload reference of the first exportable attachment.

    :param bundle: The already loaded result bundle to walk.
    :param test_data_path: Path to the result bundle on disk.
    :returns: A (filename, payload reference identifier) tuple, or None if the
              bundle has no attachment with a payload reference.
    """
    if not bundle.actions_invocation_record.actions:
        return None

    action = bundle.actions_invocation_record.actions[0]
    if not action.actionResult.testsRef:
        return None

    summaries = get_test_plan_run_summaries(test_data_path, action.actionResult.testsRef.id)
    if not summaries.summaries or not summaries.summaries[0].testableSummaries:
        return None

    testable = summaries.summaries[0].testableSummaries[0]
    for test in testable.all_tests():
        if not isinstance(test, xcresult.ActionTestMetadata) or not test.summaryRef:
            continue
        summary = get_action_test_summary(test_data_path, test.summaryRef.id)
        for activity in summary.activitySummaries or []:
            for attachment in activity.attachments or []:
                if attachment.payloadRef:
                    return attachment.filename or "test", attachment.payloadRef.id

    return None


def _first_testable(bundle: xcresult.Xcresults, test_data_path: str):
    """Return the first testable summary in the bundle, or None if there is none.

    :param bundle: The already loaded result bundle to walk.
    :param test_data_path: Path to the result bundle on disk.
    :returns: The first ActionTestableSummary, or None.
    """
    if not bundle.actions_invocation_record.actions:
        return None

    action = bundle.actions_invocation_record.actions[0]
    if not action.actionResult.testsRef:
        return None

    summaries = get_test_plan_run_summaries(test_data_path, action.actionResult.testsRef.id)
    if not summaries.summaries or not summaries.summaries[0].testableSummaries:
        return None

    return summaries.summaries[0].testableSummaries[0]


def test_deserialize_string():
    """Test deserializing a string."""
    data = {"_type": {"_name": "String"}, "_value": "test"}
    result = deserialize(data)
    assert result == "test"


def test_deserialize_int():
    """Test deserializing an int."""
    data = {"_type": {"_name": "Int"}, "_value": "42"}
    result = deserialize(data)
    assert result == 42


def test_deserialize_double():
    """Test deserializing a double."""
    data = {"_type": {"_name": "Double"}, "_value": "3.14"}
    result = deserialize(data)
    assert result == 3.14


def test_deserialize_bool_true():
    """Test deserializing a bool (true)."""
    data = {"_type": {"_name": "Bool"}, "_value": "true"}
    result = deserialize(data)
    assert result is True


def test_deserialize_bool_false():
    """Test deserializing a bool (false)."""
    data = {"_type": {"_name": "Bool"}, "_value": "false"}
    result = deserialize(data)
    assert result is False


def test_deserialize_date():
    """Test deserializing a date."""
    data = {"_type": {"_name": "Date"}, "_value": "2020-11-28T15:51:36.975000+0000"}
    result = deserialize(data)
    assert result == datetime.datetime(
        2020, 11, 28, 15, 51, 36, 975000, tzinfo=datetime.timezone.utc
    )


def test_deserialize_array():
    """Test deserializing an array."""
    data = {
        "_type": {"_name": "Array"},
        "_values": [
            {"_type": {"_name": "String"}, "_value": "test1"},
            {"_type": {"_name": "String"}, "_value": "test2"},
        ],
    }
    result = deserialize(data)
    assert result == ["test1", "test2"]


def test_deserialize_unknown_primitive():
    """Test deserializing an unknown primitive type."""
    data = {"_type": {"_name": "UnknownType"}, "_value": "test"}
    try:
        deserialize(data)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown type" in str(e)


def test_deserialize_unsupported_type():
    """Test deserializing an unsupported type."""
    data = {"_type": {"_name": "UnsupportedModel"}, "someProperty": "value"}
    try:
        deserialize(data)
        assert False, "Should have raised UnsupportedTypeException"
    except UnsupportedTypeException:
        pass


def test_deserialize_with_unsupported_property():
    """Test deserializing with an unsupported property."""
    data = {
        "_type": {"_name": "ActionPlatformRecord"},
        "identifier": {"_type": {"_name": "String"}, "_value": "test"},
        "unsupportedProperty": {
            "_type": {"_name": "UnsupportedType"},
            "value": "test",
        },
    }
    # Should log warning but not fail
    result = deserialize(data)
    assert isinstance(result, xcresult.ActionPlatformRecord)
    assert result.identifier == "test"


def test_get_actions_invocation_record():
    """Test getting the actions invocation record."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
    result = get_actions_invocation_record(test_data_path)
    assert isinstance(result, xcresult.ActionsInvocationRecord)


def test_get_with_identifier():
    """Test get with an identifier."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
    # First get the base record to get an identifier
    base = get_actions_invocation_record(test_data_path)
    if base.actions and base.actions[0].actionResult.testsRef:
        test_id = base.actions[0].actionResult.testsRef.id
        result = get(test_data_path, test_id)
        assert isinstance(result, dict)


def test_get_test_plan_run_summaries():
    """Test getting test plan run summaries."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")
    base = get_actions_invocation_record(test_data_path)
    if base.actions and base.actions[0].actionResult.testsRef:
        test_id = base.actions[0].actionResult.testsRef.id
        result = get_test_plan_run_summaries(test_data_path, test_id)
        assert isinstance(result, xcresult.ActionTestPlanRunSummaries)


def test_get_action_test_summary():
    """Test getting an action test summary."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestFailure.xcresult")
    bundle = xcresult.Xcresults(test_data_path)

    # Navigate to get a test summary ref
    if bundle.actions_invocation_record.actions:
        action = bundle.actions_invocation_record.actions[0]
        if action.actionResult.testsRef:
            summaries = get_test_plan_run_summaries(test_data_path, action.actionResult.testsRef.id)
            if summaries.summaries and summaries.summaries[0].testableSummaries:
                testable = summaries.summaries[0].testableSummaries[0]
                all_tests = testable.all_tests()
                for test in all_tests:
                    if isinstance(test, xcresult.ActionTestMetadata) and test.summaryRef:
                        result = get_action_test_summary(test_data_path, test.summaryRef.id)
                        assert isinstance(result, xcresult.ActionTestSummary)
                        break


def test_export_attachment():
    """Test exporting an attachment."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestFailure.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        # This will fail if there are no attachments, which is okay
        # We're just testing the export_attachment function exists and can be called
        bundle = xcresult.Xcresults(test_data_path)
        attachment = _first_attachment(bundle, test_data_path)
        if attachment is None:
            return

        filename, payload_id = attachment
        output_path = os.path.join(temp_dir, filename)
        export_attachment(test_data_path, payload_id, "file", output_path)
        assert os.path.exists(output_path)


def test_export_action_test_summary_group():
    """Test exporting action test summary group."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestFailure.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        if bundle.actions_invocation_record.actions:
            action = bundle.actions_invocation_record.actions[0]
            if action.actionResult.testsRef:
                summaries = get_test_plan_run_summaries(
                    test_data_path, action.actionResult.testsRef.id
                )
                if summaries.summaries and summaries.summaries[0].testableSummaries:
                    testable = summaries.summaries[0].testableSummaries[0]
                    if testable.tests:
                        for test in testable.tests:
                            export_action_test_summary_group(test_data_path, test, temp_dir)


def test_export_action_test_summary_group_skipped():
    """Test exporting a skipped test."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock skipped test
        mock_test = xcresult.ActionTestMetadata()
        mock_test.testStatus = "Skipped"
        mock_test.identifier = "test"
        mock_test.identifierURL = "test://com.apple.xcode/test"

        export_action_test_summary_group(test_data_path, mock_test, temp_dir)


def test_export_action_test_summary_group_no_identifier_url():
    """Test exporting a test with no identifier URL."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        mock_test = xcresult.ActionTestMetadata()
        mock_test.testStatus = "Success"
        mock_test.identifier = "test"
        mock_test.identifierURL = None

        export_action_test_summary_group(test_data_path, mock_test, temp_dir)


def test_export_action_test_summary_group_no_summary_ref():
    """Test exporting a test with no summary ref."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        mock_test = xcresult.ActionTestMetadata()
        mock_test.testStatus = "Success"
        mock_test.identifier = "test"
        mock_test.identifierURL = "test://com.apple.xcode/test"
        mock_test.summaryRef = None

        export_action_test_summary_group(test_data_path, mock_test, temp_dir)


def test_export_action_test_summary_group_with_subtests():
    """Test exporting an ActionTestSummaryGroup with subtests."""
    test_data_path = os.path.join(os.path.dirname(__file__), "data", "TestSuccess.xcresult")

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        testable = _first_testable(bundle, test_data_path)
        if testable is None:
            return

        # Look for an ActionTestSummaryGroup
        for test in testable.tests or []:
            if isinstance(test, xcresult.ActionTestSummaryGroup):
                export_action_test_summary_group(test_data_path, test, temp_dir)
                break
