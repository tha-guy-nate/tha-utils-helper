import pytest
from tha_utils_helper import ThaStr, StrError


# ---------------------------------------------------------------------------
# format_str — single value
# ---------------------------------------------------------------------------

def test_format_str_strip() -> None:
    assert ThaStr.format_str("  hello  ") == "hello"

def test_format_str_no_strip() -> None:
    assert ThaStr.format_str("  hello  ", strip=False) == "  hello  "

def test_format_str_upper() -> None:
    assert ThaStr.format_str("hello", case="upper") == "HELLO"

def test_format_str_lower() -> None:
    assert ThaStr.format_str("HELLO", case="lower") == "hello"

def test_format_str_title() -> None:
    assert ThaStr.format_str("hello world", case="title") == "Hello World"

def test_format_str_replace_literal() -> None:
    assert ThaStr.format_str("hello world", replace={"world": "there"}) == "hello there"

def test_format_str_replace_regex() -> None:
    assert ThaStr.format_str("foo123bar", replace={r"\d+": "#"}, regex=True) == "foo#bar"

def test_format_str_invalid_case() -> None:
    with pytest.raises(StrError):
        ThaStr.format_str("hello", case="sentence")

def test_format_str_combined() -> None:
    assert ThaStr.format_str("  Hello World  ", case="lower", replace={"world": "there"}) == "hello there"


# ---------------------------------------------------------------------------
# slugify — single value
# ---------------------------------------------------------------------------

def test_slugify_basic() -> None:
    assert ThaStr.slugify("Hello World") == "hello-world"

def test_slugify_special_chars() -> None:
    assert ThaStr.slugify("foo & bar!") == "foo-bar"

def test_slugify_unicode() -> None:
    assert ThaStr.slugify("café") == "cafe"

def test_slugify_custom_sep() -> None:
    assert ThaStr.slugify("Hello World", sep="_") == "hello_world"

def test_slugify_prefix_suffix() -> None:
    assert ThaStr.slugify("hello", prefix="pre-", suffix="-suf") == "pre-hello-suf"

def test_slugify_collapses_seps() -> None:
    assert ThaStr.slugify("foo   bar") == "foo-bar"

def test_slugify_strips_leading_trailing_sep() -> None:
    assert ThaStr.slugify("--hello--") == "hello"


# ---------------------------------------------------------------------------
# format_str_rows
# ---------------------------------------------------------------------------

