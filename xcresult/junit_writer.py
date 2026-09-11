"""JUnit reports built from modern xcresult test trees and individual runs."""

# pylint: disable=c-extension-no-member

from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace
import logging
import os
from pathlib import Path
import re

from lxml import etree as ET

from xcresult.model import Attachment, TestAttachmentDetails, TestDetails, TestNode
from xcresult.xcresult_base import XcresultsBase

Element = ET._Element  # pylint: disable=protected-access  # pyright: ignore[reportPrivateUsage]
TestFilter = Callable[[TestNode], bool]
_EXECUTION_DIMENSIONS = {"Device", "Test Plan Configuration", "Arguments", "Repetition"}


def _walk(nodes: list[TestNode]) -> Iterator[TestNode]:
    """Walk a modern test tree in report order.

    :param nodes: Roots of the tree.
    :returns: Each node, including roots.
    """
    for node in nodes:
        yield node
        yield from _walk(node.children or [])


def _seconds(node: TestNode) -> float:
    """Read numeric seconds, falling back to Apple's formatted duration.

    :param node: A test or run node.
    :returns: Duration in seconds.
    """
    if node.durationInSeconds is not None:
        return node.durationInSeconds
    if node.duration is None:
        return 0.0
    duration = node.duration.replace(",", ".")
    parts = re.findall(r"(\d+(?:\.\d+)?)\s*(ms|d|h|m|s)", duration)
    remainder = re.sub(r"(\d+(?:\.\d+)?)\s*(ms|d|h|m|s)", "", duration).strip()
    if not parts or remainder:
        raise ValueError(f"Unrecognized test duration: {node.duration!r}")
    units = {"d": 86400, "h": 3600, "m": 60, "s": 1, "ms": 0.001}
    return sum(float(value) * units[unit] for value, unit in parts)


@dataclass(frozen=True)
class _Run:
    """A test attempt and the dimensions that distinguish it from other runs."""

    test: TestNode
    node: TestNode
    suite: str
    configuration: str
    device: str
    arguments: tuple[str, ...]
    repetition: int | None = None


def _context(run: _Run, node: TestNode) -> _Run:
    """Apply an execution dimension to an attempt's context.

    :param run: Current attempt context.
    :param node: Node carrying execution metadata.
    :returns: Updated context.
    """
    if node.nodeType == "Device":
        return replace(run, device=node.nodeIdentifier or node.name)
    if node.nodeType == "Test Plan Configuration":
        return replace(run, configuration=node.name)
    if node.nodeType == "Arguments":
        return replace(run, arguments=(*run.arguments, node.name))
    if node.nodeType == "Repetition":
        identifier = node.nodeIdentifier
        if identifier is None:
            logging.warning(
                "Repetition %s has no identifier; attachments cannot be narrowed by attempt",
                node.name,
            )
            return replace(run, repetition=None)
        if not identifier.isdecimal():
            raise ValueError(f"Invalid repetition identifier: {identifier!r}")
        return replace(run, repetition=int(identifier))
    return run


def _matches_attachment(run: _Run, attachment: Attachment) -> bool:
    """Check the execution dimensions recorded by the export manifest.

    :param run: Selected test attempt.
    :param attachment: Exported file metadata.
    :returns: Whether the attachment belongs to this environment and attempt.
    """
    return (
        (not run.configuration or attachment.configurationName == run.configuration)
        and (not run.device or run.device in {attachment.deviceId, attachment.deviceName})
        and (
            run.repetition is None
            or attachment.repetitionNumber is None
            or run.repetition == attachment.repetitionNumber
        )
        and (
            attachment.arguments is None
            or ", ".join(attachment.arguments) == ", ".join(run.arguments)
        )
    )


