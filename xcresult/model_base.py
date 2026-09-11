"""Strict, nonmutating decoding of ordinary modern xcresulttool JSON."""

from __future__ import annotations

from dataclasses import MISSING, fields, is_dataclass
import logging
import types
from typing import (
    ClassVar,
    Literal,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
    overload,
)

from xcresult.exceptions import MissingPropertyException, UnsupportedTypeException

_LOGGER = logging.getLogger(__name__)
_T = TypeVar("_T")
_Model = TypeVar("_Model", bound="XcresultObject")


class XcresultObject:
    """Base class for typed modern report dataclasses."""

    __test__: ClassVar[bool] = False

    @classmethod
    def from_dict(cls: type[_Model], data: object) -> _Model:
        """Decode a JSON object into this model without modifying the input."""
        return deserialize(data, cls)


@overload
def deserialize(data: object, target_type: type[_T]) -> _T: ...


@overload
def deserialize(data: object, target_type: object) -> object: ...


def deserialize(data: object, target_type: object) -> object:
    """Decode JSON into a model, alias, or collection with path-aware validation.

    :param data: Ordinary JSON values, not legacy ``_type`` envelopes.
    :param target_type: A dataclass or a supported Python type annotation.
    :returns: A new typed object tree.
    """
    return _deserialize(data, target_type, "$")


def _deserialize(data: object, target_type: object, path: str) -> object:
    """Recursively validate one value at its JSON property/index path."""
    origin = get_origin(target_type)
    arguments = cast(tuple[object, ...], get_args(target_type))
    if origin in (Union, types.UnionType):
        return _deserialize_union(data, arguments, path)
    if origin is Literal:
        # Apple's string enums grow over time; preserve unknown strings, not unknown types.
        if isinstance(data, str) and all(isinstance(member, str) for member in arguments):
            return data
        if any(type(data) is type(member) and data == member for member in arguments):
            return data
        raise UnsupportedTypeException(f"{path}: expected {target_type}, got {data!r}")
    if origin is list:
        if not isinstance(data, list) or len(arguments) != 1:
            raise UnsupportedTypeException(f"{path}: expected an array")
        return [
            _deserialize(value, arguments[0], f"{path}[{index}]")
            for index, value in enumerate(cast(list[object], data))
        ]
    if is_dataclass(target_type):
        return _deserialize_model(data, target_type, path)
    return _deserialize_primitive(data, target_type, path)


def _deserialize_union(data: object, arguments: tuple[object, ...], path: str) -> object:
    """Decode a union while preserving errors inside a single nullable member."""
    nonnull = tuple(member for member in arguments if member is not types.NoneType)
    if len(nonnull) != len(arguments):
        if data is None:
            return None
        if len(nonnull) == 1:
            return _deserialize(data, nonnull[0], path)
    failures: list[str] = []
    for member in arguments:
        try:
            return _deserialize(data, member, path)
        except (MissingPropertyException, UnsupportedTypeException) as error:
            failures.append(str(error))
    raise UnsupportedTypeException(f"{path}: no matching union member: {'; '.join(failures)}")


def _deserialize_model(data: object, target_type: object, path: str) -> object:
    """Decode dataclass fields and report unknown or missing properties."""
    if not isinstance(target_type, type) or not is_dataclass(target_type):
        raise UnsupportedTypeException(f"{path}: expected a dataclass type")
    if not isinstance(data, dict):
        raise UnsupportedTypeException(f"{path}: expected an object for {target_type.__name__}")
    # JSON dictionaries and typing's reflection APIs are the untyped generic boundary.
    if not all(isinstance(key, str) for key in cast(dict[object, object], data)):
        raise UnsupportedTypeException(f"{path}: expected string property names")
    values = cast(dict[str, object], data)
    hints = cast(dict[str, object], get_type_hints(target_type))
    model_fields = {field.name: field for field in fields(target_type) if field.init}
    for unknown in values.keys() - model_fields.keys():
        _LOGGER.warning("Unknown property %s.%s for %s", path, unknown, target_type.__name__)
    decoded: dict[str, object] = {}
    for name, field in model_fields.items():
        if name in values:
            decoded[name] = _deserialize(values[name], hints[name], f"{path}.{name}")
        elif field.default is MISSING and field.default_factory is MISSING:
            raise MissingPropertyException(f"{path}.{name}: missing required property")
    return target_type(**decoded)


def _deserialize_primitive(data: object, target_type: object, path: str) -> object:
    """Validate JSON scalar types without accepting bool as a numeric subtype."""
    if target_type in (None, types.NoneType):
        if data is None:
            return None
    elif target_type is float:
        # Exact types intentionally reject bool and other numeric subclasses.
        # pylint: disable-next=unidiomatic-typecheck
        if type(data) in (int, float):
            return float(cast(float, data))
    elif target_type is str or target_type is int or target_type is bool:
        # pylint: disable-next=unidiomatic-typecheck
        if type(data) is target_type:
            return data
    else:
        raise UnsupportedTypeException(f"{path}: unsupported target type {target_type!r}")
    raise UnsupportedTypeException(f"{path}: expected {target_type}, got {type(data).__name__}")
