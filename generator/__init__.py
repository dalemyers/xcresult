"""A module for generating xcresult models."""

import os
import subprocess
from typing import List, Optional, Tuple


DATA_TYPES = {
    "Int": "int",
    "String": "str",
    "Double": "float",
    "Bool": "bool",
    "Date": "datetime.datetime",
    "SchemaSerializable": "Any",
}


def get_indentation(line: str) -> int:
    if len(line) == 0:
        return 0

    count = 0
    while True:
        if line[count] == " ":
            count += 1
        else:
            break

    assert count % 2 == 0

    return int(count / 2)


def dedent(lines) -> List[str]:
    return [line[2:] for line in lines]


class XcresultType:
    def __init__(self, original: str) -> None:
        self.original = original
        self.root_type = original
        self.is_list = False
        self.is_optional = False

        if self.root_type.startswith("["):
            self.is_list = True
            self.root_type = self.root_type[1:-1]

        if self.root_type.endswith("?"):
            self.root_type = self.root_type[:-1]
            self.is_optional = True

    def python_type(self, name: str, container_type: str) -> Tuple[str, List[str]]:
        output = ""
        annotations = []
        if self.is_list:
            output += "List["

        if self.is_optional:
            output += "Optional["

        p_type = DATA_TYPES.get(self.root_type, self.root_type)

        if p_type == container_type:
            p_type = f'"{p_type}"'

        output += p_type

        if self.is_optional:
            output += "]"

        if self.is_list:
            output += "]"

        return output, annotations


class Definition:
    def __init__(
        self,
        name: str,
        kind: Optional[str],
        supertype: Optional[str],
        properties: List[Tuple[str, str]],
        original: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.kind = kind
        self.supertype = supertype if supertype else "XcresultObject"
        self.properties = properties
        self.original = original

    def dependency_types(self) -> List[str]:
        raw_types = list(map(lambda x: x[1], self.properties))
        if self.supertype:
            raw_types.append(self.supertype)

        return list(
            set(
                map(
                    lambda x: XcresultType(x).root_type,
                    filter(
                        lambda x: x not in DATA_TYPES,
                        raw_types,
                    ),
                )
            )
        )

    def python(self) -> str:
        output = []

        if self.kind != "object":
            output.append(f"# Defined Type: {self.name}")
            return output

        class_line = f"class {self.name}"
        if self.supertype is not None and self.name != "XcresultObject":
            class_line += f"({self.supertype})"
        class_line += ":"
        output.append(class_line)

        if self.original:
            output.append('    """Generated from xcresulttool format description.')
            output.append("")
            for line in self.original:
                output.append(f"    {line}")
            output.append('    """')
            output.append("")
        else:
            output.append('    """Generated from xcresulttool format description."""')

        for name, ptype in self.properties:
            xctype = XcresultType(ptype)
            python_type, annotations = xctype.python_type(name, self.name)
            output = annotations + output
            output.append(f"    {name}: {python_type}")

        additional_methods_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "additional_methods", f"{self.name}.py"
        )
        if os.path.exists(additional_methods_path):
            output.append("")
            with open(additional_methods_path) as additional_methods_file:
                for line in additional_methods_file.readlines():
                    stripped = line.rstrip()
                    if len(stripped) > 0:
                        output.append("    " + line.rstrip())
                    else:
                        output.append("")

        return output

    @staticmethod
    def from_format_description(lines) -> "Definition":
        lines = dedent(lines)
        original = lines[:]
        name_line = lines.pop(0)
        assert name_line.startswith("- ")
        name = name_line[2:].strip()
        kind = None
        supertype = None
        properties = []
        for line in lines:
            line = line.strip()
            components = line[2:].split(":")
            key = components[0].strip()
            value = ":".join(components[1:])

            if line.startswith("* "):
                if key == "Kind":
                    kind = value.strip()
                    continue

                if key == "Supertype":
                    supertype = value.strip()
                    continue

                if key == "Properties":
                    continue

                raise Exception("Unexpected line")

            if line.startswith("+ "):
                properties.append((key.strip(), value.strip()))
                continue

            raise Exception("Unexpected line")

        return Definition(name, kind, supertype, properties, original)


def get_definitions(format_description) -> List[Definition]:
    root_properties = {}
    definitions = [Definition("XcresultObject", "object", None, [])]
    buffer = []

    lines = [line for line in format_description.split("\n") if len(line.strip()) > 0]

    while True:
        if len(lines) == 0:
            definitions.append(Definition.from_format_description(buffer))
            break

        line = lines.pop(0)
        indentation = get_indentation(line)
        if indentation == 0:
            components = line.split(": ")
            if components[0] == "Types:":
                continue
            root_properties[components[0]] = ": ".join(components[1:])
            continue

        if indentation == 1 and len(buffer) != 0:
            definitions.append(Definition.from_format_description(buffer))
            buffer = [line]
            continue

        buffer.append(line)

    return definitions


def order_definitions(definitions: List[Definition]) -> List[Definition]:
    output = []
    definition_dict = {definition.name: definition for definition in definitions}
    dependency_types = {
        definition.name: set(definition.dependency_types()) for definition in definitions
    }

    while len(dependency_types) > 0:
        keys_to_delete = []

        for key in dependency_types.keys():
            values = dependency_types[key]

            if len(values) > 1:
                continue

            if len(values) == 1 and list(values)[0] != key:
                continue

            output.append(definition_dict[key])
            keys_to_delete.append(key)

        for key in keys_to_delete:
            del dependency_types[key]

            for subkey in dependency_types.keys():
                if key in dependency_types[subkey]:
                    dependency_types[subkey].remove(key)

            continue

    return output


def generate(output_path: str):
    output = subprocess.run(
        ["xcrun", "xcresulttool", "formatDescription"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    ).stdout

    definitions = get_definitions(output)
    definitions = order_definitions(definitions)

    with open(output_path, "w") as output_file:
        output_file.write('"""Autogenerated models for xcresulttool."""\n\n')
        output_file.write("import datetime\n")
        output_file.write("import sys\n")
        output_file.write("from typing import Any, Dict, List, Optional\n")
        output_file.write("import urllib.parse\n")
        output_file.write("\n\n")
        output_file.write("# pylint: disable=too-many-lines\n")
        output_file.write("# pylint: disable=invalid-name\n")
        output_file.write("\n\n")

        for definition in definitions:
            for line in definition.python():
                output_file.write(line + "\n")
            output_file.write("\n\n")
        output_file.write("\n")

        output_file.write("_CURRENT_MODULE = sys.modules[__name__]\n")
        output_file.write("_MODEL_NAMES = dir(_CURRENT_MODULE)\n")
        output_file.write('_MODEL_NAMES = [m for m in _MODEL_NAMES if not m.startswith("__")]\n')
        output_file.write(
            "_RESOLVED_MODELS = [getattr(_CURRENT_MODULE, m) for m in _MODEL_NAMES]\n"
        )
        output_file.write("# pylint: disable=unidiomatic-typecheck\n")
        output_file.write(
            "_RESOLVED_MODELS = [m for m in _RESOLVED_MODELS if type(m) == type(type) and issubclass(m, XcresultObject)]\n"
        )
        output_file.write("# pylint: enable=unidiomatic-typecheck\n")
        output_file.write("MODELS = {m.__name__: m for m in _RESOLVED_MODELS}\n")


if __name__ == "__main__":
    generate("/Users/dalemy/Projects/xcresult/xcresult/model.py")