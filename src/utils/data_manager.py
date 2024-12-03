import click
import csv
from datetime import datetime
from typing import Dict
from pathlib import Path
from collections import defaultdict


DATA_DIR = Path("data")
CSV_FILE_PATH = DATA_DIR / "expenses.csv"
FIELD_NAMES = ["ID", "Date", "Description", "Category", "Amount"]


def initialize_csv():
    try:
        CSV_FILE_PATH.parent.mkdir(exist_ok=True)
        with CSV_FILE_PATH.open("x", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
    except FileExistsError:
        pass


def save_expense(expense: Dict[str, str]):
    with CSV_FILE_PATH.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(expense)


def get_next_expense_id() -> int:
    try:
        with CSV_FILE_PATH.open("r", newline="") as file:
            reader = csv.DictReader(file)
            ids = [int(row["ID"]) for row in reader if row["ID"].isdigit()]
            return max(ids, default=0) + 1
    except FileNotFoundError:
        return 1


def filter_expenses(reader, target_year, target_month=None, target_category=None):
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
