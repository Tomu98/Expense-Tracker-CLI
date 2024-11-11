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


def get_expenses_count() -> int:
    with open(CSV_FILE_PATH, "r", newline="") as file:
        # The header is ignored and only non-empty lines are counted.
        return sum(1 for line in file if line.strip()) - 1

def read_expenses() -> list:
    with open(CSV_FILE_PATH, "r", newline="") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
