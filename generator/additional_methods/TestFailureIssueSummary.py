def pretty_message(self, path_prefix: str | None) -> str:
    """Format the message nicely for review.

    :param path_prefix: Any path prefix to remove

    :returns: A pretty message
    """
    # pylint: disable=no-member
    output = f"* [{self.producingTarget}] {self.testCaseName} -> {self.message}"

    documentLocationInCreatingWorkspace = self.documentLocationInCreatingWorkspace

    if documentLocationInCreatingWorkspace is None or not documentLocationInCreatingWorkspace.path:
        return output

    relative_path = documentLocationInCreatingWorkspace.path

    if path_prefix:
        relative_path = relative_path.replace(path_prefix, "")

    return (
        output
        + f"\n  Found in {relative_path}:{documentLocationInCreatingWorkspace.starting_line_number}:{documentLocationInCreatingWorkspace.starting_column_number}"
    )
    # pylint: enable=no-member
