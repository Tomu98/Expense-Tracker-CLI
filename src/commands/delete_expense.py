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
                    "Are you sure you want to delete all expenses? (y/n)",
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
                        console.print(f"\n[error]Error when deleting all expenses:[/error] {e}\n")
                    return
                elif confirmation in ["n", "no"]:
                    console.print("\n[warning]Deletion cancelled.[/warning]\n")
                    return
                else:
                    console.print("\n[warning]Please enter a valid response:[/warning] [success]'y'[/success] or [error]'n'[/error] (or [success]'yes'[/success]/[error]'no'[/error]).\n")

        if not id or int(id) <= 0:
            raise click.BadParameter("You must provide a valid positive ID.", param_hint="'--id'")

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
        console.print("\n[error]Error:[/error] Expense file not found.\n")
    except Exception as e:
        console.print(f"\n[error]Error when eliminating expense:[/error] {e}\n")
