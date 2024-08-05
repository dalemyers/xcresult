"""A module for generating xcresult models."""

import os
import subprocess


DATA_TYPES = {
    "Bool": "bool",
    "Data": "bytes",
    "Date": "datetime.datetime",
    "Double": "float",
    "Int": "int",
    "Int16": "int",
    "Int32": "int",
    "Int64": "int",
    "Int8": "int",
    "SchemaSerializable": "Any",
    "String": "str",
    "UInt16": "int",
    "UInt32": "int",
    "UInt64": "int",
    "UInt8": "int",
    "URL": "str",
}


def get_indentation(line: str) -> int:
    """Get the indentation level of a line.

    Every 2 spaces counts as 1 level.

    :param line: The line to check

    :returns: The indentation level
    """

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


def dedent(lines: list[str]) -> list[str]:
    """Dedent a list of lines by one level.

    :param lines: The lines to dedent

    :returns: The dedented lines
    """
    return [line[2:] for line in lines]


class XcresultType:
    """A class for converting xcresult types to Python types."""

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

    def python_type(self, container_type: str) -> str:
        """Convert the xcresult type to a Python type.

        :param container_type: The name of the container type

        :returns: The Python code for the type
        """

        p_type = DATA_TYPES.get(self.root_type, self.root_type)

        is_self_referential = p_type == container_type

        if is_self_referential:
            p_type = f'"{p_type}"'

        if self.is_optional:
            if is_self_referential:
                p_type = f"Optional[{p_type}]"
            else:
                p_type = f"{p_type} | None"

        if self.is_list:
            p_type = f"list[{p_type}]"

        return p_type


class Definition:
    """A class for representing a definition in the xcresulttool format description."""

    def __init__(
        self,
        name: str,
        kind: str | None,
        supertype: str | None,
        properties: list[tuple[str, str]],
        original: list[str] | None = None,
    ) -> None:
        self.name = name
        self.kind = kind
        self.supertype = supertype if supertype else "XcresultObject"
        self.properties = properties
        self.original = original

    def dependency_types(self) -> list[str]:
        """Return a list of the types that this definition uses.

        :returns: The list of types
        """
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

    def _generate_definition_header(self) -> tuple[list[str], bool]:
        """Convert this definition to Python code."""
        output = []

        if self.kind != "object":
            output.append(
                f'# Defined Type: {self.name} -> {XcresultType(self.name).python_type("")}'
            )
            return output, False

        class_line = f"class {self.name}"
        if self.supertype is not None and self.name != "XcresultObject":
            class_line += f"({self.supertype})"
        class_line += ":"
        output.append(class_line)

        return output, True

    def _generate_doc_comment(self) -> list[str]:
        """Generate the doc comment for this definition."""
        output = []

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
            python_type = xctype.python_type(self.name)
            output.append(f"    {name}: {python_type}")

        return output

    def _add_additional_methods(self) -> list[str]:
        output = []

        additional_methods_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "additional_methods",
            f"{self.name}.py",
        )
        if not os.path.exists(additional_methods_path):
            return output

        output.append("")
        with open(additional_methods_path, encoding="utf-8") as additional_methods_file:
            for line in additional_methods_file.readlines():
                stripped = line.rstrip()
                if len(stripped) > 0:
                    output.append("    " + line.rstrip())
                else:
                    output.append("")

        return output

    def _add_dunder_methods(self) -> list[str]:
        output = [""]

        output.append("    def _members(self) -> tuple:")
        output.append("        properties = [")
        for name, _ in self.properties:
            output.append(f"            self.{name},")
        output.append("        ]")

        if self.name == "XcresultObject":
            output.append("        return tuple(properties)")
        else:
            output.append("        return tuple(properties + list(super()._members()))")

        output.append("")

        output.append("    def __eq__(self, other: Any) -> bool:")
        output.append("        if not isinstance(other, self.__class__):")
        output.append("            return False")
        output.append("")
        output.append("        # pylint: disable=protected-access")
        output.append("        return self._members() == other._members()")
        output.append("        # pylint: enable=protected-access")
        output.append("")

        output.append("    def __hash__(self) -> int:")
        output.append("        return xchash(self)")
        output.append("")

        return output

    def python(self) -> list[str]:
        """Convert this definition to Python code.

        :returns: The Python code
        """
        output = []

        next_output, should_continue = self._generate_definition_header()
        output.extend(next_output)

        if not should_continue:
            return output

        output.extend(self._generate_doc_comment())
        output.extend(self._add_additional_methods())
        output.extend(self._add_dunder_methods())

        return output

    @staticmethod
    def from_format_description(lines: list[str]) -> "Definition":
        """Convert the output of xcrun xcresulttool formatDescription to a Definition.

        :param lines: The lines to convert

        :returns: The Definition
        """
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


