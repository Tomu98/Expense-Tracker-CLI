import click
import csv
from utils.budget import check_budget_warning
from utils.data_manager import CSV_FILE_PATH, FIELD_NAMES
from utils.validators import validate_date, validate_category, validate_description, validate_amount


@click.command()
@click.option("--id", type=int, prompt="ID", help="ID of the expense to be updated.")
@click.option("--date", type=str, help="New date (YYYYY-MM-DD).")
@click.option("--category", type=str, help="New category.")
@click.option("--description", type=str, help="New description.")
@click.option("--amount", type=float, help="New amount.")
def update_expense(id, date, category, description, amount):
    """
    Allows the user to update an existing expense by ID.
    It validates inputs and checks if the updated expense exceeds the monthly budget limit.
    """
    try:
        if id <= 0:
            raise click.BadParameter("ID must be a positive number greater than 0.", param_hint="--id")

        if not (date or category or description or amount):
            raise click.UsageError("You must provide at least one field to update (e.g., --date.)")

        # Validate that the file exists
        try:
            with open(CSV_FILE_PATH, "r", newline="") as file:
                reader = csv.DictReader(file)
                expenses = list(reader)
        except FileNotFoundError:
            click.echo("Error: Expense file not found.")
            return

        # Find the ID and update if it exists
        expense_found = False
        updated_date = None
        for expense in expenses:
            if expense["ID"] == str(id):
                expense_found = True

                if date:
                    validated_date = validate_date(date)
                    expense["Date"] = validated_date
                    updated_date = validated_date
                else:
                    updated_date = expense["Date"]

                if category:
                    expense["Category"] = validate_category(category)

                if description:
                    expense["Description"] = validate_description(description)

                if amount is not None:
                    expense["Amount"] = f"{validate_amount(amount):.2f}"

                break

        if not expense_found:
            click.echo(f"Error: No expense found with ID '{id}'.")
            return

        # Overwrite file with updated data
        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(expenses)

        click.echo(f"Expense with ID '{id}' successfully updated.")

        # Check if the updated expense affects the monthly budget
        expense_year, expense_month = map(int, updated_date.split("-")[:2])

        # Budget message
        budget_warning_message = check_budget_warning(expense_year, expense_month)
        if budget_warning_message is not None:
            click.echo(budget_warning_message)

    except click.BadParameter as e:
        click.echo(f"Validation error: {e}")
    except click.UsageError as e:
        click.echo(f"Usage error: {e}")
    except Exception as e:
        click.echo(f"Error updating expense: {e}")
