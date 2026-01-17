"""Final tests to get xcresulttool.py to 100% coverage."""

import os
import sys
import subprocess
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.xcresulttool import deserialize, _export

# pylint: enable=wrong-import-position


def test_export_subprocess_call():
    """
    Test the _export function that calls subprocess.
    This covers lines 151-166 in xcresulttool.py.
    """
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    # Mock subprocess.run to avoid actually calling xcrun
    with mock.patch('xcresult.xcresulttool.subprocess.run') as mock_run:
        # Configure the mock to simulate successful execution
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=b'',
            stderr=b''
        )

        # Call _export which should trigger lines 151-166
        _export(test_data_path, "fake-id", "file", "/tmp/output.txt")

        # Verify subprocess.run was called
        assert mock_run.called

        # Verify it was called with the correct command structure
        call_args = mock_run.call_args
        command = call_args[0][0]

        assert command[0] == "xcrun"
        assert command[1] == "xcresulttool"
        assert command[2] == "export"
        assert "--path" in command
        assert test_data_path in command
        assert "--id" in command
        assert "fake-id" in command
        assert "--type" in command
        assert "file" in command
        assert "--output-path" in command
        assert "/tmp/output.txt" in command
        assert "--legacy" in command

        # Verify check=True was passed
        assert call_args[1]['check'] is True
        assert 'stdout' in call_args[1]
        assert 'stderr' in call_args[1]


def test_export_subprocess_with_directory_type():
    """Test _export with directory type."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch('xcresult.xcresulttool.subprocess.run') as mock_run:
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'', stderr=b'')

        # Call with directory type
        _export(test_data_path, "test-id", "directory", "/tmp/output_dir")

        # Verify the command includes directory type
        call_args = mock_run.call_args
        command = call_args[0][0]

        assert "directory" in command
        assert "/tmp/output_dir" in command


def test_export_subprocess_error_handling():
    """Test that _export propagates subprocess errors."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )

    with mock.patch('xcresult.xcresulttool.subprocess.run') as mock_run:
        # Simulate subprocess failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['xcrun', 'xcresulttool'],
            stderr=b'xcresulttool error'
        )

        # Should raise the CalledProcessError
        try:
            _export(test_data_path, "fake-id", "file", "/tmp/output.txt")
            assert False, "Expected CalledProcessError"
        except subprocess.CalledProcessError as e:
            assert e.returncode == 1
