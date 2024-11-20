import click
import csv
from utils.validators import validate_date, validate_category, validate_description, validate_amount
from data_manager import CSV_FILE_PATH, FIELD_NAMES


@click.command()
@click.option("--id", prompt="ID", help="ID of the expense to be updated.")
@click.option("--new-date", type=str, help="New date (YYYYY-MM-DD).")
@click.option("--new-category", type=str, help="New category.")
@click.option("--new-description", type=str, help="New description.")
@click.option("--new-amount", type=float, help="New amount.")
def update_expense(id, new_date, new_category, new_description, new_amount):
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)

        expense_found = False
        for expense in expenses:
            if expense["ID"] == id:
                expense_found = True

                if new_date:
                    expense["Date"] = validate_date(new_date)

                if new_category:
                    expense["Category"] = validate_category(new_category)

                if new_description:
                    expense["Description"] = validate_description(new_description)

                if new_amount is not None:
                    expense["Amount"] = f"{validate_amount(new_amount):.2f}"

                break

        if not expense_found:
            click.echo(f"No expense found with ID {id}.")
            return

        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(expenses)

        click.echo(f"Expense with ID {id} successfully updated.")

    except FileNotFoundError:
        click.echo("Error: Expense file not found.")
    except click.BadParameter as e:
        click.echo(f"Validation error: {e}")
    except Exception as e:
        click.echo(f"Error updating expense: {e}")
