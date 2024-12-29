import click
from datetime import datetime
from styles.colors import console
from utils.budget import check_budget_warning
from utils.data_manager import initialize_csv, save_expense, get_next_expense_id
from utils.validators import validate_date, validate_amount, validate_category, validate_description


@click.command()
@click.option("--date", type=str, default=None, help="Date of the expense (optional).")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
@click.option("--category", type=str, prompt="Category", help="Category of the expense.")
@click.option("--description", type=str, default=None, help="Expense description.")
def add_expense(date, amount, category, description):
    """
    Adds a new expense, including category, description, and amount.
    Validates inputs, saves the expense, and checks for budget warnings.
    """
    initialize_csv()

    # Validations
    amount = validate_amount(amount)
    category = validate_category(category)
    description = validate_description(description)
    if date:
        expense_date = validate_date(date)
    else:
        expense_date = datetime.now().strftime("%Y-%m-%d")

    # Generate new expense ID and date
    new_id = get_next_expense_id()

    expense = {
        "ID": str(new_id),
        "Date": expense_date,
        "Amount": f"{amount:.2f}",
        "Category": category,
        "Description": description,
    }

    save_expense(expense)

    # Check if the expense exceeds the budget
    current_year = datetime.now().year
    current_month = datetime.now().month

    console.print(
    "\n[success]Expense added successfully:[/success]\n"
    f"[white]- ID: [id]{new_id}[/id][/white]\n"
    f"[white]- Date: [date]{expense_date}[/date][/white]\n"
    f"[white]- Amount: [amount]${amount:.2f}[/amount][/white]\n"
    f"[white]- Category: [category]'{category}'[/category][/white]\n"
    f"[white]- Description: [description]'{description}'[/description][/white]\n"
    )

    budget_warning_message = check_budget_warning(current_year, current_month)
    if budget_warning_message is not None:
        console.print(budget_warning_message)
