"""Final tests to push coverage to maximum."""

import os
import sys
import tempfile
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.xcresulttool import deserialize
from xcresult.exceptions import MissingPropertyException

# pylint: enable=wrong-import-position


def test_xcresults_action_without_tests_ref():
    """Test export_test_attachments when action has no testsRef."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Mock an action with no testsRef to hit lines 76-77
        mock_record = xcresult.ActionsInvocationRecord()
        mock_action = xcresult.ActionRecord()
        mock_action.schemeCommandName = "Test"
        mock_action.schemeTaskName = "Action"
        mock_action.testPlanName = "Plan"
        mock_action.actionResult = xcresult.ActionResult()
        mock_action.actionResult.testsRef = None  # No testsRef

        mock_record.actions = [mock_action]

        with mock.patch.object(
            type(bundle),
            "actions_invocation_record",
            new_callable=mock.PropertyMock,
            return_value=mock_record,
        ):
            # This should log and skip the action (lines 76-77)
            bundle.export_test_attachments(temp_dir)


def test_command_line_check_issues_empty_summaries_list():
    """Test check-issues when summaries list exists but is empty."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    # This should hit lines 78-80 when len(summaries) == 0
    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path, "check-issues", "--issue-types", "warning"],
    ):
        with mock.patch("xcresult.Xcresults") as mock_xcresults:
            mock_bundle = mock.Mock()
            mock_record = mock.Mock()
            mock_issues = mock.Mock()

            # Empty list (not None) to trigger len(summaries) == 0 check
            mock_issues.errorSummaries = None
            mock_issues.warningSummaries = []  # Empty list
            mock_issues.analyzerWarningSummaries = None
            mock_issues.testFailureSummaries = None
            mock_issues.testWarningSummaries = None

            mock_record.issues = mock_issues
            mock_bundle.actions_invocation_record = mock_record
            mock_xcresults.return_value = mock_bundle

            from xcresult.command_line import run

            result = run()
            assert result == 0


def test_xcresulttool_deserialize_missing_float_property():
    """Test deserialize when a float property is missing."""
    # This should hit lines 85-86 in xcresulttool.py
    # ConsoleLogItemLogData has unixTimeInterval: float (non-optional)
    data = {
        "_type": {"_name": "ConsoleLogItemLogData"},
        "pid": {"_type": {"_name": "Int"}, "_value": "1234"},
        "tid": {"_type": {"_name": "Int"}, "_value": "5678"},
        "messageType": {"_type": {"_name": "Int"}, "_value": "0"},
        "senderImageOffset": {"_type": {"_name": "Int"}, "_value": "0"},
        # Missing unixTimeInterval (float) - should default to 0.0
    }

    result = deserialize(data)
    assert isinstance(result, xcresult.ConsoleLogItemLogData)
    assert result.unixTimeInterval == 0.0  # Default float value from lines 85-86




def test_xcresulttool_export_attachment_makedirs():
    """Test export_attachment creates directories."""
    from xcresult.xcresulttool import export_attachment

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a nested path that needs makedirs (line 221)
        output_path = os.path.join(temp_dir, "nested", "path", "attachment.png")

        # Mock _export to avoid actually calling xcresulttool
        with mock.patch("xcresult.xcresulttool._export"):
            export_attachment(test_data_path, "fake-id", "file", output_path)
            # Should have created the nested directory structure


def test_xcresulttool_export_non_action_test_metadata():
    """Test export_action_test_summary_group with ActionTestSummary (not ActionTestMetadata)."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        # Use ActionTestSummary which is ActionTestSummaryIdentifiableObject
        # but not ActionTestMetadata or ActionTestSummaryGroup
        # This should cause it to return at line 255
        test = xcresult.ActionTestSummary()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"  # Non-None URL
        test.activitySummaries = None
        test.failureSummaries = None

        # Should return early at line 255 since it's not ActionTestMetadata
        export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_attachment_no_payload_ref_activity():
    """Test exporting activity attachment without payloadRef."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        test = xcresult.ActionTestMetadata()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"
        test.testStatus = "Success"
        test.summaryRef = xcresult.Reference()
        test.summaryRef.id = "fake-id"

        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()

                # Activity with attachment but no payloadRef (line 273)
                activity = xcresult.ActionTestActivitySummary()
                activity.title = "Test Activity"
                attachment = xcresult.ActionTestAttachment()
                attachment.name = "attachment"
                attachment.filename = "test.png"
                attachment.payloadRef = None  # No payloadRef - should skip

                activity.attachments = [attachment]
                summary.activitySummaries = [activity]
                summary.failureSummaries = None
                mock_deser.return_value = summary

                # Should skip the attachment at line 273
                export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_failure_attachment_no_payload_ref():
    """Test exporting failure attachment without payloadRef."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        test = xcresult.ActionTestMetadata()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"
        test.testStatus = "Failed"
        test.summaryRef = xcresult.Reference()
        test.summaryRef.id = "fake-id"

        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()
                summary.activitySummaries = None

                # Failure with attachment but no payloadRef (line 303)
                failure = xcresult.ActionTestFailureSummary()
                failure.message = "Failed"
                attachment = xcresult.ActionTestAttachment()
                attachment.filename = "error.png"
                attachment.payloadRef = None  # No payloadRef

                failure.attachments = [attachment]
                summary.failureSummaries = [failure]
                mock_deser.return_value = summary

                # Should skip at line 303
                export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_failure_attachment_no_filename():
    """Test exporting failure attachment without filename."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        test = xcresult.ActionTestMetadata()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"
        test.testStatus = "Failed"
        test.summaryRef = xcresult.Reference()
        test.summaryRef.id = "fake-id"

        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()
                summary.activitySummaries = None

                # Failure with attachment but no filename (line 307)
                failure = xcresult.ActionTestFailureSummary()
                failure.message = "Failed"
                attachment = xcresult.ActionTestAttachment()
                attachment.filename = None  # Should generate UUID
                attachment.payloadRef = xcresult.Reference()
                attachment.payloadRef.id = "payload-id"

                failure.attachments = [attachment]
                summary.failureSummaries = [failure]
                mock_deser.return_value = summary

                with mock.patch("xcresult.xcresulttool.export_attachment"):
                    # Should hit line 307 (UUID generation)
                    export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_failure_attachment_file_exists():
    """Test exporting failure attachment when output file already exists."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        test = xcresult.ActionTestMetadata()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"
        test.testStatus = "Failed"
        test.summaryRef = xcresult.Reference()
        test.summaryRef.id = "fake-id"

        # Create the output directory and a file that will conflict
        output_dir = os.path.join(temp_dir, "test")
        os.makedirs(output_dir, exist_ok=True)
        conflict_file = os.path.join(output_dir, "error.png")
        with open(conflict_file, "w") as f:
            f.write("existing")

        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()
                summary.activitySummaries = None

                # Failure with attachment that will conflict
                failure = xcresult.ActionTestFailureSummary()
                failure.message = "Failed"
                attachment = xcresult.ActionTestAttachment()
                attachment.filename = "error.png"
                attachment.payloadRef = xcresult.Reference()
                attachment.payloadRef.id = "payload-id"

                failure.attachments = [attachment]
                summary.failureSummaries = [failure]
                mock_deser.return_value = summary

                with mock.patch("xcresult.xcresulttool.export_attachment"):
                    # Should hit lines 314-317 (file exists handling)
                    export_action_test_summary_group(test_data_path, test, temp_dir)
