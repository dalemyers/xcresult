"""Regression coverage for modern report commands and bundle access."""

import json
from pathlib import Path
import shutil
import subprocess
from unittest.mock import Mock, patch

import pytest

from xcresult import Xcresults, xcresulttool
from xcresult.exceptions import XcresultException
from xcresult.model import SCHEMA_VERSION, ContentAvailability, TestNode, Tests


@pytest.fixture(name="availability")
def fixture_availability() -> ContentAvailability:
    """Provide a bundle with test content."""
    return ContentAvailability(
        hasCoverage=False, hasDiagnostics=True, hasTestResults=True, logs=["build", "action"]
    )


def test_lazy_reports_and_absolute_path(availability: ContentAvailability) -> None:
    """Read each summary property once and resolve relative bundle paths."""
    with patch.object(xcresulttool, "get_content_availability", return_value=availability) as read:
        bundle = Xcresults("example.xcresult")
        read.assert_not_called()
        assert bundle.path == str(Path("example.xcresult").absolute())
        assert bundle.content_availability is availability
        assert bundle.content_availability is availability
        read.assert_called_once_with(bundle.path)


@pytest.mark.parametrize(
    ("property_name", "reader"),
    [
        ("build_results", "get_build_results"),
        ("test_summary", "get_test_summary"),
        ("tests", "get_tests"),
    ],
)
def test_report_properties_are_cached(property_name: str, reader: str) -> None:
    """Cache each independently loaded report."""
    with patch.object(xcresulttool, reader) as read:
        bundle = Xcresults("example.xcresult")
        assert getattr(bundle, property_name) is read.return_value
        assert getattr(bundle, property_name) is read.return_value
        read.assert_called_once_with(bundle.path)


@pytest.mark.parametrize(
    ("method", "reader"),
    [("test_details", "get_test_details"), ("test_activities", "get_test_activities")],
)
def test_test_selectors(method: str, reader: str) -> None:
    """Pass identifier URLs unchanged to detailed reports."""
    with patch.object(xcresulttool, reader) as read:
        bundle = Xcresults("example.xcresult")
        identifier = "test://com.apple.xcode/Target/Suite/test()"
        assert getattr(bundle, method)(identifier) is read.return_value
        read.assert_called_once_with(bundle.path, identifier)


def test_get_tests_uses_modern_command() -> None:
    """Decode ordinary JSON rather than legacy typed envelopes."""
    data = {
        "testPlanConfigurations": [],
        "devices": [],
        "testNodes": [{"nodeType": "Test Case", "name": "test()", "result": "Passed"}],
    }
    with patch("subprocess.run", return_value=Mock(stdout=json.dumps(data))) as run:
        report = xcresulttool.get_tests("/results with spaces.xcresult")
    assert isinstance(report, Tests)
    assert isinstance(report.testNodes[0], TestNode)
    assert report.testNodes[0].result == "Passed"
    assert run.call_args.args[0] == [
        "xcrun",
        "xcresulttool",
        "get",
        "test-results",
        "tests",
        "--path",
        "/results with spaces.xcresult",
        "--compact",
        "--schema-version",
        SCHEMA_VERSION,
    ]


@pytest.mark.parametrize(
    ("reader", "arguments", "command"),
    [
        ("get_test_summary", (), ["test-results", "summary"]),
        (
            "get_test_details",
            ("Suite/test()",),
            ["test-results", "test-details", "--test-id", "Suite/test()"],
        ),
        (
            "get_test_activities",
            ("Suite/test()",),
            ["test-results", "activities", "--test-id", "Suite/test()"],
        ),
        ("get_build_results", (), ["build-results"]),
        ("get_content_availability", (), ["content-availability"]),
    ],
)
def test_modern_report_routing(reader: str, arguments: tuple[str, ...], command: list[str]) -> None:
    """Route all public getters through a named modern endpoint."""
    with patch.object(xcresulttool, "_get") as get:
        getattr(xcresulttool, reader)("/bundle", *arguments)
    assert get.call_args.args[:2] == ("/bundle", command)


