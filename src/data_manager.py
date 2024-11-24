import os
import csv
import json
import click
from pathlib import Path
from typing import Dict


CSV_FILE_PATH = os.path.join("data", "expenses.csv")
FIELD_NAMES = ["ID", "Date", "Description", "Category", "Amount"]
BUDGET_FILE_PATH = Path("data/budgets.json")


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


def initialize_budget_file():
    if not BUDGET_FILE_PATH.exists():
        with open(BUDGET_FILE_PATH, "w") as file:
            json.dump({}, file)


def read_budget():
    if not BUDGET_FILE_PATH.exists():
        initialize_budget_file()
    with open(BUDGET_FILE_PATH, "r") as file:
        return json.load(file)


def save_budget(budgets):
    sorted_budgets = {k: budgets[k] for k in sorted(budgets.keys(), reverse=True)}

    with open(BUDGET_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(sorted_budgets, file, indent=4, ensure_ascii=False)


def update_budget(month: int, year: int, amount: float):
    budgets = read_budget()
    key = f"{year}-{month:02d}"

    if key in budgets:
        click.echo(f"Warning: A budget for {year}-{month:02d} already exists.")

        while True:
            confirmation = click.prompt(f"Do you want to update the budget for {year}-{month:02d}? (y/n)", type=str).lower()

            if confirmation in ['y', 'yes']:
                budgets[key] = amount
                save_budget(budgets)
                click.echo(f"Budget for {year}-{month:02d} updated to ${amount:.2f}.")
                return
            elif confirmation in ['n', 'no']:
                click.echo(f"Budget for {year}-{month:02d} remains unchanged at ${amount:.2f}.")
                return
            else:
                click.echo("Invalid input. Please enter 'y/yes' or 'n/no'.")
    else:
        budgets[key] = amount
        save_budget(budgets)
        click.echo(f"Budget for {year}-{month:02d} set at ${amount:.2f}.")
