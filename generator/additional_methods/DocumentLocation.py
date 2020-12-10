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
    return self.url.split("#")[0].replace("file://", "")


@property
def location(self) -> str:
    return self.url.split("#")[1]


@property
def location_details(self) -> str:
    return urllib.parse.parse_qs(self.location)


def _get_property(self, key: str, *, offset: int = 0) -> Optional[int]:
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
    return int(self.location_details["CharacterRangeLen"][0]) + 1


@property
def character_range_location(self) -> Optional[int]:
    return self._get_property("CharacterRangeLoc")


@property
def ending_column_number(self) -> Optional[int]:
    return self._get_property("EndingColumnNumber", offset=1)


@property
def ending_line_number(self) -> Optional[int]:
    return self._get_property("EndingLineNumber", offset=1)


@property
def location_encoding(self) -> Optional[int]:
    return self._get_property("LocationEncoding")


@property
def starting_column_number(self) -> Optional[int]:
    return self._get_property("StartingColumnNumber", offset=1)


@property
def starting_line_number(self) -> Optional[int]:
    return self._get_property("StartingLineNumber", offset=1)
