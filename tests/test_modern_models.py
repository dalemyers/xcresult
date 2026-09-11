"""Regression tests for strict modern JSON models and decoding."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Literal, get_args

import pytest

from xcresult.exceptions import MissingPropertyException, UnsupportedTypeException
from xcresult.model import (
    Activities,
    ActivityAttachment,
    Attachment,
    AttachmentDetails,
    BuildResults,
    ContentAvailability,
    Summary,
    TestNode as Node,
    TestNodeType as NodeType,
    TestResult as Result,
    Tests as Nodes,
)
from xcresult.model_base import XcresultObject, deserialize


def test_models_are_not_pytest_test_classes() -> None:
    """Prevent imported Apple Test-prefixed models from being collected by pytest."""
    assert Node.__test__ is False
    assert Nodes.__test__ is False


def test_recursive_decode_is_typed_and_nonmutating() -> None:
    """Build independent recursive object trees without consuming source properties."""
    data = {
        "testPlanConfigurations": [],
        "devices": [],
        "testNodes": [
            {
                "name": "suite",
                "nodeType": "Test Suite",
                "children": [{"name": "test", "nodeType": "Test Case", "durationInSeconds": 2}],
            }
        ],
    }
    original = deepcopy(data)
    result = Nodes.from_dict(data)
    assert isinstance(result.testNodes[0], Node)
    children = result.testNodes[0].children
    assert children is not None
    child = children[0]
    assert isinstance(child, Node)
    assert child.durationInSeconds == 2.0
    assert isinstance(child.durationInSeconds, float)
    assert child.children is None
    result.testNodes.clear()
    assert data == original


def test_required_and_optional_properties() -> None:
    """Do not replace missing required fields with None or fabricated defaults."""
    with pytest.raises(TypeError):
        # pylint: disable-next=missing-kwoa
        Node(name="missing nodeType")  # type: ignore[call-arg] # pyright: ignore[reportCallIssue]
    with pytest.raises(MissingPropertyException, match=r"\$\.nodeType"):
        Node.from_dict({"name": "missing nodeType"})
    with pytest.raises(MissingPropertyException, match=r"\$\.children\[0\]\.name"):
        Node.from_dict(
            {"name": "suite", "nodeType": "Test Suite", "children": [{"nodeType": "Test Case"}]}
        )
    node = Node.from_dict({"name": "test", "nodeType": "Test Case", "children": None})
    assert node.children is None
    with pytest.raises(UnsupportedTypeException, match=r"\$\.name"):
        Node.from_dict({"name": None, "nodeType": "Test Case"})


@pytest.mark.parametrize(
    ("value", "target"),
    [
        (True, int),
        (1, bool),
        ("2", int),
        ("2.0", float),
        (False, float),
        (3, str),
        ({}, list[str]),
        ([1], list[str]),
        ([], Node),
        ({"name": 12, "nodeType": "Test Case"}, Node),
        ({1: "value"}, Node),
        ({}, dict[str, str]),
    ],
)
def test_invalid_types_are_rejected(value: object, target: object) -> None:
    """Distinguish JSON types without coercing strings or treating booleans as numbers."""
    with pytest.raises(UnsupportedTypeException, match=r"\$"):
        deserialize(value, target)


def test_unknown_properties_are_logged(caplog: pytest.LogCaptureFixture) -> None:
    """Ignore forward-compatible properties with a useful diagnostic path."""
    node = Node.from_dict({"name": "test", "nodeType": "Future Node", "newField": {"a": 1}})
    assert node.nodeType == "Future Node"
    assert "$.newField" in caplog.text
    assert "TestNode" in caplog.text


def test_future_string_enums_and_numeric_literals() -> None:
    """Keep new Apple enum strings but still enforce their underlying JSON type."""
    assert deserialize("New State", Literal["Passed", "Failed"]) == "New State"
    assert deserialize(1, Literal[1, 2]) == 1
    with pytest.raises(UnsupportedTypeException):
        deserialize(True, Literal[1, 2])
    with pytest.raises(UnsupportedTypeException):
        deserialize(3, Literal[1, 2])


def test_public_enum_aliases_declare_string_fallback() -> None:
    """Generated public enum annotations agree with their forward-compatible decoder."""
    assert str in get_args(Result)
    assert str in get_args(NodeType)
    node = Node.from_dict({"name": "test", "nodeType": "Future Node", "result": "Future Result"})
    assert node.nodeType == "Future Node"
    assert node.result == "Future Result"


def test_manifest_array_and_distinct_attachments() -> None:
    """Decode the exported manifest's named array without confusing activity payloads."""
    manifest = [
        {
            "testIdentifier": "Suite/test",
            "attachments": [
                {
                    "exportedFileName": "image.png",
                    "suggestedHumanReadableName": "Screenshot.png",
                    "isAssociatedWithFailure": False,
                    "configurationName": "Debug",
                    "deviceName": "Mac",
                    "deviceId": "device",
                    "arguments": ["42"],
                }
            ],
        }
    ]
    result = deserialize(manifest, AttachmentDetails)
    assert isinstance(result[0].attachments[0], Attachment)
    assert result[0].attachments[0].arguments == ["42"]
    activity = ActivityAttachment.from_dict({"name": "log", "uuid": "id", "lifetime": "keepAlways"})
    assert activity.payloadId is None
    with pytest.raises(MissingPropertyException):
        Attachment.from_dict({"name": "log", "uuid": "id", "lifetime": "keepAlways"})


