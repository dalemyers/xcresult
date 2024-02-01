"""A module for dealing with xcresults."""

import datetime
import json
import logging
import os
import subprocess
from typing import Any, cast, Dict, get_type_hints, Optional

from xcresult import model
from xcresult.model import (
    ActionsInvocationRecord,
    ActionTestPlanRunSummaries,
    ActionTestSummary,
    ActionTestSummaryGroup,
)


class UnsupportedType(Exception):
    """A new and, as yet, unsupported type."""


# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
def deserialize(data: Dict[str, Any]) -> Any:
    """Deserialize the xcresulttool data into Python objects.

    :param data: The data to deserialize

    :returns: The deserialized object(s)
    """

    type_info = data["_type"]
    type_name = type_info["_name"]

    del data["_type"]

    if type_name == "Array":
        output = []
        for value in data["_values"]:
            output.append(deserialize(value))
        return output

    if "_value" in data:
        # Primitive type
        if type_name == "String":
            return data["_value"]
        if type_name == "Int":
            return int(data["_value"])
        if type_name == "Double":
            return float(data["_value"])
        if type_name == "Bool":
            return data["_value"].lower() == "true"
        if type_name == "Date":
            return datetime.datetime.strptime(data["_value"], "%Y-%m-%dT%H:%M:%S.%f%z")
        raise ValueError("Unknown type: " + type_name)

    xc_class = model.MODELS.get(type_name)

    if xc_class is None:
        raise UnsupportedType()

    instance = xc_class.__new__(xc_class)

    for key, value in data.items():
        try:
            setattr(instance, key, deserialize(value))
        except UnsupportedType:
            logging.warning(
                f"Found unsupported property on {type_name} when deserializing: {key}"
            )
            continue

    for property_name, property_type in get_type_hints(xc_class).items():
        if not hasattr(instance, property_name):
            if property_type == int:
                setattr(instance, property_name, 0)
                continue

            if property_type == bool:
                setattr(instance, property_name, False)
                continue

            if property_type == str:
                setattr(instance, property_name, "")
                continue

            if property_type == float:
                setattr(instance, property_name, 0.0)
                continue

            if str(property_type).startswith("typing.List["):
                setattr(instance, property_name, None)
                continue

            if not str(property_type).startswith("typing.Optional["):
                raise ValueError()

            setattr(instance, property_name, None)

    return instance


# pylint: enable=too-many-return-statements
# pylint: enable=too-many-branches


def get(path: str, identifier: Optional[str] = None) -> Dict[str, Any]:
    """Get the some xcresult info.

    :param path: The path to the xcresult bundle

    :returns: The deserialized data
    """

    command = ["xcrun", "xcresulttool", "get", "--path", path, "--format", "json"]

    if identifier:
        command += ["--id", identifier]

    output = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    ).stdout

    return cast(Dict[str, Any], json.loads(output))


def _export(path: str, identifier: str, object_type: str, output_path: str):
    """Export a file/directory from the xcresult bundle.

    :param path: The path to the xcresult bundle
    :param identifier: The identifier of the object to export
    :param object_type: The type of the object to export ("file" or "directory")
    :param output_path: The root path to write out to (attachments will be placed in a class/testname folder structure)
    """

    command = [
        "xcrun",
        "xcresulttool",
        "export",
        "--path",
        path,
        "--id",
        identifier,
        "--type",
        object_type,
        "--output-path",
        output_path,
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )


def get_actions_invocation_record(path) -> ActionsInvocationRecord:
    """Get the base xcresult info.

    :param path: The path to the xcresult bundle

    :returns: The deserialized data
    """
    object_data = get(path)
    return cast(ActionsInvocationRecord, deserialize(object_data))


def get_test_plan_run_summaries(
    path: str, identifier: str
) -> ActionTestPlanRunSummaries:
    """Get an ActionTestPlanRunSummaries.

    :param path: The path to the xcresult bundle
    :param identifier: The identifier to get

    :returns: The deserialized data
    """
    object_data = get(path, identifier)
    return cast(ActionTestPlanRunSummaries, deserialize(object_data))


def get_action_test_summary(path: str, identifier: str) -> ActionTestSummary:
    """Get an ActionTestSummary.

    :param path: The path to the xcresult bundle
    :param identifier: The identifier to get

    :returns: The deserialized data
    """
    object_data = get(path, identifier)
    return cast(ActionTestSummary, deserialize(object_data))


def export_attachment(
    path: str, identifier: str, type_identifier: str, output_path
) -> None:
    """Get an attachment from an xcresult bundle.

    The name will be the attachment name generated if available.

    :param path: The path of the xcresult bundle
    :param identifier: The identifier of the attachment to export
    :param type_identifier: The type of the attachment to export (.e.g. 'public.png')
    :param output_folder: The output folder to write the attachments to
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _export(path, identifier, type_identifier, output_path)


def export_action_test_summary_group(
    results_path: str,
    test: model.ActionTestSummaryIdentifiableObject,
    output_path: str,
) -> None:
    """Handle an ActionTestSummaryGroup."""
    if isinstance(test, ActionTestSummaryGroup):
        for subtest in test.subtests or []:
            export_action_test_summary_group(results_path, subtest, output_path)
        return

    identifier = test.summaryRef.id
    data = deserialize(get(results_path, identifier))

    relative_path = test.identifierURL.replace("test://com.apple.xcode/", "")

    for activity_summary in data.activitySummaries:
        if activity_summary.attachments is None:
            continue
        for attachment in activity_summary.attachments:
            if attachment.payloadRef is None:
                continue
            identifier = attachment.payloadRef.id
            export_attachment(
                results_path,
                identifier,
                "file",
                os.path.join(
                    output_path, "summary", relative_path, attachment.filename
                ),
            )

    for summary in data.failureSummaries:
        for attachment in summary.attachments:
            if attachment.payloadRef is None:
                continue
            identifier = attachment.payloadRef.id
            export_attachment(
                results_path,
                identifier,
                "file",
                os.path.join(
                    output_path, "failure", relative_path, attachment.filename
                ),
            )
