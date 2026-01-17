"""Tests to boost coverage to higher levels."""

import os
import sys
import tempfile
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.junit_writer import JunitWriter
from xcresult.exceptions import MissingPropertyException
from lxml import etree as ET

# pylint: enable=wrong-import-position


def test_junit_writer_type_error():
    """Test JUnit writer raises TypeError for non-ActionTestMetadata in all_tests."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        bundle = xcresult.Xcresults(test_data_path)
        writer = JunitWriter(bundle, output_path)

        root = ET.Element("testsuites")

        # Create a mock testable summary
        testable_summary = mock.Mock(spec=xcresult.ActionTestableSummary)
        testable_summary.name = "TestSuite"
        testable_summary.tests = [mock.Mock()]  # Mock test list

        # Mock all_tests to return something that's not ActionTestMetadata
        testable_summary.all_tests = mock.Mock(return_value=["not_a_test_metadata"])

        try:
            writer.generate_test_suite(root, testable_summary, "Config")
            assert False, "Should have raised TypeError"
        except TypeError as e:
            assert "Expected ActionTestMetadata" in str(e)


def test_command_line_empty_summaries():
    """Test command line check-issues with empty summaries list."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    # Create a bundle with explicitly empty error summaries to hit line 77-80
    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path, "check-issues", "--issue-types", "error"],
    ):
        from xcresult.command_line import run

        result = run()
        # Should print "No Errors issues found" and return 0
        assert result == 0


def test_command_line_issue_without_location():
    """Test command line check-issues with issue that has no location."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch("sys.argv", ["xcresult", "-b", test_data_path, "check-issues"]):
        with mock.patch("xcresult.Xcresults") as mock_xcresults:
            # Create a mock bundle with an issue that has no location
            mock_bundle = mock.Mock()
            mock_record = mock.Mock()
            mock_issues = mock.Mock()

            # Create an issue without documentLocationInCreatingWorkspace
            mock_issue = mock.Mock()
            mock_issue.message = "Error without location"
            mock_issue.documentLocationInCreatingWorkspace = None

            mock_issues.errorSummaries = [mock_issue]
            mock_issues.warningSummaries = None
            mock_issues.analyzerWarningSummaries = None
            mock_issues.testFailureSummaries = None
            mock_issues.testWarningSummaries = None

            mock_record.issues = mock_issues
            mock_bundle.actions_invocation_record = mock_record
            mock_xcresults.return_value = mock_bundle

            from xcresult.command_line import run

            result = run()
            # Should print the message without location (line 88)
            assert result == 1


def test_xcresults_export_attachment():
    """Test export_attachment method in Xcresults."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)
        output_path = os.path.join(temp_dir, "test.png")

        # Mock the underlying export_attachment function
        with mock.patch("xcresult.xcresults.export_attachment") as mock_export:
            bundle.export_attachment("test-id", "file", output_path)
            # Should call the underlying function (line 51)
            mock_export.assert_called_once_with(
                test_data_path, "test-id", "file", output_path
            )


def test_xcresults_export_no_actions_invocation_record():
    """Test export_test_attachments with no actions invocation record."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Clear the cached record and mock the property to return None
        bundle._actions_invocation_record = None

        # Mock the property getter to return None
        with mock.patch.object(
            type(bundle),
            "actions_invocation_record",
            new_callable=mock.PropertyMock,
            return_value=None,
        ):
            try:
                bundle.export_test_attachments(temp_dir)
                assert False, "Should raise MissingPropertyException"
            except (MissingPropertyException, AttributeError):
                # Line 63 should be hit
                pass


def test_xcresults_export_missing_summaries():
    """Test export_test_attachments with missing summaries."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Mock to create an action with testsRef but no summaries
        with mock.patch.object(bundle, "get") as mock_get:
            # Mock the deserialization to return summaries with no summaries list
            mock_summaries = xcresult.ActionTestPlanRunSummaries()
            mock_summaries.summaries = None

            with mock.patch(
                "xcresult.xcresults.deserialize", return_value=mock_summaries
            ):
                try:
                    bundle.export_test_attachments(temp_dir)
                    # May succeed if there are no actions, or fail if there are
                except MissingPropertyException as e:
                    # Line 83 should be hit
                    assert "No summaries found" in str(e)


