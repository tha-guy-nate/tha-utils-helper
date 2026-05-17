from __future__ import annotations

from typing import Any


class TypeUtils:
    _TRUTHY = {"true", "yes", "1", "t", "y"}
    _FALSY = {"false", "no", "0", "f", "n"}

    @staticmethod
    def normalize_bool(val: Any) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, int):
            if val == 1:
                return True
            if val == 0:
                return False
        if isinstance(val, str):
            normalized = val.strip().lower()
            if normalized in TypeUtils._TRUTHY:
                return True
            if normalized in TypeUtils._FALSY:
                return False
        raise ValueError(f"Cannot normalize {val!r} to bool")

    @staticmethod
    def safe_int(val: Any) -> int | None:
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def safe_float(val: Any) -> float | None:
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def normalize_bool_rows(
        rows: list[dict[str, Any]],
        column: str,
        *,
        out_column: str | None = None,
    ) -> list[dict[str, Any]]:
        target = out_column if out_column is not None else column
        result = []
        for row in rows:
            row_copy = dict(row)
            try:
                row_copy[target] = TypeUtils.normalize_bool(row_copy[column])
            except (ValueError, TypeError):
                row_copy[target] = None
            result.append(row_copy)
        return result

    @staticmethod
    def safe_int_rows(
        rows: list[dict[str, Any]],
        column: str,
        *,
        out_column: str | None = None,
    ) -> list[dict[str, Any]]:
        target = out_column if out_column is not None else column
        return [{**row, target: TypeUtils.safe_int(row[column])} for row in rows]

    @staticmethod
    def safe_float_rows(
        rows: list[dict[str, Any]],
        column: str,
        *,
        out_column: str | None = None,
    ) -> list[dict[str, Any]]:
        target = out_column if out_column is not None else column
        return [{**row, target: TypeUtils.safe_float(row[column])} for row in rows]
