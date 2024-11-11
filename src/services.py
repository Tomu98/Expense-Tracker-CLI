from data_manager import initialize_csv, save_expense, get_expenses_count
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
