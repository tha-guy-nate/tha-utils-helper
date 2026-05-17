from tha_utils_helper import DictUtils


# --- pick ---

def test_pick_subset() -> None:
    assert DictUtils.pick({"a": 1, "b": 2, "c": 3}, ["a", "c"]) == {"a": 1, "c": 3}


def test_pick_all_keys() -> None:
    d = {"a": 1, "b": 2}
    assert DictUtils.pick(d, ["a", "b"]) == d


def test_pick_no_keys() -> None:
    assert DictUtils.pick({"a": 1}, []) == {}


def test_pick_missing_keys_ignored() -> None:
    assert DictUtils.pick({"a": 1}, ["a", "z"]) == {"a": 1}


def test_pick_empty_dict() -> None:
    assert DictUtils.pick({}, ["a"]) == {}


# --- omit ---

def test_omit_subset() -> None:
    assert DictUtils.omit({"a": 1, "b": 2, "c": 3}, ["b"]) == {"a": 1, "c": 3}


def test_omit_all_keys() -> None:
    assert DictUtils.omit({"a": 1, "b": 2}, ["a", "b"]) == {}


def test_omit_no_keys() -> None:
    d = {"a": 1, "b": 2}
    assert DictUtils.omit(d, []) == d


def test_omit_missing_keys_ignored() -> None:
    assert DictUtils.omit({"a": 1}, ["z"]) == {"a": 1}


# --- safe_get ---

def test_safe_get_single_key() -> None:
    assert DictUtils.safe_get({"a": 1}, "a") == 1


def test_safe_get_nested() -> None:
    assert DictUtils.safe_get({"a": {"b": {"c": 42}}}, "a", "b", "c") == 42


def test_safe_get_missing_key_returns_none() -> None:
    assert DictUtils.safe_get({"a": 1}, "z") is None


def test_safe_get_missing_nested_key_returns_none() -> None:
    assert DictUtils.safe_get({"a": {"b": 1}}, "a", "z") is None


def test_safe_get_non_dict_mid_path_returns_none() -> None:
    assert DictUtils.safe_get({"a": 99}, "a", "b") is None


def test_safe_get_no_keys() -> None:
    d = {"a": 1}
    assert DictUtils.safe_get(d) is d


# --- rename_keys ---

def test_rename_keys_basic() -> None:
    result = DictUtils.rename_keys({"studentUniqueId": 1, "name": "A"}, {"studentUniqueId": "student_id"})
    assert result == {"student_id": 1, "name": "A"}


def test_rename_keys_unmapped_keys_preserved() -> None:
    assert DictUtils.rename_keys({"a": 1, "b": 2}, {"a": "x"}) == {"x": 1, "b": 2}


def test_rename_keys_empty_mapping() -> None:
    d = {"a": 1}
    assert DictUtils.rename_keys(d, {}) == d


def test_rename_keys_empty_dict() -> None:
    assert DictUtils.rename_keys({}, {"a": "b"}) == {}


# --- pick_rows ---

def test_pick_rows_basic() -> None:
    rows = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
    assert DictUtils.pick_rows(rows, ["a", "c"]) == [{"a": 1, "c": 3}, {"a": 4, "c": 6}]

def test_pick_rows_returns_new_list() -> None:
    rows = [{"a": 1}]
    assert DictUtils.pick_rows(rows, ["a"]) is not rows

def test_pick_rows_immutable() -> None:
    rows = [{"a": 1, "b": 2}]
    DictUtils.pick_rows(rows, ["a"])
    assert "b" in rows[0]

def test_pick_rows_empty() -> None:
    assert DictUtils.pick_rows([], ["a"]) == []


# --- omit_rows ---

def test_omit_rows_basic() -> None:
    rows = [{"a": 1, "b": 2, "c": 3}]
    assert DictUtils.omit_rows(rows, ["b"]) == [{"a": 1, "c": 3}]

def test_omit_rows_returns_new_list() -> None:
    rows = [{"a": 1}]
    assert DictUtils.omit_rows(rows, []) is not rows

def test_omit_rows_empty() -> None:
    assert DictUtils.omit_rows([], ["a"]) == []


# --- rename_keys_rows ---

def test_rename_keys_rows_basic() -> None:
    rows = [{"studentId": "1", "name": "A"}, {"studentId": "2", "name": "B"}]
    assert DictUtils.rename_keys_rows(rows, {"studentId": "id"}) == [
        {"id": "1", "name": "A"},
        {"id": "2", "name": "B"},
    ]

def test_rename_keys_rows_returns_new_list() -> None:
    rows = [{"a": 1}]
    assert DictUtils.rename_keys_rows(rows, {}) is not rows

def test_rename_keys_rows_immutable() -> None:
    rows = [{"studentId": "1"}]
    DictUtils.rename_keys_rows(rows, {"studentId": "id"})
    assert "studentId" in rows[0]

def test_rename_keys_rows_empty() -> None:
    assert DictUtils.rename_keys_rows([], {"a": "b"}) == []
