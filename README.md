# tha-utils-helper

[![CI](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/tha-guy-nate/tha-utils-helper/actions/workflows/ci.yml)

A small Python utility library with general-purpose helpers for the `tha-*` ecosystem. No dependencies, no classes — just functions.

## Install

```bash
pip install tha-utils-helper
```

## Quick start

```python
from tha_utils_helper import chunk_list

chunk_list([1, 2, 3, 4, 5], 2)
# [[1, 2], [3, 4], [5]]
```

## API

### `chunk_list(lst, size)`

```python
chunk_list(lst: list[T], size: int) -> list[list[T]]
```

Splits `lst` into consecutive chunks of `size`. The final chunk may be smaller if the list doesn't divide evenly. Raises `ValueError` if `size < 1`.

```python
chunk_list([1, 2, 3, 4, 5], 2)   # [[1, 2], [3, 4], [5]]
chunk_list([1, 2, 3], 3)          # [[1, 2, 3]]
chunk_list([], 5)                  # []
```

## License

MIT
