import pytest

from tha_utils_helper import chunk_list


def test_chunk_even_split() -> None:
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_uneven_split() -> None:
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_size_larger_than_list() -> None:
    assert chunk_list([1, 2], 10) == [[1, 2]]


def test_chunk_size_equals_list() -> None:
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]


def test_chunk_size_one() -> None:
    assert chunk_list([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_empty_list() -> None:
    assert chunk_list([], 5) == []


def test_chunk_size_zero_raises() -> None:
    with pytest.raises(ValueError):
        chunk_list([1, 2, 3], 0)


def test_chunk_size_negative_raises() -> None:
    with pytest.raises(ValueError):
        chunk_list([1, 2, 3], -1)


def test_chunk_preserves_types() -> None:
    result = chunk_list(["a", "b", "c"], 2)
    assert result == [["a", "b"], ["c"]]
