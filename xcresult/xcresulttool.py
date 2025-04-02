"""A module for dealing with xcresults."""

import datetime
import json
import logging
import os
import subprocess
from typing import Any, cast, get_type_hints
import uuid

from xcresult import model
from xcresult.exceptions import UnsupportedTypeException
from xcresult.model import (
    ActionsInvocationRecord,
    ActionTestPlanRunSummaries,
    ActionTestSummary,
    ActionTestSummaryGroup,
)


# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
def deserialize(data: dict[str, Any]) -> Any:
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
        raise UnsupportedTypeException()

    instance = xc_class.__new__(xc_class)

    for key, value in data.items():
        try:
            setattr(instance, key, deserialize(value))
        except UnsupportedTypeException:
            logging.warning(f"Found unsupported property on {type_name} when deserializing: {key}")
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

            if str(property_type).startswith("list["):
                setattr(instance, property_name, None)
                continue

            if not (
                str(property_type).startswith("typing.Optional[")
                or str(property_type).endswith(" | None")
            ):
                raise ValueError()

            setattr(instance, property_name, None)

    return instance


# pylint: enable=too-many-return-statements
# pylint: enable=too-many-branches


def get(path: str, identifier: str | None = None) -> dict[str, Any]:
    """Get the some xcresult info.

    :param path: The path to the xcresult bundle

    :returns: The deserialized data
    """

    command = [
        "xcrun",
        "xcresulttool",
        "get",
        "--path",
        path,
        "--format",
        "json",
        "--legacy",
    ]

    if identifier:
        command += ["--id", identifier]

    logging.debug("Running: %s", " ".join(command))

    output = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    ).stdout

    return cast(dict[str, Any], json.loads(output))


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
        "--legacy",
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


def get_test_plan_run_summaries(path: str, identifier: str) -> ActionTestPlanRunSummaries:
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


def export_attachment(path: str, identifier: str, type_identifier: str, output_path) -> None:
    """Get an attachment from an xcresult bundle.

    The name will be the attachment name generated if available.

    :param path: The path of the xcresult bundle
    :param identifier: The identifier of the attachment to export
    :param type_identifier: The type of the attachment to export (.e.g. 'public.png')
    :param output_folder: The output folder to write the attachments to
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _export(path, identifier, type_identifier, output_path)


# pylint: disable=too-many-branches
def export_action_test_summary_group(
    results_path: str,
    test: model.ActionTestSummaryIdentifiableObject,
    output_path: str,
    log_depth: int = 0,
) -> None:
    """Handle an ActionTestSummaryGroup."""

    log_prefix = "\t" * log_depth

    if isinstance(test, model.ActionTestMetadata) and test.testStatus == "Skipped":
        # If it was skipped, there is no data to export
        logging.debug(f"{log_prefix}Skipping processing test that was skipped: {test.identifier}")
        return

    if test.identifierURL is None:
        # This happens if there was an error during the test
        logging.debug(
            f"{log_prefix}Skipping processing test that had no identifier URL (usually due to an error during the test)"
        )
        return

    if isinstance(test, ActionTestSummaryGroup):
        for subtest in test.subtests or []:
            logging.info(f"{log_prefix}\tExporting subtest: {subtest.identifier}")
            export_action_test_summary_group(results_path, subtest, output_path, log_depth + 2)
        return

    if not isinstance(test, model.ActionTestMetadata):
        return

    if test.summaryRef is None:
        return

    identifier = test.summaryRef.id
    data = cast(ActionTestSummary, deserialize(get(results_path, identifier)))

    relative_path = test.identifierURL.replace("test://com.apple.xcode/", "")

    if data.activitySummaries:
        for activity_summary in data.activitySummaries:
            logging.info(f"{log_prefix}\tExporting activity summary: {activity_summary.title}")
            if activity_summary.attachments is None:
                continue
            for attachment in activity_summary.attachments:
                logging.info(f"{log_prefix}\t\tExporting attachment: {attachment.name}")
                if attachment.payloadRef is None:
                    continue
                identifier = attachment.payloadRef.id

                if attachment.filename is None:
                    file_name = str(uuid.uuid4())
                else:
                    file_name = attachment.filename

                output_file_path = os.path.join(output_path, relative_path, file_name)

                while os.path.exists(output_file_path):
                    suffix = str(uuid.uuid4()).split("-", maxsplit=1)[0]
                    file_name, file_ext = os.path.splitext(file_name)
                    new_file_name = f"{file_name}-{suffix}{file_ext}"
                    output_file_path = os.path.join(output_path, relative_path, new_file_name)

                export_attachment(
                    results_path,
                    identifier,
                    "file",
                    output_file_path,
                )

    if data.failureSummaries:
        for summary in data.failureSummaries:
            if summary.attachments is None:
                continue

            for attachment in summary.attachments:
                if attachment.payloadRef is None:
                    continue
                identifier = attachment.payloadRef.id

                if attachment.filename is None:
                    file_name = str(uuid.uuid4())
                else:
                    file_name = attachment.filename

                output_file_path = os.path.join(output_path, relative_path, file_name)

                while os.path.exists(output_file_path):
                    suffix = str(uuid.uuid4()).split("-", maxsplit=1)[0]
                    file_name, file_ext = os.path.splitext(file_name)
                    new_file_name = f"{file_name}-{suffix}{file_ext}"
                    output_file_path = os.path.join(output_path, relative_path, new_file_name)

                export_attachment(
                    results_path,
                    identifier,
                    "file",
                    output_file_path,
                )


# pylint: enable=too-many-branches
