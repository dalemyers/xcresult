"""High-level access to modern xcresult reports."""

from functools import cached_property

from xcresult import xcresulttool
from xcresult.junit_writer import JunitWriter, TestFilter
from xcresult.model import (
    Activities,
    BuildResults,
    ContentAvailability,
    Summary,
    TestAttachmentDetails,
    TestDetails,
    Tests,
)
from xcresult.xcresult_base import XcresultsBase


class Xcresults(XcresultsBase):
    """A result bundle with lazily loaded report snapshots."""

    @property
    def content_availability(self) -> ContentAvailability:
        """Get the bundle's available content."""
        return self._content_availability

    @cached_property
    def _content_availability(self) -> ContentAvailability:
        """Load content availability once."""
        return xcresulttool.get_content_availability(self.path)

    @cached_property
    def build_results(self) -> BuildResults:
        """Get build issues and metadata."""
        return xcresulttool.get_build_results(self.path)

    @cached_property
    def test_summary(self) -> Summary:
        """Get test counts, failures, warnings, and destinations."""
        return xcresulttool.get_test_summary(self.path)

    @property
    def tests(self) -> Tests:
        """Get the test hierarchy."""
        return self._tests

    @cached_property
    def _tests(self) -> Tests:
        """Load the test hierarchy once."""
        return xcresulttool.get_tests(self.path)

    def test_details(self, test_id: str) -> TestDetails:
        """Get individual runs for a test.

        :param test_id: Test identifier URL or string.
        :returns: The test details report.
        """
        return xcresulttool.get_test_details(self.path, test_id)

    def test_activities(self, test_id: str) -> Activities:
        """Get activity trees for a test.

        :param test_id: Test identifier URL or string.
        :returns: The test activities report.
        """
        return xcresulttool.get_test_activities(self.path, test_id)

    def export_test_attachments(
        self, output_path: str, test_id: str | None = None
    ) -> list[TestAttachmentDetails]:
        """Export attachments using the modern manifest layout.

        :param output_path: Directory for files and ``manifest.json``.
        :param test_id: Optional test or suite identifier.
        :returns: Manifest entries for the exported files.
        """
        return xcresulttool.export_test_attachments(self.path, output_path, test_id)

    # pylint: disable=too-many-positional-arguments
    def write_junit(
        self,
        path: str,
        export_attachments_path: str | None = None,
        test_class_prefix: str | None = None,
        test_class_suffix: str | None = None,
        collapse_retries: bool = False,
        test_filter: TestFilter | None = None,
    ) -> None:
        """Write a JUnit report from individual modern test runs.

        :param path: Output XML path.
        :param export_attachments_path: Optional attachment export directory.
        :param test_class_prefix: Optional classname prefix.
        :param test_class_suffix: Optional classname suffix.
        :param collapse_retries: Keep one attempt per test, arguments, device, and
            configuration, preferring a passing attempt.
        :param test_filter: Predicate receiving the modern TestNode for a test;
            return False to exclude it from both XML and counts.
        """
        JunitWriter(
            self,
            path,
            export_attachments_path,
            test_class_prefix,
            test_class_suffix,
            collapse_retries,
            test_filter,
        ).write()
