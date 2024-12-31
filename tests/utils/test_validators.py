import pytest
from datetime import datetime
from click import BadParameter
from src.utils.validators import *


# Tests para validate_date
def test_validate_date_valid():
    today = datetime.now().strftime("%Y-%m-%d")
    assert validate_date(today) == today


def test_validate_date_invalid_format():
    with pytest.raises(BadParameter, match="Invalid date format or values in"):
        validate_date("2024-31-12")


def test_validate_date_future():
    future_date = (datetime.now().date().replace(year=datetime.now().year + 1)).strftime("%Y-%m-%d")
    with pytest.raises(BadParameter, match="Please enter a valid past or current date."):
        validate_date(future_date)


# Tests para validate_amount
def test_validate_amount_valid():
    assert validate_amount(5000.75) == 5000.75


def test_validate_amount_zero_or_negative():
    with pytest.raises(BadParameter, match="Amount must be positive"):
        validate_amount(0)

    with pytest.raises(BadParameter, match="Amount must be positive"):
        validate_amount(-50)


def test_validate_amount_exceeds_max():
    with pytest.raises(BadParameter, match="not exceed \\$100000"):
        validate_amount(200000)


def test_validate_amount_insignificant():
    with pytest.raises(BadParameter, match="greater than \\$0.00 after rounding"):
        validate_amount(0.004)


# Tests para validate_category
def test_validate_category_valid():
    assert validate_category("groceries") == "Groceries"


def test_validate_category_invalid():
    with pytest.raises(BadParameter, match="is not a valid category"):
        validate_category("InvalidCategory")


# Tests for validate_description
def test_validate_description_valid():
    assert validate_description("Groceries expense") == "Groceries expense"


def test_validate_description_too_short():
    with pytest.raises(BadParameter, match="Description must be at least 3 characters"):
        validate_description("Hi")


def test_validate_description_too_long():
    with pytest.raises(BadParameter, match="Description must be no more than 60 characters"):
        validate_description("a" * 61)


def test_validate_description_empty():
    assert validate_description("") == "..."


# Tests for validate_budget_amount
def test_validate_budget_amount_valid():
    assert validate_budget_amount(5000) == 5000


def test_validate_budget_amount_zero_or_negative():
    with pytest.raises(BadParameter, match="greater than \\$0 and less than"):
        validate_budget_amount(0)

    with pytest.raises(BadParameter, match="greater than \\$0 and less than"):
        validate_budget_amount(-500)


def test_validate_budget_amount_exceeds_max():
    with pytest.raises(BadParameter, match="less than \\$100000"):
        validate_budget_amount(200000)
