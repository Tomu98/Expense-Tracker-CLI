import click
from utils.budget import check_budget_warning
from utils.validators import validate_category, validate_description, validate_amount
from data_manager import initialize_csv, save_expense, get_next_expense_id
from datetime import datetime


@click.command()
@click.option("--category", type=str, prompt="Category", help="Category of the expense.")
@click.option("--description", type=str, default=None, help="Expense description.")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
def add_expense(category, description, amount):
    initialize_csv()

    # Validations
    category = validate_category(category)
    description = validate_description(description)
    amount = validate_amount(amount)

    # Generate new expense ID and date
    new_id = get_next_expense_id()
    expense_date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "ID": str(new_id),
        "Date": expense_date,
        "Category": category,
        "Description": description,
        "Amount": f"{amount:.2f}"
    }

    save_expense(expense)

    # Check if the expense exceeds the budget
    current_year = datetime.now().year
    current_month = datetime.now().month

    click.echo(f"Expense added successfully (ID: {new_id}, Category: '{category}', Amount: ${amount:.2f})")

    budget_warning_message = check_budget_warning(current_year, current_month)
    if budget_warning_message is not None:
        click.echo(budget_warning_message)

# Comprobar que todo esté bien ahora que agregué la función de presupuesto
