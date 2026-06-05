from utils.validation import validate_project_input


def test_valid_create_input():
    assert validate_project_input({"name": "My Project"}, require_all=True) is None


def test_valid_full_input():
    data = {"name": "X", "description": "Y", "status": "active"}
    assert validate_project_input(data, require_all=True) is None


def test_missing_name_on_create():
    error = validate_project_input({}, require_all=True)
    assert error is not None and "name" in error


def test_blank_name_on_create():
    assert validate_project_input({"name": "   "}, require_all=True) is not None


def test_name_too_long():
    assert validate_project_input({"name": "a" * 101}) is not None


def test_invalid_status():
    error = validate_project_input({"name": "ok", "status": "invalid"})
    assert error is not None and "status" in error


def test_all_valid_statuses():
    for status in ("active", "archived", "completed", "paused"):
        assert validate_project_input({"name": "X", "status": status}) is None


def test_description_too_long():
    assert validate_project_input({"name": "x", "description": "d" * 1001}) is not None


def test_non_dict_input():
    assert validate_project_input("not a dict") is not None


def test_partial_update_no_name_required():
    assert validate_project_input({"status": "archived"}, require_all=False) is None
