def all_tests(self) -> list:
    """Get all subtests.

    :returns: All subtests
    """
    if not self.tests:
        return []

    return flatten(
        [
            test.all_subtests()
            for test in self.tests
            if isinstance(test, (ActionTestSummaryGroup, ActionTestMetadata))
        ]
    )
