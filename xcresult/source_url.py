"""Helpers for reading the source locations attached to modern xcresult issues.

Xcode 27's reports replaced the legacy ``documentLocationInCreatingWorkspace``
object with a plain ``sourceURL`` string on each issue. The URL keeps the same
shape Xcode has always used, e.g.::

    file:///path/to/File.swift#StartingLineNumber=328&StartingColumnNumber=35

The line and column numbers in the fragment are zero based, so they are
converted to the one based values editors and build logs report.
"""

from __future__ import annotations

from dataclasses import dataclass
import urllib.parse


@dataclass(frozen=True)
class SourceLocation:
    """A decoded location from an issue's ``sourceURL``."""

    path: str
    starting_line_number: int | None = None
    starting_column_number: int | None = None

    def __str__(self) -> str:
        """Format the location as ``path``, ``path:line``, or ``path:line:column``.

        :returns: The path with whichever coordinates are available appended.
        """
        if self.starting_line_number is None:
            return self.path

        if self.starting_column_number is None:
            return f"{self.path}:{self.starting_line_number}"

        return f"{self.path}:{self.starting_line_number}:{self.starting_column_number}"


def _fragment_number(fragment: dict[str, list[str]], key: str) -> int | None:
    """Read a zero based number from a source URL fragment as a one based value.

    :param fragment: The parsed fragment of the source URL.
    :param key: The fragment key to read.

    :returns: The one based value if it is present and valid, None otherwise.
    """

    values = fragment.get(key)

    if not values:
        return None

    try:
        value = int(values[0])
    except ValueError:
        return None

    if value < 0:
        return None

    return value + 1


def parse_source_url(source_url: str | None) -> SourceLocation | None:
    """Decode the file path and coordinates from an issue's source URL.

    :param source_url: The ``sourceURL`` from an xcresult issue.

    :returns: The decoded location, or None if there is no usable file path.
    """

    if not source_url:
        return None

    parsed = urllib.parse.urlparse(source_url)

    if not parsed.path:
        return None

    fragment = urllib.parse.parse_qs(parsed.fragment)

    return SourceLocation(
        path=urllib.parse.unquote(parsed.path),
        starting_line_number=_fragment_number(fragment, "StartingLineNumber"),
        starting_column_number=_fragment_number(fragment, "StartingColumnNumber"),
    )
