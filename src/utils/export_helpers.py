import csv
import json
from openpyxl import Workbook


def write_csv(output_path, data):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Date", "Description", "Category", "Amount"])
        writer.writeheader()
        writer.writerows(data)


def write_json(output_path, data):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def write_excel(output_path, data):
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Write header
    headers = ["ID", "Date", "Description", "Category", "Amount"]
    ws.append(headers)

    # Write data rows
    for row in data:
        ws.append([row["ID"], row["Date"], row["Description"], row["Category"], row["Amount"]])

    wb.save(output_path)

# Lo que ví:
# - Incluir información del presupuesto en los archivos exportados
