# tha-utils-helper

[![CI](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml)

A small Python utility library with general-purpose helpers for the `tha-*` ecosystem. No dependencies — just classes with static methods.

## Install

```bash
pip install tha-utils-helper
```

## Quick start

```python
from tha_utils_helper import ListUtils, DictUtils, TypeUtils

ListUtils.chunk([1, 2, 3, 4, 5], 2)
# [[1, 2], [3, 4], [5]]

DictUtils.safe_get({"student": {"id": 42}}, "student", "id")
# 42

TypeUtils.normalize_bool("yes")
# True
```

## API

### `ListUtils`

| Method | Description |
|---|---|
| `chunk(lst, size)` | Split a list into consecutive chunks of `size`. Final chunk may be smaller. Raises `ValueError` if `size < 1` |
| `flatten(lst)` | Flatten one level of nesting — a list of lists into a single list |

```python
ListUtils.chunk([1, 2, 3, 4, 5], 2)   # [[1, 2], [3, 4], [5]]
ListUtils.flatten([[1, 2], [3, 4]])    # [1, 2, 3, 4]
```

### `DictUtils`

| Method | Description |
|---|---|
| `pick(d, keys)` | Return a new dict with only the specified keys |
| `omit(d, keys)` | Return a new dict with the specified keys removed |
| `safe_get(d, *keys)` | Traverse nested dicts without raising — returns `None` if any key is missing or the path hits a non-dict |
| `rename_keys(d, mapping)` | Return a new dict with keys renamed according to `mapping`. Unmapped keys are preserved |

```python
DictUtils.pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])
# {"a": 1, "c": 3}

DictUtils.omit({"a": 1, "b": 2, "c": 3}, ["b"])
# {"a": 1, "c": 3}

DictUtils.safe_get({"student": {"id": 42}}, "student", "id")
# 42

DictUtils.safe_get({"student": {"id": 42}}, "student", "missing")
# None

DictUtils.rename_keys({"studentUniqueId": 1, "name": "A"}, {"studentUniqueId": "student_id"})
# {"student_id": 1, "name": "A"}
```

### `TypeUtils`

| Method | Description |
|---|---|
| `normalize_bool(val)` | Coerce strings, ints, and bools to `bool`. Raises `ValueError` for unrecognized values |
| `safe_int(val)` | Parse to `int`, returns `None` on failure |
| `safe_float(val)` | Parse to `float`, returns `None` on failure |

`normalize_bool` recognizes:

| Truthy | Falsy |
|---|---|
| `True`, `1`, `"true"`, `"yes"`, `"1"`, `"t"`, `"y"` | `False`, `0`, `"false"`, `"no"`, `"0"`, `"f"`, `"n"` |

String matching is case-insensitive and strips whitespace.

```python
TypeUtils.normalize_bool("Yes")   # True
TypeUtils.normalize_bool("0")     # False
TypeUtils.normalize_bool("maybe") # raises ValueError

TypeUtils.safe_int("42")   # 42
TypeUtils.safe_int("abc")  # None

TypeUtils.safe_float("3.14")  # 3.14
TypeUtils.safe_float(None)    # None
```

## Alternatives

This library is intentionally limited in scope — it exists as a zero-dependency utility layer with consistent naming for the `tha-*` ecosystem. If you need something more comprehensive, these are the go-to options:

- [**toolz**](https://toolz.readthedocs.io) — covers most of what's here and much more: chunking, flattening, pick, omit, nested get, and functional composition
- [**more-itertools**](https://more-itertools.readthedocs.io) — extensive iterable utilities including chunking and flattening
- [**funcy**](https://funcy.readthedocs.io) — functional helpers including `pick`, `omit`, `chunks`, and silent type coercions

## License

MIT
