def pretty_message(self, path_prefix: Optional[str]) -> str:
    """Format the message nicely for review.

    :param path_prefix: Any path prefix to remove

    :returns: A pretty message
    """
    output = f"* [{super().producingTarget}] {self.testCaseName} -> {super().message}"

    documentLocationInCreatingWorkspace = super().documentLocationInCreatingWorkspace

    if (
        documentLocationInCreatingWorkspace is None
        or documentLocationInCreatingWorkspace.path is None
    ):
        return output

    relative_path = documentLocationInCreatingWorkspace.path

    if path_prefix:
        relative_path = relative_path.replace(path_prefix, "")

    return (
        output
        + f"\n  Found in {relative_path}:{documentLocationInCreatingWorkspace.starting_line_number}:{documentLocationInCreatingWorkspace.starting_column_number}"
    )