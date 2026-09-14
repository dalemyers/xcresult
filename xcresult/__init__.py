"""A module for dealing with xcresults."""

# This is the 'umbrella' import for the module so we need to import everything
# pylint: disable=unused-import
# pyright: reportUnusedImport=false
from xcresult import source_url
from xcresult import xcresulttool
from xcresult.exceptions import (
    MissingPropertyException,
    UnsupportedTypeException,
    XcresultException,
)
from xcresult.model import *
from xcresult.model_base import XcresultObject, deserialize

# xcresult.model exports a generated SourceLocation wire type, so only the
# decoding helper is re-exported here. Use xcresult.source_url.SourceLocation
# for the decoded issue location type.
from xcresult.source_url import parse_source_url
from xcresult.xcresults import Xcresults

# pylint: enable=unused-import
