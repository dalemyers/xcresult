#!/usr/bin/env python3

"""Command line handler for xcresult."""

from __future__ import annotations

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

    if not os.path.isdir(args.output_path):
        print("Output folder does not exist or is not a directory", file=sys.stderr)
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
        print("Output file already exists", file=sys.stderr)
        return 1

    try:
        bundle = xcresult.Xcresults(args.bundle_path)
        bundle.write_junit(
            args.output_path,
            args.export_attachments_path,
            collapse_retries=args.collapse_retries,
        )
        # pylint: disable=broad-exception-caught
    except Exception as ex:
        # pylint: enable=broad-exception-caught
        print(f"Could not export junit: {ex}", file=sys.stderr)
        return 1

    return 0


def _check_summary_type(
    summaries: Sequence[xcresult.Issue | xcresult.TestFailure] | None,
    summary_name: str,
) -> bool:
    """Print every issue in a selected category and report whether any exist."""
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
        message = summary.message if isinstance(summary, xcresult.Issue) else summary.failureText
        location = (
            xcresult.parse_source_url(summary.sourceURL)
            if isinstance(summary, xcresult.Issue)
            else None
        )
        if location is not None:
            print(f"{location} -> {message}")
        else:
            print(message)

    print()

    return True


def _handle_check_issues(args: argparse.Namespace) -> int:
    """Handle the check-issues sub command."""

    selected = set(IssueType) if args.issue_types is None else set(args.issue_types)
    found_issues = False
    try:
        bundle = xcresult.Xcresults(args.bundle_path)
        build_categories = (
            (IssueType.ERROR, "errors", "Errors"),
            (IssueType.WARNING, "warnings", "Warnings"),
            (IssueType.ANALYZER_WARNING, "analyzerWarnings", "Analyzer Warnings"),
        )
        if any(issue_type in selected for issue_type, _, _ in build_categories):
            build_results = bundle.build_results
            for issue_type, attribute, name in build_categories:
                if issue_type in selected:
                    found_issues = (
                        _check_summary_type(getattr(build_results, attribute), name) or found_issues
                    )

        test_categories = (
            (IssueType.TEST_FAILURE, "testFailures", "Test Failures"),
            (IssueType.TEST_WARNING, "runtimeWarnings", "Test Warnings"),
        )
        if any(issue_type in selected for issue_type, _, _ in test_categories):
            summary = bundle.test_summary if bundle.content_availability.hasTestResults else None
            for issue_type, attribute, name in test_categories:
                if issue_type in selected:
                    issues = getattr(summary, attribute) if summary is not None else None
                    found_issues = _check_summary_type(issues, name) or found_issues
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(f"Could not check issues: {ex}", file=sys.stderr)
        return 1

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

    junit_parser.add_argument(
        "--collapse-retries",
        dest="collapse_retries",
        action="store_true",
        help=(
            "Collapse the multiple results a test produces under "
            "-retry-tests-on-failure into a single testcase (a pass if any "
            "attempt passed). Default: one testcase per attempt."
        ),
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

    if not hasattr(args, "subcommand"):
        parser.print_help()
        return 1

    if not os.path.exists(args.bundle_path):
        print("Bundle path does not exist", file=sys.stderr)
        return 1

    if not os.path.isdir(args.bundle_path):
        print("Bundle path is not a valid bundle", file=sys.stderr)
        return 1

    if args.subcommand == "export":
        return _handle_export(args)

    if args.subcommand == "junit":
        return _handle_junit(args)

    if args.subcommand == "check-issues":
        return _handle_check_issues(args)

    print("Unrecognized command", file=sys.stderr)
    return 1


def run() -> int:
    """Entry point for poetry generated command line tool."""
    return _handle_arguments()


if __name__ == "__main__":
    sys.exit(_handle_arguments())
