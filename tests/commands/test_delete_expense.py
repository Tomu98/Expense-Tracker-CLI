import pytest
from click.testing import CliRunner
from src.commands.delete_expense import delete_expense


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_expenses():
    return [
        {"ID": "1", "Date": "2025-01-07", "Amount": "50.00", "Category": "Groceries", "Description": "Snacks with my sweetheart :)"},
        {"ID": "2", "Date": "2025-01-07", "Amount": "30.00", "Category": "Others", "Description": "Bus ticket"}
    ]


@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch('src.commands.delete_expense.CSV_FILE_PATH', 'expenses.csv')

    return {
        'read_expenses': mocker.patch('src.commands.delete_expense.read_expenses'),
        'csv_writer': mocker.patch('csv.DictWriter'),
        'open_mock': mocker.patch('builtins.open')
    }


def test_delete_expense_by_id_success(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--id', '1'])

    assert result.exit_code == 0
    mock_dependencies['open_mock'].assert_called_once_with(
        'expenses.csv', 'w', newline='', encoding='utf-8'
    )
    writer = mock_dependencies['csv_writer'].return_value
    assert writer.writerows.call_args[0][0] == [mock_expenses[1]]


def test_delete_expense_by_prompt(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, input='2\n')

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert writer.writerows.call_args[0][0] == [mock_expenses[0]]


def test_delete_all_expenses_confirmed(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--all'], input='y\n')

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value

    assert writer.writerows.call_count == 0
    assert writer.writeheader.call_count == 1


def test_delete_all_expenses_cancelled(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--all'], input='n\n')

    assert result.exit_code == 0

    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called
    assert not writer.writeheader.called


def test_delete_all_expenses_invalid_then_cancel(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--all'], input='invalid\nn\n')

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called


def test_delete_expense_invalid_id(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--id', '999'])

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called


def test_delete_expense_negative_id(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses

    result = runner.invoke(delete_expense, ['--id', '-1'])

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called


def test_delete_expense_no_expenses(runner, mock_dependencies):
    mock_dependencies['read_expenses'].return_value = []

    result = runner.invoke(delete_expense, ['--id', '1'])

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called


def test_delete_expense_file_not_found(runner, mock_dependencies):
    mock_dependencies['read_expenses'].side_effect = FileNotFoundError()

    result = runner.invoke(delete_expense, ['--id', '1'])

    assert result.exit_code == 0
    writer = mock_dependencies['csv_writer'].return_value
    assert not writer.writerows.called


def test_delete_expense_write_error(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['open_mock'].side_effect = PermissionError("Access denied")

    result = runner.invoke(delete_expense, ['--all'], input='y\n')

    assert result.exit_code == 0
    assert "Access denied" in str(result.output)
