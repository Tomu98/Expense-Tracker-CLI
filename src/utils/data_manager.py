import click
import csv
from datetime import datetime
from typing import Dict
from pathlib import Path
from collections import defaultdict


DATA_DIR = Path("data")
CSV_FILE_PATH = DATA_DIR / "expenses.csv"
FIELD_NAMES = ["ID", "Date", "Amount", "Category", "Description"]


def initialize_csv():
    """
    Initializes the expenses CSV file.
    Creates the file and writes the header if it doesn't exist.
    """
    try:
        CSV_FILE_PATH.parent.mkdir(exist_ok=True)
        with CSV_FILE_PATH.open("x", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
    except FileExistsError:
        pass


def save_expense(expense: Dict[str, str]):
    """
    Saves a single expense entry to the CSV file.

    Args:
        expense (Dict[str, str]): A dictionary representing the expense with keys corresponding to FIELD_NAMES.
    """
    with CSV_FILE_PATH.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(expense)


def get_next_expense_id() -> int:
    """
    Retrieves the next available ID for a new expense entry.

    Returns:
        int: The next available ID, incremented from the highest ID found in the file. 
             If the file is empty or doesn't exist, returns 1.
    """
    try:
        with CSV_FILE_PATH.open("r", newline="") as file:
            reader = csv.DictReader(file)
            ids = [int(row["ID"]) for row in reader if row["ID"].isdigit()]
            return max(ids, default=0) + 1
    except FileNotFoundError:
        return 1


def parse_date(date_str):
    """
    Parse a date string in the format 'YYYY' or 'YYYY-MM' and return the corresponding year and month.
    If only 'YYYY' is provided, the month defaults to None.
    """
    try:
        if len(date_str) == 4:
            return int(date_str), None
        elif len(date_str) == 7:
            parsed_date = datetime.strptime(date_str, "%Y-%m")
            return parsed_date.year, parsed_date.month
        else:
            raise ValueError
    except ValueError:
        raise click.BadParameter("Invalid date format. Use 'YYYY' or 'YYYY-MM' and ensure it's a valid date.", param_hint="'--date'")


def filter_expenses(reader, target_year, target_month=None, target_category=None):
    """
    Filters expenses by year, month, and category.

    Args:
        reader: CSV reader object with expense data.
        target_year (int): Year to filter by.
        target_month (int, optional): Month (1-12). Defaults to all months.
        target_category (str, optional): Category. Defaults to all categories.

    Returns:
        tuple: (total_expense, filtered_expense, category_summary)
    """
    total_expense = 0.00
    filtered_expense = 0.00
    category_summary = defaultdict(float)

    for row in reader:
        try:
            date = datetime.strptime(row["Date"], "%Y-%m-%d")
            amount = float(row["Amount"])
            category = row["Category"].capitalize()

            total_expense += amount

            matches_date = (not target_month or date.month == target_month) and date.year == target_year
            matches_category = not target_category or category == target_category

            if matches_date and matches_category:
                filtered_expense += amount
                category_summary[category] += amount

        except ValueError as e:
            click.echo(f"Skipping row due to error: {e}")

    return total_expense, filtered_expense, category_summary
