"""Synthetic coverage of schema resolution and modern model generation."""

from collections.abc import Iterator
from copy import deepcopy
import json
import sys
from types import ModuleType
from typing import cast, get_args
from unittest.mock import Mock, patch

import pytest

from generator import (
    ENDPOINTS,
    SCHEMA_VERSION,
    ModelGenerator,
    SchemaError,
    correct_schema_errors,
    load_schemas,
)
from xcresult.model_base import deserialize


def _module(schemas: dict[str, object]) -> ModuleType:
    """Compile generated models in memory so forward annotations can be resolved."""
    module_name = "_generated_test_models"
    module = ModuleType(module_name)
    sys.modules[module_name] = module
    try:
        exec(  # pylint: disable=exec-used
            ModelGenerator([{"schemas": schemas}]).render(), module.__dict__
        )
    except Exception:
        del sys.modules[module_name]
        raise
    return module


@pytest.fixture(autouse=True)
def fixture_cleanup_generated_module() -> Iterator[None]:
    """Remove the in-memory generated module after every test."""
    yield
    sys.modules.pop("_generated_test_models", None)


def test_recursive_nodes_inline_objects_named_arrays() -> None:
    """Resolve recursion, forward aliases, and anonymous array item objects."""
    # These attributes exist only after executing the generated model module.
    # pylint: disable=no-member
    module = _module(
        {
            "Manifest": {"type": "array", "items": {"$ref": "#/schemas/Node"}},
            "Node": {
                "type": "object",
                "properties": {
                    "name": {"$ref": "#/schemas/Name"},
                    "children": {"$ref": "#/schemas/Manifest"},
                    "arguments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"value": {"type": "string"}},
                            "required": ["value"],
                        },
                    },
                },
                "required": ["name"],
            },
            "Name": {"type": "string"},
        }
    )
    result = deserialize(
        [{"name": "parent", "children": [{"name": "child"}], "arguments": [{"value": "1"}]}],
        module.Manifest,
    )
    assert result[0].children[0].name == "child"
    assert result[0].arguments[0].value == "1"
    assert result[0].children[0].children is None
    with pytest.raises(TypeError):
        module.Node()
    with pytest.raises(TypeError):
        module.Node("positional")


def test_generation_is_deterministic_and_nonmutating() -> None:
    """Repeated rendering preserves the original schema documents."""
    documents = [{"schemas": {"Flag": {"type": "boolean"}}}]
    original = deepcopy(documents)
    generator = ModelGenerator(cast(list[dict[str, object]], documents))
    assert generator.render() == generator.render()
    assert documents == original


def test_duplicate_definition_handling() -> None:
    """Deduplicate identical definitions but reject conflicting definitions."""
    first: dict[str, object] = {"schemas": {"Name": {"type": "string"}}}
    assert "Name: TypeAlias = str" in ModelGenerator([first, first]).render()
    with pytest.raises(SchemaError, match="Incompatible duplicate.*Name"):
        ModelGenerator([first, {"schemas": {"Name": {"type": "integer"}}}])


@pytest.mark.parametrize(
    "schema",
    [
        {},
        {"type": "mystery"},
        {"type": ["string", "null"]},
        {"oneOf": [{"type": "string"}, {"type": "integer"}]},
        {"type": "object", "additionalProperties": {"type": "string"}},
        {"type": "array"},
        {"type": "array", "items": [{"type": "string"}]},
        {"type": "string", "pattern": "[a-z]+"},
        {"type": "string", "enum": [1]},
        {"type": "string", "enum": []},
        {"$ref": "#/schemas/Missing"},
        {"$ref": "https://example.com/schema"},
        {"$ref": "#/schemas/Name", "type": "string"},
        {"type": "object", "required": ["missing"]},
        {"type": "object", "properties": {"class": {"type": "string"}}},
    ],
)
def test_unsupported_or_malformed_schema_fails(schema: dict[str, object]) -> None:
    """Never silently degrade an unsupported schema into an untyped model."""
    with pytest.raises(SchemaError):
        ModelGenerator([{"schemas": {"Name": schema}}]).render()


def test_incompatible_inline_definition_fails() -> None:
    """Inline-generated names must not overwrite independently named types."""
    with pytest.raises(SchemaError, match="Incompatible duplicate.*NodeValue"):
        ModelGenerator(
            [
                {
                    "schemas": {
                        "NodeValue": {"type": "string"},
                        "Node": {
                            "type": "object",
                            "properties": {"value": {"type": "object", "properties": {}}},
                        },
                    }
                }
            ]
        ).render()


def test_recursive_scalar_aliases_fail_explicitly() -> None:
    """Detect impossible alias cycles instead of hanging during dependency sorting."""
    with pytest.raises(SchemaError, match="Recursive aliases"):
        ModelGenerator(
            [
                {
                    "schemas": {
                        "First": {"$ref": "#/schemas/Second"},
                        "Second": {"$ref": "#/schemas/First"},
                    }
                }
            ]
        ).render()


