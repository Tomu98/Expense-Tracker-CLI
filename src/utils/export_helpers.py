import re
import csv
import json
from openpyxl import Workbook
from datetime import datetime
from styles.colors import console


def validate_expenses_data(data):
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Invalid data format. Expected a list of dictionaries.")


def format_budget_summary(budget_info):
    return {
        "Budget Amount": f"${budget_info['budget_amount']:.2f}",
        "Current Expenses": f"${budget_info['current_expenses']:.2f}",
        "Remaining Budget": f"${budget_info['remaining_budget']:.2f}",
    }


def write_csv(output_path, data, budget_info=None):
    """
    Exports expense data and optional budget summary to a CSV file.

    Args:
        output_path (str): Path to save the CSV file.
        data (list of dict): List of expenses, each represented as a dictionary.
        budget_info (dict, optional): Budget summary including budget amount, current expenses,
                                      and remaining budget. Defaults to None.
    """
    validate_expenses_data(data)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Date", "Amount", "Category", "Description"])
        writer.writeheader()
        writer.writerows(data)

        if budget_info:
            summary = format_budget_summary(budget_info)
            writer.writerow({})
            writer.writerow({"ID": "Budget Information"})
            writer.writerow({
                "Date": "Budget Amount",
                "Description": "",
                "Category": "",
                "Amount": summary["Budget Amount"]
            })
            writer.writerow({
                "Date": "Current Expenses",
                "Description": "",
                "Category": "",
                "Amount": summary["Current Expenses"]
            })
            writer.writerow({
                "Date": "Remaining Budget",
                "Description": "",
                "Category": "",
                "Amount": summary["Remaining Budget"]
            })


def write_json(output_path, data, budget_info=None):
    """
    Exports expense data and optional budget summary to a JSON file.

    Args:
        output_path (str): Path to save the JSON file.
        data (list of dict): List of expenses, each represented as a dictionary.
        budget_info (dict, optional): Budget summary including budget amount, current expenses,
                                      and remaining budget. Defaults to None.
    """
    validate_expenses_data(data)

    output = {"expenses": data}
    if budget_info:
        output["Budget Information"] = format_budget_summary(budget_info)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)


def write_excel(output_path, data, budget_info=None):
    """
    Exports expense data and optional budget summary to an Excel file.

    Args:
        output_path (str): Path to save the Excel file.
        data (list of dict): List of expenses, each represented as a dictionary.
        budget_info (dict, optional): Budget summary including budget amount, current expenses,
                                      and remaining budget. Defaults to None.
    """
    validate_expenses_data(data)

    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    headers = ["ID", "Date", "Amount", "Category", "Description"]
    ws.append(headers)
    for row in data:
        ws.append([row["ID"], row["Date"], row["Amount"], row["Category"], row["Description"]])

    if budget_info:
        summary = format_budget_summary(budget_info)
        ws.append([])
        ws.append(["Budget Information"])
        for key, value in summary.items():
            ws.append([key, value])

    wb.save(output_path)


def generate_unique_filename(output_path):
    """
    Generates a unique filename by appending a number suffix (e.g., 'file(1).json').

    Args:
        output_path (Path): Path object representing the desired file path.

    Returns:
        Path: A unique file path with a numeric suffix if needed.
    """
    counter = 1
    original_stem = re.sub(r"\(\d+\)$", "", output_path.stem)

    while output_path.exists():
        output_path = output_path.parent / f"{original_stem}({counter}){output_path.suffix}"
        counter += 1

    return output_path


def filter_expenses(expenses, year=None, month=None, category=None):
    """
    Filters expenses based on year, month, and/or category for export.

    Args:
        expenses (list of dict): List of expenses to filter.
        year (int, optional): Target year for filtering. Defaults to None.
        month (int, optional): Target month for filtering. Defaults to None.
        category (str, optional): Target category for filtering. Defaults to None.

    Returns:
        list of dict: Filtered list of expenses.
    """
    filtered = []

    current_year = datetime.now().year

    if month and not year:
        try:
            recent_year = max(
                datetime.strptime(row["Date"], "%Y-%m-%d").year
                for row in expenses
                if "Date" in row
            )
            year = min(recent_year, current_year)
        except ValueError:
            year = current_year
            console.print(f"[error]Error:[/error] [white]Could not determine a valid year for the selected month. Defaulting to current year:[/white] [warning]{current_year}[/warning]")

    # Filtering data
    for row in expenses:
        try:
            date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
        except ValueError:
            console.print(f"[error]Error:[/error] [white]Invalid date format found in expense record. Skipping entry:[/white] [warning]{row}[/warning]")
            continue

        matches_date = (
            (not month or (date.month == month and date.year == year)) and
            (not year or date.year == year)
        )
        matches_category = not category or row["Category"].strip().lower() == category.strip().lower()

        if matches_date and matches_category:
            filtered.append(row)

    return filtered
