import click
from datetime import datetime
from styles.colors import console
from utils.budget_helpers import check_budget_warning
from utils.data_manager import initialize_csv, save_expense, get_next_expense_id
from utils.validators import validate_parse_date, validate_amount, validate_category, validate_description


@click.command()
@click.option("--date", type=str, default=None, help="Date of the expense. It's optional and defaults to today's date.")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
@click.option("--category", type=str, prompt="Category", help="Category of the expense.")
@click.option("--description", type=str, default=None, help="Expense description. You can use quotes for multiple words.")
def add_expense(date, amount, category, description):
    """
    Adds a new expense, including category, description, and amount.
    Validates inputs, saves the expense, and checks for budget warnings.
    """
    initialize_csv()

    # Validations
    if date:
        year, month, day = validate_parse_date(date, force_full_date=True)
        expense_date = f"{year:04d}-{month:02d}-{day:02d}"
    else:
        expense_date = datetime.now().strftime("%Y-%m-%d")
        year, month, day = map(int, expense_date.split('-'))
    amount = validate_amount(amount)
    category = validate_category(category)
    description = validate_description(description)

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
    console.print(
    "\n[success]Expense added successfully:[/success]\n"
    f"[white]- ID: [id]{new_id}[/id][/white]\n"
    f"[white]- Date: [date]{expense_date}[/date][/white]\n"
    f"[white]- Amount: [amount]${amount:.2f}[/amount][/white]\n"
    f"[white]- Category: [category]'{category}'[/category][/white]\n"
    f"[white]- Description: [description]'{description}'[/description][/white]"
    )

    budget_warning_message = check_budget_warning(year, month)
    if budget_warning_message is not None:
        console.print(budget_warning_message)
