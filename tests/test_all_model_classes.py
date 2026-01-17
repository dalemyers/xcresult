"""Comprehensive tests for all untested model classes."""

import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult
# pylint: enable=wrong-import-position


def test_actionabstracttestsummary_equality_and_hash():
    """Test ActionAbstractTestSummary equality and hashing."""
    obj1 = xcresult.ActionAbstractTestSummary()
    obj2 = xcresult.ActionAbstractTestSummary()
    obj3 = xcresult.ActionAbstractTestSummary()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiondevicerecord_equality_and_hash():
    """Test ActionDeviceRecord equality and hashing."""
    obj1 = xcresult.ActionDeviceRecord()
    obj2 = xcresult.ActionDeviceRecord()
    obj3 = xcresult.ActionDeviceRecord()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.isConcreteDevice = True
    obj2.isConcreteDevice = True
    obj3.isConcreteDevice = False
    obj1.operatingSystemVersion = "test_value"
    obj2.operatingSystemVersion = "test_value"
    obj3.operatingSystemVersion = "test_value_2"
    obj1.operatingSystemVersionWithBuildNumber = "test_value"
    obj2.operatingSystemVersionWithBuildNumber = "test_value"
    obj3.operatingSystemVersionWithBuildNumber = "test_value_2"
    obj1.nativeArchitecture = "test_value"
    obj2.nativeArchitecture = "test_value"
    obj3.nativeArchitecture = "test_value_2"
    obj1.modelName = "test_value"
    obj2.modelName = "test_value"
    obj3.modelName = "test_value_2"
    obj1.modelCode = "test_value"
    obj2.modelCode = "test_value"
    obj3.modelCode = "test_value_2"
    obj1.modelUTI = "test_value"
    obj2.modelUTI = "test_value"
    obj3.modelUTI = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.isWireless = True
    obj2.isWireless = True
    obj3.isWireless = False
    obj1.cpuKind = "test_value"
    obj2.cpuKind = "test_value"
    obj3.cpuKind = "test_value_2"
    obj1.cpuCount = 42
    obj2.cpuCount = 42
    obj3.cpuCount = 84
    obj1.cpuSpeedInMHz = 42
    obj2.cpuSpeedInMHz = 42
    obj3.cpuSpeedInMHz = 84
    obj1.busSpeedInMHz = 42
    obj2.busSpeedInMHz = 42
    obj3.busSpeedInMHz = 84
    obj1.ramSizeInMegabytes = 42
    obj2.ramSizeInMegabytes = 42
    obj3.ramSizeInMegabytes = 84
    obj1.physicalCPUCoresPerPackage = 42
    obj2.physicalCPUCoresPerPackage = 42
    obj3.physicalCPUCoresPerPackage = 84
    obj1.logicalCPUCoresPerPackage = 42
    obj2.logicalCPUCoresPerPackage = 42
    obj3.logicalCPUCoresPerPackage = 84
    obj1.platformRecord = None
    obj2.platformRecord = None
    obj3.platformRecord = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionplatformrecord_equality_and_hash():
    """Test ActionPlatformRecord equality and hashing."""
    obj1 = xcresult.ActionPlatformRecord()
    obj2 = xcresult.ActionPlatformRecord()
    obj3 = xcresult.ActionPlatformRecord()
    
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.userDescription = "test_value"
    obj2.userDescription = "test_value"
    obj3.userDescription = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionrecord_equality_and_hash():
    """Test ActionRecord equality and hashing."""
    obj1 = xcresult.ActionRecord()
    obj2 = xcresult.ActionRecord()
    obj3 = xcresult.ActionRecord()
    
    obj1.schemeCommandName = "test_value"
    obj2.schemeCommandName = "test_value"
    obj3.schemeCommandName = "test_value_2"
    obj1.schemeTaskName = "test_value"
    obj2.schemeTaskName = "test_value"
    obj3.schemeTaskName = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startedTime = datetime.datetime(2020, 1, 1)
    obj2.startedTime = datetime.datetime(2020, 1, 1)
    obj3.startedTime = datetime.datetime(2020, 2, 1)
    obj1.endedTime = datetime.datetime(2020, 1, 1)
    obj2.endedTime = datetime.datetime(2020, 1, 1)
    obj3.endedTime = datetime.datetime(2020, 2, 1)
    obj1.runDestination = None
    obj2.runDestination = None
    obj3.runDestination = None
    obj1.buildResult = None
    obj2.buildResult = None
    obj3.buildResult = None
    obj1.actionResult = None
    obj2.actionResult = None
    obj3.actionResult = None
    obj1.testPlanName = "test_value"
    obj2.testPlanName = "test_value"
    obj3.testPlanName = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionresult_equality_and_hash():
    """Test ActionResult equality and hashing."""
    obj1 = xcresult.ActionResult()
    obj2 = xcresult.ActionResult()
    obj3 = xcresult.ActionResult()
    
    obj1.resultName = "test_value"
    obj2.resultName = "test_value"
    obj3.resultName = "test_value_2"
    obj1.status = "test_value"
    obj2.status = "test_value"
    obj3.status = "test_value_2"
    obj1.metrics = None
    obj2.metrics = None
    obj3.metrics = None
    obj1.issues = None
    obj2.issues = None
    obj3.issues = None
    obj1.coverage = None
    obj2.coverage = None
    obj3.coverage = None
    obj1.timelineRef = None
    obj2.timelineRef = None
    obj3.timelineRef = None
    obj1.logRef = None
    obj2.logRef = None
    obj3.logRef = None
    obj1.testsRef = None
    obj2.testsRef = None
    obj3.testsRef = None
    obj1.diagnosticsRef = None
    obj2.diagnosticsRef = None
    obj3.diagnosticsRef = None
    obj1.consoleLogRef = None
    obj2.consoleLogRef = None
    obj3.consoleLogRef = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionrundestinationrecord_equality_and_hash():
    """Test ActionRunDestinationRecord equality and hashing."""
    obj1 = xcresult.ActionRunDestinationRecord()
    obj2 = xcresult.ActionRunDestinationRecord()
    obj3 = xcresult.ActionRunDestinationRecord()
    
    obj1.displayName = "test_value"
    obj2.displayName = "test_value"
    obj3.displayName = "test_value_2"
    obj1.targetArchitecture = "test_value"
    obj2.targetArchitecture = "test_value"
    obj3.targetArchitecture = "test_value_2"
    obj1.targetDeviceRecord = None
    obj2.targetDeviceRecord = None
    obj3.targetDeviceRecord = None
    obj1.localComputerRecord = None
    obj2.localComputerRecord = None
    obj3.localComputerRecord = None
    obj1.targetSDKRecord = None
    obj2.targetSDKRecord = None
    obj3.targetSDKRecord = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionsdkrecord_equality_and_hash():
    """Test ActionSDKRecord equality and hashing."""
    obj1 = xcresult.ActionSDKRecord()
    obj2 = xcresult.ActionSDKRecord()
    obj3 = xcresult.ActionSDKRecord()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.operatingSystemVersion = "test_value"
    obj2.operatingSystemVersion = "test_value"
    obj3.operatingSystemVersion = "test_value_2"
    obj1.isInternal = True
    obj2.isInternal = True
    obj3.isInternal = False
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestactivitysummary_equality_and_hash():
    """Test ActionTestActivitySummary equality and hashing."""
    obj1 = xcresult.ActionTestActivitySummary()
    obj2 = xcresult.ActionTestActivitySummary()
    obj3 = xcresult.ActionTestActivitySummary()
    
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.activityType = "test_value"
    obj2.activityType = "test_value"
    obj3.activityType = "test_value_2"
    obj1.uuid = "test_value"
    obj2.uuid = "test_value"
    obj3.uuid = "test_value_2"
    obj1.start = datetime.datetime(2020, 1, 1)
    obj2.start = datetime.datetime(2020, 1, 1)
    obj3.start = datetime.datetime(2020, 2, 1)
    obj1.finish = datetime.datetime(2020, 1, 1)
    obj2.finish = datetime.datetime(2020, 1, 1)
    obj3.finish = datetime.datetime(2020, 2, 1)
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.subactivities = None
    obj2.subactivities = None
    obj3.subactivities = None
    obj1.failureSummaryIDs = None
    obj2.failureSummaryIDs = None
    obj3.failureSummaryIDs = None
    obj1.expectedFailureIDs = None
    obj2.expectedFailureIDs = None
    obj3.expectedFailureIDs = None
    obj1.warningSummaryIDs = None
    obj2.warningSummaryIDs = None
    obj3.warningSummaryIDs = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestattachment_equality_and_hash():
    """Test ActionTestAttachment equality and hashing."""
    obj1 = xcresult.ActionTestAttachment()
    obj2 = xcresult.ActionTestAttachment()
    obj3 = xcresult.ActionTestAttachment()
    
    obj1.uniformTypeIdentifier = "test_value"
    obj2.uniformTypeIdentifier = "test_value"
    obj3.uniformTypeIdentifier = "test_value_2"
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.uuid = "test_value"
    obj2.uuid = "test_value"
    obj3.uuid = "test_value_2"
    obj1.timestamp = datetime.datetime(2020, 1, 1)
    obj2.timestamp = datetime.datetime(2020, 1, 1)
    obj3.timestamp = datetime.datetime(2020, 2, 1)
    obj1.userInfo = None
    obj2.userInfo = None
    obj3.userInfo = None
    obj1.lifetime = "test_value"
    obj2.lifetime = "test_value"
    obj3.lifetime = "test_value_2"
    obj1.inActivityIdentifier = 42
    obj2.inActivityIdentifier = 42
    obj3.inActivityIdentifier = 84
    obj1.filename = "test_value"
    obj2.filename = "test_value"
    obj3.filename = "test_value_2"
    obj1.payloadRef = None
    obj2.payloadRef = None
    obj3.payloadRef = None
    obj1.payloadSize = 42
    obj2.payloadSize = 42
    obj3.payloadSize = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestconfiguration_equality_and_hash():
    """Test ActionTestConfiguration equality and hashing."""
    obj1 = xcresult.ActionTestConfiguration()
    obj2 = xcresult.ActionTestConfiguration()
    obj3 = xcresult.ActionTestConfiguration()
    
    # Create mock SortedKeyValueArray instances
    arr1 = xcresult.SortedKeyValueArray()
    arr1.storage = []
    
    arr2 = xcresult.SortedKeyValueArray()
    arr2.storage = []
    
    arr3 = xcresult.SortedKeyValueArray()
    arr3.storage = ["different"]
    
    obj1.values = arr1
    obj2.values = arr2
    obj3.values = arr3
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_actiontestexpectedfailure_equality_and_hash():
    """Test ActionTestExpectedFailure equality and hashing."""
    obj1 = xcresult.ActionTestExpectedFailure()
    obj2 = xcresult.ActionTestExpectedFailure()
    obj3 = xcresult.ActionTestExpectedFailure()
    
    obj1.uuid = "test_value"
    obj2.uuid = "test_value"
    obj3.uuid = "test_value_2"
    obj1.failureReason = "test_value"
    obj2.failureReason = "test_value"
    obj3.failureReason = "test_value_2"
    obj1.failureSummary = None
    obj2.failureSummary = None
    obj3.failureSummary = None
    obj1.isTopLevelFailure = True
    obj2.isTopLevelFailure = True
    obj3.isTopLevelFailure = False
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestfailuresummary_equality_and_hash():
    """Test ActionTestFailureSummary equality and hashing."""
    obj1 = xcresult.ActionTestFailureSummary()
    obj2 = xcresult.ActionTestFailureSummary()
    obj3 = xcresult.ActionTestFailureSummary()
    
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.fileName = "test_value"
    obj2.fileName = "test_value"
    obj3.fileName = "test_value_2"
    obj1.lineNumber = 42
    obj2.lineNumber = 42
    obj3.lineNumber = 84
    obj1.isPerformanceFailure = True
    obj2.isPerformanceFailure = True
    obj3.isPerformanceFailure = False
    obj1.uuid = "test_value"
    obj2.uuid = "test_value"
    obj3.uuid = "test_value_2"
    obj1.issueType = "test_value"
    obj2.issueType = "test_value"
    obj3.issueType = "test_value_2"
    obj1.detailedDescription = "test_value"
    obj2.detailedDescription = "test_value"
    obj3.detailedDescription = "test_value_2"
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.associatedError = None
    obj2.associatedError = None
    obj3.associatedError = None
    obj1.sourceCodeContext = None
    obj2.sourceCodeContext = None
    obj3.sourceCodeContext = None
    obj1.timestamp = datetime.datetime(2020, 1, 1)
    obj2.timestamp = datetime.datetime(2020, 1, 1)
    obj3.timestamp = datetime.datetime(2020, 2, 1)
    obj1.isTopLevelFailure = True
    obj2.isTopLevelFailure = True
    obj3.isTopLevelFailure = False
    obj1.expression = None
    obj2.expression = None
    obj3.expression = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestissuesummary_equality_and_hash():
    """Test ActionTestIssueSummary equality and hashing."""
    obj1 = xcresult.ActionTestIssueSummary()
    obj2 = xcresult.ActionTestIssueSummary()
    obj3 = xcresult.ActionTestIssueSummary()
    
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.fileName = "test_value"
    obj2.fileName = "test_value"
    obj3.fileName = "test_value_2"
    obj1.lineNumber = 42
    obj2.lineNumber = 42
    obj3.lineNumber = 84
    obj1.uuid = "test_value"
    obj2.uuid = "test_value"
    obj3.uuid = "test_value_2"
    obj1.issueType = "test_value"
    obj2.issueType = "test_value"
    obj3.issueType = "test_value_2"
    obj1.detailedDescription = "test_value"
    obj2.detailedDescription = "test_value"
    obj3.detailedDescription = "test_value_2"
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.associatedError = None
    obj2.associatedError = None
    obj3.associatedError = None
    obj1.sourceCodeContext = None
    obj2.sourceCodeContext = None
    obj3.sourceCodeContext = None
    obj1.timestamp = datetime.datetime(2020, 1, 1)
    obj2.timestamp = datetime.datetime(2020, 1, 1)
    obj3.timestamp = datetime.datetime(2020, 2, 1)
    obj1.isTopLevel = True
    obj2.isTopLevel = True
    obj3.isTopLevel = False
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestmetadata_equality_and_hash():
    """Test ActionTestMetadata equality and hashing."""
    obj1 = xcresult.ActionTestMetadata()
    obj2 = xcresult.ActionTestMetadata()
    obj3 = xcresult.ActionTestMetadata()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.identifierURL = "test_value"
    obj2.identifierURL = "test_value"
    obj3.identifierURL = "test_value_2"
    obj1.testStatus = "test_value"
    obj2.testStatus = "test_value"
    obj3.testStatus = "test_value_2"
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.summaryRef = None
    obj2.summaryRef = None
    obj3.summaryRef = None
    obj1.performanceMetricsCount = 42
    obj2.performanceMetricsCount = 42
    obj3.performanceMetricsCount = 84
    obj1.failureSummariesCount = 42
    obj2.failureSummariesCount = 42
    obj3.failureSummariesCount = 84
    obj1.activitySummariesCount = 42
    obj2.activitySummariesCount = 42
    obj3.activitySummariesCount = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestnoticesummary_equality_and_hash():
    """Test ActionTestNoticeSummary equality and hashing."""
    obj1 = xcresult.ActionTestNoticeSummary()
    obj2 = xcresult.ActionTestNoticeSummary()
    obj3 = xcresult.ActionTestNoticeSummary()
    
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.fileName = "test_value"
    obj2.fileName = "test_value"
    obj3.fileName = "test_value_2"
    obj1.lineNumber = 42
    obj2.lineNumber = 42
    obj3.lineNumber = 84
    obj1.timestamp = datetime.datetime(2020, 1, 1)
    obj2.timestamp = datetime.datetime(2020, 1, 1)
    obj3.timestamp = datetime.datetime(2020, 2, 1)
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestperformancemetricsummary_equality_and_hash():
    """Test ActionTestPerformanceMetricSummary equality and hashing."""
    obj1 = xcresult.ActionTestPerformanceMetricSummary()
    obj2 = xcresult.ActionTestPerformanceMetricSummary()
    obj3 = xcresult.ActionTestPerformanceMetricSummary()
    
    obj1.displayName = "test_value"
    obj2.displayName = "test_value"
    obj3.displayName = "test_value_2"
    obj1.unitOfMeasurement = "test_value"
    obj2.unitOfMeasurement = "test_value"
    obj3.unitOfMeasurement = "test_value_2"
    obj1.measurements = None
    obj2.measurements = None
    obj3.measurements = None
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.baselineName = "test_value"
    obj2.baselineName = "test_value"
    obj3.baselineName = "test_value_2"
    obj1.baselineAverage = 3.14
    obj2.baselineAverage = 3.14
    obj3.baselineAverage = 6.28
    obj1.maxPercentRegression = 3.14
    obj2.maxPercentRegression = 3.14
    obj3.maxPercentRegression = 6.28
    obj1.maxPercentRelativeStandardDeviation = 3.14
    obj2.maxPercentRelativeStandardDeviation = 3.14
    obj3.maxPercentRelativeStandardDeviation = 6.28
    obj1.maxRegression = 3.14
    obj2.maxRegression = 3.14
    obj3.maxRegression = 6.28
    obj1.maxStandardDeviation = 3.14
    obj2.maxStandardDeviation = 3.14
    obj3.maxStandardDeviation = 6.28
    obj1.polarity = "test_value"
    obj2.polarity = "test_value"
    obj3.polarity = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestplanrunsummaries_equality_and_hash():
    """Test ActionTestPlanRunSummaries equality and hashing."""
    obj1 = xcresult.ActionTestPlanRunSummaries()
    obj2 = xcresult.ActionTestPlanRunSummaries()
    obj3 = xcresult.ActionTestPlanRunSummaries()
    
    obj1.summaries = []
    obj2.summaries = []
    obj3.summaries = [None]  # Different - has one element
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_actiontestplanrunsummary_equality_and_hash():
    """Test ActionTestPlanRunSummary equality and hashing."""
    obj1 = xcresult.ActionTestPlanRunSummary()
    obj2 = xcresult.ActionTestPlanRunSummary()
    obj3 = xcresult.ActionTestPlanRunSummary()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.testableSummaries = None
    obj2.testableSummaries = None
    obj3.testableSummaries = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestrepetitionpolicysummary_equality_and_hash():
    """Test ActionTestRepetitionPolicySummary equality and hashing."""
    obj1 = xcresult.ActionTestRepetitionPolicySummary()
    obj2 = xcresult.ActionTestRepetitionPolicySummary()
    obj3 = xcresult.ActionTestRepetitionPolicySummary()
    
    obj1.iteration = 42
    obj2.iteration = 42
    obj3.iteration = 84
    obj1.totalIterations = 42
    obj2.totalIterations = 42
    obj3.totalIterations = 84
    obj1.repetitionMode = "test_value"
    obj2.repetitionMode = "test_value"
    obj3.repetitionMode = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestsummary_equality_and_hash():
    """Test ActionTestSummary equality and hashing."""
    obj1 = xcresult.ActionTestSummary()
    obj2 = xcresult.ActionTestSummary()
    obj3 = xcresult.ActionTestSummary()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.identifierURL = "test_value"
    obj2.identifierURL = "test_value"
    obj3.identifierURL = "test_value_2"
    obj1.testStatus = "test_value"
    obj2.testStatus = "test_value"
    obj3.testStatus = "test_value_2"
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.performanceMetrics = None
    obj2.performanceMetrics = None
    obj3.performanceMetrics = None
    obj1.failureSummaries = None
    obj2.failureSummaries = None
    obj3.failureSummaries = None
    obj1.expectedFailures = None
    obj2.expectedFailures = None
    obj3.expectedFailures = None
    obj1.skipNoticeSummary = None
    obj2.skipNoticeSummary = None
    obj3.skipNoticeSummary = None
    obj1.activitySummaries = None
    obj2.activitySummaries = None
    obj3.activitySummaries = None
    obj1.repetitionPolicySummary = None
    obj2.repetitionPolicySummary = None
    obj3.repetitionPolicySummary = None
    obj1.arguments = None
    obj2.arguments = None
    obj3.arguments = None
    obj1.configuration = None
    obj2.configuration = None
    obj3.configuration = None
    obj1.warningSummaries = None
    obj2.warningSummaries = None
    obj3.warningSummaries = None
    obj1.summary = "test_value"
    obj2.summary = "test_value"
    obj3.summary = "test_value_2"
    obj1.documentation = None
    obj2.documentation = None
    obj3.documentation = None
    obj1.trackedIssues = None
    obj2.trackedIssues = None
    obj3.trackedIssues = None
    obj1.tags = None
    obj2.tags = None
    obj3.tags = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestsummarygroup_equality_and_hash():
    """Test ActionTestSummaryGroup equality and hashing."""
    obj1 = xcresult.ActionTestSummaryGroup()
    obj2 = xcresult.ActionTestSummaryGroup()
    obj3 = xcresult.ActionTestSummaryGroup()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.identifierURL = "test_value"
    obj2.identifierURL = "test_value"
    obj3.identifierURL = "test_value_2"
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.subtests = None
    obj2.subtests = None
    obj3.subtests = None
    obj1.failureSummaries = None
    obj2.failureSummaries = None
    obj3.failureSummaries = None
    obj1.warningSummaries = None
    obj2.warningSummaries = None
    obj3.warningSummaries = None
    obj1.expectedFailures = None
    obj2.expectedFailures = None
    obj3.expectedFailures = None
    obj1.skipNoticeSummary = None
    obj2.skipNoticeSummary = None
    obj3.skipNoticeSummary = None
    obj1.activitySummaries = None
    obj2.activitySummaries = None
    obj3.activitySummaries = None
    obj1.summary = "test_value"
    obj2.summary = "test_value"
    obj3.summary = "test_value_2"
    obj1.documentation = None
    obj2.documentation = None
    obj3.documentation = None
    obj1.trackedIssues = None
    obj2.trackedIssues = None
    obj3.trackedIssues = None
    obj1.tags = None
    obj2.tags = None
    obj3.tags = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestsummaryidentifiableobject_equality_and_hash():
    """Test ActionTestSummaryIdentifiableObject equality and hashing."""
    obj1 = xcresult.ActionTestSummaryIdentifiableObject()
    obj2 = xcresult.ActionTestSummaryIdentifiableObject()
    obj3 = xcresult.ActionTestSummaryIdentifiableObject()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.identifierURL = "test_value"
    obj2.identifierURL = "test_value"
    obj3.identifierURL = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actiontestablesummary_equality_and_hash():
    """Test ActionTestableSummary equality and hashing."""
    obj1 = xcresult.ActionTestableSummary()
    obj2 = xcresult.ActionTestableSummary()
    obj3 = xcresult.ActionTestableSummary()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.identifierURL = "test_value"
    obj2.identifierURL = "test_value"
    obj3.identifierURL = "test_value_2"
    obj1.projectRelativePath = "test_value"
    obj2.projectRelativePath = "test_value"
    obj3.projectRelativePath = "test_value_2"
    obj1.targetName = "test_value"
    obj2.targetName = "test_value"
    obj3.targetName = "test_value_2"
    obj1.testKind = "test_value"
    obj2.testKind = "test_value"
    obj3.testKind = "test_value_2"
    obj1.tests = None
    obj2.tests = None
    obj3.tests = None
    obj1.diagnosticsDirectoryName = "test_value"
    obj2.diagnosticsDirectoryName = "test_value"
    obj3.diagnosticsDirectoryName = "test_value_2"
    obj1.failureSummaries = None
    obj2.failureSummaries = None
    obj3.failureSummaries = None
    obj1.testLanguage = "test_value"
    obj2.testLanguage = "test_value"
    obj3.testLanguage = "test_value_2"
    obj1.testRegion = "test_value"
    obj2.testRegion = "test_value"
    obj3.testRegion = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionsinvocationmetadata_equality_and_hash():
    """Test ActionsInvocationMetadata equality and hashing."""
    obj1 = xcresult.ActionsInvocationMetadata()
    obj2 = xcresult.ActionsInvocationMetadata()
    obj3 = xcresult.ActionsInvocationMetadata()
    
    obj1.creatingWorkspaceFilePath = "test_value"
    obj2.creatingWorkspaceFilePath = "test_value"
    obj3.creatingWorkspaceFilePath = "test_value_2"
    obj1.uniqueIdentifier = "test_value"
    obj2.uniqueIdentifier = "test_value"
    obj3.uniqueIdentifier = "test_value_2"
    obj1.schemeIdentifier = None
    obj2.schemeIdentifier = None
    obj3.schemeIdentifier = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_actionsinvocationrecord_equality_and_hash():
    """Test ActionsInvocationRecord equality and hashing."""
    obj1 = xcresult.ActionsInvocationRecord()
    obj2 = xcresult.ActionsInvocationRecord()
    obj3 = xcresult.ActionsInvocationRecord()
    
    # Create required ResultMetrics instances
    metrics1 = xcresult.ResultMetrics()
    metrics1.analyzerWarningCount = 0
    metrics1.errorCount = 0
    metrics1.testsCount = 0
    metrics1.testsFailedCount = 0
    metrics1.testsSkippedCount = 0
    metrics1.warningCount = 0
    metrics1.totalCoveragePercentage = None
    
    metrics2 = xcresult.ResultMetrics()
    metrics2.analyzerWarningCount = 0
    metrics2.errorCount = 0
    metrics2.testsCount = 0
    metrics2.testsFailedCount = 0
    metrics2.testsSkippedCount = 0
    metrics2.warningCount = 0
    metrics2.totalCoveragePercentage = None
    
    metrics3 = xcresult.ResultMetrics()
    metrics3.analyzerWarningCount = 1  # Different
    metrics3.errorCount = 0
    metrics3.testsCount = 0
    metrics3.testsFailedCount = 0
    metrics3.testsSkippedCount = 0
    metrics3.warningCount = 0
    metrics3.totalCoveragePercentage = None
    
    # Create required ResultIssueSummaries instances
    issues1 = xcresult.ResultIssueSummaries()
    issues1.analyzerWarningSummaries = []
    issues1.errorSummaries = []
    issues1.warningSummaries = []
    issues1.testFailureSummaries = []
    issues1.testWarningSummaries = []
    
    issues2 = xcresult.ResultIssueSummaries()
    issues2.analyzerWarningSummaries = []
    issues2.errorSummaries = []
    issues2.warningSummaries = []
    issues2.testFailureSummaries = []
    issues2.testWarningSummaries = []
    
    issues3 = xcresult.ResultIssueSummaries()
    issues3.analyzerWarningSummaries = []
    issues3.errorSummaries = []
    issues3.warningSummaries = []
    issues3.testFailureSummaries = []
    issues3.testWarningSummaries = []
    
    obj1.actions = []
    obj2.actions = []
    obj3.actions = [None]
    
    obj1.metadataRef = None
    obj2.metadataRef = None
    obj3.metadataRef = None
    
    obj1.metrics = metrics1
    obj2.metrics = metrics2
    obj3.metrics = metrics3
    
    obj1.issues = issues1
    obj2.issues = issues2
    obj3.issues = issues3
    
    obj1.archive = None
    obj2.archive = None
    obj3.archive = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_activityloganalyzercontrolflowstep_equality_and_hash():
    """Test ActivityLogAnalyzerControlFlowStep equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerControlFlowStep()
    obj2 = xcresult.ActivityLogAnalyzerControlFlowStep()
    obj3 = xcresult.ActivityLogAnalyzerControlFlowStep()
    
    obj1.parentIndex = 42
    obj2.parentIndex = 42
    obj3.parentIndex = 84
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startLocation = None
    obj2.startLocation = None
    obj3.startLocation = None
    obj1.endLocation = None
    obj2.endLocation = None
    obj3.endLocation = None
    obj1.edges = None
    obj2.edges = None
    obj3.edges = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activityloganalyzercontrolflowstepedge_equality_and_hash():
    """Test ActivityLogAnalyzerControlFlowStepEdge equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerControlFlowStepEdge()
    obj2 = xcresult.ActivityLogAnalyzerControlFlowStepEdge()
    obj3 = xcresult.ActivityLogAnalyzerControlFlowStepEdge()
    
    # Create DocumentLocation instances
    loc1 = xcresult.DocumentLocation()
    loc1.url = "file:///test1.swift"
    loc1.concreteTypeName = "TestType"
    
    loc2 = xcresult.DocumentLocation()
    loc2.url = "file:///test1.swift"
    loc2.concreteTypeName = "TestType"
    
    loc3 = xcresult.DocumentLocation()
    loc3.url = "file:///test2.swift"  # Different
    loc3.concreteTypeName = "TestType"
    
    obj1.startLocation = loc1
    obj2.startLocation = loc2
    obj3.startLocation = loc3
    
    obj1.endLocation = None
    obj2.endLocation = None
    obj3.endLocation = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_activityloganalyzereventstep_equality_and_hash():
    """Test ActivityLogAnalyzerEventStep equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerEventStep()
    obj2 = xcresult.ActivityLogAnalyzerEventStep()
    obj3 = xcresult.ActivityLogAnalyzerEventStep()
    
    obj1.parentIndex = 42
    obj2.parentIndex = 42
    obj3.parentIndex = 84
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.description = "test_value"
    obj2.description = "test_value"
    obj3.description = "test_value_2"
    obj1.callDepth = 42
    obj2.callDepth = 42
    obj3.callDepth = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activityloganalyzerresultmessage_equality_and_hash():
    """Test ActivityLogAnalyzerResultMessage equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerResultMessage()
    obj2 = xcresult.ActivityLogAnalyzerResultMessage()
    obj3 = xcresult.ActivityLogAnalyzerResultMessage()
    
    obj1.type = "test_value"
    obj2.type = "test_value"
    obj3.type = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.shortTitle = "test_value"
    obj2.shortTitle = "test_value"
    obj3.shortTitle = "test_value_2"
    obj1.category = "test_value"
    obj2.category = "test_value"
    obj3.category = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.annotations = None
    obj2.annotations = None
    obj3.annotations = None
    obj1.steps = None
    obj2.steps = None
    obj3.steps = None
    obj1.resultType = "test_value"
    obj2.resultType = "test_value"
    obj3.resultType = "test_value_2"
    obj1.keyEventIndex = 42
    obj2.keyEventIndex = 42
    obj3.keyEventIndex = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activityloganalyzerstep_equality_and_hash():
    """Test ActivityLogAnalyzerStep equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerStep()
    obj2 = xcresult.ActivityLogAnalyzerStep()
    obj3 = xcresult.ActivityLogAnalyzerStep()
    
    obj1.parentIndex = 42
    obj2.parentIndex = 42
    obj3.parentIndex = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activityloganalyzerwarningmessage_equality_and_hash():
    """Test ActivityLogAnalyzerWarningMessage equality and hashing."""
    obj1 = xcresult.ActivityLogAnalyzerWarningMessage()
    obj2 = xcresult.ActivityLogAnalyzerWarningMessage()
    obj3 = xcresult.ActivityLogAnalyzerWarningMessage()
    
    obj1.type = "test_value"
    obj2.type = "test_value"
    obj3.type = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.shortTitle = "test_value"
    obj2.shortTitle = "test_value"
    obj3.shortTitle = "test_value_2"
    obj1.category = "test_value"
    obj2.category = "test_value"
    obj3.category = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.annotations = None
    obj2.annotations = None
    obj3.annotations = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogcommandinvocationsection_equality_and_hash():
    """Test ActivityLogCommandInvocationSection equality and hashing."""
    obj1 = xcresult.ActivityLogCommandInvocationSection()
    obj2 = xcresult.ActivityLogCommandInvocationSection()
    obj3 = xcresult.ActivityLogCommandInvocationSection()
    
    obj1.domainType = "test_value"
    obj2.domainType = "test_value"
    obj3.domainType = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startTime = datetime.datetime(2020, 1, 1)
    obj2.startTime = datetime.datetime(2020, 1, 1)
    obj3.startTime = datetime.datetime(2020, 2, 1)
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.result = "test_value"
    obj2.result = "test_value"
    obj3.result = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.subsections = None
    obj2.subsections = None
    obj3.subsections = None
    obj1.messages = None
    obj2.messages = None
    obj3.messages = None
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.commandDetails = "test_value"
    obj2.commandDetails = "test_value"
    obj3.commandDetails = "test_value_2"
    obj1.emittedOutput = "test_value"
    obj2.emittedOutput = "test_value"
    obj3.emittedOutput = "test_value_2"
    obj1.exitCode = 42
    obj2.exitCode = 42
    obj3.exitCode = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogmajorsection_equality_and_hash():
    """Test ActivityLogMajorSection equality and hashing."""
    obj1 = xcresult.ActivityLogMajorSection()
    obj2 = xcresult.ActivityLogMajorSection()
    obj3 = xcresult.ActivityLogMajorSection()
    
    obj1.domainType = "test_value"
    obj2.domainType = "test_value"
    obj3.domainType = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startTime = datetime.datetime(2020, 1, 1)
    obj2.startTime = datetime.datetime(2020, 1, 1)
    obj3.startTime = datetime.datetime(2020, 2, 1)
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.result = "test_value"
    obj2.result = "test_value"
    obj3.result = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.subsections = None
    obj2.subsections = None
    obj3.subsections = None
    obj1.messages = None
    obj2.messages = None
    obj3.messages = None
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.subtitle = "test_value"
    obj2.subtitle = "test_value"
    obj3.subtitle = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogmessage_equality_and_hash():
    """Test ActivityLogMessage equality and hashing."""
    obj1 = xcresult.ActivityLogMessage()
    obj2 = xcresult.ActivityLogMessage()
    obj3 = xcresult.ActivityLogMessage()
    
    obj1.type = "test_value"
    obj2.type = "test_value"
    obj3.type = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.shortTitle = "test_value"
    obj2.shortTitle = "test_value"
    obj3.shortTitle = "test_value_2"
    obj1.category = "test_value"
    obj2.category = "test_value"
    obj3.category = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.annotations = None
    obj2.annotations = None
    obj3.annotations = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogmessageannotation_equality_and_hash():
    """Test ActivityLogMessageAnnotation equality and hashing."""
    obj1 = xcresult.ActivityLogMessageAnnotation()
    obj2 = xcresult.ActivityLogMessageAnnotation()
    obj3 = xcresult.ActivityLogMessageAnnotation()
    
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogsection_equality_and_hash():
    """Test ActivityLogSection equality and hashing."""
    obj1 = xcresult.ActivityLogSection()
    obj2 = xcresult.ActivityLogSection()
    obj3 = xcresult.ActivityLogSection()
    
    obj1.domainType = "test_value"
    obj2.domainType = "test_value"
    obj3.domainType = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startTime = datetime.datetime(2020, 1, 1)
    obj2.startTime = datetime.datetime(2020, 1, 1)
    obj3.startTime = datetime.datetime(2020, 2, 1)
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.result = "test_value"
    obj2.result = "test_value"
    obj3.result = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.subsections = None
    obj2.subsections = None
    obj3.subsections = None
    obj1.messages = None
    obj2.messages = None
    obj3.messages = None
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogsectionattachment_equality_and_hash():
    """Test ActivityLogSectionAttachment equality and hashing."""
    obj1 = xcresult.ActivityLogSectionAttachment()
    obj2 = xcresult.ActivityLogSectionAttachment()
    obj3 = xcresult.ActivityLogSectionAttachment()
    
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.majorVersion = 42
    obj2.majorVersion = 42
    obj3.majorVersion = 84
    obj1.minorVersion = 42
    obj2.minorVersion = 42
    obj3.minorVersion = 84
    obj1.data = b"test_data"
    obj2.data = b"test_data"
    obj3.data = b"test_data_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogtargetbuildsection_equality_and_hash():
    """Test ActivityLogTargetBuildSection equality and hashing."""
    obj1 = xcresult.ActivityLogTargetBuildSection()
    obj2 = xcresult.ActivityLogTargetBuildSection()
    obj3 = xcresult.ActivityLogTargetBuildSection()
    
    obj1.domainType = "test_value"
    obj2.domainType = "test_value"
    obj3.domainType = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startTime = datetime.datetime(2020, 1, 1)
    obj2.startTime = datetime.datetime(2020, 1, 1)
    obj3.startTime = datetime.datetime(2020, 2, 1)
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.result = "test_value"
    obj2.result = "test_value"
    obj3.result = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.subsections = None
    obj2.subsections = None
    obj3.subsections = None
    obj1.messages = None
    obj2.messages = None
    obj3.messages = None
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.subtitle = "test_value"
    obj2.subtitle = "test_value"
    obj3.subtitle = "test_value_2"
    obj1.productType = "test_value"
    obj2.productType = "test_value"
    obj3.productType = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_activitylogunittestsection_equality_and_hash():
    """Test ActivityLogUnitTestSection equality and hashing."""
    obj1 = xcresult.ActivityLogUnitTestSection()
    obj2 = xcresult.ActivityLogUnitTestSection()
    obj3 = xcresult.ActivityLogUnitTestSection()
    
    obj1.domainType = "test_value"
    obj2.domainType = "test_value"
    obj3.domainType = "test_value_2"
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.startTime = datetime.datetime(2020, 1, 1)
    obj2.startTime = datetime.datetime(2020, 1, 1)
    obj3.startTime = datetime.datetime(2020, 2, 1)
    obj1.duration = 3.14
    obj2.duration = 3.14
    obj3.duration = 6.28
    obj1.result = "test_value"
    obj2.result = "test_value"
    obj3.result = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    obj1.subsections = None
    obj2.subsections = None
    obj3.subsections = None
    obj1.messages = None
    obj2.messages = None
    obj3.messages = None
    obj1.attachments = None
    obj2.attachments = None
    obj3.attachments = None
    obj1.testName = "test_value"
    obj2.testName = "test_value"
    obj3.testName = "test_value_2"
    obj1.suiteName = "test_value"
    obj2.suiteName = "test_value"
    obj3.suiteName = "test_value_2"
    obj1.summary = "test_value"
    obj2.summary = "test_value"
    obj3.summary = "test_value_2"
    obj1.emittedOutput = "test_value"
    obj2.emittedOutput = "test_value"
    obj3.emittedOutput = "test_value_2"
    obj1.performanceTestOutput = "test_value"
    obj2.performanceTestOutput = "test_value"
    obj3.performanceTestOutput = "test_value_2"
    obj1.testsPassedString = "test_value"
    obj2.testsPassedString = "test_value"
    obj3.testsPassedString = "test_value_2"
    obj1.wasSkipped = True
    obj2.wasSkipped = True
    obj3.wasSkipped = False
    obj1.runnablePath = "test_value"
    obj2.runnablePath = "test_value"
    obj3.runnablePath = "test_value_2"
    obj1.runnableUTI = "test_value"
    obj2.runnableUTI = "test_value"
    obj3.runnableUTI = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_archiveinfo_equality_and_hash():
    """Test ArchiveInfo equality and hashing."""
    obj1 = xcresult.ArchiveInfo()
    obj2 = xcresult.ArchiveInfo()
    obj3 = xcresult.ArchiveInfo()
    
    obj1.path = "test_value"
    obj2.path = "test_value"
    obj3.path = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_codecoverageinfo_equality_and_hash():
    """Test CodeCoverageInfo equality and hashing."""
    obj1 = xcresult.CodeCoverageInfo()
    obj2 = xcresult.CodeCoverageInfo()
    obj3 = xcresult.CodeCoverageInfo()
    
    obj1.hasCoverageData = True
    obj2.hasCoverageData = True
    obj3.hasCoverageData = False
    obj1.reportRef = None
    obj2.reportRef = None
    obj3.reportRef = None
    obj1.archiveRef = None
    obj2.archiveRef = None
    obj3.archiveRef = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_consolelogitem_equality_and_hash():
    """Test ConsoleLogItem equality and hashing."""
    obj1 = xcresult.ConsoleLogItem()
    obj2 = xcresult.ConsoleLogItem()
    obj3 = xcresult.ConsoleLogItem()
    
    obj1.adaptorType = "test_value"
    obj2.adaptorType = "test_value"
    obj3.adaptorType = "test_value_2"
    obj1.kind = "test_value"
    obj2.kind = "test_value"
    obj3.kind = "test_value_2"
    obj1.timestamp = 3.14
    obj2.timestamp = 3.14
    obj3.timestamp = 6.28
    obj1.content = "test_value"
    obj2.content = "test_value"
    obj3.content = "test_value_2"
    obj1.logData = None
    obj2.logData = None
    obj3.logData = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_consolelogitemlogdata_equality_and_hash():
    """Test ConsoleLogItemLogData equality and hashing."""
    obj1 = xcresult.ConsoleLogItemLogData()
    obj2 = xcresult.ConsoleLogItemLogData()
    obj3 = xcresult.ConsoleLogItemLogData()
    
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.subsystem = "test_value"
    obj2.subsystem = "test_value"
    obj3.subsystem = "test_value_2"
    obj1.category = "test_value"
    obj2.category = "test_value"
    obj3.category = "test_value_2"
    obj1.library = "test_value"
    obj2.library = "test_value"
    obj3.library = "test_value_2"
    obj1.format = "test_value"
    obj2.format = "test_value"
    obj3.format = "test_value_2"
    obj1.backtrace = "test_value"
    obj2.backtrace = "test_value"
    obj3.backtrace = "test_value_2"
    obj1.pid = 42
    obj2.pid = 42
    obj3.pid = 84
    obj1.processName = "test_value"
    obj2.processName = "test_value"
    obj3.processName = "test_value_2"
    obj1.sessionUUID = "test_value"
    obj2.sessionUUID = "test_value"
    obj3.sessionUUID = "test_value_2"
    obj1.tid = 42
    obj2.tid = 42
    obj3.tid = 84
    obj1.messageType = 42
    obj2.messageType = 42
    obj3.messageType = 84
    obj1.senderImagePath = "test_value"
    obj2.senderImagePath = "test_value"
    obj3.senderImagePath = "test_value_2"
    obj1.senderImageUUID = "test_value"
    obj2.senderImageUUID = "test_value"
    obj3.senderImageUUID = "test_value_2"
    obj1.senderImageOffset = 42
    obj2.senderImageOffset = 42
    obj3.senderImageOffset = 84
    obj1.unixTimeInterval = 3.14
    obj2.unixTimeInterval = 3.14
    obj3.unixTimeInterval = 6.28
    obj1.timeZone = "test_value"
    obj2.timeZone = "test_value"
    obj3.timeZone = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_consolelogsection_equality_and_hash():
    """Test ConsoleLogSection equality and hashing."""
    obj1 = xcresult.ConsoleLogSection()
    obj2 = xcresult.ConsoleLogSection()
    obj3 = xcresult.ConsoleLogSection()
    
    obj1.title = "test_value"
    obj2.title = "test_value"
    obj3.title = "test_value_2"
    obj1.items = None
    obj2.items = None
    obj3.items = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_documentlocation_equality_and_hash():
    """Test DocumentLocation equality and hashing."""
    obj1 = xcresult.DocumentLocation()
    obj2 = xcresult.DocumentLocation()
    obj3 = xcresult.DocumentLocation()
    
    obj1.url = "test_value"
    obj2.url = "test_value"
    obj3.url = "test_value_2"
    obj1.concreteTypeName = "test_value"
    obj2.concreteTypeName = "test_value"
    obj3.concreteTypeName = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_entityidentifier_equality_and_hash():
    """Test EntityIdentifier equality and hashing."""
    obj1 = xcresult.EntityIdentifier()
    obj2 = xcresult.EntityIdentifier()
    obj3 = xcresult.EntityIdentifier()
    
    obj1.entityName = "test_value"
    obj2.entityName = "test_value"
    obj3.entityName = "test_value_2"
    obj1.containerName = "test_value"
    obj2.containerName = "test_value"
    obj3.containerName = "test_value_2"
    obj1.entityType = "test_value"
    obj2.entityType = "test_value"
    obj3.entityType = "test_value_2"
    obj1.sharedState = "test_value"
    obj2.sharedState = "test_value"
    obj3.sharedState = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_issuesummary_equality_and_hash():
    """Test IssueSummary equality and hashing."""
    obj1 = xcresult.IssueSummary()
    obj2 = xcresult.IssueSummary()
    obj3 = xcresult.IssueSummary()
    
    obj1.issueType = "test_value"
    obj2.issueType = "test_value"
    obj3.issueType = "test_value_2"
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.compactMessage = "test_value"
    obj2.compactMessage = "test_value"
    obj3.compactMessage = "test_value_2"
    obj1.producingTarget = "test_value"
    obj2.producingTarget = "test_value"
    obj3.producingTarget = "test_value_2"
    obj1.documentLocationInCreatingWorkspace = None
    obj2.documentLocationInCreatingWorkspace = None
    obj3.documentLocationInCreatingWorkspace = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_issuetrackingmetadata_equality_and_hash():
    """Test IssueTrackingMetadata equality and hashing."""
    obj1 = xcresult.IssueTrackingMetadata()
    obj2 = xcresult.IssueTrackingMetadata()
    obj3 = xcresult.IssueTrackingMetadata()
    
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.url = "test_value"
    obj2.url = "test_value"
    obj3.url = "test_value_2"
    obj1.comment = "test_value"
    obj2.comment = "test_value"
    obj3.comment = "test_value_2"
    obj1.summary = "test_value"
    obj2.summary = "test_value"
    obj3.summary = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_objectid_equality_and_hash():
    """Test ObjectID equality and hashing."""
    obj1 = xcresult.ObjectID()
    obj2 = xcresult.ObjectID()
    obj3 = xcresult.ObjectID()
    
    obj1.hash = "test_value"
    obj2.hash = "test_value"
    obj3.hash = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_reference_equality_and_hash():
    """Test Reference equality and hashing."""
    obj1 = xcresult.Reference()
    obj2 = xcresult.Reference()
    obj3 = xcresult.Reference()
    
    obj1.id = "test_value"
    obj2.id = "test_value"
    obj3.id = "test_value_2"
    obj1.targetType = None
    obj2.targetType = None
    obj3.targetType = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_resultissuesummaries_equality_and_hash():
    """Test ResultIssueSummaries equality and hashing."""
    obj1 = xcresult.ResultIssueSummaries()
    obj2 = xcresult.ResultIssueSummaries()
    obj3 = xcresult.ResultIssueSummaries()
    
    obj1.analyzerWarningSummaries = []
    obj2.analyzerWarningSummaries = []
    obj3.analyzerWarningSummaries = [None]
    
    for obj in [obj1, obj2, obj3]:
        obj.errorSummaries = []
        obj.warningSummaries = []
        obj.testFailureSummaries = []
        obj.testWarningSummaries = []
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_resultmetrics_equality_and_hash():
    """Test ResultMetrics equality and hashing."""
    obj1 = xcresult.ResultMetrics()
    obj2 = xcresult.ResultMetrics()
    obj3 = xcresult.ResultMetrics()
    
    obj1.analyzerWarningCount = 42
    obj2.analyzerWarningCount = 42
    obj3.analyzerWarningCount = 84
    obj1.errorCount = 42
    obj2.errorCount = 42
    obj3.errorCount = 84
    obj1.testsCount = 42
    obj2.testsCount = 42
    obj3.testsCount = 84
    obj1.testsFailedCount = 42
    obj2.testsFailedCount = 42
    obj3.testsFailedCount = 84
    obj1.testsSkippedCount = 42
    obj2.testsSkippedCount = 42
    obj3.testsSkippedCount = 84
    obj1.warningCount = 42
    obj2.warningCount = 42
    obj3.warningCount = 84
    obj1.totalCoveragePercentage = 3.14
    obj2.totalCoveragePercentage = 3.14
    obj3.totalCoveragePercentage = 6.28
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_sortedkeyvaluearray_equality_and_hash():
    """Test SortedKeyValueArray equality and hashing."""
    obj1 = xcresult.SortedKeyValueArray()
    obj2 = xcresult.SortedKeyValueArray()
    obj3 = xcresult.SortedKeyValueArray()
    
    obj1.storage = []
    obj2.storage = []
    obj3.storage = [None]
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_sortedkeyvaluearraypair_equality_and_hash():
    """Test SortedKeyValueArrayPair equality and hashing."""
    obj1 = xcresult.SortedKeyValueArrayPair()
    obj2 = xcresult.SortedKeyValueArrayPair()
    obj3 = xcresult.SortedKeyValueArrayPair()
    
    obj1.key = "test_value"
    obj2.key = "test_value"
    obj3.key = "test_value_2"
    obj1.value = "test_any"
    obj2.value = "test_any"
    obj3.value = "test_any_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_sourcecodecontext_equality_and_hash():
    """Test SourceCodeContext equality and hashing."""
    obj1 = xcresult.SourceCodeContext()
    obj2 = xcresult.SourceCodeContext()
    obj3 = xcresult.SourceCodeContext()
    
    obj1.location = None
    obj2.location = None
    obj3.location = None
    
    obj1.callStack = []
    obj2.callStack = []
    obj3.callStack = [None]
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3

def test_sourcecodeframe_equality_and_hash():
    """Test SourceCodeFrame equality and hashing."""
    obj1 = xcresult.SourceCodeFrame()
    obj2 = xcresult.SourceCodeFrame()
    obj3 = xcresult.SourceCodeFrame()
    
    obj1.addressString = "test_value"
    obj2.addressString = "test_value"
    obj3.addressString = "test_value_2"
    obj1.symbolInfo = None
    obj2.symbolInfo = None
    obj3.symbolInfo = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_sourcecodelocation_equality_and_hash():
    """Test SourceCodeLocation equality and hashing."""
    obj1 = xcresult.SourceCodeLocation()
    obj2 = xcresult.SourceCodeLocation()
    obj3 = xcresult.SourceCodeLocation()
    
    obj1.filePath = "test_value"
    obj2.filePath = "test_value"
    obj3.filePath = "test_value_2"
    obj1.lineNumber = 42
    obj2.lineNumber = 42
    obj3.lineNumber = 84
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_sourcecodesymbolinfo_equality_and_hash():
    """Test SourceCodeSymbolInfo equality and hashing."""
    obj1 = xcresult.SourceCodeSymbolInfo()
    obj2 = xcresult.SourceCodeSymbolInfo()
    obj3 = xcresult.SourceCodeSymbolInfo()
    
    obj1.imageName = "test_value"
    obj2.imageName = "test_value"
    obj3.imageName = "test_value_2"
    obj1.symbolName = "test_value"
    obj2.symbolName = "test_value"
    obj3.symbolName = "test_value_2"
    obj1.location = None
    obj2.location = None
    obj3.location = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testargument_equality_and_hash():
    """Test TestArgument equality and hashing."""
    obj1 = xcresult.TestArgument()
    obj2 = xcresult.TestArgument()
    obj3 = xcresult.TestArgument()
    
    obj1.parameter = None
    obj2.parameter = None
    obj3.parameter = None
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.description = "test_value"
    obj2.description = "test_value"
    obj3.description = "test_value_2"
    obj1.debugDescription = "test_value"
    obj2.debugDescription = "test_value"
    obj3.debugDescription = "test_value_2"
    obj1.typeName = "test_value"
    obj2.typeName = "test_value"
    obj3.typeName = "test_value_2"
    obj1.value = None
    obj2.value = None
    obj3.value = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testassociatederror_equality_and_hash():
    """Test TestAssociatedError equality and hashing."""
    obj1 = xcresult.TestAssociatedError()
    obj2 = xcresult.TestAssociatedError()
    obj3 = xcresult.TestAssociatedError()
    
    obj1.domain = "test_value"
    obj2.domain = "test_value"
    obj3.domain = "test_value_2"
    obj1.code = 42
    obj2.code = 42
    obj3.code = 84
    obj1.userInfo = None
    obj2.userInfo = None
    obj3.userInfo = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testdocumentation_equality_and_hash():
    """Test TestDocumentation equality and hashing."""
    obj1 = xcresult.TestDocumentation()
    obj2 = xcresult.TestDocumentation()
    obj3 = xcresult.TestDocumentation()
    
    obj1.content = "test_value"
    obj2.content = "test_value"
    obj3.content = "test_value_2"
    obj1.format = "test_value"
    obj2.format = "test_value"
    obj3.format = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testexpression_equality_and_hash():
    """Test TestExpression equality and hashing."""
    obj1 = xcresult.TestExpression()
    obj2 = xcresult.TestExpression()
    obj3 = xcresult.TestExpression()
    
    obj1.sourceCode = "test_value"
    obj2.sourceCode = "test_value"
    obj3.sourceCode = "test_value_2"
    obj1.value = None
    obj2.value = None
    obj3.value = None
    obj1.subexpressions = None
    obj2.subexpressions = None
    obj3.subexpressions = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testfailureissuesummary_equality_and_hash():
    """Test TestFailureIssueSummary equality and hashing."""
    obj1 = xcresult.TestFailureIssueSummary()
    obj2 = xcresult.TestFailureIssueSummary()
    obj3 = xcresult.TestFailureIssueSummary()
    
    obj1.issueType = "test_value"
    obj2.issueType = "test_value"
    obj3.issueType = "test_value_2"
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.compactMessage = "test_value"
    obj2.compactMessage = "test_value"
    obj3.compactMessage = "test_value_2"
    obj1.producingTarget = "test_value"
    obj2.producingTarget = "test_value"
    obj3.producingTarget = "test_value_2"
    obj1.documentLocationInCreatingWorkspace = None
    obj2.documentLocationInCreatingWorkspace = None
    obj3.documentLocationInCreatingWorkspace = None
    obj1.testCaseName = "test_value"
    obj2.testCaseName = "test_value"
    obj3.testCaseName = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testissuesummary_equality_and_hash():
    """Test TestIssueSummary equality and hashing."""
    obj1 = xcresult.TestIssueSummary()
    obj2 = xcresult.TestIssueSummary()
    obj3 = xcresult.TestIssueSummary()
    
    obj1.issueType = "test_value"
    obj2.issueType = "test_value"
    obj3.issueType = "test_value_2"
    obj1.message = "test_value"
    obj2.message = "test_value"
    obj3.message = "test_value_2"
    obj1.compactMessage = "test_value"
    obj2.compactMessage = "test_value"
    obj3.compactMessage = "test_value_2"
    obj1.producingTarget = "test_value"
    obj2.producingTarget = "test_value"
    obj3.producingTarget = "test_value_2"
    obj1.documentLocationInCreatingWorkspace = None
    obj2.documentLocationInCreatingWorkspace = None
    obj3.documentLocationInCreatingWorkspace = None
    obj1.testCaseName = "test_value"
    obj2.testCaseName = "test_value"
    obj3.testCaseName = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testparameter_equality_and_hash():
    """Test TestParameter equality and hashing."""
    obj1 = xcresult.TestParameter()
    obj2 = xcresult.TestParameter()
    obj3 = xcresult.TestParameter()
    
    obj1.label = "test_value"
    obj2.label = "test_value"
    obj3.label = "test_value_2"
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.typeName = "test_value"
    obj2.typeName = "test_value"
    obj3.typeName = "test_value_2"
    obj1.fullyQualifiedTypeName = "test_value"
    obj2.fullyQualifiedTypeName = "test_value"
    obj3.fullyQualifiedTypeName = "test_value_2"
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testtag_equality_and_hash():
    """Test TestTag equality and hashing."""
    obj1 = xcresult.TestTag()
    obj2 = xcresult.TestTag()
    obj3 = xcresult.TestTag()
    
    obj1.identifier = "test_value"
    obj2.identifier = "test_value"
    obj3.identifier = "test_value_2"
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.anchors = None
    obj2.anchors = None
    obj3.anchors = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_testvalue_equality_and_hash():
    """Test TestValue equality and hashing."""
    obj1 = xcresult.TestValue()
    obj2 = xcresult.TestValue()
    obj3 = xcresult.TestValue()
    
    obj1.description = "test_value"
    obj2.description = "test_value"
    obj3.description = "test_value_2"
    obj1.debugDescription = "test_value"
    obj2.debugDescription = "test_value"
    obj3.debugDescription = "test_value_2"
    obj1.typeName = "test_value"
    obj2.typeName = "test_value"
    obj3.typeName = "test_value_2"
    obj1.fullyQualifiedTypeName = "test_value"
    obj2.fullyQualifiedTypeName = "test_value"
    obj3.fullyQualifiedTypeName = "test_value_2"
    obj1.label = "test_value"
    obj2.label = "test_value"
    obj3.label = "test_value_2"
    obj1.isCollection = True
    obj2.isCollection = True
    obj3.isCollection = False
    obj1.children = None
    obj2.children = None
    obj3.children = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3


def test_typedefinition_equality_and_hash():
    """Test TypeDefinition equality and hashing."""
    obj1 = xcresult.TypeDefinition()
    obj2 = xcresult.TypeDefinition()
    obj3 = xcresult.TypeDefinition()
    
    obj1.name = "test_value"
    obj2.name = "test_value"
    obj3.name = "test_value_2"
    obj1.supertype = None
    obj2.supertype = None
    obj3.supertype = None
    
    # Test equality
    assert obj1 == obj2
    
    # Test hashing
    assert hash(obj1) == hash(obj2)
    
    # Test _members
    assert obj1._members() == obj2._members()
    
    # Test inequality
    assert obj1 != obj3




# Additional tests for type inequality to cover __eq__ return False branches
def test_all_classes_type_inequality():
    """Test that all model classes return False when compared with different types."""
    classes_to_test = [
        "ActivityLogAnalyzerStep", "ActivityLogSectionAttachment", "EntityIdentifier",
        "ObjectID", "SortedKeyValueArrayPair", "TestDocumentation",
        "ActionAbstractTestSummary", "ActionDeviceRecord", "ActionTestNoticeSummary",
        "ActionTestPerformanceMetricSummary", "ActionTestRepetitionPolicySummary",
        "ActionsInvocationMetadata", "ActivityLogAnalyzerControlFlowStepEdge",
        "ActivityLogAnalyzerEventStep", "ActivityLogMessageAnnotation", "ArchiveInfo",
        "ConsoleLogItemLogData", "IssueSummary", "IssueTrackingMetadata", "Reference",
        "ResultMetrics", "SortedKeyValueArray", "SourceCodeLocation", "TestParameter",
        "TestTag", "TestValue", "ActionRunDestinationRecord", "ActionTestAttachment",
        "ActionTestConfiguration", "ActionTestSummaryIdentifiableObject",
        "ActivityLogAnalyzerControlFlowStep", "ActivityLogMessage", "CodeCoverageInfo",
        "ConsoleLogItem", "SourceCodeSymbolInfo", "TestArgument", "TestAssociatedError",
        "TestExpression", "TestFailureIssueSummary", "TestIssueSummary",
        "ActionTestActivitySummary", "ActionTestMetadata", "ActivityLogAnalyzerResultMessage",
        "ActivityLogAnalyzerWarningMessage", "ActivityLogSection", "ConsoleLogSection",
        "ResultIssueSummaries", "SourceCodeFrame", "ActionResult",
        "ActivityLogCommandInvocationSection", "ActivityLogMajorSection",
        "ActivityLogUnitTestSection", "SourceCodeContext", "ActionRecord",
        "ActionTestFailureSummary", "ActionTestIssueSummary",
        "ActivityLogTargetBuildSection", "ActionTestExpectedFailure",
        "ActionTestableSummary", "ActionsInvocationRecord", "ActionTestPlanRunSummary",
        "ActionTestSummary", "ActionTestSummaryGroup", "ActionTestPlanRunSummaries",
        "ActionPlatformRecord", "ActionSDKRecord", "TypeDefinition", "DocumentLocation"
    ]
    
    for class_name in classes_to_test:
        cls = getattr(xcresult, class_name)
        obj = cls()
        
        # Test inequality with different types
        assert obj != "string"
        assert obj != 123
        assert obj != None
        assert obj != []
        assert obj != {}


def test_xchash_members_call_none():
    """Test xchash when members_call is None (line 38)."""
    from xcresult.model import xchash
    
    # Create an object with _members attribute but it's None
    class TestObj:
        _members = None
    
    obj = TestObj()
    result = xchash(obj)
    assert isinstance(result, int)


def test_issuesummary_pretty_message_no_location():
    """Test IssueSummary pretty_message with no document location (lines 1056-1057)."""
    issue = xcresult.IssueSummary()
    issue.issueType = "Error"
    issue.message = "Test error message"
    issue.compactMessage = None
    issue.producingTarget = None
    issue.documentLocationInCreatingWorkspace = None
    
    result = issue.pretty_message(None)
    assert result == "* [ERROR] Test error message"


def test_issuesummary_pretty_message_with_location():
    """Test IssueSummary pretty_message with document location (lines 1059-1064)."""
    issue = xcresult.IssueSummary()
    issue.issueType = "Error"
    issue.message = "Test error message"
    issue.compactMessage = None
    issue.producingTarget = None
    
    location = xcresult.DocumentLocation()
    location.url = "file:///path/to/file.swift#StartingLineNumber=10&StartingColumnNumber=5"
    location.concreteTypeName = "TestType"
    issue.documentLocationInCreatingWorkspace = location
    
    result = issue.pretty_message(None)
    assert "Test error message" in result
    assert "/path/to/file.swift" in result
    assert ":11:" in result  # Line number +1
    assert ":6" in result  # Column number +1


def test_issuesummary_pretty_message_with_path_prefix():
    """Test IssueSummary pretty_message with path prefix removal (lines 1061-1062)."""
    issue = xcresult.IssueSummary()
    issue.issueType = "Error"
    issue.message = "Test error message"
    issue.compactMessage = None
    issue.producingTarget = None
    
    location = xcresult.DocumentLocation()
    location.url = "file:///project/src/file.swift#StartingLineNumber=10"
    location.concreteTypeName = "TestType"
    issue.documentLocationInCreatingWorkspace = location
    
    result = issue.pretty_message("/project/")
    assert "src/file.swift" in result
    assert "/project/" not in result


def test_testfailureissuesummary_pretty_message_no_location():
    """Test TestFailureIssueSummary pretty_message with no location (lines 1873-1881)."""
    issue = xcresult.TestFailureIssueSummary()
    issue.issueType = "TestFailure"
    issue.message = "Test failed"
    issue.compactMessage = None
    issue.producingTarget = "MyTarget"
    issue.documentLocationInCreatingWorkspace = None
    issue.testCaseName = "testExample"
    
    result = issue.pretty_message(None)
    assert result == "* [MyTarget] testExample -> Test failed"


def test_testfailureissuesummary_pretty_message_with_location():
    """Test TestFailureIssueSummary pretty_message with location (lines 1873, 1883-1891)."""
    issue = xcresult.TestFailureIssueSummary()
    issue.issueType = "TestFailure"
    issue.message = "Test failed"
    issue.compactMessage = None
    issue.producingTarget = "MyTarget"
    issue.testCaseName = "testExample"
    
    location = xcresult.DocumentLocation()
    location.url = "file:///path/to/test.swift#StartingLineNumber=20"
    location.concreteTypeName = "TestType"
    issue.documentLocationInCreatingWorkspace = location
    
    result = issue.pretty_message(None)
    assert "* [MyTarget] testExample -> Test failed" in result
    assert "/path/to/test.swift" in result
    assert ":21:" in result


def test_testfailureissuesummary_pretty_message_with_path_prefix():
    """Test TestFailureIssueSummary pretty_message with path prefix (lines 1885-1886)."""
    issue = xcresult.TestFailureIssueSummary()
    issue.issueType = "TestFailure"
    issue.message = "Test failed"
    issue.compactMessage = None
    issue.producingTarget = "MyTarget"
    issue.testCaseName = "testExample"
    
    location = xcresult.DocumentLocation()
    location.url = "file:///project/tests/test.swift#StartingLineNumber=20"
    location.concreteTypeName = "TestType"
    issue.documentLocationInCreatingWorkspace = location
    
    result = issue.pretty_message("/project/")
    assert "tests/test.swift" in result
    assert "/project/" not in result


def test_actiontestablesummary_all_tests_empty():
    """Test ActionTestableSummary all_tests when tests is None/empty (line 2751)."""
    summary = xcresult.ActionTestableSummary()
    summary.name = None
    summary.projectRelativePath = None
    summary.targetName = None
    summary.tests = None
    
    result = summary.all_tests()
    assert result == []
    
    summary.tests = []
    result = summary.all_tests()
    assert result == []
