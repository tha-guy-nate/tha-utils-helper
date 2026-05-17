from __future__ import annotations

from collections.abc import Collection
from typing import Any


class DictUtils:
    @staticmethod
    def pick(d: dict[str, Any], keys: Collection[str]) -> dict[str, Any]:
        return {k: v for k, v in d.items() if k in keys}

    @staticmethod
    def omit(d: dict[str, Any], keys: Collection[str]) -> dict[str, Any]:
        return {k: v for k, v in d.items() if k not in keys}

    @staticmethod
    def safe_get(d: dict[str, Any], *keys: str) -> Any:
        current: Any = d
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current

    @staticmethod
    def rename_keys(d: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
        return {mapping.get(k, k): v for k, v in d.items()}

    @staticmethod
    def pick_rows(rows: list[dict[str, Any]], keys: Collection[str]) -> list[dict[str, Any]]:
        return [DictUtils.pick(row, keys) for row in rows]

    @staticmethod
    def omit_rows(rows: list[dict[str, Any]], keys: Collection[str]) -> list[dict[str, Any]]:
        return [DictUtils.omit(row, keys) for row in rows]

    @staticmethod
    def rename_keys_rows(
        rows: list[dict[str, Any]], mapping: dict[str, str]
    ) -> list[dict[str, Any]]:
        return [DictUtils.rename_keys(row, mapping) for row in rows]
