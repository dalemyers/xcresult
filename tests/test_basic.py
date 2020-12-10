"""Test base types."""

import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import xcresult

# pylint: enable=wrong-import-position


# pylint: disable=too-many-statements


def test_import():
    """Test that import works."""
    assert xcresult is not None


def test_deserialization_1():
    """Test deserialization."""
    sample = {
        "_type": {"_name": "ActionPlatformRecord"},
        "identifier": {"_type": {"_name": "String"}, "_value": "com.apple.platform.macosx"},
        "userDescription": {"_type": {"_name": "String"}, "_value": "macOS"},
    }
    result = xcresult.xcresulttool.deserialize(sample)
    assert isinstance(result, xcresult.ActionPlatformRecord)
    assert result.identifier == "com.apple.platform.macosx"
    assert result.userDescription == "macOS"
    print(result)


def test_deserialization_2():
    """Test deserialization."""
    sample = {
        "_type": {"_name": "ActionsInvocationRecord"},
        "actions": {
            "_type": {"_name": "Array"},
            "_values": [
                {
                    "_type": {"_name": "ActionRecord"},
                    "actionResult": {
                        "_type": {"_name": "ActionResult"},
                        "coverage": {
                            "_type": {"_name": "CodeCoverageInfo"},
                            "archiveRef": {
                                "_type": {"_name": "Reference"},
                                "id": {
                                    "_type": {"_name": "String"},
                                    "_value": "0~qephX2M0nhu_VVtr0Gp-iT54M4AP7pUW_eJen0hhFAEDElwO-xNmOD2zQu1PCt0FPRMVWunQX3NmXmGel3KIeA==",
                                },
                            },
                            "hasCoverageData": {"_type": {"_name": "Bool"}, "_value": "true"},
                            "reportRef": {
                                "_type": {"_name": "Reference"},
                                "id": {
                                    "_type": {"_name": "String"},
                                    "_value": "0~JOxsMkzoZmY6gUwow9M2waVav3viBYaP7i8vGn8sOKCYPZ0ILPAg0hYY09zV0EMyn8uKWtaZi8MIi_xtCwNihQ==",
                                },
                            },
                        },
                        "diagnosticsRef": {
                            "_type": {"_name": "Reference"},
                            "id": {
                                "_type": {"_name": "String"},
                                "_value": "0~q4JgkvexuLJPydEC2FCpCQD5MgKtHdFf9CbfebEEKyccR0R8OmlnkwBkVbH11Ym0nTxJ5c-12mlCI8wNDPXsSg==",
                            },
                        },
                        "issues": {
                            "_type": {"_name": "ResultIssueSummaries"},
                            "testFailureSummaries": {
                                "_type": {"_name": "Array"},
                                "_values": [
                                    {
                                        "_type": {
                                            "_name": "TestFailureIssueSummary",
                                            "_supertype": {"_name": "IssueSummary"},
                                        },
                                        "documentLocationInCreatingWorkspace": {
                                            "_type": {"_name": "DocumentLocation"},
                                            "concreteTypeName": {
                                                "_type": {"_name": "String"},
                                                "_value": "DVTTextDocumentLocation",
                                            },
                                            "url": {
                                                "_type": {"_name": "String"},
                                                "_value": "/test/file/path",
                                            },
                                        },
                                        "issueType": {
                                            "_type": {"_name": "String"},
                                            "_value": "Uncategorized",
                                        },
                                        "message": {
                                            "_type": {"_name": "String"},
                                            "_value": "test failed",
                                        },
                                        "producingTarget": {
                                            "_type": {"_name": "String"},
                                            "_value": "TestTarget",
                                        },
                                        "testCaseName": {
                                            "_type": {"_name": "String"},
                                            "_value": "TestClass.testMethod()",
                                        },
                                    }
                                ],
                            },
                        },
                        "logRef": {
                            "_type": {"_name": "Reference"},
                            "id": {
                                "_type": {"_name": "String"},
                                "_value": "0~uRBpegTkX1gXzoU_WI3Gm7b8pr9LGUZn-Hps8BCD1Byyy3RhMOiCFnNMabTTMtOGrcqH-pofb6E8mEXeaqhOOA==",
                            },
                            "targetType": {
                                "_type": {"_name": "TypeDefinition"},
                                "name": {
                                    "_type": {"_name": "String"},
                                    "_value": "ActivityLogSection",
                                },
                            },
                        },
                        "metrics": {
                            "_type": {"_name": "ResultMetrics"},
                            "testsCount": {"_type": {"_name": "Int"}, "_value": "25"},
                            "testsFailedCount": {"_type": {"_name": "Int"}, "_value": "1"},
                        },
                        "resultName": {"_type": {"_name": "String"}, "_value": "action"},
                        "status": {"_type": {"_name": "String"}, "_value": "failed"},
                        "testsRef": {
                            "_type": {"_name": "Reference"},
                            "id": {
                                "_type": {"_name": "String"},
                                "_value": "0~iBYjGrT09vh0Oe-z46eWdUL_4Eg6ruIqHa9iO-BZjLqPR1v43hg6Be43MQBj0ZEYrfG3ZBl43w6723aMHAL9tg==",
                            },
                            "targetType": {
                                "_type": {"_name": "TypeDefinition"},
                                "name": {
                                    "_type": {"_name": "String"},
                                    "_value": "ActionTestPlanRunSummaries",
                                },
                            },
                        },
                    },
                    "buildResult": {
                        "_type": {"_name": "ActionResult"},
                        "coverage": {"_type": {"_name": "CodeCoverageInfo"}},
                        "issues": {"_type": {"_name": "ResultIssueSummaries"}},
                        "metrics": {"_type": {"_name": "ResultMetrics"}},
                        "resultName": {"_type": {"_name": "String"}, "_value": "build"},
                        "status": {"_type": {"_name": "String"}, "_value": "notRequested"},
                    },
                    "endedTime": {
                        "_type": {"_name": "Date"},
                        "_value": "2020-11-28T15:51:36.975+0000",
                    },
                    "runDestination": {
                        "_type": {"_name": "ActionRunDestinationRecord"},
                        "displayName": {
                            "_type": {"_name": "String"},
                            "_value": "iPhone 8",
                        },
                        "localComputerRecord": {
                            "_type": {"_name": "ActionDeviceRecord"},
                            "busSpeedInMHz": {"_type": {"_name": "Int"}, "_value": "400"},
                            "cpuCount": {"_type": {"_name": "Int"}, "_value": "1"},
                            "cpuKind": {
                                "_type": {"_name": "String"},
                                "_value": "8-Core Intel Core i9",
                            },
                            "cpuSpeedInMHz": {"_type": {"_name": "Int"}, "_value": "2400"},
                            "identifier": {
                                "_type": {"_name": "String"},
                                "_value": "8C3C9D24-E5A2-5FA6-B69E-B122A69DC18E",
                            },
                            "isConcreteDevice": {"_type": {"_name": "Bool"}, "_value": "true"},
                            "logicalCPUCoresPerPackage": {
                                "_type": {"_name": "Int"},
                                "_value": "16",
                            },
                            "modelCode": {"_type": {"_name": "String"}, "_value": "MacBookPro15,1"},
                            "modelName": {"_type": {"_name": "String"}, "_value": "MacBook Pro"},
                            "modelUTI": {
                                "_type": {"_name": "String"},
                                "_value": "com.apple.macbookpro-15-retina-touchid-2018",
                            },
                            "name": {"_type": {"_name": "String"}, "_value": "My Mac"},
                            "nativeArchitecture": {
                                "_type": {"_name": "String"},
                                "_value": "x86_64h",
                            },
                            "operatingSystemVersion": {
                                "_type": {"_name": "String"},
                                "_value": "10.15.4",
                            },
                            "operatingSystemVersionWithBuildNumber": {
                                "_type": {"_name": "String"},
                                "_value": "10.15.4 (19E266)",
                            },
                            "physicalCPUCoresPerPackage": {
                                "_type": {"_name": "Int"},
                                "_value": "8",
                            },
                            "platformRecord": {
                                "_type": {"_name": "ActionPlatformRecord"},
                                "identifier": {
                                    "_type": {"_name": "String"},
                                    "_value": "com.apple.platform.macosx",
                                },
                                "userDescription": {
                                    "_type": {"_name": "String"},
                                    "_value": "macOS",
                                },
                            },
                            "ramSizeInMegabytes": {"_type": {"_name": "Int"}, "_value": "32768"},
                        },
                        "targetArchitecture": {"_type": {"_name": "String"}, "_value": "x86_64"},
                        "targetDeviceRecord": {
                            "_type": {"_name": "ActionDeviceRecord"},
                            "identifier": {
                                "_type": {"_name": "String"},
                                "_value": "C155A343-9D28-47D5-B96D-1F3D2504CCCC",
                            },
                            "isConcreteDevice": {"_type": {"_name": "Bool"}, "_value": "true"},
                            "modelCode": {"_type": {"_name": "String"}, "_value": "iPhone10,4"},
                            "modelName": {"_type": {"_name": "String"}, "_value": "iPhone 8"},
                            "modelUTI": {
                                "_type": {"_name": "String"},
                                "_value": "com.apple.iphone-8-2",
                            },
                            "name": {
                                "_type": {"_name": "String"},
                                "_value": "iPhone 8",
                            },
                            "nativeArchitecture": {
                                "_type": {"_name": "String"},
                                "_value": "x86_64",
                            },
                            "operatingSystemVersion": {
                                "_type": {"_name": "String"},
                                "_value": "14.2",
                            },
                            "operatingSystemVersionWithBuildNumber": {
                                "_type": {"_name": "String"},
                                "_value": "14.2 (18B79)",
                            },
                            "platformRecord": {
                                "_type": {"_name": "ActionPlatformRecord"},
                                "identifier": {
                                    "_type": {"_name": "String"},
                                    "_value": "com.apple.platform.iphonesimulator",
                                },
                                "userDescription": {
                                    "_type": {"_name": "String"},
                                    "_value": "iOS Simulator",
                                },
                            },
                        },
                        "targetSDKRecord": {
                            "_type": {"_name": "ActionSDKRecord"},
                            "identifier": {
                                "_type": {"_name": "String"},
                                "_value": "iphonesimulator14.2",
                            },
                            "name": {
                                "_type": {"_name": "String"},
                                "_value": "Simulator - iOS 14.2",
                            },
                            "operatingSystemVersion": {
                                "_type": {"_name": "String"},
                                "_value": "14.2",
                            },
                        },
                    },
                    "schemeCommandName": {"_type": {"_name": "String"}, "_value": "Test"},
                    "schemeTaskName": {"_type": {"_name": "String"}, "_value": "Action"},
                    "startedTime": {
                        "_type": {"_name": "Date"},
                        "_value": "2020-11-28T15:49:41.629+0000",
                    },
                }
            ],
        },
        "issues": {
            "_type": {"_name": "ResultIssueSummaries"},
            "testFailureSummaries": {
                "_type": {"_name": "Array"},
                "_values": [
                    {
                        "_type": {
                            "_name": "TestFailureIssueSummary",
                            "_supertype": {"_name": "IssueSummary"},
                        },
                        "documentLocationInCreatingWorkspace": {
                            "_type": {"_name": "DocumentLocation"},
                            "concreteTypeName": {
                                "_type": {"_name": "String"},
                                "_value": "DVTTextDocumentLocation",
                            },
                            "url": {
                                "_type": {"_name": "String"},
                                "_value": "/test/file/path",
                            },
                        },
                        "issueType": {"_type": {"_name": "String"}, "_value": "Uncategorized"},
                        "message": {
                            "_type": {"_name": "String"},
                            "_value": "test failed",
                        },
                        "producingTarget": {
                            "_type": {"_name": "String"},
                            "_value": "TestTarget",
                        },
                        "testCaseName": {
                            "_type": {"_name": "String"},
                            "_value": "TestClass.testMethod()",
                        },
                    }
                ],
            },
        },
        "metadataRef": {
            "_type": {"_name": "Reference"},
            "id": {
                "_type": {"_name": "String"},
                "_value": "0~M5Z-APgijluGOj_O_wyB0EYAj13jOU2Dh8ceIZMfcZQQgxBXElmNOOW5k1dOgXKs5opNYU1_CvRukFmiUzHa3w==",
            },
            "targetType": {
                "_type": {"_name": "TypeDefinition"},
                "name": {"_type": {"_name": "String"}, "_value": "ActionsInvocationMetadata"},
            },
        },
        "metrics": {
            "_type": {"_name": "ResultMetrics"},
            "testsCount": {"_type": {"_name": "Int"}, "_value": "25"},
            "testsFailedCount": {"_type": {"_name": "Int"}, "_value": "1"},
        },
    }

    result = xcresult.xcresulttool.deserialize(sample)
    assert isinstance(result, xcresult.ActionsInvocationRecord)
    assert isinstance(result.actions, list)
    assert len(result.actions) == 1
    assert isinstance(result.actions[0], xcresult.ActionRecord)
    assert isinstance(result.actions[0].actionResult, xcresult.ActionResult)
    assert isinstance(result.actions[0].actionResult.coverage, xcresult.CodeCoverageInfo)
    assert isinstance(result.actions[0].actionResult.coverage.archiveRef, xcresult.Reference)
    assert (
        result.actions[0].actionResult.coverage.archiveRef.id
        == "0~qephX2M0nhu_VVtr0Gp-iT54M4AP7pUW_eJen0hhFAEDElwO-xNmOD2zQu1PCt0FPRMVWunQX3NmXmGel3KIeA=="
    )
    assert result.actions[0].actionResult.coverage.hasCoverageData
    assert isinstance(result.actions[0].actionResult.coverage.reportRef, xcresult.Reference)
    assert (
        result.actions[0].actionResult.coverage.reportRef.id
        == "0~JOxsMkzoZmY6gUwow9M2waVav3viBYaP7i8vGn8sOKCYPZ0ILPAg0hYY09zV0EMyn8uKWtaZi8MIi_xtCwNihQ=="
    )
    assert isinstance(result.actions[0].actionResult.diagnosticsRef, xcresult.Reference)
    assert (
        result.actions[0].actionResult.diagnosticsRef.id
        == "0~q4JgkvexuLJPydEC2FCpCQD5MgKtHdFf9CbfebEEKyccR0R8OmlnkwBkVbH11Ym0nTxJ5c-12mlCI8wNDPXsSg=="
    )
    assert isinstance(result.actions[0].actionResult.issues, xcresult.ResultIssueSummaries)
    assert isinstance(result.actions[0].actionResult.issues.testFailureSummaries, list)
    assert len(result.actions[0].actionResult.issues.testFailureSummaries) == 1
    assert isinstance(
        result.actions[0].actionResult.issues.testFailureSummaries[0],
        xcresult.TestFailureIssueSummary,
    )
    assert isinstance(
        result.actions[0]
        .actionResult.issues.testFailureSummaries[0]
        .documentLocationInCreatingWorkspace,
        xcresult.DocumentLocation,
    )
    assert (
        result.actions[0]
        .actionResult.issues.testFailureSummaries[0]
        .documentLocationInCreatingWorkspace.concreteTypeName
        == "DVTTextDocumentLocation"
    )
    assert (
        result.actions[0]
        .actionResult.issues.testFailureSummaries[0]
        .documentLocationInCreatingWorkspace.url
        == "/test/file/path"
    )
    assert (
        result.actions[0].actionResult.issues.testFailureSummaries[0].issueType == "Uncategorized"
    )
    assert result.actions[0].actionResult.issues.testFailureSummaries[0].message == "test failed"
    assert (
        result.actions[0].actionResult.issues.testFailureSummaries[0].producingTarget
        == "TestTarget"
    )
    assert (
        result.actions[0].actionResult.issues.testFailureSummaries[0].testCaseName
        == "TestClass.testMethod()"
    )
    assert isinstance(result.actions[0].actionResult.logRef, xcresult.Reference)
    assert (
        result.actions[0].actionResult.logRef.id
        == "0~uRBpegTkX1gXzoU_WI3Gm7b8pr9LGUZn-Hps8BCD1Byyy3RhMOiCFnNMabTTMtOGrcqH-pofb6E8mEXeaqhOOA=="
    )
    assert isinstance(result.actions[0].actionResult.logRef.targetType, xcresult.TypeDefinition)
    assert result.actions[0].actionResult.logRef.targetType.name == "ActivityLogSection"
    assert isinstance(result.actions[0].actionResult.metrics, xcresult.ResultMetrics)
    assert result.actions[0].actionResult.metrics.testsCount == 25
    assert result.actions[0].actionResult.metrics.testsFailedCount == 1
    assert result.actions[0].actionResult.resultName == "action"
    assert result.actions[0].actionResult.status == "failed"
    assert isinstance(result.actions[0].actionResult.testsRef, xcresult.Reference)
    assert (
        result.actions[0].actionResult.testsRef.id
        == "0~iBYjGrT09vh0Oe-z46eWdUL_4Eg6ruIqHa9iO-BZjLqPR1v43hg6Be43MQBj0ZEYrfG3ZBl43w6723aMHAL9tg=="
    )
    assert isinstance(result.actions[0].actionResult.testsRef.targetType, xcresult.TypeDefinition)
    assert result.actions[0].actionResult.testsRef.targetType.name == "ActionTestPlanRunSummaries"
    assert isinstance(result.actions[0].buildResult, xcresult.ActionResult)
    assert isinstance(result.actions[0].buildResult.coverage, xcresult.CodeCoverageInfo)
    assert isinstance(result.actions[0].buildResult.issues, xcresult.ResultIssueSummaries)
    assert isinstance(result.actions[0].buildResult.metrics, xcresult.ResultMetrics)
    assert result.actions[0].buildResult.resultName == "build"
    assert result.actions[0].buildResult.status == "notRequested"
    assert result.actions[0].endedTime == datetime.datetime(
        2020, 11, 28, 15, 51, 36, 975000, tzinfo=datetime.timezone.utc
    )
    assert isinstance(result.actions[0].runDestination, xcresult.ActionRunDestinationRecord)
    assert result.actions[0].runDestination.displayName == "iPhone 8"
    assert isinstance(
        result.actions[0].runDestination.localComputerRecord, xcresult.ActionDeviceRecord
    )
    assert result.actions[0].runDestination.localComputerRecord.busSpeedInMHz == 400
    assert result.actions[0].runDestination.localComputerRecord.cpuCount == 1
    assert result.actions[0].runDestination.localComputerRecord.cpuKind == "8-Core Intel Core i9"
    assert result.actions[0].runDestination.localComputerRecord.cpuSpeedInMHz == 2400
    assert (
        result.actions[0].runDestination.localComputerRecord.identifier
        == "8C3C9D24-E5A2-5FA6-B69E-B122A69DC18E"
    )
    assert result.actions[0].runDestination.localComputerRecord.isConcreteDevice
    assert result.actions[0].runDestination.localComputerRecord.logicalCPUCoresPerPackage == 16
    assert result.actions[0].runDestination.localComputerRecord.modelCode == "MacBookPro15,1"
    assert result.actions[0].runDestination.localComputerRecord.modelName == "MacBook Pro"
    assert (
        result.actions[0].runDestination.localComputerRecord.modelUTI
        == "com.apple.macbookpro-15-retina-touchid-2018"
    )
    assert result.actions[0].runDestination.localComputerRecord.name == "My Mac"
    assert result.actions[0].runDestination.localComputerRecord.nativeArchitecture == "x86_64h"
    assert result.actions[0].runDestination.localComputerRecord.operatingSystemVersion == "10.15.4"
    assert (
        result.actions[0].runDestination.localComputerRecord.operatingSystemVersionWithBuildNumber
        == "10.15.4 (19E266)"
    )
    assert result.actions[0].runDestination.localComputerRecord.physicalCPUCoresPerPackage == 8
    assert isinstance(
        result.actions[0].runDestination.localComputerRecord.platformRecord,
        xcresult.ActionPlatformRecord,
    )
    assert (
        result.actions[0].runDestination.localComputerRecord.platformRecord.identifier
        == "com.apple.platform.macosx"
    )
    assert (
        result.actions[0].runDestination.localComputerRecord.platformRecord.userDescription
        == "macOS"
    )
    assert result.actions[0].runDestination.localComputerRecord.ramSizeInMegabytes == 32768
    assert result.actions[0].runDestination.targetArchitecture == "x86_64"
    assert isinstance(
        result.actions[0].runDestination.targetDeviceRecord, xcresult.ActionDeviceRecord
    )
    assert (
        result.actions[0].runDestination.targetDeviceRecord.identifier
        == "C155A343-9D28-47D5-B96D-1F3D2504CCCC"
    )
    assert result.actions[0].runDestination.targetDeviceRecord.isConcreteDevice
    assert result.actions[0].runDestination.targetDeviceRecord.modelCode == "iPhone10,4"
    assert result.actions[0].runDestination.targetDeviceRecord.modelName == "iPhone 8"
    assert result.actions[0].runDestination.targetDeviceRecord.modelUTI == "com.apple.iphone-8-2"
    assert result.actions[0].runDestination.targetDeviceRecord.name == "iPhone 8"
    assert result.actions[0].runDestination.targetDeviceRecord.nativeArchitecture == "x86_64"
    assert result.actions[0].runDestination.targetDeviceRecord.operatingSystemVersion == "14.2"
    assert (
        result.actions[0].runDestination.targetDeviceRecord.operatingSystemVersionWithBuildNumber
        == "14.2 (18B79)"
    )
    assert isinstance(
        result.actions[0].runDestination.targetDeviceRecord.platformRecord,
        xcresult.ActionPlatformRecord,
    )
    assert (
        result.actions[0].runDestination.targetDeviceRecord.platformRecord.identifier
        == "com.apple.platform.iphonesimulator"
    )
    assert (
        result.actions[0].runDestination.targetDeviceRecord.platformRecord.userDescription
        == "iOS Simulator"
    )
    assert isinstance(result.actions[0].runDestination.targetSDKRecord, xcresult.ActionSDKRecord)
    assert result.actions[0].runDestination.targetSDKRecord.identifier == "iphonesimulator14.2"
    assert result.actions[0].runDestination.targetSDKRecord.name == "Simulator - iOS 14.2"
    assert result.actions[0].runDestination.targetSDKRecord.operatingSystemVersion == "14.2"
    assert result.actions[0].schemeCommandName == "Test"
    assert result.actions[0].schemeTaskName == "Action"
    assert result.actions[0].startedTime == datetime.datetime(
        2020, 11, 28, 15, 49, 41, 629000, tzinfo=datetime.timezone.utc
    )
    assert isinstance(result.issues, xcresult.ResultIssueSummaries)
    assert isinstance(result.issues.testFailureSummaries, list)
    assert len(result.issues.testFailureSummaries) == 1
    assert isinstance(result.issues.testFailureSummaries[0], xcresult.TestFailureIssueSummary)
    assert isinstance(
        result.issues.testFailureSummaries[0].documentLocationInCreatingWorkspace,
        xcresult.DocumentLocation,
    )
    assert (
        result.issues.testFailureSummaries[0].documentLocationInCreatingWorkspace.concreteTypeName
        == "DVTTextDocumentLocation"
    )
    assert (
        result.issues.testFailureSummaries[0].documentLocationInCreatingWorkspace.url
        == "/test/file/path"
    )
    assert result.issues.testFailureSummaries[0].issueType == "Uncategorized"
    assert result.issues.testFailureSummaries[0].message == "test failed"
    assert result.issues.testFailureSummaries[0].producingTarget == "TestTarget"
    assert result.issues.testFailureSummaries[0].testCaseName == "TestClass.testMethod()"
    assert isinstance(result.metadataRef, xcresult.Reference)
    assert (
        result.metadataRef.id
        == "0~M5Z-APgijluGOj_O_wyB0EYAj13jOU2Dh8ceIZMfcZQQgxBXElmNOOW5k1dOgXKs5opNYU1_CvRukFmiUzHa3w=="
    )
    assert isinstance(result.metadataRef.targetType, xcresult.TypeDefinition)
    assert result.metadataRef.targetType.name == "ActionsInvocationMetadata"
    assert isinstance(result.metrics, xcresult.ResultMetrics)
    assert result.metrics.testsCount == 25
    assert result.metrics.testsFailedCount == 1
