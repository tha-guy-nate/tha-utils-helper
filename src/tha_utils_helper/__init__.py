"""tha-utils-helper: general-purpose utility classes for the tha-* ecosystem."""

from .date_utils import ThaDT
from .dict_utils import ThaDict
from .errors import DateError, NumError, StrError, UtilsError
from .list_utils import ThaList
from .num_utils import ThaNum
from .str_utils import ThaStr
from .type_utils import ThaType

# Backwards-compat aliases (old Utils names → new Tha* names)
DictUtils = ThaDict
ListUtils = ThaList
TypeUtils = ThaType

__version__ = "0.2.2"
__all__ = [
    "ThaDict",
    "ThaList",
    "ThaType",
    "ThaStr",
    "ThaNum",
    "ThaDT",
    "UtilsError",
    "StrError",
    "NumError",
    "DateError",
    # backwards-compat
    "DictUtils",
    "ListUtils",
    "TypeUtils",
]