def test_content_availability_requires_all_fields() -> None:
    """Keep required booleans and empty collections rather than relying on truthiness."""
    result = ContentAvailability.from_dict(
        {"hasCoverage": False, "hasDiagnostics": False, "hasTestResults": False, "logs": []}
    )
    assert result.logs == []
    assert result.hasCoverage is False
    with pytest.raises(MissingPropertyException, match="logs"):
        ContentAvailability.from_dict(
            {"hasCoverage": False, "hasDiagnostics": False, "hasTestResults": False}
        )


def test_required_nullable_fields_remain_required() -> None:
    """Nullable annotation alone does not imply a default or optional property."""

    @dataclass(kw_only=True)
    class Nullable(XcresultObject):
        """Synthetic required nullable field."""

        value: str | None

    assert Nullable.from_dict({"value": None}).value is None
    with pytest.raises(MissingPropertyException, match="value"):
        Nullable.from_dict({})


def test_build_results_decode_nested_device_and_issues() -> None:
    """Decode build reports using their endpoint schema's required fields."""
    report = BuildResults.from_dict(
        {
            "destination": {
                "deviceId": "mac",
                "deviceName": "Mac",
                "architecture": "arm64",
                "modelName": "Mac",
                "osVersion": "27",
            },
            "startTime": 1,
            "endTime": 2,
            "analyzerWarnings": [],
            "warnings": [{"issueType": "Warning", "message": "example"}],
            "errors": [],
        }
    )
    assert report.destination.deviceName == "Mac"
    assert report.warnings[0].message == "example"
    assert report.warnings[0].sourceURL is None
    assert report.status is None


def test_verified_summary_and_activity_wire_arrays() -> None:
    """Decode the array shapes verified in public modern xcresulttool reports."""
    device = {
        "architecture": "arm64",
        "deviceId": "device",
        "deviceName": "iPhone 17 Pro",
        "modelName": "iPhone 17 Pro",
        "osVersion": "26.2",
    }
    configuration = {"configurationId": "1", "configurationName": "Test Scheme Action"}
    summary = Summary.from_dict(
        {
            "title": "Tests",
            "environmentDescription": "iOS Simulator",
            "topInsights": [],
            "result": "Passed",
            "totalTestCount": 1,
            "passedTests": 1,
            "failedTests": 0,
            "skippedTests": 0,
            "expectedFailures": 0,
            "statistics": [],
            "devicesAndConfigurations": [
                {
                    "device": device,
                    "testPlanConfiguration": configuration,
                    "passedTests": 1,
                    "failedTests": 0,
                    "skippedTests": 0,
                    "expectedFailures": 0,
                }
            ],
            "testFailures": [],
            "runtimeWarnings": [],
        }
    )
    assert summary.devicesAndConfigurations[0].device.deviceName == "iPhone 17 Pro"
    activities = Activities.from_dict(
        {
            "testIdentifier": "Suite/test()",
            "testName": "test()",
            "testRuns": [
                {"activities": [], "device": device, "testPlanConfiguration": configuration}
            ],
        }
    )
    assert activities.testRuns[0].activities == []
    assert activities.testRuns[0].testPlanConfiguration.configurationId == "1"
    assert (
        Activities.from_dict(
            {"testIdentifier": "Suite/test()", "testName": "test()", "testRuns": []}
        ).testRuns
        == []
    )
