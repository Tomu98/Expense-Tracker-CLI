import click
import csv
from styles.colors import console
from utils.data_manager import CSV_FILE_PATH, FIELD_NAMES


@click.command()
@click.option("--id", type=int, required=False, help="ID of the expense to delete.")
@click.option("--all", is_flag=True, help="Delete all expenses.")
def delete_expense(id, all):
    """
    Delete a specific expense by ID or clear all expenses after user confirmation.
    """
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)

        if not expenses:
            console.print("[warning]No expenses found. Nothing to delete.[/warning]")
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
                        with open(CSV_FILE_PATH, "w", newline="") as file:
                            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
                            writer.writeheader()
                        console.print("[success]All expenses have been deleted successfully.[/success]")
                    except Exception as e:
                        console.print(f"[danger]Error when deleting all expenses:[/danger] {e}")
                    return
                elif confirmation in ["n", "no"]:
                    console.print("[warning]Deletion cancelled.[/warning]")
                    return
                else:
                    console.print("[warning]Please enter a valid response:[/warning] 'y' or 'n' (or 'yes'/'no').")

        if not id or int(id) <= 0:
            raise click.BadParameter("You must provide a valid positive ID.", param_hint="'--id'")

        updated_expenses = [expense for expense in expenses if int(expense["ID"]) != id]

        if len(updated_expenses) == len(expenses):
            console.print(f"[danger]No expense found with ID [id]{id}[/id].[/danger]")
            return

        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(updated_expenses)

        console.print(f"[success]Expense with ID [id]{id}[/id] has been deleted successfully.[/success]")

    except FileNotFoundError:
        console.print("[danger]Error:[/danger] Expense file not found.")
    except Exception as e:
        console.print(f"[danger]Error when eliminating expense:[/danger] {e}")
