def pretty_message(self, path_prefix: Optional[str]) -> str:
    """Format the message nicely for review.

    :param path_prefix: Any path prefix to remove

    :returns: A pretty message
    """
    if self.documentLocationInCreatingWorkspace is None:
        return f"* [ERROR] {self.message}"

    relative_path = self.documentLocationInCreatingWorkspace.path

    if path_prefix:
        relative_path = relative_path.replace(path_prefix, "")

    return f"* [ERROR] {self.message}\n  Found in {relative_path}:{self.documentLocationInCreatingWorkspace.starting_line_number}:{self.documentLocationInCreatingWorkspace.starting_column_number}"
