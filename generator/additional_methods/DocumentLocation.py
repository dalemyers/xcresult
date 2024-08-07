@staticmethod
def empty() -> "DocumentLocation":
    """Create a new "empty" instance

    :returns: A new instance
    """
    instance = DocumentLocation.__new__(DocumentLocation)
    instance.concreteTypeName = ""
    instance.url = "file://#CharacterRangeLen=0&EndingColumnNumber=0&EndingLineNumber=0&StartingColumnNumber=0&StartingLineNumber=0"
    return instance


@property
def path(self) -> str:
    """Get the path of the document if set, empty string otherwise.

    :returns: The path of the document
    """
    return self.url.split("#", maxsplit=1)[0].replace("file://", "")


@property
def location(self) -> str:
    """Get the raw location inside the document

    :returns: The location inside the document
    """
    return self.url.split("#")[1]


@property
def location_details(self) -> dict[str, list[str]]:
    """Get the raw location parameters inside the document

    :returns: The location parametersinside the document
    """
    return urllib.parse.parse_qs(self.location)


def _get_property(self, key: str, *, offset: int = 0) -> int | None:
    """Get a property from the location details.

    :param key: The key for the property
    :param offset: Any offset to apply to the value (if found)

    :returns: The property as an int value if found, None otherwise
    """
    value = self.location_details.get(key)
    if value is None:
        return None
    return int(value[0]) + offset


@property
def character_range_length(self) -> int:
    """Get the character range length

    :returns: The character range length
    """
    return int(self.location_details["CharacterRangeLen"][0]) + 1


@property
def character_range_location(self) -> int | None:
    """Get the character range location if set, None otherwise

    :returns: The character range location
    """
    return self._get_property("CharacterRangeLoc")


@property
def ending_column_number(self) -> int | None:
    """Get the ending column number if set, None otherwise

    :returns: The ending column number
    """
    return self._get_property("EndingColumnNumber", offset=1)


@property
def ending_line_number(self) -> int | None:
    """Get the ending line number if set, None otherwise

    :returns: The ending line number
    """
    return self._get_property("EndingLineNumber", offset=1)


@property
def location_encoding(self) -> int | None:
    """Get the location encoding if set, None otherwise

    :returns: The location encoding
    """
    return self._get_property("LocationEncoding")


@property
def starting_column_number(self) -> int | None:
    """Get the starting column number if set, None otherwise

    :returns: The starting column number
    """
    return self._get_property("StartingColumnNumber", offset=1)


@property
def starting_line_number(self) -> int | None:
    """Get the starting line number if set, None otherwise

    :returns: The starting line number
    """
    return self._get_property("StartingLineNumber", offset=1)
