"""Unit tests for the modern xcresult command line boundary."""

# pylint: disable=duplicate-code

import argparse
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Callable
from unittest import mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.command_line import IssueType, run

# pylint: enable=wrong-import-position

BUNDLE_PATH = "results.xcresult"
OUTPUT_PATH = "output"
CATEGORIES = [
    ("error", "errors", "Errors", "build"),
    ("warning", "warnings", "Warnings", "build"),
    ("analyzer-warning", "analyzerWarnings", "Analyzer Warnings", "build"),
    ("test-failure", "testFailures", "Test Failures", "summary"),
    ("test-warning", "runtimeWarnings", "Test Warnings", "summary"),
]


def path_predicate(*paths: str) -> Callable[[str], bool]:
    """Build a typed filesystem predicate matching only the supplied paths."""

    def matches(path: str) -> bool:
        """Report whether the requested path is in this mock filesystem."""
        return path in paths

    return matches


@pytest.fixture(name="cli")
def fixture_cli(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """Mock bundle commands and filesystem checks without invoking xcresulttool."""
    build = SimpleNamespace(errors=[], warnings=[], analyzerWarnings=[])
    summary = SimpleNamespace(testFailures=[], runtimeWarnings=[])
    availability = SimpleNamespace(hasTestResults=True)
    bundle = mock.Mock(
        spec=[
            "build_results",
            "test_summary",
            "content_availability",
            "export_test_attachments",
            "write_junit",
        ]
    )
    properties = {
        "build": mock.PropertyMock(return_value=build),
        "summary": mock.PropertyMock(return_value=summary),
        "availability": mock.PropertyMock(return_value=availability),
    }
    type(bundle).build_results = properties["build"]
    type(bundle).test_summary = properties["summary"]
    type(bundle).content_availability = properties["availability"]
    constructor = mock.Mock(return_value=bundle)
    monkeypatch.setattr(xcresult, "Xcresults", constructor)
    monkeypatch.setattr(os.path, "exists", path_predicate(BUNDLE_PATH))
    monkeypatch.setattr(os.path, "isdir", path_predicate(BUNDLE_PATH, OUTPUT_PATH))
    return SimpleNamespace(
        bundle=bundle,
        constructor=constructor,
        build=build,
        summary=summary,
        availability=availability,
        properties=properties,
    )


def invoke(monkeypatch: pytest.MonkeyPatch, *arguments: str) -> int:
    """Run the CLI with the supplied subcommand arguments."""
    monkeypatch.setattr(sys, "argv", ["xcresult", "-b", BUNDLE_PATH, *arguments])
    return run()


def issue(message: str, source_url: str | None = None) -> xcresult.Issue:
    """Create a modern issue at the CLI boundary."""
    return xcresult.Issue(
        message=message,
        issueType="Warning",
        sourceURL=source_url,
        targetName=None,
        className=None,
    )


def failure(message: str) -> xcresult.TestFailure:
    """Create a modern test failure, which has no issue message or source URL."""
    return xcresult.TestFailure(
        failureText=message,
        testName="testExample()",
        targetName="Tests",
        testIdentifier=1,
        testIdentifierString="Suite/testExample()",
    )


def test_issue_type_enum() -> None:
    """Keep the public issue category spellings stable."""
    assert [value.value for value in IssueType] == [category[0] for category in CATEGORIES]


@pytest.mark.parametrize("category,attribute,title,report", CATEGORIES)
def test_each_issue_category(
    *,
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    category: str,
    attribute: str,
    title: str,
    report: str,
) -> None:
    """Print only the selected category and request only the necessary reports."""
    record = (
        failure("test failed")
        if report == "summary" and category == "test-failure"
        else issue("bad")
    )
    setattr(getattr(cli, report), attribute, [record])
    assert invoke(monkeypatch, "check-issues", "--issue-types", category) == 1
    output = capsys.readouterr()
    assert f"=== {title} ===" in output.out
    assert ("test failed" if category == "test-failure" else "bad") in output.out
    assert output.out.count("===") == 2
    assert "Issues found." in output.out
    assert not output.err
    cli.properties[report].assert_called_once_with()
    if report == "build":
        cli.properties["summary"].assert_not_called()
        cli.properties["availability"].assert_not_called()
    else:
        cli.properties["build"].assert_not_called()
        cli.properties["availability"].assert_called_once_with()


def test_all_categories_are_printed(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Finding an earlier issue must not short-circuit any later category."""
    for category, attribute, _, report in CATEGORIES:
        record = failure(category) if category == "test-failure" else issue(category)
        setattr(getattr(cli, report), attribute, [record])
    assert invoke(monkeypatch, "check-issues") == 1
    output = capsys.readouterr()
    for category, _, title, _ in CATEGORIES:
        assert f"=== {title} ===\n{category}\n" in output.out
    for prop in cli.properties.values():
        prop.assert_called_once_with()
    assert not output.err


def test_multiple_selected_categories(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Print all selected categories, even when the first has issues."""
    cli.build.errors = [issue("compiler error")]
    cli.summary.runtimeWarnings = [issue("runtime warning")]
    assert invoke(monkeypatch, "check-issues", "--issue-types", "error", "test-warning") == 1
    output = capsys.readouterr().out
    assert "compiler error" in output
    assert "runtime warning" in output
    assert "=== Warnings ===" not in output
    assert "=== Analyzer Warnings ===" not in output
    assert "=== Test Failures ===" not in output


@pytest.mark.parametrize("has_tests", [True, False])
def test_empty_results(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    has_tests: bool,
) -> None:
    """Empty or build-only bundles do not report issues or request unavailable tests."""
    cli.availability.hasTestResults = has_tests
    if not has_tests:
        cli.properties["summary"].side_effect = AssertionError("Tests are unavailable")
    assert invoke(monkeypatch, "check-issues") == 0
    output = capsys.readouterr()
    assert "No issues found." in output.out
    assert "No Errors issues found." in output.out
    assert not output.err
    assert cli.properties["summary"].call_count == int(has_tests)


def test_build_only_bundle_preserves_errors(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Build errors survive absent test results and every selected category prints."""
    cli.availability.hasTestResults = False
    cli.build.errors = [issue("build failed")]
    assert invoke(monkeypatch, "check-issues") == 1
    output = capsys.readouterr().out
    assert "build failed" in output
    assert "No Test Failures found." in output
    assert "No Test Warnings found." in output
    cli.properties["summary"].assert_not_called()


def test_test_only_selection_without_tests(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """No build or summary command is needed for unavailable, selected test issues."""
    cli.availability.hasTestResults = False
    assert invoke(monkeypatch, "check-issues", "--issue-types", "test-failure") == 0
    assert "No Test Failures found." in capsys.readouterr().out
    cli.properties["summary"].assert_not_called()
    cli.properties["build"].assert_not_called()


def test_unselected_issues_do_not_fail(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Only selected categories affect the command's exit code."""
    cli.build.errors = [issue("unselected compiler error")]
    cli.summary.testFailures = [failure("unselected test failure")]
    assert invoke(monkeypatch, "check-issues", "--issue-types", "warning") == 0
    output = capsys.readouterr().out
    assert "unselected" not in output
    assert "No issues found." in output
    cli.properties["summary"].assert_not_called()


@pytest.mark.parametrize(
    "source_url,expected",
    [
        (None, "problem"),
        ("", "problem"),
        (
            "file:///project/My%20File.swift#StartingLineNumber=0&StartingColumnNumber=2",
            "/project/My File.swift:1:3 -> problem",
        ),
        ("file:///project/File.swift", "/project/File.swift -> problem"),
        ("file:///project/File.swift#StartingLineNumber=9", "/project/File.swift:10 -> problem"),
        ("file:///project/File.swift#StartingColumnNumber=2", "/project/File.swift -> problem"),
        ("file:///project/File.swift#StartingLineNumber=bad", "/project/File.swift -> problem"),
        ("file:///project/File.swift#StartingLineNumber=-1", "/project/File.swift -> problem"),
        (
            "file:///project/File.swift#StartingLineNumber=1&StartingColumnNumber=bad",
            "/project/File.swift:2 -> problem",
        ),
        ("file:///project/File.swift#StartingLineNumber=", "/project/File.swift -> problem"),
    ],
)
def test_source_url_formatting(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    source_url: str | None,
    expected: str,
) -> None:
    """Decode source paths and safely convert available coordinates to one-based values."""
    cli.build.errors = [issue("problem", source_url)]
    assert invoke(monkeypatch, "check-issues", "--issue-types", "error") == 1
    output = capsys.readouterr()
    assert f"\n{expected}\n" in output.out
    assert not output.err


def test_export_wiring(cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch) -> None:
    """Export attachments using the modern bundle API and unchanged CLI arguments."""
    assert invoke(monkeypatch, "export", "-o", OUTPUT_PATH) == 0
    cli.constructor.assert_called_once_with(BUNDLE_PATH)
    cli.bundle.export_test_attachments.assert_called_once_with(OUTPUT_PATH)


@pytest.mark.parametrize("collapse", [False, True])
@pytest.mark.parametrize("attachments", [None, "attachments"])
def test_junit_wiring(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    collapse: bool,
    attachments: str | None,
) -> None:
    """Preserve attachment export and both retry-collapse modes in JUnit calls."""
    arguments = ["junit", "-o", OUTPUT_PATH]
    if attachments:
        arguments += ["--export-attachments-path", attachments]
    if collapse:
        arguments.append("--collapse-retries")
    assert invoke(monkeypatch, *arguments) == 0
    cli.constructor.assert_called_once_with(BUNDLE_PATH)
    cli.bundle.write_junit.assert_called_once_with(
        OUTPUT_PATH, attachments, collapse_retries=collapse
    )


@pytest.mark.parametrize("command", ["export", "junit", "check-issues"])
@pytest.mark.parametrize("construction_error", [True, False])
@pytest.mark.parametrize("error_type", [xcresult.XcresultException, OSError, ValueError])
def test_operational_errors(
    *,
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    command: str,
    construction_error: bool,
    error_type: type[Exception],
) -> None:
    """All handlers report construction and command failures to stderr, returning one."""
    error = error_type("xcresulttool stderr: unsupported bundle")
    if construction_error:
        cli.constructor.side_effect = error
    elif command == "check-issues":
        cli.properties["build"].side_effect = error
    else:
        method = "write_junit" if command == "junit" else "export_test_attachments"
        getattr(cli.bundle, method).side_effect = error
    arguments = [command] if command == "check-issues" else [command, "-o", OUTPUT_PATH]
    assert invoke(monkeypatch, *arguments) == 1
    output = capsys.readouterr()
    assert "xcresulttool stderr: unsupported bundle" in output.err
    assert "No issues found." not in output.out


@pytest.mark.parametrize("property_name", ["availability", "summary"])
def test_test_report_errors_are_not_hidden(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    property_name: str,
) -> None:
    """A failed test report is not silently treated as an empty or build-only bundle."""
    cli.properties[property_name].side_effect = xcresult.XcresultException("test report failed")
    assert invoke(monkeypatch, "check-issues", "--issue-types", "test-failure") == 1
    output = capsys.readouterr()
    assert "test report failed" in output.err
    assert "No issues found." not in output.out


@pytest.mark.parametrize("command", ["export", "junit", "check-issues"])
@pytest.mark.parametrize("exists", [False, True])
def test_invalid_bundle(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    command: str,
    exists: bool,
) -> None:
    """Missing paths and non-directory bundles fail before executing a bundle command."""
    monkeypatch.setattr(os.path, "exists", path_predicate(*([BUNDLE_PATH] if exists else [])))
    monkeypatch.setattr(os.path, "isdir", path_predicate())
    arguments = [command] if command == "check-issues" else [command, "-o", OUTPUT_PATH]
    assert invoke(monkeypatch, *arguments) == 1
    expected = "not a valid bundle" if exists else "does not exist"
    assert expected in capsys.readouterr().err
    cli.constructor.assert_not_called()


def test_export_invalid_output(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Export requires an existing directory and does not invoke xcresulttool otherwise."""
    monkeypatch.setattr(os.path, "isdir", path_predicate(BUNDLE_PATH))
    assert invoke(monkeypatch, "export", "-o", OUTPUT_PATH) == 1
    assert "Output folder does not exist" in capsys.readouterr().err
    cli.constructor.assert_not_called()


def test_junit_existing_output(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An existing output is never overwritten."""
    monkeypatch.setattr(os.path, "exists", path_predicate(BUNDLE_PATH, OUTPUT_PATH))
    assert invoke(monkeypatch, "junit", "-o", OUTPUT_PATH) == 1
    assert "Output file already exists" in capsys.readouterr().err
    cli.constructor.assert_not_called()


def test_no_subcommand(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A missing subcommand prints usage and returns one."""
    assert invoke(monkeypatch) == 1
    assert "usage:" in capsys.readouterr().out
    cli.constructor.assert_not_called()


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["-b", BUNDLE_PATH, "unknown"],
        ["-b", BUNDLE_PATH, "export"],
        ["-b", BUNDLE_PATH, "junit"],
        ["-b", BUNDLE_PATH, "check-issues", "--issue-types"],
        ["-b", BUNDLE_PATH, "check-issues", "--issue-types", "unknown"],
    ],
)
def test_invalid_arguments(
    cli: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    arguments: list[str],
) -> None:
    """Argparse rejects invalid or incomplete arguments with the conventional exit code."""
    monkeypatch.setattr(sys, "argv", ["xcresult", *arguments])
    with pytest.raises(SystemExit) as error:
        run()
    assert error.value.code == 2
    assert "usage:" in capsys.readouterr().err
    cli.constructor.assert_not_called()


def test_unrecognized_command(
    cli: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The dispatcher reports unsupported commands defensively."""

    def parse_arguments(_parser: argparse.ArgumentParser) -> SimpleNamespace:
        """Supply a command that argparse would normally reject."""
        return SimpleNamespace(subcommand="invalid", bundle_path=BUNDLE_PATH)

    monkeypatch.setattr("argparse.ArgumentParser.parse_args", parse_arguments)
    assert invoke(monkeypatch) == 1
    assert "Unrecognized command" in capsys.readouterr().err
    cli.constructor.assert_not_called()


def test_standalone_script_import() -> None:
    """The CLI can execute directly without an installed package or PYTHONPATH."""
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(root / "xcresult" / "command_line.py"), "--help"],
        cwd=root / "tests",
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "check-issues" in result.stdout
