"""Test model classes."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
from xcresult.model import flatten, xchash, XcresultObject

# pylint: enable=wrong-import-position


def test_flatten():
    """Test the flatten function."""
    nested_list = [[1, 2], [3, 4], [5]]
    result = flatten(nested_list)
    assert result == [1, 2, 3, 4, 5]


def test_flatten_empty():
    """Test flatten with empty list."""
    result = flatten([])
    assert result == []


def test_xchash_primitive():
    """Test xchash with primitive value."""
    result = xchash("test")
    assert isinstance(result, int)


def test_xchash_list():
    """Test xchash with list."""
    result = xchash([1, 2, 3])
    assert isinstance(result, int)


def test_xchash_dict():
    """Test xchash with dict."""
    result = xchash({"a": 1, "b": 2})
    assert isinstance(result, int)


def test_xchash_object():
    """Test xchash with XcresultObject."""
    obj = xcresult.ActionPlatformRecord()
    obj.identifier = "test"
    obj.userDescription = "test"
    result = xchash(obj)
    assert isinstance(result, int)


def test_xchash_object_no_members():
    """Test xchash with object without _members."""

    class NoMembers:
        pass

    obj = NoMembers()
    result = xchash(obj)
    assert isinstance(result, int)


def test_xcresult_object_base():
    """Test XcresultObject base class."""
    obj = XcresultObject()
    assert obj._members() == ()


def test_xcresult_object_eq_same_type():
    """Test XcresultObject equality with same type."""
    obj1 = XcresultObject()
    obj2 = XcresultObject()
    assert obj1 == obj2


def test_xcresult_object_eq_different_type():
    """Test XcresultObject equality with different type."""
    obj = XcresultObject()
    assert obj != "string"


def test_xcresult_object_hash():
    """Test XcresultObject hash."""
    obj = XcresultObject()
    result = hash(obj)
    assert isinstance(result, int)


def test_action_platform_record_members():
    """Test ActionPlatformRecord _members."""
    record = xcresult.ActionPlatformRecord()
    record.identifier = "test-id"
    record.userDescription = "test-desc"
    members = record._members()
    assert "test-id" in members
    assert "test-desc" in members


def test_action_platform_record_eq():
    """Test ActionPlatformRecord equality."""
    record1 = xcresult.ActionPlatformRecord()
    record1.identifier = "test-id"
    record1.userDescription = "test-desc"

    record2 = xcresult.ActionPlatformRecord()
    record2.identifier = "test-id"
    record2.userDescription = "test-desc"

    assert record1 == record2


def test_action_platform_record_not_eq():
    """Test ActionPlatformRecord inequality."""
    record1 = xcresult.ActionPlatformRecord()
    record1.identifier = "test-id-1"
    record1.userDescription = "test-desc"

    record2 = xcresult.ActionPlatformRecord()
    record2.identifier = "test-id-2"
    record2.userDescription = "test-desc"

    assert record1 != record2


def test_action_platform_record_hash():
    """Test ActionPlatformRecord hash."""
    record = xcresult.ActionPlatformRecord()
    record.identifier = "test-id"
    record.userDescription = "test-desc"
    result = hash(record)
    assert isinstance(result, int)


def test_action_sdk_record_members():
    """Test ActionSDKRecord."""
    record = xcresult.ActionSDKRecord()
    record.name = "SDK"
    record.identifier = "sdk-id"
    record.operatingSystemVersion = "14.0"
    record.isInternal = False
    members = record._members()
    assert "SDK" in members
    assert "sdk-id" in members


def test_action_sdk_record_eq():
    """Test ActionSDKRecord equality."""
    record1 = xcresult.ActionSDKRecord()
    record1.name = "SDK"
    record1.identifier = "sdk-id"
    record1.operatingSystemVersion = "14.0"
    record1.isInternal = False

    record2 = xcresult.ActionSDKRecord()
    record2.name = "SDK"
    record2.identifier = "sdk-id"
    record2.operatingSystemVersion = "14.0"
    record2.isInternal = False

    assert record1 == record2


def test_action_sdk_record_hash():
    """Test ActionSDKRecord hash."""
    record = xcresult.ActionSDKRecord()
    record.name = "SDK"
    record.identifier = "sdk-id"
    record.operatingSystemVersion = "14.0"
    record.isInternal = False
    result = hash(record)
    assert isinstance(result, int)


def test_document_location():
    """Test DocumentLocation."""
    location = xcresult.DocumentLocation()
    location.url = "file:///path/to/file.swift#StartingLineNumber=10"
    location.concreteTypeName = "DVTTextDocumentLocation"

    # Test path property
    assert location.path == "/path/to/file.swift"

    # Test starting_line_number property (offset by 1)
    assert location.starting_line_number == 11

    # Test starting_column_number property
    assert location.starting_column_number is None


def test_document_location_with_column():
    """Test DocumentLocation with column number."""
    location = xcresult.DocumentLocation()
    location.url = "file:///path/to/file.swift#StartingLineNumber=10&StartingColumnNumber=5"
    location.concreteTypeName = "DVTTextDocumentLocation"

    assert location.path == "/path/to/file.swift"
    assert location.starting_line_number == 11
    assert location.starting_column_number == 6


def test_document_location_empty():
    """Test DocumentLocation empty method."""
    location = xcresult.DocumentLocation.empty()
    assert location.path is not None
    assert location.starting_line_number is not None


def test_document_location_properties():
    """Test DocumentLocation various properties."""
    location = xcresult.DocumentLocation()
    location.url = "file:///path/to/file.swift#StartingLineNumber=10&EndingLineNumber=20&StartingColumnNumber=5&EndingColumnNumber=15&CharacterRangeLen=10"
    location.concreteTypeName = "DVTTextDocumentLocation"

    assert location.path == "/path/to/file.swift"
    assert location.starting_line_number == 11
    assert location.starting_column_number == 6
    assert location.ending_line_number == 21
    assert location.ending_column_number == 16


def test_issue_summary():
    """Test IssueSummary."""
    summary = xcresult.IssueSummary()
    summary.message = "Test issue"
    summary.issueType = "error"

    assert summary.message == "Test issue"
    assert summary.issueType == "error"


def test_action_testable_summary_all_tests():
    """Test ActionTestableSummary all_tests method."""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "data", "TestSuccess.xcresult"
    )
    bundle = xcresult.Xcresults(test_data_path)

    if bundle.actions_invocation_record.actions:
        action = bundle.actions_invocation_record.actions[0]
        if action.actionResult.testsRef:
            from xcresult.xcresulttool import get_test_plan_run_summaries

            summaries = get_test_plan_run_summaries(
                test_data_path, action.actionResult.testsRef.id
            )
            if summaries.summaries and summaries.summaries[0].testableSummaries:
                testable = summaries.summaries[0].testableSummaries[0]
                all_tests = testable.all_tests()
                assert isinstance(all_tests, list)
                assert len(all_tests) > 0


def test_action_test_summary_group_all_subtests():
    """Test ActionTestSummaryGroup all_subtests method."""
    group = xcresult.ActionTestSummaryGroup()
    group.identifier = "group"

    # Create some mock tests
    test1 = xcresult.ActionTestMetadata()
    test1.identifier = "test1"

    test2 = xcresult.ActionTestMetadata()
    test2.identifier = "test2"

    group.subtests = [test1, test2]

    all_tests = group.all_subtests()
    assert len(all_tests) == 2


def test_action_test_summary_group_nested():
    """Test ActionTestSummaryGroup with nested groups."""
    parent_group = xcresult.ActionTestSummaryGroup()
    parent_group.identifier = "parent"

    child_group = xcresult.ActionTestSummaryGroup()
    child_group.identifier = "child"

    test = xcresult.ActionTestMetadata()
    test.identifier = "test"

    child_group.subtests = [test]
    parent_group.subtests = [child_group]

    all_tests = parent_group.all_subtests()
    assert len(all_tests) == 1
    assert all_tests[0].identifier == "test"


def test_action_test_summary_group_no_subtests():
    """Test ActionTestSummaryGroup with no subtests."""
    group = xcresult.ActionTestSummaryGroup()
    group.identifier = "group"
    group.subtests = None

    all_tests = group.all_subtests()
    assert all_tests == []


def test_action_test_metadata_all_subtests():
    """Test ActionTestMetadata all_subtests method."""
    test = xcresult.ActionTestMetadata()
    test.identifier = "test"
    test.identifierURL = "test://url"
    test.name = "test"
    test.testStatus = "Success"
    test.duration = 0.0
    test.summaryRef = None
    test.performanceMetricsCount = 0
    test.failureSummariesCount = 0
    test.activitySummariesCount = 0

    all_tests = test.all_subtests()
    assert len(all_tests) == 1
    # Just check it returns the right object
    assert all_tests[0].identifier == test.identifier


def test_reference():
    """Test Reference class."""
    ref = xcresult.Reference()
    ref.id = "test-id"
    ref.targetType = xcresult.TypeDefinition()
    ref.targetType.name = "TestType"

    assert ref.id == "test-id"
    assert ref.targetType.name == "TestType"


def test_type_definition():
    """Test TypeDefinition class."""
    type_def = xcresult.TypeDefinition()
    type_def.name = "TestType"

    assert type_def.name == "TestType"


def test_code_coverage_info():
    """Test CodeCoverageInfo class."""
    coverage = xcresult.CodeCoverageInfo()
    coverage.hasCoverageData = True

    assert coverage.hasCoverageData is True


def test_result_issue_summaries():
    """Test ResultIssueSummaries class."""
    summaries = xcresult.ResultIssueSummaries()
    summaries.errorSummaries = []
    summaries.warningSummaries = []
    summaries.testFailureSummaries = []

    assert summaries.errorSummaries == []


def test_action_result():
    """Test ActionResult class."""
    result = xcresult.ActionResult()
    result.resultName = "test"
    result.status = "succeeded"

    assert result.resultName == "test"
    assert result.status == "succeeded"


def test_action_record():
    """Test ActionRecord class."""
    record = xcresult.ActionRecord()
    record.schemeCommandName = "Test"
    record.schemeTaskName = "Action"

    assert record.schemeCommandName == "Test"


def test_actions_invocation_record():
    """Test ActionsInvocationRecord class."""
    record = xcresult.ActionsInvocationRecord()
    record.actions = []

    assert record.actions == []


def test_action_device_record():
    """Test ActionDeviceRecord class."""
    device = xcresult.ActionDeviceRecord()
    device.modelName = "iPhone 12"
    device.identifier = "device-id"
    device.isConcreteDevice = True

    assert device.modelName == "iPhone 12"


def test_action_run_destination_record():
    """Test ActionRunDestinationRecord class."""
    destination = xcresult.ActionRunDestinationRecord()
    destination.displayName = "iPhone 12"
    destination.targetArchitecture = "arm64"

    assert destination.displayName == "iPhone 12"


def test_result_metrics():
    """Test ResultMetrics class."""
    metrics = xcresult.ResultMetrics()
    metrics.testsCount = 10
    metrics.testsFailedCount = 2

    assert metrics.testsCount == 10
    assert metrics.testsFailedCount == 2


def test_activity_log_section():
    """Test ActivityLogSection class."""
    section = xcresult.ActivityLogSection()
    section.title = "Test Section"

    assert section.title == "Test Section"
