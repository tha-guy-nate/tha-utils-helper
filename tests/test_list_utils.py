import pytest

from tha_utils_helper import ThaList


# --- chunk ---

def test_chunk_even_split() -> None:
    assert ThaList.chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_uneven_split() -> None:
    assert ThaList.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_size_larger_than_list() -> None:
    assert ThaList.chunk([1, 2], 10) == [[1, 2]]


def test_chunk_size_equals_list() -> None:
    assert ThaList.chunk([1, 2, 3], 3) == [[1, 2, 3]]


def test_chunk_size_one() -> None:
    assert ThaList.chunk([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_empty_list() -> None:
    assert ThaList.chunk([], 5) == []


def test_chunk_size_zero_raises() -> None:
    with pytest.raises(ValueError):
        ThaList.chunk([1, 2, 3], 0)


def test_chunk_size_negative_raises() -> None:
    with pytest.raises(ValueError):
        ThaList.chunk([1, 2, 3], -1)


def test_chunk_preserves_types() -> None:
    assert ThaList.chunk(["a", "b", "c"], 2) == [["a", "b"], ["c"]]


# --- flatten ---

def test_flatten_basic() -> None:
    assert ThaList.flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_uneven_sublists() -> None:
    assert ThaList.flatten([[1], [2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]


def test_flatten_empty_outer() -> None:
    assert ThaList.flatten([]) == []


def test_flatten_empty_inner() -> None:
    assert ThaList.flatten([[], [], []]) == []


def test_flatten_single_sublist() -> None:
    assert ThaList.flatten([[1, 2, 3]]) == [1, 2, 3]


def test_flatten_preserves_types() -> None:
    assert ThaList.flatten([["a", "b"], ["c"]]) == ["a", "b", "c"]
