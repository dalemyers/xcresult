"""Exception definitions."""


class XcresultException(Exception):
    """Base result type for exceptions."""


class UnsupportedTypeException(XcresultException):
    """A new and, as yet, unsupported type."""


class MissingPropertyException(XcresultException):
    """A required property is missing."""
