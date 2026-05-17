class UtilsError(Exception):
    """Base class for tha-utils-helper errors."""


class StrError(UtilsError):
    """Raised for invalid string operation configuration or unparseable values."""


class NumError(UtilsError):
    """Raised for invalid numeric configuration or unparseable values."""


class DateError(UtilsError):
    """Raised for invalid date values or unrecognized date formats."""
