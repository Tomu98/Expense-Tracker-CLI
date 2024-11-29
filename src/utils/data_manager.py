import csv
from typing import Dict
from pathlib import Path


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
