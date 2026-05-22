import re

import pytest
from tha_utils_helper import ThaDT, DateError


# --- ThaDT.now ---

def test_now_default_format() -> None:
    result = ThaDT.now()
    assert re.match(r"\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}", result)

def test_now_custom_format() -> None:
    result = ThaDT.now("%m/%d/%Y")
    assert re.match(r"\d{2}/\d{2}/\d{4}", result)


# --- ThaDT.format_date: input format coverage ---

def test_iso_date() -> None:
    assert ThaDT.format_date("2024-04-15", "%m/%d") == "04/15"

def test_us_slash_full() -> None:
    assert ThaDT.format_date("04/15/2024", "%Y-%m-%d") == "2024-04-15"

def test_us_slash_short_year() -> None:
    assert ThaDT.format_date("04/15/24", "%Y-%m-%d") == "2024-04-15"

def test_us_dash_full() -> None:
    assert ThaDT.format_date("04-15-2024", "%Y-%m-%d") == "2024-04-15"

def test_us_dash_short_year() -> None:
    assert ThaDT.format_date("04-15-24", "%Y-%m-%d") == "2024-04-15"

def test_compact_iso() -> None:
    assert ThaDT.format_date("20240415", "%m/%d/%Y") == "04/15/2024"

def test_iso_slash() -> None:
    assert ThaDT.format_date("2024/04/15", "%m/%d/%Y") == "04/15/2024"

def test_long_month_name() -> None:
    assert ThaDT.format_date("April 15, 2024", "%m/%d/%Y") == "04/15/2024"

def test_short_month_name() -> None:
    assert ThaDT.format_date("Apr 15, 2024", "%m/%d/%Y") == "04/15/2024"

def test_long_month_no_comma() -> None:
    assert ThaDT.format_date("April 15 2024", "%Y-%m-%d") == "2024-04-15"

def test_short_month_no_comma() -> None:
    assert ThaDT.format_date("Apr 15 2024", "%Y-%m-%d") == "2024-04-15"

def test_iso_year_month() -> None:
    assert ThaDT.format_date("2024-04", "%m/%Y") == "04/2024"

def test_oracle_format_full_year() -> None:
    assert ThaDT.format_date("15-Jan-2024", "%m/%d/%Y") == "01/15/2024"

def test_oracle_format_short_year() -> None:
    assert ThaDT.format_date("15-Jan-24", "%m/%d/%Y") == "01/15/2024"

def test_day_first_long_month() -> None:
    assert ThaDT.format_date("15 April 2024", "%m/%d/%Y") == "04/15/2024"

def test_day_first_short_month() -> None:
    assert ThaDT.format_date("15 Apr 2024", "%m/%d/%Y") == "04/15/2024"

def test_strips_whitespace() -> None:
    assert ThaDT.format_date("  2024-04-15  ", "%m/%d") == "04/15"

def test_unrecognized_raises() -> None:
    with pytest.raises(DateError, match="Unrecognized"):
        ThaDT.format_date("not-a-date", "%m/%d")


# --- No-year inputs always raise ---

def test_us_slash_no_year_raises() -> None:
    with pytest.raises(DateError, match="year"):
        ThaDT.format_date("04/15", "%m/%d/%Y")

def test_short_month_no_year_raises() -> None:
    with pytest.raises(DateError, match="year"):
        ThaDT.format_date("Apr 15", "%m/%d/%Y")

def test_long_month_no_year_raises() -> None:
    with pytest.raises(DateError, match="year"):
        ThaDT.format_date("April 15", "%m/%d/%Y")

def test_day_dash_month_abbv_no_year_raises() -> None:
    with pytest.raises(DateError, match="year"):
        ThaDT.format_date("15-Jan", "%m/%d/%Y")


# --- Output format coverage ---

def test_output_includes_year() -> None:
    assert ThaDT.format_date("2024-04-15", "%m/%d/%Y") == "04/15/2024"

def test_output_month_day_year_short() -> None:
    assert ThaDT.format_date("2024-04-15", "%m/%d/%y") == "04/15/24"

def test_output_full_month_name() -> None:
    assert ThaDT.format_date("2024-04-15", "%B %d, %Y") == "April 15, 2024"

def test_output_oracle_style() -> None:
    assert ThaDT.format_date("2024-01-15", "%d-%b") == "15-Jan"


# --- ThaDT.format_date_rows ---

def test_rows_basic(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    result = dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d")
    assert result[0]["Start Date"] == "04/15"
    assert result[1]["Start Date"] == "04/16"
    assert result[2]["Start Date"] == "04/17"

def test_rows_out_column(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    result = dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d", out_column="Short Date")
    assert result[0]["Short Date"] == "04/15"
    assert result[0]["Start Date"] == "2024-04-15"

def test_rows_input_not_mutated(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    original = [r.copy() for r in dt_rows]
    dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d")
    assert dt_rows == original

def test_rows_returns_new_list(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    result = dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d")
    assert result is not dt_rows

def test_rows_count_preserved(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    result = dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d")
    assert len(result) == len(dt_rows)

def test_rows_stores_result(dt_runner: ThaDT, dt_rows: list[dict]) -> None:
    result = dt_runner.format_date_rows(dt_rows, "Start Date", "%m/%d")
    assert dt_runner.rows is result

def test_rows_on_error_sets_status(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "not-a-date"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", on_error="error")
    assert result[0]["row status"] == "error"
    assert "Unrecognized" in result[0]["message"]
    assert result[0]["Start Date"] == ""

def test_rows_no_year_sets_status(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "04/15"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d/%Y", on_error="error")
    assert result[0]["row status"] == "error"
    assert "year" in result[0]["message"]

def test_rows_on_error_skip_leaves_row_unchanged(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "not-a-date"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", on_error="skip")
    assert result[0]["Start Date"] == "not-a-date"
    assert "row status" not in result[0]

def test_rows_on_error_blank_adds_empty(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "not-a-date"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", on_error="blank")
    assert result[0]["Start Date"] == ""
    assert result[0].get("row status") != "error"

def test_rows_invalid_on_error_raises(dt_runner: ThaDT) -> None:
    with pytest.raises(DateError, match="on_error"):
        dt_runner.format_date_rows([], "Start Date", "%m/%d", on_error="bad")

def test_rows_skip_error_status_by_default(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "2024-04-15", "row status": "error", "message": "prior"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d")
    assert result[0]["Start Date"] == "2024-04-15"
    assert result[0]["message"] == "prior"

def test_rows_skip_warning_status_by_default(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "2024-04-15", "row status": "warning"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d")
    assert result[0]["Start Date"] == "2024-04-15"

def test_rows_custom_skip_statuses(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "2024-04-15", "row status": "pending"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", skip_statuses=["pending"])
    assert result[0]["Start Date"] == "2024-04-15"

def test_rows_empty_skip_statuses_processes_all(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": "2024-04-15", "row status": "error"}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", skip_statuses=[])
    assert result[0]["Start Date"] == "04/15"

def test_rows_empty_column_on_error(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": ""}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", on_error="error")
    assert result[0]["row status"] == "error"
    assert result[0]["Start Date"] == ""

def test_rows_empty_column_blank(dt_runner: ThaDT) -> None:
    rows = [{"id": "1", "Start Date": ""}]
    result = dt_runner.format_date_rows(rows, "Start Date", "%m/%d", on_error="blank")
    assert result[0]["Start Date"] == ""
    assert result[0].get("row status") != "error"

def test_rows_empty_input_returns_empty(dt_runner: ThaDT) -> None:
    result = dt_runner.format_date_rows([], "Start Date", "%m/%d")
    assert result == []
