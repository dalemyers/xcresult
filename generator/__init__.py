"""Generate typed models from the modern xcresulttool JSON endpoint schemas.

Run ``python -m generator`` using Xcode 27. Schema version 0.4 is deliberately
pinned so a newer Xcode cannot silently change the checked-in public model API.
"""

from __future__ import annotations

from copy import deepcopy
import json
import keyword
from pathlib import Path
import subprocess
from typing import cast

SCHEMA_VERSION = "0.4.0"
ENDPOINTS = (
    ("get", "test-results", "summary"),
    ("get", "test-results", "tests"),
    ("get", "test-results", "test-details"),
    ("get", "test-results", "activities"),
    ("get", "build-results"),
    ("get", "content-availability"),
    ("export", "attachments"),
)


class SchemaError(ValueError):
    """An endpoint schema cannot be represented safely."""


def _mapping(value: object, path: str) -> dict[str, object]:
    """Validate a JSON object at the untyped JSON parsing boundary."""
    if not isinstance(value, dict):
        raise SchemaError(f"{path}: expected an object")
    if not all(isinstance(key, str) for key in cast(dict[object, object], value)):
        raise SchemaError(f"{path}: expected string keys")
    return cast(dict[str, object], value)


def _name(value: str) -> str:
    """Validate an identifier without changing Apple's public field spelling."""
    if not value.isidentifier() or keyword.iskeyword(value):
        raise SchemaError(f"Unsupported Python identifier: {value!r}")
    return value


def _type_name(value: str) -> str:
    """Prevent schema types from shadowing names used by generated annotations."""
    _name(value)
    if value in {
        "str",
        "int",
        "float",
        "bool",
        "list",
        "Literal",
        "TypeAlias",
        "NoneType",
        "XcresultObject",
        "dataclass",
        "SCHEMA_VERSION",
        "__all__",
    }:
        raise SchemaError(f"Schema type shadows a generated name: {value}")
    return value


def _rename_references(value: object, renames: dict[str, str]) -> object:
    """Copy a schema while consistently renaming endpoint-local references."""
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, item in _mapping(cast(object, value), "schema").items():
            if key == "$ref" and isinstance(item, str):
                prefix = "#/schemas/"
                if not item.startswith(prefix):
                    raise SchemaError(f"Unsupported reference {item!r}")
                item = prefix + renames.get(item[len(prefix) :], item[len(prefix) :])
            result[key] = _rename_references(item, renames)
        return result
    if isinstance(value, list):
        return [_rename_references(item, renames) for item in cast(list[object], value)]
    return value


def correct_schema_errors(
    document: dict[str, object], endpoint: tuple[str, ...]
) -> dict[str, object]:
    """Correct two verified Apple schema 0.4.0 object-versus-array mistakes.

    Public raw JSON evidence (not locally regenerated reports):
    - codemagic-ci-cd/cli-tools commit feb80b2d944923402e56b825f40c038a39f35b64,
      tests/models/xctests/mocks/test_results_summary.json, lines 1-21.
    - alvarhansen/OpenXCResultTool commit 070f69b6ed758fc997707b2591ce43d26b25e3db,
      Tests/Fixtures/Test-RandomStuff-2026.01.11_12-36-33-+0200.activities.testExample.json,
      lines 1-25.

    Source URLs:
    https://github.com/codemagic-ci-cd/cli-tools/blob/feb80b2d944923402e56b825f40c038a39f35b64/tests/models/xctests/mocks/test_results_summary.json#L1-L21
    https://github.com/alvarhansen/OpenXCResultTool/blob/070f69b6ed758fc997707b2591ce43d26b25e3db/Tests/Fixtures/Test-RandomStuff-2026.01.11_12-36-33-%2B0200.activities.testExample.json#L1-L25

    Both properties contain arrays on the wire. Keep these endpoint-specific
    corrections narrow, and fail rather than guessing if the schema changes.
    """
    corrected = deepcopy(document)
    corrections: dict[tuple[str, ...], tuple[str, str, str]] = {
        ("get", "test-results", "summary"): (
            "Summary",
            "devicesAndConfigurations",
            "DeviceAndConfigurationSummary",
        ),
        ("get", "test-results", "activities"): ("Activities", "testRuns", "TestRunActivities"),
    }
    if endpoint not in corrections:
        return corrected
    model, field, target = corrections[endpoint]
    schemas = _mapping(corrected.get("schemas"), "schemas")
    definition = _mapping(schemas.get(model), model)
    properties = _mapping(definition.get("properties"), f"{model}.properties")
    reference = {"$ref": f"#/schemas/{target}"}
    array = {"type": "array", "items": reference}
    if properties.get(field) not in (reference, array):
        raise SchemaError(f"{model}.{field}: verified schema correction no longer applies")
    properties[field] = array
    return corrected


