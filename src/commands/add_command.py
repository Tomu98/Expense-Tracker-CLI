import click
from data_manager import initialize_csv, save_expense, get_expenses_count, VALID_CATEGORIES
from datetime import datetime


@click.command()
@click.option("--category", type=str, prompt="Category", help="Category of the expense.")
@click.option("--description", default=None, help="Expense description.")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
def add_expense(category, description, amount):
    initialize_csv()

    # Validate category
    category = category.capitalize()
    if category not in VALID_CATEGORIES:
        click.echo("Invalid category. Choose from: " + ", ".join(VALID_CATEGORIES))
        return

    # Validate amount
    try:
        if amount <= 0:
            raise ValueError("Amount must be a positive number and higher than 0.")
        if amount > 100000:
            raise ValueError(f"Amount exceeds the maximum limit of $100000.")
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    # Validate description
    if description:
        if len(description) < 3:
            click.echo(f"Error: Description must be at least 3 characters.")
            return
        elif len(description) > 100:
            click.echo(f"Error: Description must be no more than 100 characters.")
            return
    else:
        description = "..."

    # Generate new expense ID and date
    new_id = get_expenses_count() + 1
    expense_date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "ID": str(new_id),
        "Date": expense_date,
        "Category": category,
        "Description": description,
        "Amount": f"{amount:.2f}"
    }

    save_expense(expense)

    click.echo(f"Expense added successfully (ID: {new_id}, Category: '{category}', Amount: ${amount:.2f})")
