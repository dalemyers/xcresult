"""A module for dealing with xcresults."""

import datetime
import json
import logging
import os
import subprocess
from typing import Any, cast, Dict, get_type_hints, List, Optional, Tuple

from xcresult import model
from xcresult.model import (
    ActionsInvocationRecord,
    ActionRecord,
    ActionTestableSummary,
    ActionTestAttachment,
    ActionTestMetadata,
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
        raise Exception("Unknown type: " + type_name)

    xc_class = model.MODELS.get(type_name)

    if xc_class is None:
        raise UnsupportedType()

    instance = xc_class.__new__(xc_class)

    for key, value in data.items():
        try:
            setattr(instance, key, deserialize(value))
        except UnsupportedType:
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

            if str(property_type).startswith("typing.List["):
                setattr(instance, property_name, None)
                continue

            if not str(property_type).startswith("typing.Optional["):
                raise Exception()

            setattr(instance, property_name, None)

    return instance


# pylint: enable=too-many-return-statements
# pylint: enable=too-many-branches


def _get(path: str, identifier: Optional[str] = None) -> Dict[str, Any]:
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
    object_data = _get(path)
    return cast(ActionsInvocationRecord, deserialize(object_data))


def get_test_plan_run_summaries(path: str, identifier: str) -> ActionTestPlanRunSummaries:
    """Get an ActionTestPlanRunSummaries.

    :param path: The path to the xcresult bundle
    :param identifier: The identifier to get

    :returns: The deserialized data
    """
    object_data = _get(path, identifier)
    return cast(ActionTestPlanRunSummaries, deserialize(object_data))


def get_action_test_summary(path: str, identifier: str) -> ActionTestSummary:
    """Get an ActionTestSummary.

    :param path: The path to the xcresult bundle
    :param identifier: The identifier to get

    :returns: The deserialized data
    """
    object_data = _get(path, identifier)
    return cast(ActionTestSummary, deserialize(object_data))


def _get_attachments_for_action_testable_summary(
    path: str,
    testable_summary: ActionTestableSummary,
) -> List[Tuple[ActionTestMetadata, ActionTestAttachment]]:
    """Get all attachments in an action.

    :param path: The path to the xcresult bundle
    :param testable_summary: The action testable summary to get the attachments for

    :returns: A list of test attachments (with the test metadata)
    """

    attachments: List[Tuple[ActionTestMetadata, ActionTestAttachment]] = []

    tests = []
    test_stack = testable_summary.tests
    while len(test_stack) > 0:
        test = test_stack.pop(0)
        if isinstance(test, ActionTestSummaryGroup):
            group = cast(ActionTestSummaryGroup, test)
            for subtest in group.subtests or []:
                test_stack.append(subtest)
        else:
            tests.append(test)

    tests = [test for test in tests if isinstance(test, ActionTestMetadata)]
    test_metadata = cast(List[ActionTestMetadata], tests)
    test_summary_references = [
        (test, test.summaryRef) for test in test_metadata if test.summaryRef is not None
    ]

    for test, summary in test_summary_references:
        full_summary = get_action_test_summary(path, summary.id)
        if full_summary.activitySummaries is not None:
            for activity_summary in full_summary.activitySummaries:
                if activity_summary.attachments is not None:
                    for attachment in activity_summary.attachments:
                        attachments.append((test, attachment))

    return attachments


def _get_attachments_for_action(
    path: str,
    action: ActionRecord,
) -> Optional[List[Tuple[ActionTestMetadata, ActionTestAttachment]]]:
    """Get all attachments in an action.

    :param path: The path to the xcresult bundle
    :param action: The action to get the attachments for

    :returns: A list of test attachments (with the test metadata)
    """

    attachments: List[Tuple[ActionTestMetadata, ActionTestAttachment]] = []

    test_ref = action.actionResult.testsRef

    if test_ref is None:
        return None

    test_plan_run_summaries = get_test_plan_run_summaries(path, test_ref.id)

    for test_plan_run_summary in test_plan_run_summaries.summaries:
        for testable_summary in test_plan_run_summary.testableSummaries:
            attachments.extend(_get_attachments_for_action_testable_summary(path, testable_summary))

    return attachments


def export_attachments(path: str, output_folder: str) -> None:
    """Get all attachments in an xcresult bundle.

    The attachments will be placed into the `output_folder` with a sub-folder
    for each test class, and a sub-folder for each test within that class.

    The name will be the attachment name generated if available.

    :param path: The path of the xcresult bundle
    :param output_folder: The output folder to write the attachments to
    """

    invocation_record = get_actions_invocation_record(path)
    actions = [
        action for action in invocation_record.actions if action.actionResult.testsRef is not None
    ]

    attachments = []

    for action in actions:
        action_attachments = _get_attachments_for_action(path, action)
        if action_attachments is None:
            continue
        attachments.extend(action_attachments)

    for index, (test, attachment) in enumerate(attachments):

        if attachment.payloadRef is None:
            continue

        identifier = attachment.payloadRef.id

        if test.identifier is None:
            test_identifier = f"Unknown_Identifier_{index}"
        else:
            test_identifier = test.identifier

        folder_name = os.path.join(output_folder, test_identifier)

        if attachment.filename is None:
            filename = test_identifier
        else:
            filename = attachment.filename

        if folder_name.endswith("()"):
            folder_name = folder_name[:-2]

        os.makedirs(folder_name, exist_ok=True)
        _export(path, identifier, "file", os.path.join(folder_name, filename))
