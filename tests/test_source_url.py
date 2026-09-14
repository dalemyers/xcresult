"""Test source URL decoding."""

import pytest

import xcresult
import xcresult.model
from xcresult.source_url import SourceLocation, parse_source_url


@pytest.mark.parametrize("source_url", [None, ""])
def test_missing_source_url(source_url: str | None) -> None:
    """Treat absent and empty source URLs as having no location."""
    assert parse_source_url(source_url) is None


def test_no_path() -> None:
    """Reject URLs that carry no file path."""
    assert parse_source_url("file://") is None


def test_line_and_column() -> None:
    """Convert zero based fragment coordinates to one based values."""
    location = parse_source_url(
        "file:///project/File.swift#StartingLineNumber=328&StartingColumnNumber=35"
    )
    assert location == SourceLocation(
        path="/project/File.swift",
        starting_line_number=329,
        starting_column_number=36,
    )


def test_percent_encoded_path() -> None:
    """Decode percent escapes in the file path."""
    location = parse_source_url("file:///project/My%20File.swift#StartingLineNumber=0")
    assert location is not None
    assert location.path == "/project/My File.swift"
    assert location.starting_line_number == 1


def test_no_fragment() -> None:
    """Report the path alone when the URL carries no coordinates."""
    assert parse_source_url("file:///project/File.swift") == SourceLocation(
        path="/project/File.swift"
    )


def test_column_without_line() -> None:
    """Decode a column independently of a missing line."""
    location = parse_source_url("file:///project/File.swift#StartingColumnNumber=2")
    assert location == SourceLocation(
        path="/project/File.swift",
        starting_line_number=None,
        starting_column_number=3,
    )


@pytest.mark.parametrize("value", ["bad", "-1", "", "1.5"])
def test_unusable_coordinates(value: str) -> None:
    """Ignore fragment values that are blank, negative, or not integers."""
    location = parse_source_url(f"file:///project/File.swift#StartingLineNumber={value}")
    assert location is not None
    assert location.path == "/project/File.swift"
    assert location.starting_line_number is None


@pytest.mark.parametrize(
    "location,expected",
    [
        (SourceLocation(path="/a/File.swift"), "/a/File.swift"),
        (SourceLocation(path="/a/File.swift", starting_line_number=7), "/a/File.swift:7"),
        (
            SourceLocation(path="/a/File.swift", starting_line_number=7, starting_column_number=2),
            "/a/File.swift:7:2",
        ),
        (
            SourceLocation(path="/a/File.swift", starting_column_number=2),
            "/a/File.swift",
        ),
    ],
)
def test_formatting(location: SourceLocation, expected: str) -> None:
    """Append only the coordinates available, stopping at the first missing one."""
    assert str(location) == expected


def test_frozen() -> None:
    """Keep decoded locations immutable."""
    location = SourceLocation(path="/a/File.swift")
    with pytest.raises(Exception):
        location.path = "/b/Other.swift"  # type: ignore[misc]


def test_exported_from_package() -> None:
    """Expose the decoding helper and module without shadowing the generated model."""
    assert xcresult.parse_source_url is parse_source_url
    assert xcresult.source_url.SourceLocation is SourceLocation
    # The generated wire type of the same name must stay reachable.
    assert xcresult.SourceLocation is xcresult.model.SourceLocation
    assert xcresult.SourceLocation is not SourceLocation
