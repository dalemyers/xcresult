"""A base class for dealing with xcresults."""

import abc
from typing import Any

from xcresult.model import ActionsInvocationRecord


class XcresultsBase(abc.ABC):
    """Wrapper around an xcresults bundle."""

    path: str
    _actions_invocation_record: ActionsInvocationRecord | None

    def __init__(self, path: str) -> None:
        self.path = path
        self._actions_invocation_record = None

    @property
    def actions_invocation_record(self) -> ActionsInvocationRecord:
        """Get the actions invocation record

        This is the default response when using xcresulttool

        :returns: An ActionsInvocationRecord
        """
        raise NotImplementedError()

    def get(self, identifier: str) -> dict[str, Any]:
        """Run a get command on bundle with the given id.

        :param id: The ID of the item to get.
        """
        raise NotImplementedError()

    def export_test_attachments(self, output_path: str):
        """Export test attachments from the xcresult bundle.

        :param output_path: The path to export the attachments to.
        """
        raise NotImplementedError()
