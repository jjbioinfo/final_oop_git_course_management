"""Shared validation helpers for the Course Management System."""

from numbers import Integral


def require_text(value: object, field_name: str) -> str:
    """Return non-empty text after removing surrounding spaces."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be text")
    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned_value


def require_identifier(value: object, field_name: str) -> str:
    """Return a non-empty string representation of an identifier."""
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError(f"{field_name} must be a string or integer")
    cleaned_value = str(value).strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned_value


def require_positive_integer(value: object, field_name: str) -> int:
    """Return an integer greater than zero."""
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{field_name} must be a whole number")
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return int(value)
