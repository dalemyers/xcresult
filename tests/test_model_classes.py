"""Comprehensive tests for model classes to increase coverage."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult

# pylint: enable=wrong-import-position


def test_xchash_with_members_none():
    """Test xchash when _members attribute doesn't exist."""
    from xcresult.model import xchash

    # Test with object that has no _members attribute (line 38)
    obj = object()
    result = xchash(obj)
    assert isinstance(result, int)


def test_xchash_with_dict():
    """Test xchash with dictionary (lines 27-31)."""
    from xcresult.model import xchash

    # Test with nested dictionaries (lines 28-31)
    test_dict = {"key1": "value1", "key2": {"nested": "value"}}
    result = xchash(test_dict)
    assert isinstance(result, int)


def test_xchash_with_list():
    """Test xchash with list (lines 22-25)."""
    from xcresult.model import xchash

    # Test with nested lists (line 24)
    test_list = [1, 2, [3, 4], 5]
    result = xchash(test_list)
    assert isinstance(result, int)


def test_flatten_with_values():
    """Test flatten function (line 15)."""
    from xcresult.model import flatten

    # Test flatten (line 15)
    nested = [[1, 2], [3, 4], [5]]
    result = flatten(nested)
    assert result == [1, 2, 3, 4, 5]


def test_xcresult_object_not_equal_different_type():
    """Test XcresultObject inequality with different types (lines 53-57)."""
    from xcresult.model import XcresultObject

    obj = XcresultObject()

    # Test inequality with different type (line 57)
    assert obj != "string"
    assert obj != 123
    assert obj != None


def test_xcresult_object_hash():
    """Test XcresultObject hash (line 61)."""
    from xcresult.model import XcresultObject

    obj = XcresultObject()
    result = hash(obj)
    assert isinstance(result, int)


def test_action_platform_record_all_members():
    """Test ActionPlatformRecord with all properties."""
    record = xcresult.ActionPlatformRecord()
    record.identifier = "platform-id"
    record.userDescription = "Platform Description"

    record2 = xcresult.ActionPlatformRecord()
    record2.identifier = "platform-id"
    record2.userDescription = "Platform Description"

    # Test equality
    assert record == record2
    assert hash(record) == hash(record2)

    # Test members
    members = record._members()
    assert "platform-id" in members
    assert "Platform Description" in members

    # Test inequality
    record3 = xcresult.ActionPlatformRecord()
    record3.identifier = "different-id"
    record3.userDescription = "Platform Description"
    assert record != record3


def test_action_sdk_record_all_members():
    """Test ActionSDKRecord with all properties."""
    sdk = xcresult.ActionSDKRecord()
    sdk.name = "iOS SDK"
    sdk.identifier = "sdk-id"
    sdk.operatingSystemVersion = "15.0"
    sdk.isInternal = False

    sdk2 = xcresult.ActionSDKRecord()
    sdk2.name = "iOS SDK"
    sdk2.identifier = "sdk-id"
    sdk2.operatingSystemVersion = "15.0"
    sdk2.isInternal = False

    assert sdk == sdk2
    assert hash(sdk) == hash(sdk2)

    members = sdk._members()
    assert "iOS SDK" in members
    assert "sdk-id" in members


def test_type_definition_all_members():
    """Test TypeDefinition with all properties."""
    typedef = xcresult.TypeDefinition()
    typedef.name = "String"
    typedef.supertype = None

    typedef2 = xcresult.TypeDefinition()
    typedef2.name = "String"
    typedef2.supertype = None

    assert typedef == typedef2
    assert hash(typedef) == hash(typedef2)

    members = typedef._members()
    assert "String" in members


