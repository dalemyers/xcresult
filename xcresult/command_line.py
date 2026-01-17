#!/usr/bin/env python3

"""Command line handler for xcresult."""

import argparse
import enum
import os
import sys
from typing import Sequence

try:
    import xcresult
except ImportError:  # pragma: no cover
    # Insert the package into the PATH
    # This fallback is for standalone script execution and is tested via integration tests
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))
    import xcresult


class IssueType(enum.Enum):
    """Enum for issue types."""

    ERROR = "error"
    WARNING = "warning"
    ANALYZER_WARNING = "analyzer-warning"
    TEST_FAILURE = "test-failure"
    TEST_WARNING = "test-warning"


def _handle_export(args: argparse.Namespace) -> int:
    """Handle the export sub command."""

    if not os.path.exists(args.output_path):
        print("Output folder does not exist")
        return 1

    try:
        bundle = xcresult.Xcresults(args.bundle_path)
        bundle.export_test_attachments(args.output_path)
        # pylint: disable=broad-exception-caught
    except Exception as ex:
        # pylint: enable=broad-exception-caught
        print(f"Could not export attachments: {ex}", file=sys.stderr)
        return 1

    return 0


def _handle_junit(args: argparse.Namespace) -> int:
    """Handle the junit sub command."""

    if os.path.exists(args.output_path):
        print("Output file already exists")
        return 1

    try:
        bundle = xcresult.Xcresults(args.bundle_path)
        bundle.write_junit(args.output_path, args.export_attachments_path)
        # pylint: disable=broad-exception-caught
    except Exception as ex:
        # pylint: enable=broad-exception-caught
        print(f"Could not export junit: {ex}", file=sys.stderr)
        return 1

    return 0


def _check_summary_type(
    summaries: Sequence[xcresult.IssueSummary] | None,
    summary_name: str,
) -> bool:
    print(f"=== {summary_name} ===")
    if summaries is None:
        print(f"No {summary_name} found.")
        print()
        return False

    if len(summaries) == 0:
        print(f"No {summary_name} issues found.")
        print()
        return False

    for summary in summaries:
        if location := summary.documentLocationInCreatingWorkspace:
            print(
                f"{location.path}:{location.starting_line_number}:{location.starting_column_number} -> {summary.message}"
            )
        else:
            print(summary.message)

    print()

    return True


def _handle_check_issues(args: argparse.Namespace) -> int:
    """Handle the check-issues sub command."""

    bundle = xcresult.Xcresults(args.bundle_path)

    found_issues = False

    if args.issue_types is None or IssueType.ERROR in args.issue_types:
        found_issues = found_issues or _check_summary_type(
            bundle.actions_invocation_record.issues.errorSummaries,
            "Errors",
        )

    if args.issue_types is None or IssueType.WARNING in args.issue_types:
        found_issues = found_issues or _check_summary_type(
            bundle.actions_invocation_record.issues.warningSummaries,
            "Warnings",
        )

    if args.issue_types is None or IssueType.ANALYZER_WARNING in args.issue_types:
        found_issues = found_issues or _check_summary_type(
            bundle.actions_invocation_record.issues.analyzerWarningSummaries,
            "Analyzer Warnings",
        )

    if args.issue_types is None or IssueType.TEST_FAILURE in args.issue_types:
        found_issues = found_issues or _check_summary_type(
            bundle.actions_invocation_record.issues.testFailureSummaries,
            "Test Failures",
        )

    if args.issue_types is None or IssueType.TEST_WARNING in args.issue_types:
        found_issues = found_issues or _check_summary_type(
            bundle.actions_invocation_record.issues.testWarningSummaries,
            "Test Warnings",
        )

    if found_issues:
        print()
        print("Issues found.")
        return 1

    print("No issues found.")
    return 0


def _handle_arguments() -> int:
    """Handle command line arguments and call the correct method."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--bundle-path",
        dest="bundle_path",
        action="store",
        required=True,
        help="Set the path to the xcresults bundle",
    )

    subparsers = parser.add_subparsers()

    export_parser = subparsers.add_parser("export", help="Export attachments from a bundle")

    export_parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        action="store",
        required=True,
        help="Set the output path for the attachments to be written to",
    )

    export_parser.set_defaults(subcommand="export")

    junit_parser = subparsers.add_parser("junit", help="Export test results as a .junit file")

    junit_parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        action="store",
        required=True,
        help="Set the output path for the junit XML to be written to",
    )

    junit_parser.add_argument(
        "--export-attachments-path",
        dest="export_attachments_path",
        action="store",
        help="Set the output path for the attachments to be written to",
    )

    junit_parser.set_defaults(subcommand="junit")

    check_issues_parser = subparsers.add_parser("check-issues", help="Check for issues in results")

    check_issues_parser.add_argument(
        "--issue-types",
        dest="issue_types",
        type=IssueType,
        nargs="+",
        choices=list(IssueType),
        metavar=str({i.value for i in list(IssueType)}),
        help="Set the issue types to report. Will return all issues if not specified.",
    )

    check_issues_parser.set_defaults(subcommand="check-issues")

    args = parser.parse_args()

    try:
        _ = args.subcommand
    # pylint: disable=broad-exception-caught
    except Exception:
        # pylint: enable=broad-exception-caught
        parser.print_help()
        return 1

    if not os.path.exists(args.bundle_path):
        print("Bundle path does not exist")
        return 1

    if not os.path.isdir(args.bundle_path):
        print("Bundle path is not a valid bundle")
        return 1

    if args.subcommand == "export":
        return _handle_export(args)

    if args.subcommand == "junit":
        return _handle_junit(args)

    if args.subcommand == "check-issues":
        return _handle_check_issues(args)

    print("Unrecognized command")
    return 1


def run() -> int:
    """Entry point for poetry generated command line tool."""
    return _handle_arguments()


if __name__ == "__main__":
    sys.exit(_handle_arguments())
