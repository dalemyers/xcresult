"""JUnit regressions for the modern test report contract."""

# pylint: disable=c-extension-no-member
# pylint: disable=duplicate-code
# pylint: disable=import-outside-toplevel

from pathlib import Path
from unittest.mock import Mock

from lxml import etree as ET
import pytest

from xcresult.junit_writer import JunitWriter, TestFilter
from xcresult.model import (
    Attachment,
    Configuration,
    ContentAvailability,
    Device,
    SourceLocation,
    TestAttachmentDetails,
    TestDetails,
    TestNode,
    TestResult,
    Tests,
)
from xcresult.xcresult_base import XcresultsBase


def _node(name: str = "test()", **properties: object) -> TestNode:
    """Create a modern test node from ordinary JSON-shaped fields."""
    return TestNode.from_dict({"name": name, "nodeType": "Test Case", **properties})


def _run(status: str, **properties: object) -> TestNode:
    """Create an individual execution node."""
    return _node(
        "Run 1", nodeType="Test Case Run", result=status, durationInSeconds=1.25, **properties
    )


def _details(runs: list[TestNode], result: TestResult = "Failed") -> TestDetails:
    """Create detailed runs for the example test."""
    return TestDetails(
        testIdentifier="Suite/test()",
        testIdentifierURL="test://target/Suite/test()",
        testName="test()",
        testDescription="A test",
        duration="2s",
        durationInSeconds=2.0,
        testPlanConfigurations=[Configuration(configurationId="1", configurationName="Debug")],
        devices=[
            Device(
                deviceId="mac",
                deviceName="Mac",
                architecture="arm64",
                modelName="Mac",
                osVersion="27",
            )
        ],
        testRuns=runs,
        testResult=result,
        hasPerformanceMetrics=False,
        hasMediaAttachments=False,
    )


@pytest.fixture(name="bundle")
def fixture_bundle() -> Mock:
    """Supply a typed-interface test double without running Xcode."""
    bundle = Mock(spec=XcresultsBase)
    bundle.content_availability = ContentAvailability(
        hasCoverage=False, hasDiagnostics=False, hasTestResults=True, logs=[]
    )
    test = _node(nodeIdentifier="Suite/test()", nodeIdentifierURL="test://target/Suite/test()")
    bundle.tests = Tests(
        testPlanConfigurations=[],
        devices=[],
        testNodes=[
            TestNode(
                nodeType="Unit test bundle",
                name="Target",
                children=[TestNode(nodeType="Test Suite", name="Suite", children=[test])],
            )
        ],
    )
    bundle.test_details.return_value = _details([_run("Failed"), _run("Passed")])
    bundle.export_test_attachments.return_value = []
    return bundle


def _write(
    bundle: Mock,
    tmp_path: Path,
    *,
    collapse_retries: bool = False,
    test_filter: TestFilter | None = None,
    export_attachments_path: str | None = None,
    test_class_prefix: str | None = None,
    test_class_suffix: str | None = None,
) -> ET._Element:
    """Generate and read a report."""
    output = tmp_path / "report.xml"
    JunitWriter(
        bundle,
        str(output),
        export_attachments_path=export_attachments_path,
        test_class_prefix=test_class_prefix,
        test_class_suffix=test_class_suffix,
        collapse_retries=collapse_retries,
        test_filter=test_filter,
    ).write()
    return ET.parse(str(output)).getroot()


def _find(root: ET._Element, path: str) -> ET._Element:
    """Find a required XML element."""
    element = root.find(path)
    assert element is not None, path
    return element


def test_default_preserves_attempts(bundle: Mock, tmp_path: Path) -> None:
    """Do not report an aggregate pass in place of a failed initial attempt."""
    root = _write(bundle, tmp_path)
    assert root.get("tests") == "2"
    assert root.get("failures") == "1"
    assert root.get("time") == "2.5"
    assert len(root.findall(".//testcase")) == 2
    assert _find(root, "testsuite").get("name") == "Target/Suite"
    bundle.test_details.assert_called_once_with("test://target/Suite/test()")


