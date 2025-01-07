import pytest
from click.testing import CliRunner
from datetime import datetime
from src.commands.add_expense import add_expense


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def expense_data():
    return {
        "amount": "50.00",
        "category": "Groceries",
        "description": "Weekly groceries",
        "date": "2025-01-07"
    }


@pytest.fixture
def mock_dependencies(mocker):
    return {
        'initialize_csv': mocker.patch('src.commands.add_expense.initialize_csv'),
        'save_expense': mocker.patch('src.commands.add_expense.save_expense'),
        'get_next_id': mocker.patch('src.commands.add_expense.get_next_expense_id', return_value="1"),
        'check_budget': mocker.patch('src.commands.add_expense.check_budget_warning')
    }


def test_add_expense_success(runner, mock_dependencies, expense_data):
    result = runner.invoke(add_expense, [
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])
    assert result.exit_code == 0

    mock_dependencies['initialize_csv'].assert_called_once()
    mock_dependencies['save_expense'].assert_called_once_with({
        'ID': '1',
        'Date': expense_data["date"],
        'Amount': expense_data["amount"],
        'Category': expense_data["category"],
        'Description': expense_data["description"]
    })
    mock_dependencies['check_budget'].assert_called_once_with(2025, 1)


def test_add_expense_with_prompts(runner, mock_dependencies):
    result = runner.invoke(add_expense, input='50.00\ngroceries\n')
    assert result.exit_code == 0

    mock_dependencies['initialize_csv'].assert_called_once()
    called_expense = mock_dependencies['save_expense'].call_args[0][0]
    assert called_expense['Amount'] == '50.00'
    assert called_expense['Category'] == 'Groceries'
    assert called_expense['Description'] == '...'
    assert called_expense['Date'] == datetime.now().strftime("%Y-%m-%d")


def test_add_expense_file_not_found(runner, mock_dependencies, expense_data):
    mock_dependencies['initialize_csv'].side_effect = FileNotFoundError("CSV file not found")

    result = runner.invoke(add_expense, [
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])

    assert result.exit_code == 1


def test_add_expense_saving_error(runner, mock_dependencies, expense_data):
    mock_dependencies['save_expense'].side_effect = ValueError("Error saving expense")

    result = runner.invoke(add_expense, [
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])

    assert result.exit_code == 1


def test_add_expense_empty_id(runner, mock_dependencies):
    mock_dependencies['get_next_id'].side_effect = Exception("Error retrieving next expense ID")

    result = runner.invoke(add_expense, [
        '--amount', '50.00',
        '--category', 'Groceries'
    ])

    assert result.exit_code == 1
    mock_dependencies['save_expense'].assert_not_called()


def test_add_expense_error_handling(runner, mock_dependencies):
    mock_dependencies['initialize_csv'].side_effect = PermissionError("Access denied")

    result = runner.invoke(add_expense, [
        '--amount', '50.00',
        '--category', 'Groceries'
    ])

    assert result.exit_code == 1
    assert "Access denied" in str(result.exception)


def test_add_expense_budget_warning(runner, mock_dependencies, expense_data):
    mock_dependencies['check_budget'].return_value = "[warning] You have exceeded your monthly budget!"

    result = runner.invoke(add_expense, [
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])

    assert result.exit_code == 0


def test_add_expense_no_budget_set(runner, mock_dependencies, expense_data):
    mock_dependencies['check_budget'].return_value = None

    result = runner.invoke(add_expense, [
        '--date', expense_data["date"],
        '--amount', expense_data["amount"],
        '--category', expense_data["category"],
        '--description', expense_data["description"]
    ])

    assert result.exit_code == 0
