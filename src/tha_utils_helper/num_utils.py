from __future__ import annotations

from typing import Any

from .errors import NumError

_CURRENCY = frozenset("$€£¥₹₩₽₺₫฿₱₴")


class ThaNum:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    @staticmethod
    def format_num(
        value: str | int | float,
        *,
        strip_currency: bool = True,
        strip_commas: bool = True,
        round_to: int | None = None,
        cast: str = "float",
    ) -> float | int:
        if cast not in ("float", "int"):
            raise NumError(f"Invalid cast {cast!r} — must be 'float' or 'int'")

        if isinstance(value, bool):
            raise NumError(f"Cannot parse {value!r} as a number")

        if isinstance(value, (int, float)):
            result = float(value)
        else:
            cleaned = str(value).strip()

            negative = False
            if cleaned.startswith("(") and cleaned.endswith(")"):
                negative = True
                cleaned = cleaned[1:-1].strip()

            if strip_currency:
                cleaned = "".join(c for c in cleaned if c not in _CURRENCY).strip()

            if strip_commas:
                cleaned = cleaned.replace(",", "")

            cleaned = cleaned.strip()

            try:
                result = float(cleaned)
            except ValueError:
                raise NumError(f"Cannot parse {value!r} as a number")

            if negative:
                result = -result

        if round_to is not None:
            result = round(result, round_to)

        if cast == "int":
            return int(result)
        return result

    def format_num_rows(
        self,
        rows: list[dict[str, Any]],
        column: str,
        *,
        strip_currency: bool = True,
        strip_commas: bool = True,
        round_to: int | None = None,
        cast: str = "float",
        out_column: str | None = None,
        on_error: str = "error",
        skip_statuses: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if on_error not in ("error", "skip", "blank"):
            raise NumError(f"Invalid on_error {on_error!r} — must be 'error', 'skip', or 'blank'")

        _skip = ["error", "warning"] if skip_statuses is None else skip_statuses
        target = out_column if out_column is not None else column
        result = []

        for row in rows:
            if row.get("row status") in _skip:
                result.append(dict(row))
                continue

            row_copy = dict(row)
            try:
                row_copy[target] = self.format_num(
                    row_copy[column],
                    strip_currency=strip_currency,
                    strip_commas=strip_commas,
                    round_to=round_to,
                    cast=cast,
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
