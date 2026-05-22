from __future__ import annotations

from datetime import datetime

from .errors import DateError

_INPUT_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
    "%Y%m%d",
    "%Y-%m",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%m-%d-%Y",
    "%m/%d",
    "%B %d, %Y",
    "%b %d, %Y",
    "%B %d %Y",
    "%b %d %Y",
    "%B %d",
    "%b %d",
    "%d-%b",
]

_ON_ERROR = {"error", "skip", "blank"}


def _parse(value: str) -> datetime:
    for fmt in _INPUT_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    raise DateError(f"Unrecognized date format: {value!r}")


class ThaDT:
    def __init__(self) -> None:
        self.rows: list[dict] = []  # type: ignore[type-arg]

    @staticmethod
    def now(fmt: str = "%Y_%m_%d_%H_%M_%S") -> str:
        return datetime.now().strftime(fmt)

    @staticmethod
    def format_date(value: str, to_fmt: str) -> str:
        return _parse(value).strftime(to_fmt)

    def format_date_rows(
        self,
        rows: list[dict],  # type: ignore[type-arg]
        column: str,
        to_fmt: str,
        *,
        out_column: str | None = None,
        on_error: str = "error",
        skip_statuses: list[str] | None = None,
    ) -> list[dict]:  # type: ignore[type-arg]
        if on_error not in _ON_ERROR:
            raise DateError(f"on_error must be one of {sorted(_ON_ERROR)!r}, got {on_error!r}")

        statuses_to_skip = set(skip_statuses if skip_statuses is not None else ["error", "warning"])
        dest = out_column if out_column is not None else column

        output = []
        for row in rows:
            if row.get("row status") in statuses_to_skip:
                output.append(row.copy())
                continue

            raw = row.get(column, "")
            if not raw:
                new_row = row.copy()
                if on_error == "error":
                    new_row["row status"] = "error"
                    new_row["message"] = f"Column {column!r} is empty or missing"
                    new_row[dest] = ""
                elif on_error == "blank":
                    new_row[dest] = ""
                output.append(new_row)
                continue

            try:
                formatted = self.format_date(str(raw), to_fmt)
            except DateError as exc:
                new_row = row.copy()
                if on_error == "error":
                    new_row["row status"] = "error"
                    new_row["message"] = str(exc)
                    new_row[dest] = ""
                elif on_error == "blank":
                    new_row[dest] = ""
                output.append(new_row)
                continue

            new_row = row.copy()
            new_row[dest] = formatted
            output.append(new_row)

        self.rows = output
        return output
