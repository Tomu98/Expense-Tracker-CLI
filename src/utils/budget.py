import csv
import json
import click
from pathlib import Path
from datetime import datetime
from utils.data_manager import CSV_FILE_PATH


BUDGET_FILE_PATH = Path("data/budgets.json")


def initialize_budget_file():
    BUDGET_FILE_PATH.parent.mkdir(exist_ok=True)
    if not BUDGET_FILE_PATH.exists():
        BUDGET_FILE_PATH.write_text("{}", encoding="utf-8")


def read_budget():
    if not BUDGET_FILE_PATH.exists():
        initialize_budget_file()
    return json.loads(BUDGET_FILE_PATH.read_text(encoding="utf-8"))


def save_budget(budgets):
    sorted_budgets = {k: budgets[k] for k in sorted(budgets.keys(), reverse=True)}
    BUDGET_FILE_PATH.write_text(
        json.dumps(sorted_budgets, indent=4, ensure_ascii=False), encoding="utf-8"
    )


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


def calculate_monthly_expenses(year: int, month: int) -> float:
    total_expenses = 0.0

    try:
        with CSV_FILE_PATH.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expense_date = datetime.strptime(row["Date"], "%Y-%m-%d")
                    if expense_date.year == year and expense_date.month == month:
                        total_expenses += float(row["Amount"])
                except ValueError:
                    continue
    except FileNotFoundError:
        total_expenses = 0.0

    return total_expenses


def check_budget_warning(year: int, month: int) -> str:
    budgets = read_budget()
    key = f"{year}-{month:02d}"

    if key in budgets:
        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(year, month)

        if current_expenses > budget_amount:
            return (
                f"Warning: You have exceeded your monthly budget for ${budget_amount:.2f} "
                f"with a total expense of ${current_expenses:.2f}."
            )
        else:
            remaining = budget_amount - current_expenses
            return (
                f"Monthly budget: ${budget_amount:.2f}.\n"
                f"Current expenses: ${current_expenses:.2f}.\n"
                f"Remaining budget: ${remaining:.2f}."
            )

    return None
