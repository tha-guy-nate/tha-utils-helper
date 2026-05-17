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


# --- normalize_bool_rows ---

def test_normalize_bool_rows_basic() -> None:
    rows = [{"active": "yes"}, {"active": "no"}]
    result = TypeUtils.normalize_bool_rows(rows, "active")
    assert result[0]["active"] is True
    assert result[1]["active"] is False

def test_normalize_bool_rows_out_column() -> None:
    rows = [{"active": "yes"}]
    result = TypeUtils.normalize_bool_rows(rows, "active", out_column="active_bool")
    assert result[0]["active_bool"] is True
    assert result[0]["active"] == "yes"

def test_normalize_bool_rows_invalid_returns_none() -> None:
    rows = [{"active": "maybe"}]
    result = TypeUtils.normalize_bool_rows(rows, "active")
    assert result[0]["active"] is None

def test_normalize_bool_rows_immutable() -> None:
    rows = [{"active": "yes"}]
    TypeUtils.normalize_bool_rows(rows, "active")
    assert rows[0]["active"] == "yes"

def test_normalize_bool_rows_returns_new_list() -> None:
    rows = [{"active": "yes"}]
    assert TypeUtils.normalize_bool_rows(rows, "active") is not rows

def test_normalize_bool_rows_empty() -> None:
    assert TypeUtils.normalize_bool_rows([], "active") == []


# --- safe_int_rows ---

def test_safe_int_rows_basic() -> None:
    rows = [{"count": "42"}, {"count": "abc"}]
    result = TypeUtils.safe_int_rows(rows, "count")
    assert result[0]["count"] == 42
    assert result[1]["count"] is None

def test_safe_int_rows_out_column() -> None:
    rows = [{"count": "42"}]
    result = TypeUtils.safe_int_rows(rows, "count", out_column="count_int")
    assert result[0]["count_int"] == 42
    assert result[0]["count"] == "42"

def test_safe_int_rows_returns_new_list() -> None:
    rows = [{"count": "1"}]
    assert TypeUtils.safe_int_rows(rows, "count") is not rows

def test_safe_int_rows_immutable() -> None:
    rows = [{"count": "42"}]
    TypeUtils.safe_int_rows(rows, "count")
    assert rows[0]["count"] == "42"

def test_safe_int_rows_empty() -> None:
    assert TypeUtils.safe_int_rows([], "count") == []


# --- safe_float_rows ---

def test_safe_float_rows_basic() -> None:
    rows = [{"amount": "3.14"}, {"amount": "bad"}]
    result = TypeUtils.safe_float_rows(rows, "amount")
    assert result[0]["amount"] == pytest.approx(3.14)
    assert result[1]["amount"] is None

def test_safe_float_rows_out_column() -> None:
    rows = [{"amount": "3.14"}]
    result = TypeUtils.safe_float_rows(rows, "amount", out_column="amount_float")
    assert result[0]["amount_float"] == pytest.approx(3.14)
    assert result[0]["amount"] == "3.14"

def test_safe_float_rows_returns_new_list() -> None:
    rows = [{"amount": "1.0"}]
    assert TypeUtils.safe_float_rows(rows, "amount") is not rows

def test_safe_float_rows_empty() -> None:
    assert TypeUtils.safe_float_rows([], "amount") == []
