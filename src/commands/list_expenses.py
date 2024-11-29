import click
import csv
from rich.console import Console
from rich.table import Table
from utils.data_manager import CSV_FILE_PATH
from utils.validators import validate_category, validate_amount, validate_date


@click.command()
@click.option("--category", help="Filter expenses by category.")
@click.option("--start-date", help="Filter expenses from a specific start date (YYYY-MM-DD).")
@click.option("--end-date", help="Filter expenses up to a specific end date (YYYY-MM-DD).")
@click.option("--min-amount", type=float, help="Filter expenses with a minimum amount.")
@click.option("--max-amount", type=float, help="Filter expenses with a maximum amount.")
def list_expenses(category, start_date, end_date, min_amount, max_amount):
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = [row for row in reader]
    except FileNotFoundError:
        click.echo("Error: No expenses file was found.")
        return
    except Exception as e:
        click.echo(f"Error reading file: {e}")
        return

    if not expenses:
        click.echo("No expenses recorded.")
        return

    # Filters
    try:
        if category:
            category = validate_category(category)
            expenses = [expense for expense in expenses if expense["Category"].capitalize() == category]

        if start_date:
            validate_date(start_date)
            expenses = [expense for expense in expenses if expense["Date"] >= start_date]

        if end_date:
            validate_date(end_date)
            expenses = [expense for expense in expenses if expense["Date"] <= end_date]

        if min_amount is not None:
            min_amount = validate_amount(min_amount)
            expenses = [expense for expense in expenses if float(expense["Amount"]) >= min_amount]

        if max_amount is not None:
            max_amount = validate_amount(max_amount)
            expenses = [expense for expense in expenses if float(expense["Amount"]) <= max_amount]

    except click.BadParameter as e:
        click.echo(e.message)
        return

    if not expenses:
        click.echo("No expenses matched the given filters.")
        return

    # Create table
    table = Table(title="Filtered Expenses" if category or start_date or end_date or min_amount or max_amount else "Expenses")

    table.add_column("ID", style="dim", width=6)
    table.add_column("Date", justify="center", width=12)
    table.add_column("Description", justify="left", max_width=60)
    table.add_column("Category", justify="left", width=15)
    table.add_column("Amount", justify="right", width=10)

    for expense in expenses:
        table.add_row(
            expense["ID"],
            expense["Date"],
            expense["Description"],
            expense["Category"],
            f"${expense['Amount']}"
        )

    console = Console()
    console.print(table)

# Ver si tengo que añadir información del presupuesto
