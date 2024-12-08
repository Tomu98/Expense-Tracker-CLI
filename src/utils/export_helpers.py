import csv
import json
from openpyxl import Workbook


def write_csv(output_path, data, budget_info=None):
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