def test_scalar_alias_order_nulls_and_empty_objects() -> None:
    """Emit aliases in dependency order and support null and empty object schemas."""
    # These attributes exist only after executing the generated model module.
    # pylint: disable=no-member
    module = _module(
        {
            "Names": {"type": "array", "items": {"$ref": "#/schemas/Name"}},
            "Name": {"$ref": "#/schemas/Text"},
            "Text": {"type": "string"},
            "Null": {"type": "null"},
            "Empty": {"type": "object"},
            "OptionalNull": {
                "type": "object",
                "properties": {"value": {"$ref": "#/schemas/Null"}},
            },
        }
    )
    assert deserialize(["a", "b"], module.Names) == ["a", "b"]
    assert deserialize(None, module.Null) is None
    assert module.OptionalNull.from_dict({}).value is None
    assert module.OptionalNull.from_dict({"value": None}).value is None
    assert isinstance(deserialize({}, module.Empty), module.Empty)


def test_reserved_type_names_fail() -> None:
    """Never emit schemas that accidentally shadow annotation builtins or helpers."""
    with pytest.raises(SchemaError, match="shadows a generated name"):
        ModelGenerator([{"schemas": {"list": {"type": "string"}}}])


def test_string_enum_annotations_accept_future_values() -> None:
    """Keep known-value hints without promising a closed set of wire strings."""
    # The alias exists only after executing the generated model module.
    # pylint: disable=no-member
    module = _module({"State": {"type": "string", "enum": ["Passed", "Failed"]}})
    assert str in get_args(module.State)
    assert deserialize("Future State", module.State) == "Future State"


def test_schema_commands_and_attachment_renaming() -> None:
    """Fetch all modern endpoints and consistently rename conflicting activity refs."""
    generic = json.dumps({"schemas": {}})
    activity = {
        "schemas": {
            "Activities": {
                "type": "object",
                "properties": {"testRuns": {"$ref": "#/schemas/TestRunActivities"}},
            },
            "TestRunActivities": {"type": "object"},
            "Attachment": {"type": "object", "properties": {"uuid": {"type": "string"}}},
            "ActivityNode": {
                "type": "object",
                "properties": {
                    "attachments": {
                        "type": "array",
                        "items": {"$ref": "#/schemas/Attachment"},
                    }
                },
            },
        }
    }
    summary = {
        "schemas": {
            "Summary": {
                "type": "object",
                "properties": {
                    "devicesAndConfigurations": {"$ref": "#/schemas/DeviceAndConfigurationSummary"}
                },
            },
            "DeviceAndConfigurationSummary": {"type": "object"},
        }
    }
    endpoint_output = {"summary": json.dumps(summary), "activities": json.dumps(activity)}
    responses = [Mock(stdout=endpoint_output.get(endpoint[-1], generic)) for endpoint in ENDPOINTS]
    with patch("generator.subprocess.run", side_effect=responses) as run:
        documents = load_schemas()
    assert run.call_count == len(ENDPOINTS)
    for call, endpoint in zip(run.call_args_list, ENDPOINTS):
        expected_command = ["xcrun", "xcresulttool", *endpoint]
        expected_command.extend(["--schema", "--schema-version", SCHEMA_VERSION])
        assert call.args[0] == expected_command
        assert call.kwargs == {"check": True, "capture_output": True, "text": True}
    source = ModelGenerator(documents).render()
    assert "class ActivityAttachment(" in source
    assert "attachments: list[ActivityAttachment] | None = None" in source
    assert "class Attachment(" not in source


@pytest.mark.parametrize(
    ("endpoint", "model", "field", "target"),
    [
        (
            ("get", "test-results", "summary"),
            "Summary",
            "devicesAndConfigurations",
            "DeviceAndConfigurationSummary",
        ),
        (
            ("get", "test-results", "activities"),
            "Activities",
            "testRuns",
            "TestRunActivities",
        ),
    ],
)
def test_array_corrections_are_narrow_and_nonmutating(
    endpoint: tuple[str, ...], model: str, field: str, target: str
) -> None:
    """Correct only verified shapes, supporting an upstream fix without guessing."""
    reference = {"$ref": f"#/schemas/{target}"}
    properties: dict[str, object] = {field: reference}
    document: dict[str, object] = {"schemas": {model: {"type": "object", "properties": properties}}}
    original = deepcopy(document)
    corrected = correct_schema_errors(document, endpoint)
    assert corrected == {
        "schemas": {
            model: {
                "type": "object",
                "properties": {field: {"type": "array", "items": reference}},
            }
        }
    }
    assert correct_schema_errors(corrected, endpoint) == corrected
    assert document == original
    assert correct_schema_errors(document, ("get", "build-results")) == document
    properties[field] = {"type": "string"}
    with pytest.raises(SchemaError, match="correction no longer applies"):
        correct_schema_errors(document, endpoint)