def test_tool_error_preserves_stderr() -> None:
    """Expose the actual xcresulttool diagnostic instead of an empty fallback."""
    error = subprocess.CalledProcessError(64, ["xcrun"], stderr="Unsupported bundle format\n")
    with patch("subprocess.run", side_effect=error):
        with pytest.raises(XcresultException, match="Unsupported bundle format"):
            xcresulttool.get_tests("/bundle")


def test_missing_tool_reports_error() -> None:
    """Report an unavailable Xcode installation."""
    with patch("subprocess.run", side_effect=FileNotFoundError("xcrun")):
        with pytest.raises(XcresultException, match="Could not run xcresulttool"):
            xcresulttool.get_tests("/bundle")


def test_malformed_json_is_not_silently_accepted() -> None:
    """Propagate malformed reports."""
    with patch("subprocess.run", return_value=Mock(stdout="not json")):
        with pytest.raises(json.JSONDecodeError):
            xcresulttool.get_tests("/bundle")


def test_export_reads_manifest(tmp_path: Path) -> None:
    """Use modern export filenames and test selectors, including empty manifests."""
    manifest = [
        {
            "testIdentifier": "Suite/test()",
            "testIdentifierURL": "test://target/Suite/test()",
            "attachments": [
                {
                    "exportedFileName": "payload.txt",
                    "suggestedHumanReadableName": "Text.txt",
                    "isAssociatedWithFailure": True,
                    "configurationName": "Debug",
                    "deviceName": "Mac",
                    "deviceId": "mac-id",
                }
            ],
        }
    ]
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with patch("subprocess.run", return_value=Mock(stdout="")) as run:
        entries = Xcresults("/bundle").export_test_attachments(str(tmp_path), "Suite/test()")
    assert entries[0].attachments[0].exportedFileName == "payload.txt"
    assert run.call_args.args[0] == [
        "xcrun",
        "xcresulttool",
        "export",
        "attachments",
        "--path",
        "/bundle",
        "--output-path",
        str(tmp_path),
        "--schema-version",
        SCHEMA_VERSION,
        "--test-id",
        "Suite/test()",
    ]
    (tmp_path / "manifest.json").write_text("[]", encoding="utf-8")
    with patch("subprocess.run", return_value=Mock(stdout="")):
        assert xcresulttool.export_test_attachments("/bundle", str(tmp_path)) == []


def test_export_missing_manifest_fails(tmp_path: Path) -> None:
    """A successful process without its expected manifest is not a successful export."""
    with patch("subprocess.run", return_value=Mock(stdout="")):
        with pytest.raises(FileNotFoundError):
            xcresulttool.export_test_attachments("/bundle", str(tmp_path))


@pytest.mark.parametrize("manifest", ["{}", "[{}]"])
def test_export_malformed_manifest_fails(tmp_path: Path, manifest: str) -> None:
    """Reject malformed manifest roots and entries."""
    (tmp_path / "manifest.json").write_text(manifest, encoding="utf-8")
    with patch("subprocess.run", return_value=Mock(stdout="")):
        with pytest.raises((ValueError, TypeError, XcresultException)):
            xcresulttool.export_test_attachments("/bundle", str(tmp_path))


def test_real_build_report(tmp_path: Path) -> None:
    """Decode a real build-only report without modifying the checked-in fixture."""
    if shutil.which("xcrun") is None:
        pytest.skip("Requires Xcode's xcresulttool")
    original = Path(__file__).parent / "data" / "BaseProjectFailure.xcresult"
    bundle_path = tmp_path / original.name
    shutil.copytree(original, bundle_path)
    report = Xcresults(str(bundle_path)).build_results
    assert report.errorCount == 1
    assert len(report.errors) == 1
    assert "Unable to open base configuration" in report.errors[0].message
    assert report.warningCount == len(report.warnings) == 1
