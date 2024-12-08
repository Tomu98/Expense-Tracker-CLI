import click
import csv
from utils.data_manager import CSV_FILE_PATH, FIELD_NAMES


@click.command()
@click.option("--id", type=int, required=True, help="ID of the expense to delete.")
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
            click.echo("No expenses found. Nothing to delete.")
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
                        click.echo("All expenses have been deleted successfully.")
                    except Exception as e:
                        click.echo(f"Error when deleting all expenses: {e}")
                    return
                elif confirmation in ["n", "no"]:
                    click.echo("Deletion cancelled.")
                    return
                else:
                    click.echo("Please enter a valid response: 'y' or 'n' (or 'yes'/'no').")

        if not id or int(id) <= 0:
            raise click.BadParameter("You must provide a valid positive ID.", param_hint="'--id'")

        updated_expenses = [expense for expense in expenses if expense["ID"] != id]

        if len(updated_expenses) == len(expenses):
            click.echo(f"No expense found with ID {id}.")
            return

        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(updated_expenses)

        click.echo(f"Expense with ID {id} has been deleted successfully.")

    except FileNotFoundError:
        click.echo("Error: Expense file not found.")
    except Exception as e:
        click.echo(f"Error when eliminating expense: {e}")
