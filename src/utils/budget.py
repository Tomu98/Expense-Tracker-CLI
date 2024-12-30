import csv
import json
import click
from pathlib import Path
from datetime import datetime
from styles.colors import console
from utils.data_manager import CSV_FILE_PATH


BUDGET_FILE_PATH = Path("data/budgets.json")


def initialize_budget_file():
    """
    Initializes the budget file.
    Creates the directory and file if they don't exist.
    The budget file is stored in JSON format.
    """
    BUDGET_FILE_PATH.parent.mkdir(exist_ok=True)
    if not BUDGET_FILE_PATH.exists():
        BUDGET_FILE_PATH.write_text("{}", encoding="utf-8")


def read_budget():
    """
    Reads the budget data from the budget file.

    Returns:
        dict: A dictionary containing the budget data, where keys are "YYYY-MM" strings
              and values are the budget amounts for those months.
    """
    if not BUDGET_FILE_PATH.exists():
        initialize_budget_file()
    return json.loads(BUDGET_FILE_PATH.read_text(encoding="utf-8"))


def save_budget(budgets):
    """
    Saves the budget data to the budget file in a sorted order.

    Args:
        budgets (dict): A dictionary containing budget data to save.
    """
    sorted_budgets = {k: budgets[k] for k in sorted(budgets.keys(), reverse=True)}
    BUDGET_FILE_PATH.write_text(
        json.dumps(sorted_budgets, indent=4, ensure_ascii=False), encoding="utf-8"
    )


def update_budget(month: int, year: int, amount: float):
    """
    Updates or creates a budget for a specific month and year.

    Args:
        month (int): The month for which the budget is being set (1-12).
        year (int): The year for which the budget is being set (e.g., 2024).
        amount (float): The budget amount to set.
    """
    budgets = read_budget()
    key = f"{year}-{month:02d}"

    if key in budgets:
        console.print(f"\n[warning]Warning:[/warning] A budget for [date]{year}-{month:02d}[/date] already exists.")

        while True:
            confirmation = click.prompt(f"Do you want to update the budget for {year}-{month:02d}? (y/n)", type=str).lower()

            if confirmation in ['y', 'yes']:
                budgets[key] = amount
                save_budget(budgets)
                console.print(f"\nBudget for [date]{year}-{month:02d}[/date] updated to [budget]${amount:.2f}[/budget].\n")
                return
            elif confirmation in ['n', 'no']:
                console.print(f"\nBudget for [date]{year}-{month:02d}[/date] remains unchanged at [budget]${amount:.2f}[/budget].\n")
                return
            else:
                console.print("\n[warning]Invalid input[/warning]. Please enter [success]'y/yes'[/success] or [error]'n/no'[/error].\n")
    else:
        budgets[key] = amount
        save_budget(budgets)
        console.print(f"\nBudget for [date]{year}-{month:02d}[/date] set at [budget]${amount:.2f}[/budget].\n")


def calculate_monthly_expenses(year: int, month: int) -> float:
    """
    Calculates the total expenses for a specific month and year from the expense data.

    Args:
        year (int): The year of the expenses to calculate.
        month (int): The month of the expenses to calculate.

    Returns:
        float: The total amount of expenses for the specified month and year.
    """
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
    """
    Checks if the expenses for a specific month and year exceed the budget.

    Args:
        year (int): The year to check the budget for.
        month (int): The month to check the budget for.

    Returns:
        str: A warning message if expenses exceed the budget, or information about the remaining budget.
             Returns None if no budget is set for the specified month and year.
    """
    budgets = read_budget()
    key = f"{year}-{month:02d}"

    if key in budgets:
        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(year, month)

        if current_expenses > budget_amount:
            return (
                f"[warning]Warning:[/warning] [white]You have exceeded your monthly budget for [/white]"
                f"[white][amount]${budget_amount:.2f}[/amount] with a total expense of [amount2]${current_expenses:.2f}[/amount2][/white].\n"
            )
        else:
            remaining = budget_amount - current_expenses
            return (
                f"\n[info]Budget information:[/info]\n"
                f"- Monthly budget: [budget]${budget_amount:.2f}[/budget]\n"
                f"- Current expenses: [amount]${current_expenses:.2f}[/amount]\n"
                f"- Remaining budget: [budget2]${remaining:.2f}[/budget2]\n"
            )

    return None


def get_budget_summary(year: int, month: int) -> dict:
    """
    Provides a summary of the budget and expenses for a specific month and year.

    Args:
        year (int): The year to summarize.
        month (int): The month to summarize.

    Returns:
        dict: A dictionary containing the budget summary, with keys.
    """
    budgets = read_budget()
    key = f"{year}-{month:02d}"
    summary = {"budget_set": False, "budget_amount": 0.0, "current_expenses": 0.0, "remaining_budget": 0.0}

    if key in budgets:
        summary["budget_set"] = True
        summary["budget_amount"] = budgets[key]
        summary["current_expenses"] = calculate_monthly_expenses(year, month)
        summary["remaining_budget"] = budgets[key] - summary["current_expenses"]

    return summary