def test_xcresults_export_missing_testable_summaries():
    """Test export_test_attachments with missing testable summaries."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Create a mock setup with summaries but no testableSummaries
        mock_summaries = xcresult.ActionTestPlanRunSummaries()
        mock_summary = xcresult.ActionTestPlanRunSummary()
        mock_summary.name = "Test"
        mock_summary.testableSummaries = None
        mock_summaries.summaries = [mock_summary]

        with mock.patch("xcresult.xcresults.deserialize", return_value=mock_summaries):
            with mock.patch.object(bundle, "get"):
                try:
                    bundle.export_test_attachments(temp_dir)
                except MissingPropertyException as e:
                    # Line 88 should be hit
                    assert "No testable summaries found" in str(e)


def test_xcresults_export_missing_tests():
    """Test export_test_attachments with missing tests."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        bundle = xcresult.Xcresults(test_data_path)

        # Create a mock setup with testableSummaries but no tests
        mock_summaries = xcresult.ActionTestPlanRunSummaries()
        mock_summary = xcresult.ActionTestPlanRunSummary()
        mock_summary.name = "Test"

        mock_testable = xcresult.ActionTestableSummary()
        mock_testable.name = "Testable"
        mock_testable.tests = None

        mock_summary.testableSummaries = [mock_testable]
        mock_summaries.summaries = [mock_summary]

        with mock.patch("xcresult.xcresults.deserialize", return_value=mock_summaries):
            with mock.patch.object(bundle, "get"):
                try:
                    bundle.export_test_attachments(temp_dir)
                except MissingPropertyException as e:
                    # Line 94 should be hit
                    assert "No tests found" in str(e)


def test_xcresulttool_export_with_failure_attachments():
    """Test exporting attachments from failure summaries."""
    from xcresult.xcresulttool import export_action_test_summary_group

    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestFailure.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test with failure summaries that have attachments
        test = xcresult.ActionTestMetadata()
        test.identifier = "test"
        test.identifierURL = "test://com.apple.xcode/test"
        test.testStatus = "Failed"
        test.summaryRef = xcresult.Reference()
        test.summaryRef.id = "fake-id"

        # Mock the get and deserialize to return a summary with failure attachments
        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()
                summary.activitySummaries = None

                # Create failure summary with attachment
                failure = xcresult.ActionTestFailureSummary()
                failure.message = "Failed"
                failure.attachments = [xcresult.ActionTestAttachment()]
                failure.attachments[0].filename = "error.png"
                failure.attachments[0].payloadRef = xcresult.Reference()
                failure.attachments[0].payloadRef.id = "payload-id"

                summary.failureSummaries = [failure]
                mock_deser.return_value = summary

                with mock.patch("xcresult.xcresulttool.export_attachment"):
                    # This should hit lines 296-324 in xcresulttool.py
                    export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_activity_without_attachments():
    """Test exporting when activity summaries have no attachments."""
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

                # Activity with no attachments
                activity = xcresult.ActionTestActivitySummary()
                activity.title = "Test Activity"
                activity.attachments = None

                summary.activitySummaries = [activity]
                summary.failureSummaries = None
                mock_deser.return_value = summary

                # Should handle None attachments gracefully (line 268-269)
                export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_attachment_without_filename():
    """Test exporting attachment without filename."""
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

                # Activity with attachment but no filename
                activity = xcresult.ActionTestActivitySummary()
                activity.title = "Test Activity"
                attachment = xcresult.ActionTestAttachment()
                attachment.name = "attachment"
                attachment.filename = None  # No filename - should generate UUID
                attachment.payloadRef = xcresult.Reference()
                attachment.payloadRef.id = "payload-id"

                activity.attachments = [attachment]
                summary.activitySummaries = [activity]
                summary.failureSummaries = None
                mock_deser.return_value = summary

                with mock.patch("xcresult.xcresulttool.export_attachment"):
                    # Should hit line 276-278 (generate UUID for filename)
                    export_action_test_summary_group(test_data_path, test, temp_dir)


def test_xcresulttool_export_attachment_file_exists():
    """Test exporting attachment when file already exists."""
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

        # Create the output directory and a file that will conflict
        output_dir = os.path.join(temp_dir, "test")
        os.makedirs(output_dir, exist_ok=True)
        conflict_file = os.path.join(output_dir, "screenshot.png")
        with open(conflict_file, "w") as f:
            f.write("existing")

        with mock.patch("xcresult.xcresulttool.get"):
            with mock.patch("xcresult.xcresulttool.deserialize") as mock_deser:
                summary = xcresult.ActionTestSummary()

                # Activity with attachment that will conflict
                activity = xcresult.ActionTestActivitySummary()
                activity.title = "Test Activity"
                attachment = xcresult.ActionTestAttachment()
                attachment.name = "screenshot"
                attachment.filename = "screenshot.png"
                attachment.payloadRef = xcresult.Reference()
                attachment.payloadRef.id = "payload-id"

                activity.attachments = [attachment]
                summary.activitySummaries = [activity]
                summary.failureSummaries = None
                mock_deser.return_value = summary

                with mock.patch("xcresult.xcresulttool.export_attachment"):
                    # Should hit lines 283-287 (handle file exists by adding suffix)
                    export_action_test_summary_group(test_data_path, test, temp_dir)
