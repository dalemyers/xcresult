"""Opt-in end-to-end tests against Xcode and the real result bundles."""

# pylint: disable=c-extension-no-member

import os
from pathlib import Path
import shutil

from lxml import etree as ET
import pytest

from xcresult import Xcresults
from xcresult.model import TestNode

pytestmark = pytest.mark.skipif(
    os.environ.get("XCRESULT_RUN_INTEGRATION") != "1",
    reason="Set XCRESULT_RUN_INTEGRATION=1 to run live Xcode test-report/export checks",
)


def _cases(nodes: list[TestNode]) -> list[TestNode]:
    """Collect test cases without their diagnostic children."""
    cases: list[TestNode] = []
    for node in nodes:
        if node.nodeType == "Test Case":
            cases.append(node)
        else:
            cases.extend(_cases(node.children or []))
    return cases


@pytest.mark.parametrize("name", ["TestSuccess", "TestFailure"])
def test_live_reports_and_exports(tmp_path: Path, name: str) -> None:
    """Read test reports, activities, attachments, and JUnit from an isolated bundle."""
    original = Path(__file__).parent / "data" / f"{name}.xcresult"
    copy = tmp_path / original.name
    shutil.copytree(original, copy)
    bundle = Xcresults(str(copy))
    assert bundle.content_availability.hasTestResults
    summary = bundle.test_summary
    assert summary.totalTestCount > 0
    cases = _cases(bundle.tests.testNodes)
    assert cases
    for test in cases:
        identifier = test.nodeIdentifierURL or test.nodeIdentifier
        assert identifier is not None
        details = bundle.test_details(identifier)
        assert details.testName
        if details.testRuns:
            assert bundle.test_activities(identifier).testRuns
    attachments_path = tmp_path / "attachments"
    manifest = bundle.export_test_attachments(str(attachments_path))
    assert (attachments_path / "manifest.json").is_file()
    for entry in manifest:
        for attachment in entry.attachments:
            assert (attachments_path / attachment.exportedFileName).is_file()
    report = tmp_path / "report.xml"
    bundle.write_junit(
        str(report),
        export_attachments_path=str(tmp_path / "junit-attachments"),
        collapse_retries=True,
    )
    root = ET.parse(str(report)).getroot()
    assert int(root.get("tests", "0")) == len(root.findall(".//testcase")) > 0
    assert int(root.get("failures", "0")) == len(root.findall(".//failure"))
    if name == "TestSuccess":
        assert summary.failedTests == int(root.get("failures", "0")) == 0
    elif name == "TestFailure":
        assert summary.failedTests > 0
        assert int(root.get("failures", "0")) > 0
        if any(entry.attachments for entry in manifest):
            links = [
                line[len("[[ATTACHMENT|") : -2]
                for element in root.findall(".//system-out")
                for line in (element.text or "").splitlines()
                if line.startswith("[[ATTACHMENT|") and line.endswith("]]")
            ]
            assert links
            assert all((report.parent / link).is_file() for link in links)
