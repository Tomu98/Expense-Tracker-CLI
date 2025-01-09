import pytest
from click.testing import CliRunner
from src.commands.list_expenses import list_expenses


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_expenses():
    return [
        {"ID": "1", "Date": "2025-01-07", "Amount": "50.00", "Category": "Groceries", "Description": "Weekly groceries"},
        {"ID": "2", "Date": "2025-01-15", "Amount": "30.00", "Category": "Leisure", "Description": "Movies"},
        {"ID": "3", "Date": "2025-02-01", "Amount": "75.50", "Category": "Groceries", "Description": "Monthly groceries"},
        {"ID": "4", "Date": "2025-03-10", "Amount": "150.00", "Category": "Electronics", "Description": "Headphones"}
    ]


@pytest.fixture
def mock_dependencies(mocker):
    return {
        'read_expenses': mocker.patch('src.commands.list_expenses.read_expenses'),
        'validate_category': mocker.patch('src.commands.list_expenses.validate_category'),
        'validate_parse_date': mocker.patch('src.commands.list_expenses.validate_parse_date'),
        'validate_amount': mocker.patch('src.commands.list_expenses.validate_amount')
    }


def test_list_all_expenses(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(list_expenses)

    assert result.exit_code == 0
    assert "Expenses" in result.output
    assert "Filtered Expenses" not in result.output
    for expense in mock_expenses:
        assert expense["ID"] in result.output
        assert expense["Date"] in result.output
        assert expense["Category"] in result.output
        assert expense["Description"] in result.output
        assert f"$ {float(expense['Amount']):.2f}" in result.output


def test_list_expenses_by_category(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_category'].return_value = "Groceries"

    result = runner.invoke(list_expenses, ['--category', 'groceries'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Weekly groceries" in result.output
    assert "Monthly groceries" in result.output
    assert "Movies" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_date_range(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = None

    result = runner.invoke(list_expenses, ['--from', '2025-01-15', '--to', '2025-02-01'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Movies" in result.output
    assert "Monthly groceries" in result.output
    assert "Weekly groceries" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_from_date(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = None

    result = runner.invoke(list_expenses, ['--from', '2025-02-01'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Monthly groceries" in result.output
    assert "Headphones" in result.output
    assert "Weekly groceries" not in result.output
    assert "Movies" not in result.output


def test_list_expenses_to_date(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = None

    result = runner.invoke(list_expenses, ['--to', '2025-01-15'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Weekly groceries" in result.output
    assert "Movies" in result.output
    assert "Monthly groceries" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_amount_range(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_amount'].side_effect = lambda x: x

    result = runner.invoke(list_expenses, ['--min', '50', '--max', '100'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Weekly groceries" in result.output
    assert "Monthly groceries" in result.output
    assert "Movies" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_min_amount(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_amount'].side_effect = lambda x: x

    result = runner.invoke(list_expenses, ['--min', '75'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Monthly groceries" in result.output
    assert "Headphones" in result.output
    assert "Weekly groceries" not in result.output
    assert "Movies" not in result.output


def test_list_expenses_max_amount(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_amount'].side_effect = lambda x: x

    result = runner.invoke(list_expenses, ['--max', '50'])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Weekly groceries" in result.output
    assert "Movies" in result.output
    assert "Monthly groceries" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_combined_filters(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_category'].return_value = "Groceries"
    mock_dependencies['validate_amount'].side_effect = lambda x: x
    mock_dependencies['validate_parse_date'].return_value = None

    result = runner.invoke(list_expenses, [
        '--category', 'groceries',
        '--from', '2025-01-15',
        '--min', '50'
    ])

    assert result.exit_code == 0
    assert "Filtered Expenses" in result.output
    assert "Monthly groceries" in result.output
    assert "Weekly groceries" not in result.output
    assert "Movies" not in result.output
    assert "Headphones" not in result.output


def test_list_expenses_no_file(runner, mock_dependencies):
    mock_dependencies['read_expenses'].side_effect = FileNotFoundError()

    result = runner.invoke(list_expenses)

    assert result.exit_code == 0
    assert "No expenses file was found" in result.output


def test_list_expenses_empty_file(runner, mock_dependencies):
    mock_dependencies['read_expenses'].return_value = []

    result = runner.invoke(list_expenses)

    assert result.exit_code == 0
    assert "No expenses recorded" in result.output


def test_list_expenses_no_matches(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_category'].return_value = "Transport"

    result = runner.invoke(list_expenses, ['--category', 'transport'])

    assert result.exit_code == 0
    assert "No expenses matched the given filters" in result.output
