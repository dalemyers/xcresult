"""Autogenerated models for xcresulttool."""

import datetime
import sys
from typing import Any, List, Optional


class XcresultObject:
    """Generated from xcresulttool format description."""


class ActionPlatformRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionPlatformRecord
      * Kind: object
      * Properties:
        + identifier: String
        + userDescription: String
    """

    identifier: str
    userDescription: str


class ActionSDKRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionSDKRecord
      * Kind: object
      * Properties:
        + name: String
        + identifier: String
        + operatingSystemVersion: String
        + isInternal: Bool
    """

    name: str
    identifier: str
    operatingSystemVersion: str
    isInternal: bool


class ActivityLogAnalyzerStep(XcresultObject):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerStep
      * Kind: object
      * Properties:
        + parentIndex: Int
    """

    parentIndex: int


# Defined Type: Array


# Defined Type: Bool


# Defined Type: Date


class DocumentLocation(XcresultObject):
    """Generated from xcresulttool format description.

    - DocumentLocation
      * Kind: object
      * Properties:
        + url: String
        + concreteTypeName: String
    """

    url: str
    concreteTypeName: str

    @staticmethod
    def empty() -> "DocumentLocation":
        """Create a new "empty" instance

        :returns: A new instance
        """
        instance = DocumentLocation.__new__(DocumentLocation)
        instance.concreteTypeName = ""
        instance.url = "file://#CharacterRangeLen=0&EndingColumnNumber=0&EndingLineNumber=0&StartingColumnNumber=0&StartingLineNumber=0"
        return instance

    @property
    def path(self) -> str:
        return self.url.split("#")[0].replace("file://", "")

    @property
    def location(self) -> str:
        return self.url.split("#")[1]

    @property
    def location_details(self) -> str:
        return urllib.parse.parse_qs(self.location)

    def _get_property(self, key: str, *, offset: int = 0) -> Optional[int]:
        """Get a property from the location details.

        :param key: The key for the property
        :param offset: Any offset to apply to the value (if found)

        :returns: The property as an int value if found, None otherwise
        """
        value = self.location_details.get(key)
        if value is None:
            return None
        return int(value[0]) + offset

    @property
    def character_range_length(self) -> int:
        return int(self.location_details["CharacterRangeLen"][0]) + 1

    @property
    def character_range_location(self) -> Optional[int]:
        return self._get_property("CharacterRangeLoc")

    @property
    def ending_column_number(self) -> Optional[int]:
        return self._get_property("EndingColumnNumber", offset=1)

    @property
    def ending_line_number(self) -> Optional[int]:
        return self._get_property("EndingLineNumber", offset=1)

    @property
    def location_encoding(self) -> Optional[int]:
        return self._get_property("LocationEncoding")

    @property
    def starting_column_number(self) -> Optional[int]:
        return self._get_property("StartingColumnNumber", offset=1)

    @property
    def starting_line_number(self) -> Optional[int]:
        return self._get_property("StartingLineNumber", offset=1)


# Defined Type: Double


class EntityIdentifier(XcresultObject):
    """Generated from xcresulttool format description.

    - EntityIdentifier
      * Kind: object
      * Properties:
        + entityName: String
        + containerName: String
        + entityType: String
        + sharedState: String
    """

    entityName: str
    containerName: str
    entityType: str
    sharedState: str


# Defined Type: Int


class ObjectID(XcresultObject):
    """Generated from xcresulttool format description.

    - ObjectID
      * Kind: object
      * Properties:
        + hash: String
    """

    hash: str


class ResultMetrics(XcresultObject):
    """Generated from xcresulttool format description.

    - ResultMetrics
      * Kind: object
      * Properties:
        + analyzerWarningCount: Int
        + errorCount: Int
        + testsCount: Int
        + testsFailedCount: Int
        + testsSkippedCount: Int
        + warningCount: Int
    """

    analyzerWarningCount: int
    errorCount: int
    testsCount: int
    testsFailedCount: int
    testsSkippedCount: int
    warningCount: int


class SortedKeyValueArrayPair(XcresultObject):
    """Generated from xcresulttool format description.

    - SortedKeyValueArrayPair
      * Kind: object
      * Properties:
        + key: String
        + value: SchemaSerializable
    """

    key: str
    value: Any


# Defined Type: String


class TypeDefinition(XcresultObject):
    """Generated from xcresulttool format description.

    - TypeDefinition
      * Kind: object
      * Properties:
        + name: String
        + supertype: TypeDefinition?
    """

    name: str
    supertype: Optional["TypeDefinition"]


class ActionAbstractTestSummary(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionAbstractTestSummary
      * Kind: object
      * Properties:
        + name: String?
    """

    name: Optional[str]


class ActionDeviceRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionDeviceRecord
      * Kind: object
      * Properties:
        + name: String
        + isConcreteDevice: Bool
        + operatingSystemVersion: String
        + operatingSystemVersionWithBuildNumber: String
        + nativeArchitecture: String
        + modelName: String
        + modelCode: String
        + modelUTI: String
        + identifier: String
        + isWireless: Bool
        + cpuKind: String
        + cpuCount: Int?
        + cpuSpeedInMHz: Int?
        + busSpeedInMHz: Int?
        + ramSizeInMegabytes: Int?
        + physicalCPUCoresPerPackage: Int?
        + logicalCPUCoresPerPackage: Int?
        + platformRecord: ActionPlatformRecord
    """

    name: str
    isConcreteDevice: bool
    operatingSystemVersion: str
    operatingSystemVersionWithBuildNumber: str
    nativeArchitecture: str
    modelName: str
    modelCode: str
    modelUTI: str
    identifier: str
    isWireless: bool
    cpuKind: str
    cpuCount: Optional[int]
    cpuSpeedInMHz: Optional[int]
    busSpeedInMHz: Optional[int]
    ramSizeInMegabytes: Optional[int]
    physicalCPUCoresPerPackage: Optional[int]
    logicalCPUCoresPerPackage: Optional[int]
    platformRecord: ActionPlatformRecord


class ActionTestNoticeSummary(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestNoticeSummary
      * Kind: object
      * Properties:
        + message: String?
        + fileName: String
        + lineNumber: Int
    """

    message: Optional[str]
    fileName: str
    lineNumber: int


