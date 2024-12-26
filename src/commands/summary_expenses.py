import click
import csv
from datetime import datetime
from styles.colors import console
from utils.budget import read_budget, calculate_monthly_expenses
from utils.data_manager import CSV_FILE_PATH, filter_expenses
from utils.validators import validate_date, validate_category


@click.command()
@click.option("--month", type=int, help="Month number to show the summary (1-12).")
@click.option("--year", type=int, help="Year to show the summary (e.g., 2024).")
@click.option("--category", type=str, help="Filter expenses by a specific category.")
def summary(month, year, category):
    """
    Displays a summary of expenses, optionally filtered by year, month or category.
    It also includes budget information, if applicable, and provides a breakdown of expenses by category.
    """
    try:
        current_date = datetime.now()
        current_year = current_date.year

        # Validate initial values
        if month is not None and (month <= 0 or month > 12):
            raise click.BadParameter("Month must be between 1 and 12.", param_hint="'--month'")
        if year is not None and (year < 1800 or year > current_year):
            raise click.BadParameter(f"Year must be between 1800 and {current_year}.", param_hint="'--year'")

        # Default values for filters
        target_year = year if year else current_year
        target_month = month
        target_category = category.capitalize() if category else None

        # Validate remaining entries
        if target_month:
            validate_date(f"{target_year}-{target_month:02d}-01")
        if target_category:
            validate_category(target_category)

        # Read and process CSV file
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            total_expense, filtered_expense, category_summary = filter_expenses(
                reader, target_year, target_month, target_category
            )

        # Read the budget for the target month and year
        budgets = read_budget()
        budget_key = f"{target_year}-{target_month:02d}" if target_month else None
        budget_amount = budgets.get(budget_key) if budget_key else None

        # Show results
        if target_month or year or target_category:
            if filtered_expense == 0.00:
                console.print("[warning]No expenses found for the specified filters.[/warning]")
                return

            filter_desc = []
            if target_month:
                month_name = datetime(target_year, target_month, 1).strftime("%B")
                filter_desc.append(f"{month_name} {target_year}")
            elif year:
                filter_desc.append(f"{target_year}")
            if target_category:
                filter_desc.append(f"category '{target_category}'")

            filter_text = " and ".join(filter_desc)
            console.print(f"\n[white]Total expenses for {filter_text}: [amount]${filtered_expense:.2f}[/amount][/white]")

            if budget_amount is not None:
                current_expenses = calculate_monthly_expenses(target_year, target_month)
                remaining_budget = budget_amount - current_expenses
                console.print(f"\n[white]Budget for {filter_text}: [budget]${budget_amount:.2f}[/budget][/white]")
                console.print(f"[white]Remaining budget: [budget2]${remaining_budget:.2f}[budget2][/white]")

            # Show breakdown only if no category is specified
            if not target_category:
                console.print("\n[white]Breakdown by category:[/white]")
                for cat, amount in category_summary.items():
                    console.print(f"- [category2]{cat}:[/category2] [amount]${amount:.2f}[/amount]")

        else:
            console.print(f"\n[white]Total expenses:[/white] [amount]${total_expense:.2f}[/amount]\n")

    except FileNotFoundError:
        console.print("[danger]Error:[/danger] No expenses file was found.")
