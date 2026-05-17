import pytest

from tha_utils_helper import TypeUtils


# --- normalize_bool ---

def test_normalize_bool_true_bool() -> None:
    assert TypeUtils.normalize_bool(True) is True


def test_normalize_bool_false_bool() -> None:
    assert TypeUtils.normalize_bool(False) is False


def test_normalize_bool_int_one() -> None:
    assert TypeUtils.normalize_bool(1) is True


def test_normalize_bool_int_zero() -> None:
    assert TypeUtils.normalize_bool(0) is False


def test_normalize_bool_string_true_variants() -> None:
    for val in ("true", "True", "TRUE", "yes", "Yes", "1", "t", "y"):
        assert TypeUtils.normalize_bool(val) is True, f"expected True for {val!r}"


def test_normalize_bool_string_false_variants() -> None:
    for val in ("false", "False", "FALSE", "no", "No", "0", "f", "n"):
        assert TypeUtils.normalize_bool(val) is False, f"expected False for {val!r}"


def test_normalize_bool_whitespace_stripped() -> None:
    assert TypeUtils.normalize_bool("  true  ") is True


def test_normalize_bool_invalid_raises() -> None:
    with pytest.raises(ValueError):
        TypeUtils.normalize_bool("maybe")


def test_normalize_bool_none_raises() -> None:
    with pytest.raises((ValueError, TypeError)):
        TypeUtils.normalize_bool(None)


# --- safe_int ---

def test_safe_int_valid_string() -> None:
    assert TypeUtils.safe_int("42") == 42


def test_safe_int_valid_int() -> None:
    assert TypeUtils.safe_int(7) == 7


def test_safe_int_float_string() -> None:
    assert TypeUtils.safe_int("3.14") is None


def test_safe_int_invalid_string() -> None:
    assert TypeUtils.safe_int("abc") is None


def test_safe_int_none() -> None:
    assert TypeUtils.safe_int(None) is None


def test_safe_int_empty_string() -> None:
    assert TypeUtils.safe_int("") is None


# --- safe_float ---

def test_safe_float_valid_string() -> None:
    assert TypeUtils.safe_float("3.14") == pytest.approx(3.14)


def test_safe_float_int_string() -> None:
    assert TypeUtils.safe_float("42") == 42.0


def test_safe_float_valid_float() -> None:
    assert TypeUtils.safe_float(1.5) == 1.5


def test_safe_float_invalid_string() -> None:
    assert TypeUtils.safe_float("abc") is None


def test_safe_float_none() -> None:
    assert TypeUtils.safe_float(None) is None


def test_safe_float_empty_string() -> None:
    assert TypeUtils.safe_float("") is None
