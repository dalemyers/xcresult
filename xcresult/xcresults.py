"""A class for dealing with xcresults."""

import logging
from typing import Any, cast

from xcresult.exceptions import (
    MissingPropertyException,
)
from xcresult.junit_writer import JunitWriter
from xcresult.model import ActionsInvocationRecord, ActionTestPlanRunSummaries
from xcresult.xcresult_base import XcresultsBase
from xcresult.xcresulttool import (
    deserialize,
    export_attachment,
    get_actions_invocation_record,
    get,
    export_action_test_summary_group,
)

# pylint: enable=unused-import


class Xcresults(XcresultsBase):
    """Wrapper around an xcresults bundle."""

    path: str
    _actions_invocation_record: ActionsInvocationRecord | None

    @property
    def actions_invocation_record(self) -> ActionsInvocationRecord:
        """Get the actions invocation record

        This is the default response when using xcresulttool

        :returns: An ActionsInvocationRecord
        """
        if not self._actions_invocation_record:
            logging.debug("Actions invocation record not found, fetching...")
            self._actions_invocation_record = get_actions_invocation_record(self.path)
            assert self._actions_invocation_record is not None
        return self._actions_invocation_record

    def export_attachment(self, identifier: str, type_identifier: str, output_path: str) -> None:
        """Get an attachment from an xcresult bundle.

        :param path: The path of the xcresult bundle
        :param identifier: The identifier of the attachment to export
        :param type_identifier: The type of the attachment to export (.e.g. 'public.png')
        :param output_path: The output path to write the attachment to
        """
        export_attachment(self.path, identifier, type_identifier, output_path)

    def get(self, identifier: str) -> dict[str, Any]:
        """Run a get command on bundle with the given id.

        :param id: The ID of the item to get.
        """
        return get(self.path, identifier)

    def export_test_attachments(self, output_path: str):
        """Export all test attachments."""
        if not self.actions_invocation_record:
            raise MissingPropertyException("No actions invocation record found")

        if not self.actions_invocation_record.actions:
            raise MissingPropertyException("No actions found")

        logging.info("Exporting test attachments")

        for action in self.actions_invocation_record.actions:
            logging.info(
                f"\tExporting action: {action.schemeCommandName} - {action.schemeTaskName} - {action.testPlanName}"
            )

            if action.actionResult.testsRef is None:
                logging.info("\tNo testRef set on action.actionResult, skipping.")
                continue

            test_id = action.actionResult.testsRef.id
            summaries = cast(ActionTestPlanRunSummaries, deserialize(self.get(test_id)))

            if not summaries.summaries:
                raise MissingPropertyException("No summaries found")

            for summary in summaries.summaries:
                logging.info(f"\t\tExporting summary: {summary.name}")
                if not summary.testableSummaries:
                    raise MissingPropertyException("No testable summaries found")

                for testable_summary in summary.testableSummaries:
                    logging.info(f"\t\t\tExporting testable summary: {testable_summary.name}")

                    if not testable_summary.tests:
                        raise MissingPropertyException("No tests found")

                    for test in testable_summary.tests:
                        logging.info(f"\t\t\t\tExporting test: {test.identifier}")
                        export_action_test_summary_group(self.path, test, output_path, 5)

    def write_junit(
        self,
        path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
    ) -> None:
        """Write the test results as a junit.

        :param path: The path to write the junit to
        :param export_attachments_path: The path to write the attachments to. If None, the attachments will not be exported.
        """
        JunitWriter(
            self, path, export_attachments_path, test_class_prefix, test_class_suffix
        ).write()
