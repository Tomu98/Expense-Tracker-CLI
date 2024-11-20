import csv
import os
from typing import Dict


CSV_FILE_PATH = os.path.join("data", "expenses.csv")
FIELD_NAMES = ["ID", "Date", "Description", "Category", "Amount"]


def initialize_csv():
    try:
        with open(CSV_FILE_PATH, "x", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
    except FileExistsError:
        pass


def save_expense(expense: Dict[str, str]):
    with open(CSV_FILE_PATH, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(expense)


def get_next_expense_id() -> int:
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            ids = [int(row["ID"]) for row in reader if row["ID"].isdigit()]
            return max(ids, default=0) + 1
    except FileNotFoundError:
        return 1
