"""Test xcresult base class."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
from xcresult.xcresult_base import XcresultsBase

# pylint: enable=wrong-import-position


class MockXcresults(XcresultsBase):
    """Mock implementation of XcresultsBase for testing."""

    def __init__(self, path: str):
        super().__init__(path)

    @property
    def actions_invocation_record(self):
        """Return None for testing."""
        return None

    def get(self, identifier: str):
        """Return empty dict for testing."""
        return {}

    def export_test_attachments(self, output_path: str):
        """Do nothing for testing."""
        pass


def test_init_absolute_path():
    """Test initialization with absolute path."""
    test_path = "/absolute/path/to/result.xcresult"
    xcresults = MockXcresults(test_path)
    assert xcresults.path == test_path


def test_init_relative_path():
    """Test initialization with relative path."""
    test_path = "relative/path/to/result.xcresult"
    xcresults = MockXcresults(test_path)
    expected_path = os.path.join(os.getcwd(), test_path)
    assert xcresults.path == expected_path


def test_actions_invocation_record_not_implemented():
    """Test that actions_invocation_record raises NotImplementedError in base class."""

    class UnimplementedXcresults(XcresultsBase):
        pass

    xcresults = UnimplementedXcresults("/test/path")

    try:
        _ = xcresults.actions_invocation_record
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass


def test_get_not_implemented():
    """Test that get raises NotImplementedError in base class."""

    class UnimplementedXcresults(XcresultsBase):
        pass

    xcresults = UnimplementedXcresults("/test/path")

    try:
        xcresults.get("test-id")
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass


def test_export_test_attachments_not_implemented():
    """Test that export_test_attachments raises NotImplementedError in base class."""

    class UnimplementedXcresults(XcresultsBase):
        pass

    xcresults = UnimplementedXcresults("/test/path")

    try:
        xcresults.export_test_attachments("/output/path")
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass


def test_actions_invocation_record_cached():
    """Test that _actions_invocation_record is initialized to None."""
    xcresults = MockXcresults("/test/path")
    assert xcresults._actions_invocation_record is None
