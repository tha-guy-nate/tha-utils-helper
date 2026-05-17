from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def chunk_list(lst: list[T], size: int) -> list[list[T]]:
    if size < 1:
        raise ValueError("size must be >= 1")
    return [lst[i : i + size] for i in range(0, len(lst), size)]
