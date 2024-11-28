import csv
from datetime import datetime
from data_manager import CSV_FILE_PATH, read_budget


def calculate_monthly_expenses(year: int, month: int) -> float:
    total_expenses = 0.0

    try:
        with open(CSV_FILE_PATH, "r", newline="", encoding="utf-8") as file:
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
                f"Monthly budget: ${budget_amount:.2f}. "
                f"Current expenses: ${current_expenses:.2f}. "
                f"Remaining budget: ${remaining:.2f}."
            )

    return None
