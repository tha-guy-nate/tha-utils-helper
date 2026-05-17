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