class ActionTestPerformanceMetricSummary(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestPerformanceMetricSummary
      * Kind: object
      * Properties:
        + displayName: String
        + unitOfMeasurement: String
        + measurements: [Double]
        + identifier: String?
        + baselineName: String?
        + baselineAverage: Double?
        + maxPercentRegression: Double?
        + maxPercentRelativeStandardDeviation: Double?
        + maxRegression: Double?
        + maxStandardDeviation: Double?
    """

    displayName: str
    unitOfMeasurement: str
    measurements: List[float]
    identifier: Optional[str]
    baselineName: Optional[str]
    baselineAverage: Optional[float]
    maxPercentRegression: Optional[float]
    maxPercentRelativeStandardDeviation: Optional[float]
    maxRegression: Optional[float]
    maxStandardDeviation: Optional[float]


class ActionsInvocationMetadata(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionsInvocationMetadata
      * Kind: object
      * Properties:
        + creatingWorkspaceFilePath: String
        + uniqueIdentifier: String
        + schemeIdentifier: EntityIdentifier?
    """

    creatingWorkspaceFilePath: str
    uniqueIdentifier: str
    schemeIdentifier: Optional[EntityIdentifier]


class ActivityLogAnalyzerControlFlowStepEdge(XcresultObject):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerControlFlowStepEdge
      * Kind: object
      * Properties:
        + startLocation: DocumentLocation?
        + endLocation: DocumentLocation?
    """

    startLocation: Optional[DocumentLocation]
    endLocation: Optional[DocumentLocation]


class ActivityLogAnalyzerEventStep(ActivityLogAnalyzerStep):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerEventStep
      * Supertype: ActivityLogAnalyzerStep
      * Kind: object
      * Properties:
        + title: String
        + location: DocumentLocation?
        + description: String
        + callDepth: Int
    """

    title: str
    location: Optional[DocumentLocation]
    description: str
    callDepth: int


class ActivityLogMessageAnnotation(XcresultObject):
    """Generated from xcresulttool format description.

    - ActivityLogMessageAnnotation
      * Kind: object
      * Properties:
        + title: String
        + location: DocumentLocation?
    """

    title: str
    location: Optional[DocumentLocation]


class ArchiveInfo(XcresultObject):
    """Generated from xcresulttool format description.

    - ArchiveInfo
      * Kind: object
      * Properties:
        + path: String?
    """

    path: Optional[str]


class IssueSummary(XcresultObject):
    """Generated from xcresulttool format description.

    - IssueSummary
      * Kind: object
      * Properties:
        + issueType: String
        + message: String
        + producingTarget: String?
        + documentLocationInCreatingWorkspace: DocumentLocation?
    """

    issueType: str
    message: str
    producingTarget: Optional[str]
    documentLocationInCreatingWorkspace: Optional[DocumentLocation]

    def pretty_message(self, path_prefix: Optional[str]) -> str:
        """Format the message nicely for review.

        :param path_prefix: Any path prefix to remove

        :returns: A pretty message
        """
        if self.documentLocationInCreatingWorkspace is None:
            return f"* [{self.level.value.upper()}] " + self.message

        relative_path = self.documentLocationInCreatingWorkspace.path

        if path_prefix:
            relative_path = relative_path.replace(path_prefix, "")

        return f"* [ERROR] {self.message}\n  Found in {relative_path}:{self.documentLocationInCreatingWorkspace.starting_line_number}:{self.documentLocationInCreatingWorkspace.starting_column_number}"


class Reference(XcresultObject):
    """Generated from xcresulttool format description.

    - Reference
      * Kind: object
      * Properties:
        + id: String
        + targetType: TypeDefinition?
    """

    id: str
    targetType: Optional[TypeDefinition]


class SortedKeyValueArray(XcresultObject):
    """Generated from xcresulttool format description.

    - SortedKeyValueArray
      * Kind: object
      * Properties:
        + storage: [SortedKeyValueArrayPair]
    """

    storage: List[SortedKeyValueArrayPair]


class SourceCodeLocation(XcresultObject):
    """Generated from xcresulttool format description.

    - SourceCodeLocation
      * Kind: object
      * Properties:
        + filePath: String?
        + lineNumber: Int?
    """

    filePath: Optional[str]
    lineNumber: Optional[int]


class ActionRunDestinationRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionRunDestinationRecord
      * Kind: object
      * Properties:
        + displayName: String
        + targetArchitecture: String
        + targetDeviceRecord: ActionDeviceRecord
        + localComputerRecord: ActionDeviceRecord
        + targetSDKRecord: ActionSDKRecord
    """

    displayName: str
    targetArchitecture: str
    targetDeviceRecord: ActionDeviceRecord
    localComputerRecord: ActionDeviceRecord
    targetSDKRecord: ActionSDKRecord


class ActionTestAttachment(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestAttachment
      * Kind: object
      * Properties:
        + uniformTypeIdentifier: String
        + name: String?
        + timestamp: Date?
        + userInfo: SortedKeyValueArray?
        + lifetime: String
        + inActivityIdentifier: Int
        + filename: String?
        + payloadRef: Reference?
        + payloadSize: Int
    """

    uniformTypeIdentifier: str
    name: Optional[str]
    timestamp: Optional[datetime.datetime]
    userInfo: Optional[SortedKeyValueArray]
    lifetime: str
    inActivityIdentifier: int
    filename: Optional[str]
    payloadRef: Optional[Reference]
    payloadSize: int


class ActionTestSummaryIdentifiableObject(ActionAbstractTestSummary):
    """Generated from xcresulttool format description.

    - ActionTestSummaryIdentifiableObject
      * Supertype: ActionAbstractTestSummary
      * Kind: object
      * Properties:
        + identifier: String?
    """

    identifier: Optional[str]


class ActivityLogAnalyzerControlFlowStep(ActivityLogAnalyzerStep):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerControlFlowStep
      * Supertype: ActivityLogAnalyzerStep
      * Kind: object
      * Properties:
        + title: String
        + startLocation: DocumentLocation?
        + endLocation: DocumentLocation?
        + edges: [ActivityLogAnalyzerControlFlowStepEdge]
    """

    title: str
    startLocation: Optional[DocumentLocation]
    endLocation: Optional[DocumentLocation]
    edges: List[ActivityLogAnalyzerControlFlowStepEdge]


class ActivityLogMessage(XcresultObject):
    """Generated from xcresulttool format description.

    - ActivityLogMessage
      * Kind: object
      * Properties:
        + type: String
        + title: String
        + shortTitle: String?
        + category: String?
        + location: DocumentLocation?
        + annotations: [ActivityLogMessageAnnotation]
    """

    type: str
    title: str
    shortTitle: Optional[str]
    category: Optional[str]
    location: Optional[DocumentLocation]
    annotations: List[ActivityLogMessageAnnotation]


class CodeCoverageInfo(XcresultObject):
    """Generated from xcresulttool format description.

    - CodeCoverageInfo
      * Kind: object
      * Properties:
        + hasCoverageData: Bool
        + reportRef: Reference?
        + archiveRef: Reference?
    """

    hasCoverageData: bool
    reportRef: Optional[Reference]
    archiveRef: Optional[Reference]


class SourceCodeSymbolInfo(XcresultObject):
    """Generated from xcresulttool format description.

    - SourceCodeSymbolInfo
      * Kind: object
      * Properties:
        + imageName: String?
        + symbolName: String?
        + location: SourceCodeLocation?
    """

    imageName: Optional[str]
    symbolName: Optional[str]
    location: Optional[SourceCodeLocation]


class TestAssociatedError(XcresultObject):
    """Generated from xcresulttool format description.

    - TestAssociatedError
      * Kind: object
      * Properties:
        + domain: String?
        + code: Int?
        + userInfo: SortedKeyValueArray?
    """

    domain: Optional[str]
    code: Optional[int]
    userInfo: Optional[SortedKeyValueArray]


class TestFailureIssueSummary(IssueSummary):
    """Generated from xcresulttool format description.

    - TestFailureIssueSummary
      * Supertype: IssueSummary
      * Kind: object
      * Properties:
        + testCaseName: String
    """

    testCaseName: str

    def pretty_message(self, path_prefix: Optional[str]) -> str:
        """Format the message nicely for review.

        :param path_prefix: Any path prefix to remove

        :returns: A pretty message
        """
        output = f"* [{self.producingTarget}] {self.testCaseName} -> {self.message}"

        if (
            self.documentLocationInCreatingWorkspace is None
            or self.documentLocationInCreatingWorkspace.path is None
        ):
            return output

        relative_path = self.documentLocationInCreatingWorkspace.path

        if path_prefix:
            relative_path = relative_path.replace(path_prefix, "")

        return (
            output
            + f"\n  Found in {relative_path}:{self.documentLocationInCreatingWorkspace.starting_line_number}:{self.documentLocationInCreatingWorkspace.starting_column_number}"
        )


class ActionTestActivitySummary(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestActivitySummary
      * Kind: object
      * Properties:
        + title: String
        + activityType: String
        + uuid: String
        + start: Date?
        + finish: Date?
        + attachments: [ActionTestAttachment]
        + subactivities: [ActionTestActivitySummary]
        + failureSummaryIDs: [String]
    """

    title: str
    activityType: str
    uuid: str
    start: Optional[datetime.datetime]
    finish: Optional[datetime.datetime]
    attachments: List[ActionTestAttachment]
    subactivities: List["ActionTestActivitySummary"]
    failureSummaryIDs: List[str]


class ActionTestMetadata(ActionTestSummaryIdentifiableObject):
    """Generated from xcresulttool format description.

    - ActionTestMetadata
      * Supertype: ActionTestSummaryIdentifiableObject
      * Kind: object
      * Properties:
        + testStatus: String
        + duration: Double?
        + summaryRef: Reference?
        + performanceMetricsCount: Int
        + failureSummariesCount: Int
        + activitySummariesCount: Int
    """

    testStatus: str
    duration: Optional[float]
    summaryRef: Optional[Reference]
    performanceMetricsCount: int
    failureSummariesCount: int
    activitySummariesCount: int


class ActionTestSummaryGroup(ActionTestSummaryIdentifiableObject):
    """Generated from xcresulttool format description.

    - ActionTestSummaryGroup
      * Supertype: ActionTestSummaryIdentifiableObject
      * Kind: object
      * Properties:
        + duration: Double
        + subtests: [ActionTestSummaryIdentifiableObject]
    """

    duration: float
    subtests: List[ActionTestSummaryIdentifiableObject]


class ActivityLogAnalyzerResultMessage(ActivityLogMessage):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerResultMessage
      * Supertype: ActivityLogMessage
      * Kind: object
      * Properties:
        + steps: [ActivityLogAnalyzerStep]
        + resultType: String?
        + keyEventIndex: Int
    """

    steps: List[ActivityLogAnalyzerStep]
    resultType: Optional[str]
    keyEventIndex: int


class ActivityLogAnalyzerWarningMessage(ActivityLogMessage):
    """Generated from xcresulttool format description.

    - ActivityLogAnalyzerWarningMessage
      * Supertype: ActivityLogMessage
      * Kind: object
    """


class ActivityLogSection(XcresultObject):
    """Generated from xcresulttool format description.

    - ActivityLogSection
      * Kind: object
      * Properties:
        + domainType: String
        + title: String
        + startTime: Date?
        + duration: Double
        + result: String?
        + location: DocumentLocation?
        + subsections: [ActivityLogSection]
        + messages: [ActivityLogMessage]
    """

    domainType: str
    title: str
    startTime: Optional[datetime.datetime]
    duration: float
    result: Optional[str]
    location: Optional[DocumentLocation]
    subsections: List["ActivityLogSection"]
    messages: List[ActivityLogMessage]


class ResultIssueSummaries(XcresultObject):
    """Generated from xcresulttool format description.

    - ResultIssueSummaries
      * Kind: object
      * Properties:
        + analyzerWarningSummaries: [IssueSummary]
        + errorSummaries: [IssueSummary]
        + testFailureSummaries: [TestFailureIssueSummary]
        + warningSummaries: [IssueSummary]
    """

    analyzerWarningSummaries: List[IssueSummary]
    errorSummaries: List[IssueSummary]
    testFailureSummaries: List[TestFailureIssueSummary]
    warningSummaries: List[IssueSummary]


class SourceCodeFrame(XcresultObject):
    """Generated from xcresulttool format description.

    - SourceCodeFrame
      * Kind: object
      * Properties:
        + addressString: String?
        + symbolInfo: SourceCodeSymbolInfo?
    """

    addressString: Optional[str]
    symbolInfo: Optional[SourceCodeSymbolInfo]


class ActionResult(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionResult
      * Kind: object
      * Properties:
        + resultName: String
        + status: String
        + metrics: ResultMetrics
        + issues: ResultIssueSummaries
        + coverage: CodeCoverageInfo
        + timelineRef: Reference?
        + logRef: Reference?
        + testsRef: Reference?
        + diagnosticsRef: Reference?
    """

    resultName: str
    status: str
    metrics: ResultMetrics
    issues: ResultIssueSummaries
    coverage: CodeCoverageInfo
    timelineRef: Optional[Reference]
    logRef: Optional[Reference]
    testsRef: Optional[Reference]
    diagnosticsRef: Optional[Reference]


class ActivityLogCommandInvocationSection(ActivityLogSection):
    """Generated from xcresulttool format description.

    - ActivityLogCommandInvocationSection
      * Supertype: ActivityLogSection
      * Kind: object
      * Properties:
        + commandDetails: String
        + emittedOutput: String
        + exitCode: Int?
    """

    commandDetails: str
    emittedOutput: str
    exitCode: Optional[int]


class ActivityLogMajorSection(ActivityLogSection):
    """Generated from xcresulttool format description.

    - ActivityLogMajorSection
      * Supertype: ActivityLogSection
      * Kind: object
      * Properties:
        + subtitle: String
    """

    subtitle: str


class ActivityLogUnitTestSection(ActivityLogSection):
    """Generated from xcresulttool format description.

    - ActivityLogUnitTestSection
      * Supertype: ActivityLogSection
      * Kind: object
      * Properties:
        + testName: String?
        + suiteName: String?
        + summary: String?
        + emittedOutput: String?
        + performanceTestOutput: String?
        + testsPassedString: String?
        + wasSkipped: Bool
        + runnablePath: String?
        + runnableUTI: String?
    """

    testName: Optional[str]
    suiteName: Optional[str]
    summary: Optional[str]
    emittedOutput: Optional[str]
    performanceTestOutput: Optional[str]
    testsPassedString: Optional[str]
    wasSkipped: bool
    runnablePath: Optional[str]
    runnableUTI: Optional[str]


class SourceCodeContext(XcresultObject):
    """Generated from xcresulttool format description.

    - SourceCodeContext
      * Kind: object
      * Properties:
        + location: SourceCodeLocation?
        + callStack: [SourceCodeFrame]
    """

    location: Optional[SourceCodeLocation]
    callStack: List[SourceCodeFrame]


class ActionRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionRecord
      * Kind: object
      * Properties:
        + schemeCommandName: String
        + schemeTaskName: String
        + title: String?
        + startedTime: Date
        + endedTime: Date
        + runDestination: ActionRunDestinationRecord
        + buildResult: ActionResult
        + actionResult: ActionResult
    """

    schemeCommandName: str
    schemeTaskName: str
    title: Optional[str]
    startedTime: datetime.datetime
    endedTime: datetime.datetime
    runDestination: ActionRunDestinationRecord
    buildResult: ActionResult
    actionResult: ActionResult


class ActionTestFailureSummary(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestFailureSummary
      * Kind: object
      * Properties:
        + message: String?
        + fileName: String
        + lineNumber: Int
        + isPerformanceFailure: Bool
        + uuid: String
        + issueType: String?
        + detailedDescription: String?
        + attachments: [ActionTestAttachment]
        + associatedError: TestAssociatedError?
        + sourceCodeContext: SourceCodeContext?
        + timestamp: Date?
        + isTopLevelFailure: Bool
    """

    message: Optional[str]
    fileName: str
    lineNumber: int
    isPerformanceFailure: bool
    uuid: str
    issueType: Optional[str]
    detailedDescription: Optional[str]
    attachments: List[ActionTestAttachment]
    associatedError: Optional[TestAssociatedError]
    sourceCodeContext: Optional[SourceCodeContext]
    timestamp: Optional[datetime.datetime]
    isTopLevelFailure: bool


class ActivityLogTargetBuildSection(ActivityLogMajorSection):
    """Generated from xcresulttool format description.

    - ActivityLogTargetBuildSection
      * Supertype: ActivityLogMajorSection
      * Kind: object
      * Properties:
        + productType: String?
    """

    productType: Optional[str]


class ActionTestSummary(ActionTestSummaryIdentifiableObject):
    """Generated from xcresulttool format description.

    - ActionTestSummary
      * Supertype: ActionTestSummaryIdentifiableObject
      * Kind: object
      * Properties:
        + testStatus: String
        + duration: Double
        + performanceMetrics: [ActionTestPerformanceMetricSummary]
        + failureSummaries: [ActionTestFailureSummary]
        + skipNoticeSummary: ActionTestNoticeSummary?
        + activitySummaries: [ActionTestActivitySummary]
    """

    testStatus: str
    duration: float
    performanceMetrics: List[ActionTestPerformanceMetricSummary]
    failureSummaries: List[ActionTestFailureSummary]
    skipNoticeSummary: Optional[ActionTestNoticeSummary]
    activitySummaries: List[ActionTestActivitySummary]


class ActionTestableSummary(ActionAbstractTestSummary):
    """Generated from xcresulttool format description.

    - ActionTestableSummary
      * Supertype: ActionAbstractTestSummary
      * Kind: object
      * Properties:
        + projectRelativePath: String?
        + targetName: String?
        + testKind: String?
        + tests: [ActionTestSummaryIdentifiableObject]
        + diagnosticsDirectoryName: String?
        + failureSummaries: [ActionTestFailureSummary]
        + testLanguage: String?
        + testRegion: String?
    """

    projectRelativePath: Optional[str]
    targetName: Optional[str]
    testKind: Optional[str]
    tests: List[ActionTestSummaryIdentifiableObject]
    diagnosticsDirectoryName: Optional[str]
    failureSummaries: List[ActionTestFailureSummary]
    testLanguage: Optional[str]
    testRegion: Optional[str]


class ActionsInvocationRecord(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionsInvocationRecord
      * Kind: object
      * Properties:
        + metadataRef: Reference?
        + metrics: ResultMetrics
        + issues: ResultIssueSummaries
        + actions: [ActionRecord]
        + archive: ArchiveInfo?
    """

    metadataRef: Optional[Reference]
    metrics: ResultMetrics
    issues: ResultIssueSummaries
    actions: List[ActionRecord]
    archive: Optional[ArchiveInfo]


class ActionTestPlanRunSummary(ActionAbstractTestSummary):
    """Generated from xcresulttool format description.

    - ActionTestPlanRunSummary
      * Supertype: ActionAbstractTestSummary
      * Kind: object
      * Properties:
        + testableSummaries: [ActionTestableSummary]
    """

    testableSummaries: List[ActionTestableSummary]


class ActionTestPlanRunSummaries(XcresultObject):
    """Generated from xcresulttool format description.

    - ActionTestPlanRunSummaries
      * Kind: object
      * Properties:
        + summaries: [ActionTestPlanRunSummary]
    """

    summaries: List[ActionTestPlanRunSummary]


_CURRENT_MODULE = sys.modules[__name__]
_MODEL_NAMES = dir(_CURRENT_MODULE)
_MODEL_NAMES = [m for m in _MODEL_NAMES if not m.startswith("__")]
_RESOLVED_MODELS = [getattr(_CURRENT_MODULE, m) for m in _MODEL_NAMES]
# pylint: disable=unidiomatic-typecheck
_RESOLVED_MODELS = [
    m for m in _RESOLVED_MODELS if type(m) == type(type) and issubclass(m, XcresultObject)
]
# pylint: enable=unidiomatic-typecheck
MODELS = {m.__name__: m for m in _RESOLVED_MODELS}
