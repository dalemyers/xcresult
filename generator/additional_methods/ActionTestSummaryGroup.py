def all_subtests(self) -> list[ActionTestSummaryIdentifiableObject]:
    """Get all subtests.

    :returns: All subtests
    """
    if not self.subtests:
        return []

    return flatten(
        [
            test.all_subtests()
            for test in self.subtests
            if isinstance(test, (ActionTestSummaryGroup, ActionTestMetadata))
        ]
    )
