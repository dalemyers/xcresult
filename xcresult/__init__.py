"""A module for dealing with xcresults."""

import datetime
import json
import os
import subprocess
from typing import Any, cast, Dict, get_type_hints, List, Optional, Tuple

from xcresult import model
from xcresult.model import *
from xcresult.xcresulttool import export_attachments, get_actions_invocation_record


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

    def export_attachments(self, output_folder: str) -> None:
        """Export all attachments in an xcresult bundle.

        The attachments will be placed into the `output_folder` with a sub-folder
        for each test class, and a sub-folder for each test within that class.

        The name will be the attachment name generated if available.

        :param output_folder: The output folder to write the attachments to
        """
        export_attachments(self.path, output_folder)
