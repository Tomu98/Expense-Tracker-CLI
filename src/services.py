import csv
from data_manager import CSV_FILE_PATH, FIELD_NAMES, initialize_csv, save_expense, get_expenses_count, read_expenses
from datetime import datetime



def add_expense(category: str, description: str, amount: float):
    initialize_csv()

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
    return new_id


def delete_expense(expense_id: str):
    expenses = read_expenses()
    updated_expenses = [expense for expense in expenses if expense["ID"] != expense_id]

    if len(updated_expenses) == len(expenses):
        return False

    with open(CSV_FILE_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(updated_expenses)

    return True
