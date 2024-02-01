"""A module for dealing with xcresults."""

from typing import Any, Optional

from xcresult.model import *
from xcresult.xcresulttool import (
    deserialize,
    export_attachment,
    get_actions_invocation_record,
    get,
    export_action_test_summary_group,
)


class Xcresults:
    """Wrapper around an xcresults bundle."""

    path: str
    _actions_invocation_record: Optional[ActionsInvocationRecord]

    def __init__(self, path: str) -> None:
        self.path = path
        self._actions_invocation_record = None

    @property
    def actions_invocation_record(self) -> ActionsInvocationRecord:
        """Get the actions invocation record

        This is the default response when using xcresulttool

        :returns: An ActionsInvocationRecord
        """
        if not self._actions_invocation_record:
            self._actions_invocation_record = get_actions_invocation_record(self.path)
            assert self._actions_invocation_record is not None
        return self._actions_invocation_record

    def export_attachment(
        self, identifier: str, type_identifier: str, output_path: str
    ) -> None:
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
        for action in self.actions_invocation_record.actions:
            test_id = action.actionResult.testsRef.id
            summaries = deserialize(self.get(test_id))
            for summary in summaries.summaries:
                for testable_summary in summary.testableSummaries:
                    for test in testable_summary.tests:
                        export_action_test_summary_group(self.path, test, output_path)