def test_collapse_prefers_pass(bundle: Mock, tmp_path: Path) -> None:
    """A passing retry wins and suite counts are based only on emitted attempts."""
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "1"
    assert root.get("failures") == "0"
    assert root.get("time") == "1.25"
    assert _find(root, "testsuite").get("tests") == "1"
    assert root.find(".//failure") is None


@pytest.mark.parametrize(
    ("statuses", "failures", "skipped"),
    [
        (["Failed", "Failed"], "1", "0"),
        (["Skipped", "Failed"], "1", "0"),
        (["Skipped", "Skipped"], "0", "1"),
        (["Expected Failure"], "0", "0"),
        (["unknown"], "1", "0"),
        (["Skipped", "unknown"], "1", "0"),
    ],
)
def test_collapse_statuses(
    bundle: Mock, tmp_path: Path, statuses: list[str], failures: str, skipped: str
) -> None:
    """Keep failures, skips and expected failures distinct."""
    bundle.test_details.return_value = _details([_run(status) for status in statuses])
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "1"
    assert root.get("failures") == failures
    assert root.get("skipped") == skipped


def test_filter_removes_xml_and_counts(bundle: Mock, tmp_path: Path) -> None:
    """An excluded test produces no empty suite or inflated totals."""
    root = _write(
        bundle,
        tmp_path,
        collapse_retries=True,
        test_filter=lambda test: test.nodeIdentifier != "Suite/test()",
    )
    assert root.get("tests") == root.get("failures") == root.get("skipped") == "0"
    assert not root.findall("testsuite")


def test_prefix_and_suffix(bundle: Mock, tmp_path: Path) -> None:
    """Preserve classname customization."""
    root = _write(bundle, tmp_path, test_class_prefix="Prefix", test_class_suffix="Suffix")
    assert _find(root, ".//testcase").get("classname") == "Prefix.Suite.Suffix"


def test_failure_location_and_skip_reason(bundle: Mock, tmp_path: Path) -> None:
    """Write modern diagnostic child nodes, not legacy summary references."""
    failure = TestNode(
        nodeType="Failure Message",
        name="Expected true",
        sourceLocation=SourceLocation(filePath="/Tests.swift", lineNumber=42),
    )
    skip = TestNode(nodeType="Skip Message", name="Not supported")
    bundle.test_details.return_value = _details(
        [
            TestNode(nodeType="Test Case Run", name="Run 1", result="Failed", children=[failure]),
            TestNode(nodeType="Test Case Run", name="Run 2", result="Skipped", children=[skip]),
        ]
    )
    root = _write(bundle, tmp_path)
    assert _find(root, ".//failure").get("message") == "Expected true (/Tests.swift:42)"
    assert _find(root, ".//skipped").get("message") == "Not supported"


def test_no_runs_skipped_test(bundle: Mock, tmp_path: Path) -> None:
    """Preserve skipped tests that have no per-run details."""
    bundle.test_details.return_value = _details([], result="Skipped")
    root = _write(bundle, tmp_path)
    assert root.get("tests") == root.get("skipped") == "1"


def test_build_only_bundle(bundle: Mock, tmp_path: Path) -> None:
    """Do not request test data from a build-only bundle."""
    bundle.content_availability.hasTestResults = False
    root = _write(bundle, tmp_path, export_attachments_path=str(tmp_path / "attachments"))
    assert root.get("tests") == "0"
    bundle.test_details.assert_not_called()
    bundle.export_test_attachments.assert_not_called()


