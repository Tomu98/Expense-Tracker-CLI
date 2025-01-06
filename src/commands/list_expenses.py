import click
from rich.table import Table
from styles.colors import console
from utils.data_manager import read_expenses
from utils.validators import validate_parse_date, validate_amount, validate_category


@click.command()
@click.option("--category", type=str, help="Filter by expense category")
@click.option("--from", "start_date", help="Filter expenses from this date onwards (YYYY-MM-DD). Combine with --to for a date range.")
@click.option("--to", "end_date", help="Filter expenses up to this date (YYYY-MM-DD). Combine with --from for a date range.")
@click.option("--min", "min_amount", type=float, help="Show expenses above or equal to this amount")
@click.option("--max", "max_amount", type=float, help="Show expenses below or equal to this amount")
def list_expenses(category, start_date, end_date, min_amount, max_amount):
    """
    List and filter expenses.

    Displays expenses in a formatted table with optional filters:
    - Category filter shows only expenses in the specified category
    - Date filters show expenses within the given range
    - Amount filters show expenses within the specified range

    All filters can be combined. When no filters are applied, shows all expenses.
    """
    try:
        expenses = read_expenses()
    except FileNotFoundError:
        console.print("\n[error]Error:[/error] [white]No expenses file was found.[/white]\n")
        return

    if not expenses:
        console.print("\n[warning]No expenses recorded.[/warning]\n")
        return

    # Filters
    if category:
        category = validate_category(category)
        expenses = [expense for expense in expenses if expense["Category"] == category]

    if start_date and end_date:
        validate_parse_date(start_date, force_full_date=True)
        validate_parse_date(end_date, force_full_date=True)

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        expenses = [expense for expense in expenses if start_date <= expense["Date"] <= end_date]

    if start_date and not end_date:
        validate_parse_date(start_date, force_full_date=True)
        expenses = [expense for expense in expenses if expense["Date"] >= start_date]

    if end_date and not start_date:
        validate_parse_date(end_date, force_full_date=True)
        expenses = [expense for expense in expenses if expense["Date"] <= end_date]

    if min_amount is not None:
        min_amount = validate_amount(min_amount)
        expenses = [expense for expense in expenses if float(expense["Amount"]) >= min_amount]

    if max_amount is not None:
        max_amount = validate_amount(max_amount)
        expenses = [expense for expense in expenses if float(expense["Amount"]) <= max_amount]

    if not expenses:
        console.print("\n[warning]No expenses matched the given filters.[/warning]\n")
        return

    # Create table
    table = Table(
        title="\nFiltered Expenses" if any([category, start_date, end_date, min_amount, max_amount]) 
        else "\nExpenses",
        row_styles=["none", "dim"],
    )

    table.add_column("ID", style="id", min_width=6)
    table.add_column("Date", justify="center", style="date", min_width=12)
    table.add_column("Amount", justify="right", style="amount", min_width=10)
    table.add_column("Category", justify="left", style="category", min_width=15)
    table.add_column("Description", justify="left", style="white", min_width=15, max_width=70)

    for expense in expenses:
        table.add_row(
            f"{expense['ID']}",
            f"{expense['Date']}",
            f"$ {float(expense['Amount']):.2f}",
            f"{expense['Category']}",
            f"{expense['Description']}",
        )

    console.print(table)
