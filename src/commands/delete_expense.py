import click
import csv
from styles.colors import console
from utils.data_manager import CSV_FILE_PATH, FIELD_NAMES, read_expenses


@click.command()
@click.option("--id", type=int, required=False, help="ID of the expense to delete.")
@click.option("--all", is_flag=True, help="Delete all expenses.")
def delete_expense(id, all):
    """
    Delete a specific expense by ID or clear all expenses after user confirmation.
    """
    try:
        expenses = read_expenses()
        if not expenses:
            console.print("\n[warning]No expenses found. Nothing to delete.[/warning]\n")
            return

        if all:
            while True:
                confirmation = click.prompt(
                    "\nAre you sure you want to delete all expenses? (y/n)",
                    type=str,
                    default="n"
                ).lower()

                if confirmation in ["y", "yes"]:
                    try:
                        with open(CSV_FILE_PATH, "w", newline="", encoding="utf-8") as file:
                            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
                            writer.writeheader()
                        console.print("\n[success]All expenses have been deleted successfully.[/success]\n")
                    except Exception as e:
                        console.print(f"\n[error]Error when deleting all expenses:[/error] [white]{e}[/white]\n")
                    return
                elif confirmation in ["n", "no"]:
                    console.print("\n[warning]Deletion cancelled.[/warning]\n")
                    return
                else:
                    console.print("\n[warning]Please enter a valid response:[/warning] [white][success]'y'/'yes'[/success] or [error]'n'/'no'[/error].[/white]")

        if id is None:
            id = click.prompt("Expense ID to eliminate", type=int)

        if id <= 0:
            console.print("\n[error]You must provide a valid positive ID.[/error]\n")
            return

        updated_expenses = [expense for expense in expenses if int(expense["ID"]) != id]

        if len(updated_expenses) == len(expenses):
            console.print(f"\n[error]No expense found with ID [id]{id}[/id].[/error]\n")
            return

        with open(CSV_FILE_PATH, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(updated_expenses)

        console.print(f"\n[success]Expense with ID [id]{id}[/id] has been deleted successfully.[/success]\n")

    except FileNotFoundError:
        console.print("\n[error]Error:[/error] [white]Expense file not found.[/white]\n")