def test_multiple_suite_counts_do_not_duplicate_tests(bundle: Mock, tmp_path: Path) -> None:
    """Each suite counts only its own emitted testcases."""
    bundle.tests.testNodes = [
        TestNode(
            nodeType="Test Suite",
            name="First",
            children=[
                _node("a", nodeIdentifier="First/a"),
                _node("b", nodeIdentifier="First/b"),
            ],
        ),
        TestNode(
            nodeType="Test Suite",
            name="Second",
            children=[
                _node("c", nodeIdentifier="Second/c"),
            ],
        ),
    ]
    bundle.test_details.side_effect = [
        _details([_run("Passed")]),
        _details([_run("Failed")]),
        _details([_run("Skipped")]),
    ]
    root = _write(bundle, tmp_path)
    assert root.get("tests") == "3"
    assert root.get("failures") == root.get("skipped") == "1"
    suites = root.findall("testsuite")
    assert [suite.get("tests") for suite in suites] == ["2", "1"]
    assert [suite.get("failures") for suite in suites] == ["1", "0"]
    assert [suite.get("skipped") for suite in suites] == ["0", "1"]


def test_run_children_carry_execution_dimensions(bundle: Mock, tmp_path: Path) -> None:
    """Retain environment metadata when it is attached to the run itself."""
    bundle.test_details.return_value = _details(
        [
            _run(
                "Failed",
                children=[
                    {"nodeType": "Device", "name": "Other Mac", "nodeIdentifier": "other"},
                    {"nodeType": "Test Plan Configuration", "name": "Release"},
                ],
            ),
            _run("Passed"),
        ]
    )
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "2"
    assert root.get("failures") == "1"
    assert len(root.findall("testsuite")) == 2


def test_unidentified_tests_never_collapse(bundle: Mock, tmp_path: Path) -> None:
    """Tests without stable IDs remain distinct."""
    bundle.tests.testNodes = [_node("a", result="Passed"), _node("b", result="Passed")]
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "2"
    bundle.test_details.assert_not_called()


def test_collapse_preserves_execution_dimensions(bundle: Mock, tmp_path: Path) -> None:
    """Retries must not merge executions in different environments or with different arguments."""
    runs = []
    for device in ("one", "two"):
        for configuration in ("Debug", "Release"):
            for argument in ("(1)", "(2)"):
                runs.append(
                    TestNode(
                        nodeType="Device",
                        name=device,
                        nodeIdentifier=device,
                        children=[
                            TestNode(
                                nodeType="Test Plan Configuration",
                                name=configuration,
                                children=[
                                    TestNode(
                                        nodeType="Arguments",
                                        name=argument,
                                        children=[
                                            _run("Failed"),
                                            _run("Passed"),
                                        ],
                                    )
                                ],
                            )
                        ],
                    )
                )
    bundle.test_details.return_value = _details(runs)
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "8"
    assert root.get("failures") == "0"
    assert len(root.findall("testsuite")) == 4
    assert all(suite.get("tests") == "2" for suite in root.findall("testsuite"))


def test_attachment_manifest_links(bundle: Mock, tmp_path: Path) -> None:
    """Resolve actual exported filenames and tolerate tests with no attachments."""
    output = tmp_path / "attachments"
    output.mkdir()
    (output / "file.txt").write_text("failure attachment", encoding="utf-8")
    bundle.export_test_attachments.return_value = [
        TestAttachmentDetails(
            testIdentifier="Suite/test()",
            testIdentifierURL="test://target/Suite/test()",
            attachments=[
                Attachment(
                    exportedFileName="file.txt",
                    suggestedHumanReadableName="Message.txt",
                    isAssociatedWithFailure=True,
                    configurationName="Debug",
                    deviceName="Mac",
                    deviceId="mac",
                )
            ],
        )
    ]
    root = _write(bundle, tmp_path, export_attachments_path=str(output))
    text = _find(root, ".//system-out").text
    assert text is not None
    assert "[[ATTACHMENT|attachments/file.txt]]" in text
    assert len(root.findall(".//system-out")) == 1


def test_no_attachments_needs_no_guessed_directory(bundle: Mock, tmp_path: Path) -> None:
    """A failed test without media should still produce a valid report."""
    root = _write(bundle, tmp_path, export_attachments_path=str(tmp_path / "attachments"))
    assert root.get("failures") == "1"
    assert root.find(".//system-out") is None


