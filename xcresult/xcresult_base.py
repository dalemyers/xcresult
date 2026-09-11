"""Interface consumed by the JUnit writer."""

import abc
import os

from xcresult.model import ContentAvailability, TestAttachmentDetails, TestDetails, Tests


class XcresultsBase(abc.ABC):
    """A result bundle that exposes modern test reports."""

    def __init__(self, path: str) -> None:
        self.path = os.path.abspath(path)

    @property
    @abc.abstractmethod
    def content_availability(self) -> ContentAvailability:
        """Get available bundle content."""

    @property
    @abc.abstractmethod
    def tests(self) -> Tests:
        """Get the test tree."""

    @abc.abstractmethod
    def test_details(self, test_id: str) -> TestDetails:
        """Get a test's detailed runs.

        :param test_id: Test identifier URL or string.
        :returns: The test details.
        """

    @abc.abstractmethod
    def export_test_attachments(
        self, output_path: str, test_id: str | None = None
    ) -> list[TestAttachmentDetails]:
        """Export attachments.

        :param output_path: Directory for exported files.
        :param test_id: Optional test or suite identifier.
        :returns: The export manifest.
        """
