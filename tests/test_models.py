from app.models import Task


def test_validate_data_accepts_valid_values():
    errors = Task.validate_data("Read book", "Read 10 pages")
    assert errors == []


def test_validate_data_rejects_blank_title():
    errors = Task.validate_data("   ", "desc")
    assert "Title is required." in errors


def test_validate_data_rejects_too_long_fields():
    errors = Task.validate_data("t" * 121, "d" * 501)
    assert "Title must be 120 characters or fewer." in errors
    assert "Description must be 500 characters or fewer." in errors
