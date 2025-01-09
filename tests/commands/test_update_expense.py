import pytest
from click.testing import CliRunner
from src.commands.update_expense import update_expense


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def expense_data():
    return {
        "id": 1,
        "date": "2025-01-07",
        "amount": "75.50",
        "category": "Leisure",
        "description": "Movie tickets"
    }


@pytest.fixture
def mock_dependencies(mocker):
    return {
        'read_expenses': mocker.patch('src.commands.update_expense.read_expenses', return_value=[
            {
                'ID': '1',
                'Date': '2025-01-01',
                'Amount': '50.00',
                'Category': 'Groceries',
                'Description': 'Weekly shopping'
            }
        ]),
        'check_budget': mocker.patch('src.commands.update_expense.check_budget_warning'),
        'csv_writer': mocker.patch('csv.DictWriter'),
    }


def test_update_expense_success(runner, mock_dependencies, expense_data):
    result = runner.invoke(update_expense, [
        '--id', str(expense_data["id"]),
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])

    assert result.exit_code == 0
    assert "updated successfully" in result.output
    mock_dependencies['check_budget'].assert_called_once_with(2025, 1)


def test_update_expense_partial_update(runner, mock_dependencies):
    result = runner.invoke(update_expense, [
        '--id', '1',
        '--amount', '60.00'
    ])

    assert result.exit_code == 0
    assert "updated successfully" in result.output
    mock_dependencies['read_expenses'].assert_called_once()


def test_update_expense_invalid_id(runner, mock_dependencies):
    mock_dependencies['read_expenses'].return_value = [
        {
            'ID': '2',
            'Date': '2025-01-01',
            'Amount': '50.00',
            'Category': 'Groceries',
            'Description': 'Weekly shopping'
        }
    ]

    result = runner.invoke(update_expense, [
        '--id', '999',
        '--amount', '60.00'
    ])

    assert result.exit_code == 0
    assert "No expense found with ID" in result.output
    mock_dependencies['read_expenses'].assert_called_once()


def test_update_expense_negative_id(runner):
    result = runner.invoke(update_expense, [
        '--id', '-1',
        '--amount', '60.00'
    ])

    assert result.exit_code == 0
    assert "ID must be a positive number" in result.output


def test_update_expense_no_changes(runner):
    result = runner.invoke(update_expense, ['--id', '1'])

    assert result.exit_code == 0
    assert "You must provide at least one field to update" in result.output


def test_update_expense_file_not_found(runner, mock_dependencies):
    mock_dependencies['read_expenses'].return_value = []

    result = runner.invoke(update_expense, [
        '--id', '1',
        '--amount', '60.00'
    ])

    assert result.exit_code == 0
    assert "No expenses found" in result.output
    mock_dependencies['read_expenses'].assert_called_once()


def test_update_expense_with_budget_warning(runner, mock_dependencies):
    mock_dependencies['check_budget'].return_value = "[warning]Budget warning message[/warning]"

    result = runner.invoke(update_expense, [
        '--id', '1',
        '--amount', '1000.00'
    ])

    assert result.exit_code == 0
    assert "Budget warning message" in result.output


def test_update_expense_same_values(runner, mock_dependencies):
    original_expense = {
        'ID': '1',
        'Date': '2025-01-01',
        'Amount': '50.00',
        'Category': 'Groceries',
        'Description': 'Weekly shopping'
    }

    mock_dependencies['read_expenses'].return_value = [original_expense]

    result = runner.invoke(update_expense, [
        '--id', '1',
        '--amount', '50.00',
        '--category', 'Groceries',
        '--description', 'Weekly shopping'
    ])

    assert result.exit_code == 0
    assert "updated successfully" in result.output

    mock_dependencies['read_expenses'].assert_called_once()

    assert "---> $50.00" not in result.output
    assert "---> 'Groceries'" not in result.output
    assert "---> 'Weekly shopping'" not in result.output
    
    assert "$50.00" in result.output
    assert "'Groceries'" in result.output
    assert "'Weekly shopping'" in result.output


def test_update_expense_file_error(runner, mock_dependencies):
    mock_dependencies['read_expenses'].side_effect = Exception("Error accessing file")

    result = runner.invoke(update_expense, [
        '--id', '1',
        '--amount', '60.00'
    ])

    assert result.exit_code == 0
    assert "Error updating expense" in result.output
