import pytest
from tha_utils_helper import ThaStr, ThaNum, ThaDT


@pytest.fixture
def str_runner() -> ThaStr:
    return ThaStr()


@pytest.fixture
def str_rows() -> list[dict]:
    return [
        {"id": "1", "Name": "  Alice Smith  ", "row status": "", "message": ""},
        {"id": "2", "Name": "BOB JONES", "row status": "", "message": ""},
        {"id": "3", "Name": "carol white", "row status": "", "message": ""},
    ]


@pytest.fixture
def num_runner() -> ThaNum:
    return ThaNum()


@pytest.fixture
def num_rows() -> list[dict]:
    return [
        {"id": "1", "Amount": "$1,234.56", "row status": "", "message": ""},
        {"id": "2", "Amount": "£2,000.00", "row status": "", "message": ""},
        {"id": "3", "Amount": "500", "row status": "", "message": ""},
    ]


@pytest.fixture
def dt_runner() -> ThaDT:
    return ThaDT()


@pytest.fixture
def dt_rows() -> list[dict]:
    return [
        {"id": "1", "Start Date": "2024-04-15"},
        {"id": "2", "Start Date": "04/16/2024"},
        {"id": "3", "Start Date": "Apr 17, 2024"},
    ]
