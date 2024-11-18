import click
import csv
from rich.console import Console
from rich.table import Table
from data_manager import CSV_FILE_PATH


@click.command()
def list_expenses():
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

    # Create table
    table = Table(title="Expenses")

    table.add_column("ID", style="dim", width=6)
    table.add_column("Date", justify="center", width=12)
    table.add_column("Description", justify="left", width=20)
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
