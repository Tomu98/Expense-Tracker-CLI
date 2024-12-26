import re
import csv
import json
from openpyxl import Workbook
from pathlib import Path


def write_csv(output_path, data, budget_info=None):
    """
    Exports expense data and optional budget summary to a CSV file.

    Args:
        output_path (str): Path to save the CSV file.
        data (list of dict): List of expenses, each represented as a dictionary.
        budget_info (dict, optional): Budget summary including budget amount, current expenses,
                                      and remaining budget. Defaults to None.
    """
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Date", "Description", "Category", "Amount"])
        writer.writeheader()

        # Write expenses
        writer.writerows(data)

        # Write budget information (if provided)
        if budget_info:
            writer.writerow({})
            writer.writerow({"ID": "Budget Summary"})
            writer.writerow({
                "Date": "Budget Amount",
                "Description": f"${budget_info['budget_amount']:.2f}",
                "Category": "Expenses",
                "Amount": f"${budget_info['current_expenses']:.2f}"
            })
            writer.writerow({
                "Date": "Remaining Budget",
                "Description": "",
                "Category": "",
                "Amount": f"${budget_info['remaining_budget']:.2f}"
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
    output = {"expenses": data}
    if budget_info:
        output["budget_summary"] = {
            "Budget Amount": budget_info["budget_amount"],
            "Current Expenses": budget_info["current_expenses"],
            "Remaining Budget": budget_info["remaining_budget"]
        }
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
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Write headers and data
    headers = ["ID", "Date", "Description", "Category", "Amount"]
    ws.append(headers)
    for row in data:
        ws.append([row["ID"], row["Date"], row["Description"], row["Category"], row["Amount"]])

    # Write budget information
    if budget_info:
        ws.append([])
        ws.append(["Budget Summary"])
        ws.append(["Budget Amount", f"${budget_info['budget_amount']:.2f}"])
        ws.append(["Current Expenses", f"${budget_info['current_expenses']:.2f}"])
        ws.append(["Remaining Budget", f"${budget_info['remaining_budget']:.2f}"])

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
