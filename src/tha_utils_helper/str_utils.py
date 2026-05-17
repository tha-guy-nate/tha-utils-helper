from __future__ import annotations

import re
import unicodedata
from typing import Any

from .errors import StrError


class ThaStr:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    @staticmethod
    def format_str(
        value: str,
        *,
        strip: bool = True,
        case: str | None = None,
        replace: dict[str, str] | None = None,
        regex: bool = False,
    ) -> str:
        if case not in (None, "upper", "lower", "title"):
            raise StrError(f"Invalid case {case!r} — must be 'upper', 'lower', 'title', or None")

        result = value
        if strip:
            result = result.strip()
        if case == "upper":
            result = result.upper()
        elif case == "lower":
            result = result.lower()
        elif case == "title":
            result = result.title()
        if replace:
            for pattern, repl in replace.items():
                if regex:
                    result = re.sub(pattern, repl, result)
                else:
                    result = result.replace(pattern, repl)
        return result

    @staticmethod
    def slugify(
        value: str,
        *,
        sep: str = "-",
        prefix: str = "",
        suffix: str = "",
    ) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        ascii_str = normalized.encode("ascii", "ignore").decode("ascii")
        lowered = ascii_str.lower()
        slug = re.sub(r"[^a-z0-9]+", sep, lowered)
        slug = slug.strip(sep)
        return f"{prefix}{slug}{suffix}"

    def format_str_rows(
        self,
        rows: list[dict[str, Any]],
        column: str,
        *,
        strip: bool = True,
        case: str | None = None,
        replace: dict[str, str] | None = None,
        regex: bool = False,
        out_column: str | None = None,
        on_error: str = "error",
        skip_statuses: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if on_error not in ("error", "skip", "blank"):
            raise StrError(f"Invalid on_error {on_error!r} — must be 'error', 'skip', or 'blank'")

        _skip = ["error", "warning"] if skip_statuses is None else skip_statuses
        target = out_column if out_column is not None else column
        result = []

        for row in rows:
            if row.get("row status") in _skip:
                result.append(dict(row))
                continue

            row_copy = dict(row)
            try:
                row_copy[target] = self.format_str(
                    row_copy[column],
                    strip=strip,
                    case=case,
                    replace=replace,
                    regex=regex,
                )
            except Exception as exc:
                if on_error == "error":
                    row_copy[target] = ""
                    row_copy["row status"] = "error"
                    row_copy["message"] = str(exc)
                elif on_error == "blank":
                    row_copy[target] = ""

            result.append(row_copy)

        self.rows = result
        return result

    def slugify_rows(
        self,
        rows: list[dict[str, Any]],
        columns: str | list[str],
        out_column: str,
        *,
        sep: str = "-",
        prefix: str = "",
        suffix: str = "",
        on_error: str = "error",
        skip_statuses: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if on_error not in ("error", "skip", "blank"):
            raise StrError(f"Invalid on_error {on_error!r} — must be 'error', 'skip', or 'blank'")

        _skip = ["error", "warning"] if skip_statuses is None else skip_statuses
        col_list = [columns] if isinstance(columns, str) else columns
        result = []

        for row in rows:
            if row.get("row status") in _skip:
                result.append(dict(row))
                continue

            row_copy = dict(row)
            try:
                values = []
                for c in col_list:
                    val = row_copy[c]
                    if not isinstance(val, str):
                        raise TypeError(f"Column {c!r} value must be a string, got {type(val).__name__}")
                    values.append(val)
                combined = sep.join(values)
                row_copy[out_column] = self.slugify(combined, sep=sep, prefix=prefix, suffix=suffix)
            except Exception as exc:
                if on_error == "error":
                    row_copy[out_column] = ""
                    row_copy["row status"] = "error"
                    row_copy["message"] = str(exc)
                elif on_error == "blank":
                    row_copy[out_column] = ""

            result.append(row_copy)

        self.rows = result
        return result
