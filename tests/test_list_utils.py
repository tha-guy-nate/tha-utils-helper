import pytest

from tha_utils_helper import ListUtils


# --- chunk ---

def test_chunk_even_split() -> None:
    assert ListUtils.chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_uneven_split() -> None:
    assert ListUtils.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_size_larger_than_list() -> None:
    assert ListUtils.chunk([1, 2], 10) == [[1, 2]]


def test_chunk_size_equals_list() -> None:
    assert ListUtils.chunk([1, 2, 3], 3) == [[1, 2, 3]]


def test_chunk_size_one() -> None:
    assert ListUtils.chunk([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_empty_list() -> None:
    assert ListUtils.chunk([], 5) == []


def test_chunk_size_zero_raises() -> None:
    with pytest.raises(ValueError):
        ListUtils.chunk([1, 2, 3], 0)


def test_chunk_size_negative_raises() -> None:
    with pytest.raises(ValueError):
        ListUtils.chunk([1, 2, 3], -1)


def test_chunk_preserves_types() -> None:
    assert ListUtils.chunk(["a", "b", "c"], 2) == [["a", "b"], ["c"]]


# --- flatten ---

def test_flatten_basic() -> None:
    assert ListUtils.flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_uneven_sublists() -> None:
    assert ListUtils.flatten([[1], [2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]


def test_flatten_empty_outer() -> None:
    assert ListUtils.flatten([]) == []


def test_flatten_empty_inner() -> None:
    assert ListUtils.flatten([[], [], []]) == []


def test_flatten_single_sublist() -> None:
    assert ListUtils.flatten([[1, 2, 3]]) == [1, 2, 3]


def test_flatten_preserves_types() -> None:
    assert ListUtils.flatten([["a", "b"], ["c"]]) == ["a", "b", "c"]