def load_schemas() -> list[dict[str, object]]:
    """Fetch each modern schema and disambiguate endpoint-specific type names."""
    documents: list[dict[str, object]] = []
    for endpoint in ENDPOINTS:
        command = [
            "xcrun",
            "xcresulttool",
            *endpoint,
            "--schema",
            "--schema-version",
            SCHEMA_VERSION,
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        document: dict[str, object] = _mapping(json.loads(completed.stdout), "document")
        document = correct_schema_errors(document, endpoint)
        if endpoint[-1] == "activities":
            schemas = _mapping(document.get("schemas"), "schemas")
            renames = {"Attachment": "ActivityAttachment"}
            document = {
                "schemas": {
                    renames.get(name, name): _rename_references(schema, renames)
                    for name, schema in schemas.items()
                }
            }
        documents.append(document)
    return documents


class ModelGenerator:
    """Resolve modern JSON schemas without merging incompatible definitions."""

    def __init__(self, documents: list[dict[str, object]]) -> None:
        """Copy and register the named definitions from all endpoint documents."""
        self.schemas: dict[str, dict[str, object]] = {}
        self.classes: dict[str, str] = {}
        self.aliases: dict[str, str] = {}
        self.alias_dependencies: dict[str, set[str]] = {}
        for document in documents:
            if set(document) != {"schemas"}:
                raise SchemaError("Expected a document containing only 'schemas'")
            for name, schema in _mapping(document["schemas"], "schemas").items():
                self._register(name, _mapping(schema, name))

    def _register(self, name: str, schema: dict[str, object]) -> None:
        """Register one schema, rejecting incompatible named or inline duplicates."""
        _type_name(name)
        if name in self.schemas and self.schemas[name] != schema:
            raise SchemaError(f"Incompatible duplicate schema definition: {name}")
        self.schemas[name] = deepcopy(schema)

    def _validate(self, schema: dict[str, object], path: str) -> None:
        """Reject unknown constructs rather than silently weakening their types."""
        metadata = {"description", "title", "deprecated", "format"}
        kind = schema.get("type")
        allowed = metadata | {"type"}
        if "$ref" in schema:
            allowed = metadata | {"$ref"}
        elif kind == "object":
            allowed |= {"properties", "required"}
        elif kind == "array":
            allowed |= {"items"}
        elif kind == "string":
            allowed |= {"enum"}
        elif kind not in ("integer", "number", "boolean", "null"):
            raise SchemaError(f"{path}: unsupported schema type {kind!r}")
        unknown = set(schema) - allowed
        if unknown:
            raise SchemaError(f"{path}: unsupported schema keywords {sorted(unknown)}")

    def _annotation(self, schema: dict[str, object], name: str, owner: str) -> str:
        """Resolve references and recursively register inline object definitions."""
        self._validate(schema, name)
        if "$ref" in schema:
            reference = schema["$ref"]
            if not isinstance(reference, str) or not reference.startswith("#/schemas/"):
                raise SchemaError(f"{name}: unsupported reference {reference!r}")
            target = reference.removeprefix("#/schemas/")
            if target not in self.schemas:
                raise SchemaError(f"{name}: unresolved reference {reference}")
            self.alias_dependencies.setdefault(owner, set()).add(target)
            return target
        kind = schema.get("type")
        if kind == "object":
            self._register(name, schema)
            return name
        if kind == "array":
            item = _mapping(schema.get("items"), f"{name}.items")
            return f"list[{self._annotation(item, name + 'Item', owner)}]"
        if kind == "string" and "enum" in schema:
            values = schema["enum"]
            if not isinstance(values, list) or not values:
                raise SchemaError(f"{name}: enum must be a nonempty array of strings")
            members = cast(list[object], values)
            if not all(isinstance(item, str) for item in members):
                raise SchemaError(f"{name}: only string enums are supported")
            return "Literal[" + ", ".join(repr(item) for item in members) + "] | str"
        return {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "null": "NoneType",
        }[str(kind)]

    def _class(self, name: str, schema: dict[str, object]) -> str:
        """Render keyword-only fields while preserving schema requiredness."""
        properties = _mapping(schema.get("properties", {}), f"{name}.properties")
        raw_required = schema.get("required", [])
        if not isinstance(raw_required, list):
            raise SchemaError(f"{name}.required: expected an array")
        required = cast(list[object], raw_required)
        if any(not isinstance(item, str) or item not in properties for item in required):
            raise SchemaError(f"{name}.required: unknown or invalid property")
        lines = [
            "@dataclass(kw_only=True)",
            f"class {name}(XcresultObject):",
            f'    """Modern xcresulttool {name} data."""',
        ]
        for field, raw_schema in properties.items():
            _name(field)
            field_schema = _mapping(raw_schema, f"{name}.{field}")
            annotation = self._annotation(field_schema, name + field[0].upper() + field[1:], name)
            if field not in required:
                annotation = f"{annotation} | None = None"
            lines.append(f"    {field}: {annotation}")
        return "\n".join(lines)

    def render(self) -> str:
        """Render all classes, followed by dependency-ordered scalar/array aliases."""
        while pending := [name for name in self.schemas if name not in self.classes | self.aliases]:
            for name in pending:
                schema = self.schemas[name]
                self._validate(schema, name)
                if schema.get("type") == "object":
                    self.classes[name] = self._class(name, schema)
                else:
                    self.aliases[name] = self._annotation(schema, name, name)
        imports = "from dataclasses import dataclass\nfrom typing import Literal, TypeAlias"
        if any("NoneType" in value for value in (*self.classes.values(), *self.aliases.values())):
            imports += "\nfrom types import NoneType"
        sections = [
            '"""Generated by python -m generator from modern xcresulttool schemas.\n\n'
            "Do not edit manually. Enum strings are decoded forward-compatibly.\n"
            "Summary.devicesAndConfigurations and Activities.testRuns use verified wire arrays;\n"
            'see generator.correct_schema_errors for the Apple schema corrections and evidence.\n"""',
            "from __future__ import annotations",
            "# Apple JSON property names are intentionally preserved.\n# pylint: disable=invalid-name",
            imports,
            "from xcresult.model_base import XcresultObject",
            f'SCHEMA_VERSION = "{SCHEMA_VERSION}"',
            *self.classes.values(),
        ]
        emitted = set(self.classes)
        remaining = dict(self.aliases)
        while remaining:
            ready = [
                name for name in remaining if self.alias_dependencies.get(name, set()) <= emitted
            ]
            if not ready:
                raise SchemaError(f"Recursive aliases cannot be resolved: {sorted(remaining)}")
            for name in ready:
                sections.append(f"{name}: TypeAlias = {remaining.pop(name)}")
                emitted.add(name)
        sections.append("__all__ = " + repr(["SCHEMA_VERSION", *self.schemas]))
        return "\n\n\n".join(sections) + "\n"


def generate(output_path: str | Path = "xcresult/model.py") -> None:
    """Fetch endpoint schemas and persist a Black-formatted Python model module."""
    import black  # pylint: disable=import-outside-toplevel

    source = ModelGenerator(load_schemas()).render()
    formatted = black.format_str(source, mode=black.Mode(line_length=100))
    Path(output_path).write_text(formatted, encoding="utf-8")
