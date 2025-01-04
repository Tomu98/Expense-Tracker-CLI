import pytest
import json
from src.utils.budget_helpers import (
    initialize_budget_file,
    read_budget,
    save_budget,
    update_budget,
    calculate_monthly_expenses,
    check_budget_warning,
    get_budget_summary
)


@pytest.fixture
def temp_budget_file(tmp_path):
    budget_file = tmp_path / "budgets.json"
    budget_file.write_text("{}")
    return budget_file

@pytest.fixture
def sample_budgets():
    return {
        "2024-01": 1000.0,
        "2024-02": 1200.0
    }


def test_initialize_budget_file(mocker, temp_budget_file):
    mocker.patch('src.utils.budget_helpers.BUDGET_FILE_PATH', temp_budget_file)
    initialize_budget_file()

    assert temp_budget_file.exists()
    assert json.loads(temp_budget_file.read_text()) == {}


def test_read_budget(mocker, temp_budget_file):
    mocker.patch('src.utils.budget_helpers.BUDGET_FILE_PATH', temp_budget_file)
    temp_budget_file.write_text('{"2024-01": 1000.0}')

    budgets = read_budget()
    assert budgets == {"2024-01": 1000.0}


def test_save_budget(mocker, temp_budget_file):
    test_budgets = {"2024-01": 1000.0, "2024-02": 1200.0}
    mocker.patch('src.utils.budget_helpers.BUDGET_FILE_PATH', temp_budget_file)
    
    save_budget(test_budgets)
    saved_budgets = json.loads(temp_budget_file.read_text())
    assert saved_budgets == test_budgets


def test_update_budget_new(mocker, temp_budget_file):
    mocker.patch('src.utils.budget_helpers.BUDGET_FILE_PATH', temp_budget_file)
    mocker.patch('src.utils.budget_helpers.console.print')

    update_budget(1, 2024, 1000.0)
    budgets = json.loads(temp_budget_file.read_text())
    assert budgets["2024-01"] == 1000.0


def test_update_budget_existing(mocker, temp_budget_file):
    mocker.patch('src.utils.budget_helpers.BUDGET_FILE_PATH', temp_budget_file)
    mocker.patch('src.utils.budget_helpers.console.print')
    mock_prompt = mocker.patch('click.prompt', return_value='y')

    temp_budget_file.write_text('{"2024-01": 1000.0}')
    update_budget(1, 2024, 1500.0)

    budgets = json.loads(temp_budget_file.read_text())
    assert budgets["2024-01"] == 1500.0
    assert mock_prompt.called


def test_calculate_monthly_expenses(mocker):
    mock_expenses = [
        {"Date": "2024-01-15", "Amount": "100.0"},
        {"Date": "2024-01-20", "Amount": "200.0"},
        {"Date": "2024-02-01", "Amount": "300.0"}
    ]
    mocker.patch('src.utils.budget_helpers.read_expenses', return_value=mock_expenses)
    
    expenses = calculate_monthly_expenses(2024, 1)
    assert expenses == 300.0


def test_check_budget_warning_exceed(mocker, sample_budgets):
    mocker.patch('src.utils.budget_helpers.read_budget', return_value=sample_budgets)
    mocker.patch('src.utils.budget_helpers.calculate_monthly_expenses', return_value=1100.0)

    warning = check_budget_warning(2024, 1)
    assert "exceeded" in warning.lower()


def test_check_budget_warning_remaining(mocker, sample_budgets):
    mocker.patch('src.utils.budget_helpers.read_budget', return_value=sample_budgets)
    mocker.patch('src.utils.budget_helpers.calculate_monthly_expenses', return_value=800.0)

    info = check_budget_warning(2024, 1)
    assert "remaining budget" in info.lower()


def test_get_budget_summary(mocker, sample_budgets):
    mocker.patch('src.utils.budget_helpers.read_budget', return_value=sample_budgets)
    mocker.patch('src.utils.budget_helpers.calculate_monthly_expenses', return_value=800.0)

    summary = get_budget_summary(2024, 1)
    assert summary["budget_set"] is True
    assert summary["budget_amount"] == 1000.0
    assert summary["current_expenses"] == 800.0
    assert summary["remaining_budget"] == 200.0

