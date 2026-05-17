import pytest
from tha_utils_helper import ThaNum, NumError


# ---------------------------------------------------------------------------
# format_num — single value
# ---------------------------------------------------------------------------

def test_format_num_plain_float() -> None:
    assert ThaNum.format_num("3.14") == 3.14

def test_format_num_plain_int_string() -> None:
    assert ThaNum.format_num("42") == 42.0

def test_format_num_currency_dollar() -> None:
    assert ThaNum.format_num("$1,234.56") == 1234.56

def test_format_num_currency_pound() -> None:
    assert ThaNum.format_num("£2,000.00") == 2000.0

def test_format_num_currency_euro() -> None:
    assert ThaNum.format_num("€9.99") == 9.99

def test_format_num_no_strip_currency() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num("$100", strip_currency=False)

def test_format_num_no_strip_commas() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num("1,000", strip_commas=False)

def test_format_num_parenthetical_negative() -> None:
    assert ThaNum.format_num("(500)") == -500.0

def test_format_num_parenthetical_negative_with_currency() -> None:
    assert ThaNum.format_num("($1,200.00)") == -1200.0

def test_format_num_cast_int() -> None:
    assert ThaNum.format_num("3.7", cast="int") == 3
    assert isinstance(ThaNum.format_num("3.7", cast="int"), int)

def test_format_num_cast_float_default() -> None:
    result = ThaNum.format_num("3")
    assert isinstance(result, float)

def test_format_num_round_to() -> None:
    assert ThaNum.format_num("3.14159", round_to=2) == 3.14

def test_format_num_from_int() -> None:
    assert ThaNum.format_num(42) == 42.0

def test_format_num_from_float() -> None:
    assert ThaNum.format_num(3.14) == 3.14

def test_format_num_whitespace() -> None:
    assert ThaNum.format_num("  100  ") == 100.0

def test_format_num_invalid_string() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num("N/A")

def test_format_num_empty_string() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num("")

def test_format_num_bool_raises() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num(True)  # type: ignore[arg-type]

def test_format_num_invalid_cast() -> None:
    with pytest.raises(NumError):
        ThaNum.format_num("1", cast="str")


# ---------------------------------------------------------------------------
# format_num_rows
# ---------------------------------------------------------------------------

def test_format_num_rows_basic(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount")
    assert result[0]["Amount"] == 1234.56
    assert result[1]["Amount"] == 2000.0
    assert result[2]["Amount"] == 500.0

def test_format_num_rows_immutability(num_runner: ThaNum, num_rows: list[dict]) -> None:
    original_val = num_rows[0]["Amount"]
    num_runner.format_num_rows(num_rows, "Amount")
    assert num_rows[0]["Amount"] == original_val

def test_format_num_rows_new_list(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount")
    assert result is not num_rows

def test_format_num_rows_out_column(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount", out_column="Amount Parsed")
    assert "Amount Parsed" in result[0]
    assert result[0]["Amount"] == "$1,234.56"

def test_format_num_rows_stores_self_rows(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount")
    assert num_runner.rows is result

def test_format_num_rows_cast_int(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount", cast="int")
    assert result[0]["Amount"] == 1234
    assert isinstance(result[0]["Amount"], int)

def test_format_num_rows_round_to(num_runner: ThaNum, num_rows: list[dict]) -> None:
    result = num_runner.format_num_rows(num_rows, "Amount", round_to=1)
    assert result[0]["Amount"] == 1234.6

def test_format_num_rows_on_error_error(num_runner: ThaNum) -> None:
    bad_rows = [{"Amount": "N/A", "row status": "", "message": ""}]
    result = num_runner.format_num_rows(bad_rows, "Amount")
    assert result[0]["row status"] == "error"
    assert result[0]["Amount"] == ""

def test_format_num_rows_on_error_skip(num_runner: ThaNum) -> None:
    bad_rows = [{"Amount": "N/A", "row status": "", "message": ""}]
    result = num_runner.format_num_rows(bad_rows, "Amount", on_error="skip")
    assert result[0]["Amount"] == "N/A"
    assert result[0]["row status"] == ""

def test_format_num_rows_on_error_blank(num_runner: ThaNum) -> None:
    bad_rows = [{"Amount": "N/A", "row status": "", "message": ""}]
    result = num_runner.format_num_rows(bad_rows, "Amount", on_error="blank")
    assert result[0]["Amount"] == ""
    assert result[0]["row status"] == ""

def test_format_num_rows_skip_statuses_default(num_runner: ThaNum, num_rows: list[dict]) -> None:
    num_rows[0]["row status"] = "error"
    result = num_runner.format_num_rows(num_rows, "Amount")
    assert result[0]["Amount"] == "$1,234.56"
    assert result[1]["Amount"] == 2000.0

def test_format_num_rows_skip_statuses_custom(num_runner: ThaNum, num_rows: list[dict]) -> None:
    num_rows[0]["row status"] = "pending"
    result = num_runner.format_num_rows(num_rows, "Amount", skip_statuses=["pending"])
    assert result[0]["Amount"] == "$1,234.56"
    assert result[1]["Amount"] == 2000.0

def test_format_num_rows_skip_statuses_empty(num_runner: ThaNum, num_rows: list[dict]) -> None:
    num_rows[0]["row status"] = "error"
    result = num_runner.format_num_rows(num_rows, "Amount", skip_statuses=[])
    assert result[0]["Amount"] == 1234.56

def test_format_num_rows_invalid_on_error(num_runner: ThaNum, num_rows: list[dict]) -> None:
    with pytest.raises(NumError):
        num_runner.format_num_rows(num_rows, "Amount", on_error="raise")

def test_format_num_rows_empty_input(num_runner: ThaNum) -> None:
    assert num_runner.format_num_rows([], "Amount") == []