@pytest.mark.parametrize("filename", ["../outside.txt", "/outside.txt"])
def test_attachment_manifest_cannot_escape_output(
    bundle: Mock, tmp_path: Path, filename: str
) -> None:
    """Do not emit links outside the requested attachment directory."""
    bundle.export_test_attachments.return_value = [
        TestAttachmentDetails(
            testIdentifier="Suite/test()",
            attachments=[
                Attachment(
                    exportedFileName=filename,
                    suggestedHumanReadableName="Text",
                    isAssociatedWithFailure=True,
                    configurationName="Debug",
                    deviceName="Mac",
                    deviceId="mac",
                )
            ],
        )
    ]
    with pytest.raises(ValueError, match="escapes"):
        _write(bundle, tmp_path, export_attachments_path=str(tmp_path / "attachments"))


def test_human_duration_fallback(bundle: Mock, tmp_path: Path) -> None:
    """Use seconds in XML even when the tool only provides a human duration."""
    bundle.test_details.return_value = _details(
        [TestNode(nodeType="Test Case Run", name="Run", result="Passed", duration="1m 2.5s")]
    )
    root = _write(bundle, tmp_path)
    assert _find(root, ".//testcase").get("time") == "62.5"


def test_unrecognized_run_tree_fails(bundle: Mock, tmp_path: Path) -> None:
    """Do not quietly convert a new unsupported run structure into an aggregate pass."""
    bundle.test_details.return_value = _details([_node("Run", nodeType="New Run Type")])
    with pytest.raises(ValueError, match="No test case runs"):
        _write(bundle, tmp_path)


def _configuration_runs(children: list[TestNode], status: TestResult = "Passed") -> list[TestNode]:
    """Model the public Device -> Configuration execution shape."""
    return [
        TestNode(
            nodeType="Device",
            nodeIdentifier="mac",
            name="Mac",
            result=status,
            durationInSeconds=3.5,
            children=[
                TestNode(
                    nodeType="Test Plan Configuration",
                    nodeIdentifier="1",
                    name="Debug",
                    result=status,
                    durationInSeconds=3.5,
                    children=children,
                )
            ],
        )
    ]


def test_passing_configuration_is_an_execution(bundle: Mock, tmp_path: Path) -> None:
    """Passing reports do not need a Test Case Run leaf."""
    bundle.test_details.return_value = _details(_configuration_runs([]), result="Passed")
    root = _write(bundle, tmp_path)
    assert root.get("tests") == "1"
    assert root.get("failures") == "0"
    assert root.get("time") == "3.5"


def test_failure_diagnostics_are_not_extra_runs(bundle: Mock, tmp_path: Path) -> None:
    """Multiple diagnostic Test Case Run nodes belong to one timed configuration run."""
    diagnostics = [
        TestNode(nodeType="Test Case Run", name="First assertion failed", result="Failed"),
        TestNode(nodeType="Test Case Run", name="Second assertion failed", result="Failed"),
    ]
    bundle.test_details.return_value = _details(_configuration_runs(diagnostics, "Failed"))
    root = _write(bundle, tmp_path)
    assert root.get("tests") == root.get("failures") == "1"
    assert root.get("time") == "3.5"
    assert _find(root, ".//failure").get("message") == (
        "First assertion failed\nSecond assertion failed"
    )


def test_skip_diagnostic_uses_configuration_duration(bundle: Mock, tmp_path: Path) -> None:
    """Skipped diagnostic nodes do not erase the enclosing execution metadata."""
    diagnostics = [TestNode(nodeType="Test Case Run", name="Unavailable API", result="Skipped")]
    bundle.test_details.return_value = _details(_configuration_runs(diagnostics, "Skipped"))
    root = _write(bundle, tmp_path)
    assert root.get("tests") == root.get("skipped") == "1"
    assert _find(root, ".//skipped").get("message") == "Unavailable API"


