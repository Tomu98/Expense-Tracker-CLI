import click
import csv
from styles.colors import console
from utils.budget_helpers import check_budget_warning
from utils.data_manager import CSV_FILE_PATH, FIELD_NAMES, initialize_csv, read_expenses
from utils.validators import validate_parse_date, validate_amount, validate_category, validate_description


@click.command()
@click.option("--id", type=int, prompt="ID", help="ID of the expense to be updated.")
@click.option("--date", type=str, help="New date (YYYY-MM-DD).")
@click.option("--amount", type=float, help="New amount.")
@click.option("--category", type=str, help="New category.")
@click.option("--description", type=str, help="New description. You can use quotes for multiple words.")
def update_expense(id, date, amount, category, description):
    """
    Allows the user to update an existing expense by ID.
    It validates inputs and checks if the updated expense exceeds the monthly budget limit.
    """
    try:
        if id <= 0:
            raise click.BadParameter("ID must be a positive number greater than 0.", param_hint="--id")

        if not (date or category or description or amount):
            raise click.UsageError("You must provide at least one field to update (e.g., --date).")

        initialize_csv()

        # Validate that the file exists
        expenses = read_expenses()
        if not expenses:
            console.print("\n[error]Error:[/error] No expenses found. The file is empty.\n")
            return

        # Find the ID and update if it exists
        expense_found = False
        updated_date = None
        update_summary = []
        for expense in expenses:
            if expense["ID"] == str(id):
                expense_found = True

                # Track and compare changes
                original_date = expense["Date"]
                original_category = expense["Category"]
                original_description = expense["Description"]
                original_amount = expense["Amount"]

                if date:
                    year, month, day = validate_parse_date(date, force_full_date=True)
                    validated_date = f"{year:04d}-{month:02d}-{day:02d}"
                    if original_date != validated_date:
                        update_summary.append(f"[white]- New Date: [white_dim]{original_date}[/white_dim] ---> [date]{validated_date}[/date][/white]")
                    else:
                        update_summary.append(f"[white]- Date: [date]{original_date}[/date][/white]")
                    expense["Date"] = validated_date
                    updated_date = validated_date
                else:
                    update_summary.append(f"[white]- Date: [date]{original_date}[/date][/white]")
                    updated_date = original_date

                if amount is not None:
                    validated_amount = f"{validate_amount(amount):.2f}"
                    if original_amount != validated_amount:
                        update_summary.append(f"[white]- New Amount: [white_dim]${original_amount}[/white_dim] ---> [amount]${validated_amount}[/amount][white]")
                    else:
                        update_summary.append(f"[white]- Amount: [amount]${original_amount}[/amount][white]")
                    expense["Amount"] = validated_amount
                else:
                    update_summary.append(f"[white]- Amount: [amount]${original_amount}[/amount][white]")

                if category:
                    validated_category = validate_category(category)
                    if original_category != validated_category:
                        update_summary.append(f"[white]- New Category: [white_dim]'{original_category}'[/white_dim] ---> [category]'{validated_category}'[/category][/white]")
                    else:
                        update_summary.append(f"[white]- Category: [category]'{original_category}'[/category][/white]")
                    expense["Category"] = validated_category
                else:
                    update_summary.append(f"[white]- Category: [category]'{original_category}'[category][/white]")

                if description:
                    validated_description = validate_description(description)
                    if original_description != validated_description:
                        update_summary.append(f"[white]- New Description: [white_dim]'{original_description}'[/white_dim] ---> [description]'{validated_description}'[/description][white]")
                    else:
                        update_summary.append(f"[white]- Description: [description]'{original_description}'[/description][white]")
                    expense["Description"] = validated_description
                else:
                    update_summary.append(f"[white]- Description: [description]'{original_description}'[/description][white]")

                break

        if not expense_found:
            console.print(f"\n[error]Error:[/error] No expense found with ID [id]{id}[/id].\n")
            return

        # Overwrite file with updated data
        with open(CSV_FILE_PATH, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(expenses)

        # Print the update summary
        console.print(f"\n[success]Expense with ID [id]{id}[/id] updated successfully:[/success]")
        for change in update_summary:
            console.print(change)

        # Check if the updated expense affects the monthly budget
        expense_year, expense_month, _ = map(int, updated_date.split("-"))

        # Budget message
        budget_warning_message = check_budget_warning(expense_year, expense_month)
        if budget_warning_message is not None:
            console.print(budget_warning_message)

    except click.BadParameter as e:
        console.print(f"\n[error]Validation error:[/error] [white]{e}[/white]\n")
    except click.UsageError as e:
        console.print(f"\n[error]Usage error:[/error] [white]{e}[/white]\n")
    except Exception as e:
        console.print(f"\n[error]Error updating expense:[/error] [white]{e}[/white]\n")
