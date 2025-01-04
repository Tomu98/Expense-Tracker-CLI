import pytest
import click
import csv
from io import StringIO
from textwrap import dedent
from src.utils.data_manager import initialize_csv, save_expense, get_next_expense_id, parse_date, filter_expenses


@pytest.fixture
def sample_expenses():
    csv_data = dedent(
        """\
        Date,Amount,Category,Description
        2025-01-01,100.00,Groceries,Shopping at supermarket
        2025-01-01,50.00,Leisure,Movie night
        2024-12-31,200.00,Groceries,New Year's Eve party
        INVALID-DATE,50.00,Leisure,Invalid date test
        2025-01-01,INVALID-AMOUNT,Groceries,Invalid amount test
    """
    )
    return csv.DictReader(StringIO(csv_data))


def test_initialize_csv(mocker):
    mock_mkdir = mocker.patch("pathlib.Path.mkdir")
    mock_open = mocker.patch("pathlib.Path.open", mocker.mock_open())

    initialize_csv()

    mock_mkdir.assert_called_once_with(exist_ok=True)
    mock_open.assert_called_once_with("x", newline="", encoding="utf-8")


def test_save_expense(mocker):
    mock_open = mocker.patch("pathlib.Path.open", mocker.mock_open())
    mock_writer = mocker.patch("csv.DictWriter")
    mock_writer_instance = mock_writer.return_value

    expense = {
        "ID": "1",
        "Date": "2025-01-02",
        "Amount": "100.00",
        "Category": "Groceries",
        "Description": "Supermarket shopping",
    }

    save_expense(expense)

    mock_open.assert_called_once_with("a", newline="", encoding="utf-8")
    mock_writer.assert_called_once_with(mock_open(), fieldnames=["ID", "Date", "Amount", "Category", "Description"])
    mock_writer_instance.writerow.assert_called_once_with(expense)


def test_get_next_expense_id_empty_file(mocker):
    mocker.patch("pathlib.Path.open", mocker.mock_open(read_data="ID,Date,Amount,Category,Description\n"))
    assert get_next_expense_id() == 1


def test_get_next_expense_id_non_empty_file(mocker):
    mocker.patch(
        "pathlib.Path.open",
        mocker.mock_open(
            read_data=(
                "ID,Date,Amount,Category,Description\n"
                "1,2025-01-01,100.00,Groceries,Shopping at supermarket\n"
                "2,2025-01-02,50.00,Leisure,Movie night\n"
            )
        ),
    )
    assert get_next_expense_id() == 3


@pytest.mark.parametrize(
    "date_input,expected_year,expected_month",
    [
        ("2025", 2025, None),
        ("2025-01", 2025, 1),
    ],
)
def test_parse_date_valid_formats(date_input, expected_year, expected_month):
    year, month = parse_date(date_input)
    assert year == expected_year
    assert month == expected_month


@pytest.mark.parametrize("invalid_date", ["2025-13", "abcd", "20251", "2025-012", ""],)
def test_parse_date_invalid_format(invalid_date):
    with pytest.raises(click.BadParameter, match="Invalid date format.*"):
        parse_date(invalid_date)


def test_filter_expenses_by_year(sample_expenses):
    total_expense, filtered_expense, category_summary = filter_expenses(sample_expenses, target_year=2025)
    assert total_expense == 350.00
    assert filtered_expense == 150.00
    assert category_summary["Groceries"] == 100.00
    assert category_summary["Leisure"] == 50.00


def test_filter_expenses_by_year_and_month(sample_expenses):
    total_expense, filtered_expense, category_summary = filter_expenses(sample_expenses, target_year=2025, target_month=1)
    assert total_expense == 350.00
    assert filtered_expense == 150.00
    assert category_summary["Groceries"] == 100.00


def test_filter_expenses_by_year_month_and_category(sample_expenses):
    total_expense, filtered_expense, category_summary = filter_expenses(sample_expenses, target_year=2025, target_month=1, target_category="Groceries")
    assert total_expense == 350.00
    assert filtered_expense == 100.00
    assert category_summary["Groceries"] == 100.00


def test_filter_expenses_with_invalid_rows(sample_expenses, capsys):
    total_expense, filtered_expense, category_summary = filter_expenses(sample_expenses, target_year=2025)

    assert total_expense == 350.00
    assert filtered_expense == 150.00
    assert category_summary["Groceries"] == 100.00
    assert category_summary["Leisure"] == 50.00

    captured = capsys.readouterr()
    assert "Skipping row due to error" in captured.out


def test_filter_expenses_no_filters(sample_expenses):
    total_expense, filtered_expense, category_summary = filter_expenses(sample_expenses, target_year=None)
    assert total_expense == 350.00
    assert filtered_expense == 350.00
    assert category_summary["Groceries"] == 300.00
    assert category_summary["Leisure"] == 50.00