def test_wrapperless_argument_runs_keep_individual_time(bundle: Mock, tmp_path: Path) -> None:
    """Argument leaves are executions; the top-level duration is only an average."""
    bundle.test_details.return_value = _details(
        [
            TestNode(
                nodeType="Arguments", name="one, portrait", result="Passed", durationInSeconds=1
            ),
            TestNode(
                nodeType="Arguments", name="two, landscape", result="Passed", durationInSeconds=5
            ),
        ],
        result="Passed",
    )
    root = _write(bundle, tmp_path, collapse_retries=True)
    assert root.get("tests") == "2"
    assert root.get("time") == "6"
    assert [case.get("time") for case in root.findall(".//testcase")] == ["1", "5"]


@pytest.mark.parametrize(("collapse", "tests", "failures"), [(False, "2", "1"), (True, "1", "0")])
def test_tests_tree_preserves_retries(
    bundle: Mock, tmp_path: Path, collapse: bool, tests: str, failures: str
) -> None:
    """Prefer explicit repetitions to an aggregate passing details report."""
    test = _node(nodeIdentifier="Suite/test()", nodeIdentifierURL="test://target/Suite/test()")
    test.children = [
        TestNode(
            nodeType="Repetition",
            name="First attempt",
            nodeIdentifier="1",
            result="Failed",
            durationInSeconds=1.0,
            children=[TestNode(nodeType="Failure Message", name="Failed once")],
        ),
        TestNode(
            nodeType="Repetition",
            name="Second attempt",
            nodeIdentifier="2",
            result="Passed",
            durationInSeconds=2.0,
        ),
    ]
    bundle.tests.testNodes = [test]
    bundle.test_details.return_value = _details(_configuration_runs([]), result="Passed")
    root = _write(bundle, tmp_path, collapse_retries=collapse)
    assert root.get("tests") == tests
    assert root.get("failures") == failures
    if not collapse:
        assert _find(root, ".//failure").get("message") == "Failed once"


def test_localized_decimal_duration(bundle: Mock, tmp_path: Path) -> None:
    """Handle decimal commas in legacy modern-report display durations."""
    bundle.test_details.return_value = _details(
        [
            TestNode(
                nodeType="Test Plan Configuration",
                name="Debug",
                result="Passed",
                duration="0,0011s",
            )
        ]
    )
    root = _write(bundle, tmp_path)
    assert root.get("time") == "0.0011"


def test_repetition_attachment_matching(bundle: Mock, tmp_path: Path) -> None:
    """Use numeric repetition identifiers rather than extracting numbers from display names."""
    output = tmp_path / "attachments"
    output.mkdir()
    for name in ("first.txt", "second.txt"):
        (output / name).write_text("attachment", encoding="utf-8")
    bundle.test_details.return_value = _details(
        [
            TestNode(
                nodeType="Repetition",
                nodeIdentifier="1",
                name="Attempt A",
                result="Failed",
                durationInSeconds=1,
            ),
            TestNode(
                nodeType="Repetition",
                nodeIdentifier="2",
                name="Attempt B",
                result="Failed",
                durationInSeconds=1,
            ),
        ]
    )
    bundle.export_test_attachments.return_value = [
        TestAttachmentDetails(
            testIdentifier="Suite/test()",
            attachments=[
                Attachment(
                    exportedFileName=name,
                    suggestedHumanReadableName=name,
                    isAssociatedWithFailure=True,
                    configurationName="Debug",
                    deviceName="Mac",
                    deviceId="mac",
                    repetitionNumber=number,
                )
                for number, name in enumerate(("first.txt", "second.txt"), start=1)
            ],
        )
    ]
    root = _write(bundle, tmp_path, export_attachments_path=str(output))
    assert [element.text for element in root.findall(".//system-out")] == [
        "\n[[ATTACHMENT|attachments/first.txt]]\n",
        "\n[[ATTACHMENT|attachments/second.txt]]\n",
    ]