def test_format_str_rows_basic(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.format_str_rows(str_rows, "Name", case="lower")
    assert result[0]["Name"] == "alice smith"
    assert result[1]["Name"] == "bob jones"

def test_format_str_rows_immutability(str_runner: ThaStr, str_rows: list[dict]) -> None:
    original = [dict(r) for r in str_rows]
    str_runner.format_str_rows(str_rows, "Name", case="upper")
    assert str_rows[0]["Name"] == original[0]["Name"]

def test_format_str_rows_new_list(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.format_str_rows(str_rows, "Name")
    assert result is not str_rows

def test_format_str_rows_out_column(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.format_str_rows(str_rows, "Name", case="lower", out_column="Name Lower")
    assert "Name Lower" in result[0]
    assert result[0]["Name"] == "  Alice Smith  "

def test_format_str_rows_stores_self_rows(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.format_str_rows(str_rows, "Name")
    assert str_runner.rows is result

def test_format_str_rows_on_error_error(str_runner: ThaStr) -> None:
    bad_rows = [{"Name": 123, "row status": "", "message": ""}]
    result = str_runner.format_str_rows(bad_rows, "Name")
    assert result[0]["row status"] == "error"
    assert result[0]["Name"] == ""

def test_format_str_rows_on_error_skip(str_runner: ThaStr) -> None:
    bad_rows = [{"Name": 123, "row status": "", "message": ""}]
    result = str_runner.format_str_rows(bad_rows, "Name", on_error="skip")
    assert result[0]["Name"] == 123
    assert result[0]["row status"] == ""

def test_format_str_rows_on_error_blank(str_runner: ThaStr) -> None:
    bad_rows = [{"Name": 123, "row status": "", "message": ""}]
    result = str_runner.format_str_rows(bad_rows, "Name", on_error="blank")
    assert result[0]["Name"] == ""
    assert result[0]["row status"] == ""

def test_format_str_rows_skip_statuses_default(str_runner: ThaStr, str_rows: list[dict]) -> None:
    str_rows[0]["row status"] = "error"
    result = str_runner.format_str_rows(str_rows, "Name", case="upper")
    assert result[0]["Name"] == "  Alice Smith  "
    assert result[1]["Name"] == "BOB JONES"

def test_format_str_rows_skip_statuses_custom(str_runner: ThaStr, str_rows: list[dict]) -> None:
    str_rows[0]["row status"] = "pending"
    result = str_runner.format_str_rows(str_rows, "Name", case="upper", skip_statuses=["pending"])
    assert result[0]["Name"] == "  Alice Smith  "
    assert result[1]["Name"] == "BOB JONES"

def test_format_str_rows_skip_statuses_empty(str_runner: ThaStr, str_rows: list[dict]) -> None:
    str_rows[0]["row status"] = "error"
    result = str_runner.format_str_rows(str_rows, "Name", case="upper", skip_statuses=[])
    assert result[0]["Name"] == "ALICE SMITH"

def test_format_str_rows_invalid_on_error(str_runner: ThaStr, str_rows: list[dict]) -> None:
    with pytest.raises(StrError):
        str_runner.format_str_rows(str_rows, "Name", on_error="raise")


# ---------------------------------------------------------------------------
# slugify_rows
# ---------------------------------------------------------------------------

def test_slugify_rows_single_column(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.slugify_rows(str_rows, "Name", out_column="Slug")
    assert result[0]["Slug"] == "alice-smith"

def test_slugify_rows_multiple_columns(str_runner: ThaStr) -> None:
    rows = [{"First": "Alice", "Last": "Smith", "row status": "", "message": ""}]
    result = str_runner.slugify_rows(rows, ["First", "Last"], out_column="Slug")
    assert result[0]["Slug"] == "alice-smith"

def test_slugify_rows_immutability(str_runner: ThaStr, str_rows: list[dict]) -> None:
    original = [dict(r) for r in str_rows]
    str_runner.slugify_rows(str_rows, "Name", out_column="Slug")
    assert "Slug" not in str_rows[0]
    assert str_rows[0]["Name"] == original[0]["Name"]

def test_slugify_rows_new_list(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.slugify_rows(str_rows, "Name", out_column="Slug")
    assert result is not str_rows

def test_slugify_rows_stores_self_rows(str_runner: ThaStr, str_rows: list[dict]) -> None:
    result = str_runner.slugify_rows(str_rows, "Name", out_column="Slug")
    assert str_runner.rows is result

def test_slugify_rows_prefix_suffix(str_runner: ThaStr) -> None:
    rows = [{"Code": "abc 123", "row status": "", "message": ""}]
    result = str_runner.slugify_rows(rows, "Code", out_column="Slug", prefix="id-", suffix="-v1")
    assert result[0]["Slug"] == "id-abc-123-v1"

def test_slugify_rows_skip_statuses_default(str_runner: ThaStr, str_rows: list[dict]) -> None:
    str_rows[0]["row status"] = "error"
    result = str_runner.slugify_rows(str_rows, "Name", out_column="Slug")
    assert "Slug" not in result[0]

def test_slugify_rows_on_error_error(str_runner: ThaStr) -> None:
    bad_rows = [{"Name": None, "row status": "", "message": ""}]
    result = str_runner.slugify_rows(bad_rows, "Name", out_column="Slug")
    assert result[0]["row status"] == "error"
    assert result[0]["Slug"] == ""

def test_slugify_rows_on_error_blank(str_runner: ThaStr) -> None:
    bad_rows = [{"Name": None, "row status": "", "message": ""}]
    result = str_runner.slugify_rows(bad_rows, "Name", out_column="Slug", on_error="blank")
    assert result[0]["Slug"] == ""
    assert result[0]["row status"] == ""

def test_slugify_rows_invalid_on_error(str_runner: ThaStr, str_rows: list[dict]) -> None:
    with pytest.raises(StrError):
        str_runner.slugify_rows(str_rows, "Name", out_column="Slug", on_error="raise")
