import click
from datetime import datetime
from styles.colors import console
from src.utils.budget_helpers import read_budget, calculate_monthly_expenses
from utils.data_manager import read_expenses, filter_expenses
from utils.validators import validate_parse_date, validate_category


@click.command()
@click.option("--date", type=str, help="Filter expenses by year (e.g., 2024) or year and month (e.g., 2024-01).")
@click.option("--category", type=str, help="Filter expenses by a specific category.")
def summary(date, category):
    """
    Displays a summary of expenses, optionally filtered by date or category.
    It also includes budget information, if applicable, and provides a breakdown of expenses by category.
    """
    try:
        # Parse and validate the date
        year, month, _ = validate_parse_date(date) if date else (None, None)

        # Validate the category, if provided
        target_category = category.capitalize() if category else None
        if target_category:
            validate_category(target_category)

        # Read and process CSV file
        expenses = read_expenses()
        total_expense, filtered_expense, category_summary = filter_expenses(
            expenses, year, month, target_category
        )

        # Read the budget for the target month and year
        budgets = read_budget()
        budget_key = f"{year}-{month:02d}" if year and month else None
        budget_amount = budgets.get(budget_key) if budget_key else None

        # Show results
        if year or month or target_category:
            if filtered_expense == 0.00:
                console.print("[warning]No expenses found for the specified filters.[/warning]")
                return

            # Show total expenses
            filter_desc = []
            if month:
                month_name = datetime(year, month, 1).strftime("%B")
                filter_desc.append(f"{month_name} {year}")
            elif year:
                filter_desc.append(f"{year}")
            if target_category:
                filter_desc.append(f"category '{target_category}'")

            filter_text = " and ".join(filter_desc)
            console.print(f"\n[white]Total expenses for {filter_text}: [amount]${filtered_expense:.2f}[/amount][/white]")

            # Show budget information
            if budget_amount is not None:
                current_expenses = calculate_monthly_expenses(year, month)
                remaining_budget = budget_amount - current_expenses
                console.print(f"\n[white]Budget for {month_name} {year}: [budget]${budget_amount:.2f}[/budget][/white]")
                if remaining_budget < 0:
                    console.print(f"[white]You've exceeded your budget by [amount2]${abs(remaining_budget):.2f}[/amount2][/white]")
                else:
                    console.print(f"[white]Remaining budget: [budget2]${remaining_budget:.2f}[/budget2][/white]")

            # Show breakdown only if no category is specified
            if not target_category:
                console.print("\n[white]Breakdown by category:[/white]")
                for cat, amount in category_summary.items():
                    console.print(f"- [category2]{cat}:[/category2] [amount]${amount:.2f}[/amount]")

        else:
            console.print(f"\n[white]Total expenses:[/white] [amount]${total_expense:.2f}[/amount]\n")

    except FileNotFoundError:
        console.print("[error]Error:[/error] No expenses file was found.")
    except PermissionError:
        console.print("[error]Error:[/error] Permission denied to read the expenses file.")
    except Exception as e:
        console.print(f"[error]Unexpected error:[/error] [white]{e}[/white]")