def get_definitions(format_description: str) -> list[Definition]:
    """Get the definitions from the output of xcrun xcresulttool formatDescription.

    :param format_description: The output of xcrun xcresulttool formatDescription

    :returns: The list of Definitions
    """
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


def order_definitions(definitions: list[Definition]) -> list[Definition]:
    """Order definitions such that any dependencies are defined before they are used.

    :param definitions: The definitions to order

    :returns: The ordered definitions
    """
    all_output = []
    definition_dict = {definition.name: definition for definition in definitions}
    dependency_types = {
        definition.name: set(definition.dependency_types())
        for definition in definitions
    }

    while len(dependency_types) > 0:
        keys_to_delete = []
        output = []

        for key, values in dependency_types.items():
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

        output.sort(key=lambda d: (0 if d.kind == "value" else 1, d.kind, d.name))
        all_output.extend(output)

    return all_output


def generate(output_path: str):
    """Generate the models for xcresulttool.

    :param output_path: The path to write the models to
    """
    output = subprocess.run(
        ["xcrun", "xcresulttool", "formatDescription", "--legacy"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    ).stdout

    definitions = get_definitions(output)
    definitions = order_definitions(definitions)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write('"""Autogenerated models for xcresulttool."""\n\n')
        output_file.write("import datetime\n")
        output_file.write("import sys\n")
        output_file.write("from typing import Any, Optional\n")
        output_file.write("import urllib.parse\n")
        output_file.write("\n\n")
        output_file.write("# pylint: disable=too-many-lines\n")
        output_file.write("# pylint: disable=invalid-name\n")
        output_file.write("\n\n")

        output_file.write("def xchash(item: Any) -> int:\n")
        output_file.write("    all_hashes = []\n")
        output_file.write("\n")
        output_file.write("    if isinstance(item, list):\n")
        output_file.write("        for sub_item in item:\n")
        output_file.write("            all_hashes.append(xchash(sub_item))\n")
        output_file.write("        return hash(tuple(all_hashes))\n")
        output_file.write("\n")
        output_file.write("    if isinstance(item, dict):\n")
        output_file.write("        for key, value in item.items():\n")
        output_file.write("            all_hashes.append(xchash(key))\n")
        output_file.write("            all_hashes.append(xchash(value))\n")
        output_file.write("        return hash(tuple(all_hashes))\n")
        output_file.write("\n")
        output_file.write('    if not hasattr(item, "_members"):\n')
        output_file.write("        return hash(item)\n")
        output_file.write("\n")
        output_file.write('    members_call = getattr(item, "_members", None)\n')
        output_file.write("    if members_call is None:\n")
        output_file.write("        return hash(item)\n")
        output_file.write("\n")
        output_file.write("    for member in members_call():\n")
        output_file.write("        all_hashes.append(xchash(member))\n")
        output_file.write("\n")
        output_file.write("    return hash(tuple(all_hashes))\n")
        output_file.write("\n")

        for definition in definitions:
            for line in definition.python():
                output_file.write(line + "\n")
            output_file.write("\n\n")
        output_file.write("\n")

        output_file.write("_CURRENT_MODULE = sys.modules[__name__]\n")
        output_file.write("_MODEL_NAMES = dir(_CURRENT_MODULE)\n")
        output_file.write(
            '_MODEL_NAMES = [m for m in _MODEL_NAMES if not m.startswith("__")]\n'
        )
        output_file.write(
            "_RESOLVED_MODELS = [getattr(_CURRENT_MODULE, m) for m in _MODEL_NAMES]\n"
        )
        output_file.write("# pylint: disable=unidiomatic-typecheck\n")
        output_file.write("_RESOLVED_MODELS = [\n")
        output_file.write("    m\n")
        output_file.write("    for m in _RESOLVED_MODELS\n")
        output_file.write(
            "    if type(m) == type(type) and issubclass(m, XcresultObject)\n"
        )
        output_file.write("]\n")
        output_file.write("# pylint: enable=unidiomatic-typecheck\n")
        output_file.write("MODELS = {m.__name__: m for m in _RESOLVED_MODELS}\n")


if __name__ == "__main__":
    generate(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "xcresult", "model.py")
        )
    )
