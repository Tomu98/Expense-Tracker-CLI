import pytest
from click.testing import CliRunner
from src.commands.summary_expenses import summary


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_expenses():
    return [
        {"ID": "1", "Date": "2025-01-07", "Amount": "50.00", "Category": "Groceries", "Description": "Weekly groceries for the house"},
        {"ID": "2", "Date": "2025-01-07", "Amount": "30.00", "Category": "Leisure", "Description": "I go out with my sweetheart <3"},
        {"ID": "3", "Date": "2025-02-15", "Amount": "25.00", "Category": "Groceries", "Description": "Some fruits"},
        {"ID": "4", "Date": "2024-12-23", "Amount": "4000.00", "Category": "Electronics", "Description": "New PC for Christmas :D"}
    ]


@pytest.fixture
def mock_budget():
    return {
        "2025-01": 200.00,
        "2025-02": 150.00
    }


@pytest.fixture
def mock_dependencies(mocker):
    return {
        'read_expenses': mocker.patch('src.commands.summary_expenses.read_expenses'),
        'read_budget': mocker.patch('src.commands.summary_expenses.read_budget'),
        'filter_expenses': mocker.patch('src.commands.summary_expenses.filter_expenses'),
        'calculate_monthly_expenses': mocker.patch('src.commands.summary_expenses.calculate_monthly_expenses'),
        'validate_parse_date': mocker.patch('src.commands.summary_expenses.validate_parse_date'),
        'validate_category': mocker.patch('src.commands.summary_expenses.validate_category')
    }


def test_summary_all_expenses(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        205.00,
        {"Groceries": 75.00, "Leisure": 30.00, "Electronics": 4000.00}
    )

    result = runner.invoke(summary)

    assert result.exit_code == 0
    assert "$205.00" in result.output
    assert "Groceries: $75.00" in result.output
    assert "Leisure: $30.00" in result.output
    assert "Electronics: $4000.00" in result.output


def test_summary_by_year(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = (2025, None, None)
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        105.00,
        {"Groceries": 75.00, "Leisure": 30.00}
    )

    result = runner.invoke(summary, ['--date', '2025'])

    assert result.exit_code == 0
    assert "Total expenses for 2025: $105.00" in result.output
    assert "Groceries: $75.00" in result.output
    assert "Leisure: $30.00" in result.output


def test_summary_by_month(runner, mock_dependencies, mock_expenses, mock_budget):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['read_budget'].return_value = mock_budget
    mock_dependencies['validate_parse_date'].return_value = (2025, 1, None)
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        80.00,
        {"Groceries": 50.00, "Leisure": 30.00}
    )
    mock_dependencies['calculate_monthly_expenses'].return_value = 80.00

    result = runner.invoke(summary, ['--date', '2025-01'])

    assert result.exit_code == 0
    assert "Total expenses for January 2025: $80.00" in result.output
    assert "Budget for January 2025: $200.00" in result.output
    assert "Remaining budget: $120.00" in result.output
    assert "Groceries: $50.00" in result.output
    assert "Leisure: $30.00" in result.output


def test_summary_by_category(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        75.00,
        {"Groceries": 75.00}
    )

    result = runner.invoke(summary, ['--category', 'groceries'])

    assert result.exit_code == 0
    assert "Total expenses for category 'Groceries': $75.00" in result.output
    assert "Breakdown by category" not in result.output


def test_summary_combined_filters(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = (2025, 1, None)
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        50.00,
        {"Groceries": 50.00}
    )

    result = runner.invoke(summary, ['--date', '2025-01', '--category', 'groceries'])

    assert result.exit_code == 0
    assert "Total expenses for January 2025 and category 'Groceries':" in result.output
    assert "Breakdown by category" not in result.output


def test_summary_no_expenses_for_filter(runner, mock_dependencies, mock_expenses):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['validate_parse_date'].return_value = (2023, None, None)
    mock_dependencies['filter_expenses'].return_value = (205.00, 0.00, {})

    result = runner.invoke(summary, ['--date', '2023'])

    assert result.exit_code == 0
    assert "No expenses found for the specified filters" in result.output


def test_summary_by_month_over_budget(runner, mock_dependencies, mock_expenses, mock_budget):
    mock_dependencies['read_expenses'].return_value = mock_expenses
    mock_dependencies['read_budget'].return_value = mock_budget
    mock_dependencies['validate_parse_date'].return_value = (2025, 2, None)
    mock_dependencies['filter_expenses'].return_value = (
        205.00,
        180.00,
        {"Groceries": 180.00}
    )
    mock_dependencies['calculate_monthly_expenses'].return_value = 180.00

    result = runner.invoke(summary, ['--date', '2025-02'])

    assert result.exit_code == 0
    assert "Total expenses for February 2025: $180.00" in result.output
    assert "Budget for February 2025: $150.00" in result.output
    assert "You've exceeded your budget by $30.00" in result.output


def test_summary_no_expenses(runner, mock_dependencies):
    mock_dependencies['read_expenses'].return_value = []
    mock_dependencies['filter_expenses'].return_value = (0.00, 0.00, {})

    result = runner.invoke(summary)

    assert result.exit_code == 0
    assert "$0.00" in result.output


def test_summary_permission_error(runner, mock_dependencies):
    mock_dependencies['read_expenses'].side_effect = PermissionError()

    result = runner.invoke(summary)

    assert result.exit_code == 0
    assert "Permission denied to read the expenses file" in result.output
