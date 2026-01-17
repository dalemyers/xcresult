"""Test command_line import error handling."""

import os
import sys
import subprocess


def test_command_line_import_success_path():
    """Test the normal import path (try block succeeds)."""
    # This should work normally since xcresult is already available
    import xcresult.command_line

    # Verify the module loaded successfully
    assert hasattr(xcresult.command_line, 'run')
    assert hasattr(xcresult.command_line, 'IssueType')


def test_command_line_standalone_execution():
    """
    Test running command_line.py as a standalone script.
    This is an integration test that ensures the ImportError fallback works.
    """
    # Get paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    command_line_path = os.path.join(project_root, 'xcresult', 'command_line.py')

    # Run command_line.py directly as a script with --help flag
    # This will execute the module-level import code including the try/except
    result = subprocess.run(
        [sys.executable, command_line_path, '--help'],
        capture_output=True,
        text=True,
        timeout=5,
        cwd=project_root  # Run from project root so imports can resolve
    )

    # Should succeed (exit code 0) and show help text
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert 'usage:' in result.stdout.lower() or 'xcresult' in result.stdout.lower()


def test_command_line_as_module():
    """Test running command_line as a module with python -m."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)

    # Run as module
    result = subprocess.run(
        [sys.executable, '-m', 'xcresult.command_line', '--help'],
        capture_output=True,
        text=True,
        timeout=5,
        cwd=project_root,
        env={**os.environ, 'PYTHONPATH': project_root}
    )

    # Should succeed
    assert result.returncode == 0, f"Module execution failed: {result.stderr}"
    assert 'usage:' in result.stdout.lower() or 'xcresult' in result.stdout.lower()
