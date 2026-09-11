"""Typed access to the modern xcresulttool report and export commands."""

import json
import logging
import os
import subprocess
from typing import TypeVar

from xcresult.exceptions import XcresultException
from xcresult.model import (
    SCHEMA_VERSION,
    Activities,
    BuildResults,
    ContentAvailability,
    Summary,
    TestAttachmentDetails,
    TestDetails,
    Tests,
)
from xcresult.model_base import XcresultObject, deserialize

Report = TypeVar("Report", bound=XcresultObject)


def _run(arguments: list[str]) -> str:
    """Run xcresulttool, preserving diagnostic output on failure.

    :param arguments: Arguments following ``xcresulttool``.
    :returns: The command's standard output.
    """
    command = ["xcrun", "xcresulttool", *arguments]
    logging.debug("Running: %s", " ".join(command))
    try:
        return subprocess.run(command, check=True, capture_output=True, encoding="utf-8").stdout
    except subprocess.CalledProcessError as error:
        raise XcresultException(
            f"xcresulttool {' '.join(arguments[:3])} failed: {(error.stderr or str(error)).strip()}"
        ) from error
    except OSError as error:
        raise XcresultException(f"Could not run xcresulttool: {error}") from error


def _get(path: str, command: list[str], report_type: type[Report]) -> Report:
    """Read and decode a report.

    :param path: Result bundle path.
    :param command: Modern get subcommand and any selectors.
    :param report_type: Generated model for the response.
    :returns: The typed report.
    """
    data = json.loads(
        _run(["get", *command, "--path", path, "--compact", "--schema-version", SCHEMA_VERSION])
    )
    return report_type.from_dict(data)


def get_test_summary(path: str) -> Summary:
    """Read the test summary.

    :param path: Result bundle path.
    :returns: The summary report.
    """
    return _get(path, ["test-results", "summary"], Summary)


def get_tests(path: str) -> Tests:
    """Read the test tree.

    :param path: Result bundle path.
    :returns: The test tree report.
    """
    return _get(path, ["test-results", "tests"], Tests)


def get_test_details(path: str, test_id: str) -> TestDetails:
    """Read a test's individual runs.

    :param path: Result bundle path.
    :param test_id: Test identifier URL or identifier string.
    :returns: The test details report.
    """
    return _get(path, ["test-results", "test-details", "--test-id", test_id], TestDetails)


def get_test_activities(path: str, test_id: str) -> Activities:
    """Read a test's activity trees.

    :param path: Result bundle path.
    :param test_id: Test identifier URL or identifier string.
    :returns: The activities report.
    """
    return _get(path, ["test-results", "activities", "--test-id", test_id], Activities)


def get_build_results(path: str) -> BuildResults:
    """Read build issues and metadata.

    :param path: Result bundle path.
    :returns: The build report.
    """
    return _get(path, ["build-results"], BuildResults)


def get_content_availability(path: str) -> ContentAvailability:
    """Read the available content types.

    :param path: Result bundle path.
    :returns: The availability report.
    """
    return _get(path, ["content-availability"], ContentAvailability)


def export_test_attachments(
    path: str, output_path: str, test_id: str | None = None
) -> list[TestAttachmentDetails]:
    """Export attachments and read xcresulttool's manifest.

    :param path: Result bundle path.
    :param output_path: Directory for exported files and ``manifest.json``.
    :param test_id: Optional test or suite identifier.
    :returns: Manifest entries identifying the exported files.
    """
    os.makedirs(output_path, exist_ok=True)
    arguments = [
        "export",
        "attachments",
        "--path",
        path,
        "--output-path",
        output_path,
        "--schema-version",
        SCHEMA_VERSION,
    ]
    if test_id is not None:
        arguments.extend(["--test-id", test_id])
    _run(arguments)
    with open(os.path.join(output_path, "manifest.json"), encoding="utf-8") as manifest:
        data: object = json.load(manifest)
    return deserialize(data, list[TestAttachmentDetails])
