import click
import csv
from utils.constants import VALID_CATEGORIES
from data_manager import CSV_FILE_PATH, FIELD_NAMES
from datetime import datetime


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
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        expense["Date"] = new_date
                    except ValueError:
                        click.echo("Invalid date format. Use YYYY-MM-DD.")
                        return

                if new_category:
                    new_category = new_category.capitalize()
                    if new_category not in VALID_CATEGORIES:
                        click.echo("Invalid category. Choose from: " + ", ".join(VALID_CATEGORIES))
                        return
                    expense["Category"] = new_category

                if new_description:
                    if len(new_description) < 3 or len(new_description) > 100:
                        click.echo("Description must be between 3 and 100 characters.")
                        return
                    expense["Description"] = new_description

                if new_amount is not None:
                    if new_amount <= 0 or new_amount > 100000:
                        click.echo("Amount must be a positive number between 0 and 100,000.")
                        return
                    expense["Amount"] = f"{new_amount:.2f}"

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
    except Exception as e:
        click.echo(f"Error updating expense: {e}")

# Update expense:
# - Comprobar posibles fallos
# - Hacer que lo de actualizar lo que sea del gasto sea opcional y preguntando si está seguro de actualizar
# - Asegurar que tengan las mismas validaciones de los datos en amount, description, category y date
# Lo que ví:
# --- La fecha mejor ver que no reciba una futura que no pasó aún
