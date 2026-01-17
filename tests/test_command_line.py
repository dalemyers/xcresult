"""Test command line functionality."""

import os
import sys
import tempfile
import shutil
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult.command_line
from xcresult.command_line import IssueType, run

# pylint: enable=wrong-import-position


def test_issue_type_enum():
    """Test the IssueType enum."""
    assert IssueType.ERROR.value == "error"
    assert IssueType.WARNING.value == "warning"
    assert IssueType.ANALYZER_WARNING.value == "analyzer-warning"
    assert IssueType.TEST_FAILURE.value == "test-failure"
    assert IssueType.TEST_WARNING.value == "test-warning"


def test_export_success():
    """Test successful export command."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_data_path, "export", "-o", temp_dir],
        ):
            result = run()
            assert result == 0


def test_export_missing_bundle():
    """Test export with missing bundle."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with mock.patch(
            "sys.argv",
            [
                "xcresult",
                "-b",
                "/nonexistent/path",
                "export",
                "-o",
                temp_dir,
            ],
        ):
            result = run()
            assert result == 1


def test_export_bundle_not_directory():
    """Test export with bundle that's not a directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("test")

        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_file, "export", "-o", temp_dir],
        ):
            result = run()
            assert result == 1


def test_export_missing_output_path():
    """Test export with missing output path."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch(
        "sys.argv",
        [
            "xcresult",
            "-b",
            test_data_path,
            "export",
            "-o",
            "/nonexistent/output",
        ],
    ):
        result = run()
        assert result == 1


def test_export_exception():
    """Test export with exception."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_data_path, "export", "-o", temp_dir],
        ):
            with mock.patch(
                "xcresult.Xcresults.export_test_attachments",
                side_effect=Exception("Test exception"),
            ):
                result = run()
                assert result == 1


def test_junit_success():
    """Test successful junit command."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_data_path, "junit", "-o", output_path],
        ):
            result = run()
            assert result == 0
            assert os.path.exists(output_path)


def test_junit_with_attachments():
    """Test junit command with attachments export."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        attachments_path = os.path.join(temp_dir, "attachments")
        os.makedirs(attachments_path)

        with mock.patch(
            "sys.argv",
            [
                "xcresult",
                "-b",
                test_data_path,
                "junit",
                "-o",
                output_path,
                "--export-attachments-path",
                attachments_path,
            ],
        ):
            result = run()
            assert result == 0


def test_junit_existing_output():
    """Test junit command with existing output file."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("existing")

        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_data_path, "junit", "-o", output_path],
        ):
            result = run()
            assert result == 1


def test_junit_exception():
    """Test junit command with exception."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "junit.xml")
        with mock.patch(
            "sys.argv",
            ["xcresult", "-b", test_data_path, "junit", "-o", output_path],
        ):
            with mock.patch(
                "xcresult.Xcresults.write_junit",
                side_effect=Exception("Test exception"),
            ):
                result = run()
                assert result == 1


def test_check_issues_no_issues():
    """Test check-issues with no issues."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path, "check-issues"],
    ):
        result = run()
        assert result == 0


def test_check_issues_with_failures():
    """Test check-issues with errors and warnings."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "BaseProjectFailure.xcresult"
    )

    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path, "check-issues"],
    ):
        result = run()
        assert result == 1


def test_check_issues_specific_type():
    """Test check-issues with specific issue type."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "BaseProjectFailure.xcresult"
    )

    with mock.patch(
        "sys.argv",
        [
            "xcresult",
            "-b",
            test_data_path,
            "check-issues",
            "--issue-types",
            "error",
        ],
    ):
        result = run()
        assert result == 1


def test_check_issues_multiple_types():
    """Test check-issues with multiple issue types."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "BaseProjectFailure.xcresult"
    )

    with mock.patch(
        "sys.argv",
        [
            "xcresult",
            "-b",
            test_data_path,
            "check-issues",
            "--issue-types",
            "warning",
            "error",
        ],
    ):
        result = run()
        assert result == 1


def test_check_issues_no_failures():
    """Test check-issues looking for specific type that doesn't exist."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch(
        "sys.argv",
        [
            "xcresult",
            "-b",
            test_data_path,
            "check-issues",
            "--issue-types",
            "error",
        ],
    ):
        result = run()
        assert result == 0


def test_no_subcommand():
    """Test with no subcommand."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path],
    ):
        result = run()
        assert result == 1


def test_unrecognized_command():
    """Test with unrecognized command."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    # Mock the args to have an invalid subcommand
    with mock.patch(
        "sys.argv",
        ["xcresult", "-b", test_data_path, "export"],
    ):
        with mock.patch(
            "argparse.ArgumentParser.parse_args"
        ) as mock_parse_args:
            mock_args = mock.Mock()
            mock_args.subcommand = "invalid"
            mock_args.bundle_path = test_data_path
            mock_parse_args.return_value = mock_args

            result = run()
            assert result == 1
