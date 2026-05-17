# tha-utils-helper

[![CI](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml)

A Tabular Helper utility library for the `tha-*` ecosystem. Includes general-purpose dict/list/type helpers, string normalization and slugification, numeric string parsing, and date format conversion — all with row-level error handling for CSV pipeline use.

## Install

```bash
pip install tha-utils-helper
```

## Quick start

```python
from tha_utils_helper import DictUtils, ListUtils, TypeUtils, ThaStr, ThaNum, ThaDT

# Structural helpers — work on single values or lists of row dicts
DictUtils.pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])         # {"a": 1, "c": 3}
DictUtils.rename_keys_rows(rows, {"studentUniqueId": "id"})   # rename across all rows

# String normalization
ThaStr.format_str("  HELLO WORLD  ", case="lower")            # "hello world"
ThaStr.slugify("Hello World!")                                 # "hello-world"

# Numeric parsing
ThaNum.format_num("$1,234.56")                                 # 1234.56
ThaNum.format_num("(£500)", cast="int")                        # -500

# Date formatting
ThaDT.format_date("Apr 15, 2024", "%Y-%m-%d")                 # "2024-04-15"

# Row-level processing with on_error and skip_statuses
formatter = ThaNum()
rows = formatter.format_num_rows(rows, column="Budget", cast="float", round_to=2)
```

---

## API

### `DictUtils`

Static methods for single dicts and lists of row dicts.

```python
DictUtils.pick(d, keys)               # new dict with only the specified keys
DictUtils.omit(d, keys)               # new dict with the specified keys removed
DictUtils.safe_get(d, *keys)          # traverse nested dicts safely — returns None on miss
DictUtils.rename_keys(d, mapping)     # rename keys; unmapped keys are preserved

DictUtils.pick_rows(rows, keys)       # pick() applied to every row
DictUtils.omit_rows(rows, keys)       # omit() applied to every row
DictUtils.rename_keys_rows(rows, mapping)  # rename_keys() applied to every row
```

```python
DictUtils.pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])
# {"a": 1, "c": 3}

DictUtils.safe_get({"student": {"id": 42}}, "student", "id")
# 42

DictUtils.rename_keys_rows(rows, {"studentUniqueId": "student_id"})
# [{"student_id": ..., ...}, ...]
```

---

### `ListUtils`

Static methods for lists.

```python
ListUtils.chunk(lst, size)   # split into consecutive chunks of size
ListUtils.flatten(lst)       # flatten one level of nesting
```

```python
ListUtils.chunk([1, 2, 3, 4, 5], 2)    # [[1, 2], [3, 4], [5]]
ListUtils.flatten([[1, 2], [3, 4]])     # [1, 2, 3, 4]
```

`chunk` also works on lists of row dicts directly: `ListUtils.chunk(rows, 100)`.

---

### `TypeUtils`

Static methods for coercing values. Row methods return `None` on failure (consistent with `safe_int` / `safe_float`).

```python
TypeUtils.normalize_bool(val)                                   # bool or raises ValueError
TypeUtils.safe_int(val)                                         # int | None
TypeUtils.safe_float(val)                                       # float | None

TypeUtils.normalize_bool_rows(rows, column, *, out_column=None) # None on failure
TypeUtils.safe_int_rows(rows, column, *, out_column=None)
TypeUtils.safe_float_rows(rows, column, *, out_column=None)
```

`normalize_bool` recognizes:

| Truthy | Falsy |
|---|---|
| `True`, `1`, `"true"`, `"yes"`, `"1"`, `"t"`, `"y"` | `False`, `0`, `"false"`, `"no"`, `"0"`, `"f"`, `"n"` |

String matching is case-insensitive and strips whitespace.

```python
TypeUtils.normalize_bool("Yes")     # True
TypeUtils.safe_int("3.14")          # None  (not an integer string)
TypeUtils.safe_float("abc")         # None

TypeUtils.safe_int_rows(rows, "count", out_column="count_int")
# adds "count_int" column; original "count" column preserved
```

---

### `ThaStr`

String normalization and slugification. `format_str` and `slugify` are static methods callable without instantiation. Row methods require an instance and store results in `self.rows`.

```python
ThaStr.format_str(
    value: str,
    *,
    strip: bool = True,
    case: str | None = None,     # "upper" | "lower" | "title" | None
    replace: dict[str, str] | None = None,
    regex: bool = False,
) -> str
```

```python
ThaStr.slugify(
    value: str,
    *,
    sep: str = "-",
    prefix: str = "",
    suffix: str = "",
) -> str
```

```python
runner = ThaStr()

runner.format_str_rows(
    rows,
    column,
    *,
    strip=True,
    case=None,
    replace=None,
    regex=False,
    out_column=None,
    on_error="error",            # "error" | "skip" | "blank"
    skip_statuses=None,          # default: ["error", "warning"]
) -> list[dict]

runner.slugify_rows(
    rows,
    columns,                     # str or list[str] — multiple columns are joined with sep
    out_column,
    *,
    sep="-",
    prefix="",
    suffix="",
    on_error="error",
    skip_statuses=None,
) -> list[dict]
```

```python
ThaStr.format_str("  HELLO WORLD  ", case="lower")    # "hello world"
ThaStr.slugify("Hello World!")                          # "hello-world"
ThaStr.slugify("café résumé", sep="_")                  # "cafe_resume"

runner = ThaStr()
runner.format_str_rows(rows, "Name", case="lower", out_column="Name Slug")
runner.slugify_rows(rows, ["First", "Last"], out_column="id")
```

Raises `StrError` on invalid `case` or `on_error`. Unicode is converted to ASCII via NFKD normalization.

---

### `ThaNum`

Numeric string parsing. `format_num` is a static method callable without instantiation. `format_num_rows` requires an instance and stores results in `self.rows`.

```python
ThaNum.format_num(
    value: str | int | float,
    *,
    strip_currency: bool = True,   # removes $€£¥₹₩₽₺₫฿₱₴
    strip_commas: bool = True,
    round_to: int | None = None,
    cast: str = "float",           # "float" | "int"
) -> float | int
```

```python
runner = ThaNum()

runner.format_num_rows(
    rows,
    column,
    *,
    strip_currency=True,
    strip_commas=True,
    round_to=None,
    cast="float",
    out_column=None,
    on_error="error",
    skip_statuses=None,
) -> list[dict]
```

```python
ThaNum.format_num("$1,234.56")          # 1234.56
ThaNum.format_num("(£500)", cast="int") # -500
ThaNum.format_num("€9.99", round_to=1)  # 10.0
```

Parenthetical negatives (`(100)`) are converted automatically. Raises `NumError` on unparseable input, `bool` input, or invalid `cast`.

---

### `ThaDT`

Date format auto-detection and conversion. `format_date` and `now` are static methods. `format_date_rows` requires an instance and stores results in `self.rows`.

```python
ThaDT.now(fmt="%Y_%m_%d_%H_%M_%S") -> str

ThaDT.format_date(value: str, to_fmt: str) -> str

runner = ThaDT()

runner.format_date_rows(
    rows,
    column,
    to_fmt,
    *,
    out_column=None,
    on_error="error",
    skip_statuses=None,
) -> list[dict]
```

Auto-detects: ISO 8601 (with/without time, with/without ms/Z), compact ISO (`20240415`), year-month (`2024-04`), US `MM/DD/YYYY`, US `MM/DD/YY`, `MM/DD`, long and short month names (`April 15, 2024` / `Apr 15, 2024`).

```python
ThaDT.format_date("Apr 15, 2024", "%Y-%m-%d")   # "2024-04-15"
ThaDT.format_date("04/15/2024", "%m/%d/%y")      # "04/15/24"
ThaDT.now()                                       # "2024_04_15_13_30_00"
```

Raises `DateError` on unrecognized formats or invalid `on_error`.

---

### `on_error` (all row methods)

| Value | Behaviour |
|---|---|
| `"error"` | `row status="error"`, `message=...`, output column set to `""` |
| `"skip"` | Row returned unchanged |
| `"blank"` | Output column set to `""`, row status untouched |

### `skip_statuses`

Rows whose `"row status"` value is in this list are passed through unchanged. Default: `["error", "warning"]`. Pass `[]` to process all rows regardless of status.

---

### Error classes

| Class | Raised by |
|---|---|
| `UtilsError` | Base class — catch all tha-utils-helper errors |
| `StrError` | `ThaStr` methods |
| `NumError` | `ThaNum` methods |
| `DateError` | `ThaDT` methods |

```python
from tha_utils_helper import StrError, NumError, DateError, UtilsError
```

---

## Composing with `tha-csv-runner`

```python
from tha_csv_runner import ThaCSV
from tha_utils_helper import ThaNum, ThaStr, ThaDT

csv = ThaCSV()
csv.read("Load", "input.csv", ["Org BK", "Budget", "Start Date", "Name"])

rows = ThaNum().format_num_rows(csv.rows, column="Budget", cast="float", round_to=2)
rows = ThaDT().format_date_rows(rows, column="Start Date", to_fmt="%Y-%m-%d")
rows = ThaStr().format_str_rows(rows, column="Name", case="lower")

csv.write("Write", "output.csv", rows=rows)
```

---

## Alternatives

This library is intentionally limited in scope — it exists as a zero-dependency utility layer for the `tha-*` ecosystem. If you need something more comprehensive, these are the go-to options:

**General utilities:**
- [**toolz**](https://toolz.readthedocs.io) — covers most of what's here and much more: chunking, flattening, pick, omit, nested get, and functional composition
- [**funcy**](https://funcy.readthedocs.io) — functional helpers including `pick`, `omit`, `chunks`, and silent type coercions

**String normalization / slugification:**
- [**python-slugify**](https://github.com/un33k/python-slugify) — full-featured slugification with transliteration support and configurable stop words
- [**Unidecode**](https://github.com/avian2/unidecode) — broad unicode-to-ASCII transliteration

**Numeric parsing:**
- [**babel**](https://babel.pocoo.org) — locale-aware number parsing that handles locale-specific decimal and grouping separators
- [**price-parser**](https://github.com/scrapinghub/price-parser) — extracts prices and currency from arbitrary text

**Date parsing:**
- [**python-dateutil**](https://dateutil.readthedocs.io) — flexible date parsing including fuzzy matching; no row-level error handling
- [**pendulum**](https://pendulum.eustace.io) — timezone-aware datetime with parsing and formatting

Choose this library when you want all of the above in a single zero-dependency install with consistent row-level error capture that slots into the `tha-*` pipeline.

## License

MIT
