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