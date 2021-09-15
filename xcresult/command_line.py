#!/usr/bin/env python3

"""Command line handler for xcresult."""

import argparse
import json
import os
import sys

try:
    import xcresult
except ImportError:
    # Insert the package into the PATH
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))
    import xcresult


def _handle_export(args: argparse.Namespace) -> int:
    """Handle the export sub command."""

    if not os.path.exists(args.output_path):
        print("Output folder does not exist")
        return 1

    try:
        bundle = xcresult.Xcresults(args.bundle_path)
        bundle.export_attachments(args.output_path)
    except Exception as ex:
        print(f"Could not export attachments: {ex}", file=sys.stderr)
        return 1

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

    args = parser.parse_args()

    try:
        _ = args.subcommand
    except Exception:
        parser.print_help()
        return 1

    if args.subcommand == "export":
        return _handle_export(args)

    print("Unrecognized command")
    return 1


def run() -> int:
    """Entry point for poetry generated command line tool."""
    return _handle_arguments()


if __name__ == "__main__":
    sys.exit(_handle_arguments())