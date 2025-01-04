import click
from rich.table import Table
from styles.colors import console
from utils.data_manager import read_expenses
from utils.validators import validate_parse_date, validate_amount, validate_category


@click.command()
@click.option("--category", type=str, help="Filter expenses by category.")
@click.option("--start-date", help="Filter expenses from a specific start date (YYYY-MM-DD).")
@click.option("--end-date", help="Filter expenses up to a specific end date (YYYY-MM-DD).")
@click.option("--min-amount", type=float, help="Filter expenses with a minimum amount.")
@click.option("--max-amount", type=float, help="Filter expenses with a maximum amount.")
def list_expenses(category, start_date, end_date, min_amount, max_amount):
    """
    Lists and filters. Users can filter by category, date range,
    and amount range, displaying results in a formatted table.
    """
    try:
        expenses = read_expenses()
    except FileNotFoundError:
        console.print("[error]Error:[/error] [white]No expenses file was found.[/white]")
        return
    except Exception as e:
        console.print(f"[error]Error reading file:[/error] [white]{e}[/white]")
        return

    if not expenses:
        console.print("[warning]No expenses recorded.[/warning]")
        return

    # Filters
    try:
        if category:
            category = validate_category(category)
            expenses = [expense for expense in expenses if expense["Category"].capitalize() == category]

        if start_date:
            validate_parse_date(start_date)
            expenses = [expense for expense in expenses if expense["Date"] >= start_date]

        if end_date:
            validate_parse_date(end_date)
            expenses = [expense for expense in expenses if expense["Date"] <= end_date]

        if min_amount is not None:
            min_amount = validate_amount(min_amount)
            expenses = [expense for expense in expenses if float(expense["Amount"]) >= min_amount]

        if max_amount is not None:
            max_amount = validate_amount(max_amount)
            expenses = [expense for expense in expenses if float(expense["Amount"]) <= max_amount]

    except click.BadParameter as e:
        console.print(f"[error]{e.message}[/error]")
        return

    if not expenses:
        console.print("[warning]No expenses matched the given filters.[/warning]")
        return

    # Create table
    table = Table(
        title="\nFiltered Expenses" if category or start_date or end_date or min_amount or max_amount 
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