class JunitWriter:
    """Write one testcase per run, optionally collapsing retries."""

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        results: XcresultsBase,
        junit_path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
        collapse_retries: bool = False,
        test_filter: TestFilter | None = None,
    ) -> None:
        self.results = results
        self.junit_path = junit_path
        self.export_attachments_path = export_attachments_path
        self.test_class_prefix = test_class_prefix
        self.test_class_suffix = test_class_suffix
        self.collapse_retries = collapse_retries
        self.test_filter = test_filter

    def _tests(
        self, nodes: list[TestNode], parents: tuple[str, ...] = ()
    ) -> Iterator[tuple[TestNode, str]]:
        """Find test cases without interpreting their diagnostic children as tests.

        :param nodes: Test tree roots.
        :param parents: Enclosing bundle and suite names.
        :returns: Test case and suite name pairs.
        """
        for node in nodes:
            if node.nodeType == "Test Case":
                yield node, "/".join(parents) or "Tests"
                continue
            next_parents = parents
            if node.nodeType in {"Unit test bundle", "UI test bundle", "Test Suite"}:
                next_parents = (*parents, node.name)
            yield from self._tests(node.children or [], next_parents)

    def _runs(self, test: TestNode, suite: str, details: TestDetails) -> list[_Run]:
        """Extract individual attempts from a details report.

        :param test: Test case node.
        :param suite: Enclosing suite name.
        :param details: Modern test details.
        :returns: Attempts in report order.
        """
        configuration = (
            details.testPlanConfigurations[0].configurationName
            if len(details.testPlanConfigurations) == 1
            else ""
        )
        device = details.devices[0].deviceId if len(details.devices) == 1 else ""
        initial = _Run(test, test, suite, configuration, device, ())
        runs: list[_Run] = []

        def visit(nodes: list[TestNode], context: _Run) -> None:
            """Collect attempts while retaining enclosing execution dimensions."""
            for node in nodes:
                current = _context(context, node)
                children = [
                    child
                    for child in node.children or []
                    if child.nodeType in _EXECUTION_DIMENSIONS
                    or (
                        child.nodeType == "Test Case Run"
                        and (child.durationInSeconds is not None or child.duration is not None)
                    )
                ]
                if children and node.nodeType != "Test Case Run":
                    visit(children, current)
                    continue
                if node.nodeType in _EXECUTION_DIMENSIONS | {"Test Case Run"}:
                    if node.nodeType == "Test Case Run":
                        for child in _walk(node.children or []):
                            current = _context(current, child)
                    if not current.configuration and len(details.testPlanConfigurations) > 1:
                        raise ValueError(
                            f"Missing configuration for run of {details.testIdentifier}"
                        )
                    if not current.device and len(details.devices) > 1:
                        raise ValueError(f"Missing device for run of {details.testIdentifier}")
                    runs.append(replace(current, node=node))
                else:
                    visit(node.children or [], current)

        source = details.testRuns
        # The tests tree preserves repetitions even when the details report
        # reduces them to destination/configuration aggregates.
        if any(node.nodeType == "Repetition" for node in _walk(test.children or [])) and not any(
            node.nodeType == "Repetition" for node in _walk(source)
        ):
            source = test.children or []
        visit(source, initial)
        if runs:
            return runs
        # Skipped tests can have no individual runs. The details report still
        # carries an explicit outcome; preserve it rather than inventing a pass.
        if details.testRuns:
            raise ValueError(f"No test case runs found for {details.testIdentifier}")
        return [
            replace(
                initial,
                node=replace(
                    test,
                    result=details.testResult,
                    duration=details.duration,
                    durationInSeconds=details.durationInSeconds,
                ),
            )
        ]

    def _collapse(self, runs: list[_Run]) -> list[_Run]:
        """Keep a winning attempt within each test and execution environment.

        :param runs: All attempts.
        :returns: Selected attempts in their original order.
        """
        winners: dict[tuple[object, ...], int] = {}
        rank = {"Passed": 3, "Expected Failure": 3, "Failed": 2, "Skipped": 1}
        for index, run in enumerate(runs):
            identifier = run.test.nodeIdentifierURL or run.test.nodeIdentifier
            key = (identifier or index, run.suite, run.configuration, run.device, run.arguments)
            previous = winners.get(key)
            if previous is None or rank.get(run.node.result or "", 2) > rank.get(
                runs[previous].node.result or "", 2
            ):
                winners[key] = index
        retained = set(winners.values())
        return [run for index, run in enumerate(runs) if index in retained]

    def _attachment_paths(self, run: _Run, manifest: list[TestAttachmentDetails]) -> list[str]:
        """Resolve exported filenames using the manifest, never guessed directories.

        :param run: Test attempt.
        :param manifest: Exported attachments.
        :returns: Attachment paths relative to the JUnit file.
        """
        if self.export_attachments_path is None:
            return []
        root = Path(self.export_attachments_path).resolve()
        paths: list[str] = []
        for entry in manifest:
            if run.test.nodeIdentifierURL and entry.testIdentifierURL:
                matches = run.test.nodeIdentifierURL == entry.testIdentifierURL
            else:
                matches = run.test.nodeIdentifier == entry.testIdentifier
            if not matches:
                continue
            for attachment in entry.attachments:
                if not _matches_attachment(run, attachment):
                    continue
                path = (root / attachment.exportedFileName).resolve()
                if not path.is_relative_to(root):
                    raise ValueError(f"Attachment path escapes export directory: {path}")
                if not path.is_file():
                    raise FileNotFoundError(f"Exported attachment is missing: {path}")
                relative = os.path.relpath(path, Path(self.junit_path).parent)
                if relative not in paths:
                    paths.append(relative)
        return paths

    def _testcase(
        self, suite: Element, run: _Run, manifest: list[TestAttachmentDetails]
    ) -> tuple[int, int]:
        """Write a testcase and its diagnostics.

        :param suite: Parent XML element.
        :param run: Selected test attempt.
        :param manifest: Export manifest.
        :returns: Failure and skipped counts.
        """
        identifier = run.test.nodeIdentifier or run.test.name
        classname = identifier.rsplit("/", maxsplit=1)[0]
        classname = ".".join(
            part for part in (self.test_class_prefix, classname, self.test_class_suffix) if part
        )
        case = ET.SubElement(
            suite, "testcase", classname=classname, name=run.test.name, time=str(_seconds(run.node))
        )
        status = run.node.result
        failures = 0
        skipped = 0
        messages: list[str]
        if status == "Skipped":
            skipped = 1
            messages = [
                node.name
                for node in _walk(run.node.children or [])
                if node.nodeType == "Skip Message"
                or (node.nodeType == "Test Case Run" and node.result == "Skipped")
            ]
            ET.SubElement(case, "skipped", message="\n".join(messages))
        elif status not in {"Passed", "Expected Failure"}:
            failures = 1
            messages = []
            for node in _walk(run.node.children or []):
                if node.nodeType != "Failure Message" and not (
                    node.nodeType == "Test Case Run" and node.result == "Failed"
                ):
                    continue
                message = node.name
                if node.sourceLocation is not None:
                    message += f" ({node.sourceLocation.filePath}:{node.sourceLocation.lineNumber})"
                messages.append(message)
            ET.SubElement(
                case,
                "failure",
                message="\n".join(messages) or f"Test result: {status or 'unknown'}",
            )
        if failures:
            attachments = self._attachment_paths(run, manifest)
            if attachments:
                output = ET.SubElement(case, "system-out")
                output.text = ET.CDATA(
                    "\n" + "\n".join(f"[[ATTACHMENT|{path}]]" for path in attachments) + "\n"
                )
        return failures, skipped

    def write(self) -> None:
        """Write XML, with counts calculated from the testcases actually emitted."""
        root = ET.Element("testsuites")
        runs: list[_Run] = []
        manifest: list[TestAttachmentDetails] = []
        if self.results.content_availability.hasTestResults:
            if self.export_attachments_path is not None:
                manifest = self.results.export_test_attachments(self.export_attachments_path)
            for test, suite_name in self._tests(self.results.tests.testNodes):
                identifier = test.nodeIdentifierURL or test.nodeIdentifier
                if identifier is None:
                    runs.append(_Run(test, test, suite_name, "", "", ()))
                else:
                    runs.extend(self._runs(test, suite_name, self.results.test_details(identifier)))
        if self.collapse_retries:
            runs = self._collapse(runs)
        if self.test_filter is not None:
            runs = [run for run in runs if self.test_filter(run.test)]

        groups: dict[tuple[str, str, str], list[_Run]] = {}
        for run in runs:
            groups.setdefault((run.suite, run.configuration, run.device), []).append(run)
        total_failures = 0
        total_skipped = 0
        for (name, configuration, device), group in groups.items():
            suite = ET.SubElement(root, "testsuite", name=name)
            suite.set("time", str(sum(_seconds(run.node) for run in group)))
            properties = ET.SubElement(suite, "properties")
            ET.SubElement(properties, "property", name="Configuration", value=configuration)
            ET.SubElement(properties, "property", name="Device", value=device)
            counts = [self._testcase(suite, run, manifest) for run in group]
            failures = sum(count[0] for count in counts)
            skipped = sum(count[1] for count in counts)
            suite.set("tests", str(len(group)))
            suite.set("failures", str(failures))
            suite.set("skipped", str(skipped))
            total_failures += failures
            total_skipped += skipped
        root.set("tests", str(len(runs)))
        root.set("failures", str(total_failures))
        root.set("skipped", str(total_skipped))
        root.set("time", str(sum(_seconds(run.node) for run in runs)))
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ")
        tree.write(self.junit_path, encoding="utf-8", xml_declaration=True)
