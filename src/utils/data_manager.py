import csv
from datetime import datetime
from typing import Dict
from pathlib import Path
from collections import defaultdict
from styles.colors import console


DATA_DIR = Path("data")
CSV_FILE_PATH = DATA_DIR / "expenses.csv"
FIELD_NAMES = ["ID", "Date", "Amount", "Category", "Description"]


def initialize_csv():
    """
    Initializes the expenses CSV file and ensures correct headers.
    Creates the data directory and CSV file if they don't exist.
    If the file exists, validates and corrects headers if necessary.
    """
    try:
        CSV_FILE_PATH.parent.mkdir(exist_ok=True)
        if not CSV_FILE_PATH.exists():
            with CSV_FILE_PATH.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
                writer.writeheader()
            return

        # Read first line to check if it's a valid header or data
        file_content = []
        headers_needed = False

        with CSV_FILE_PATH.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            try:
                first_row = next(reader)
                # Check if first row is data (has numeric ID) or malformed header
                try:
                    int(first_row[0])
                    file_content.append(first_row)
                    headers_needed = True
                except (ValueError, IndexError):
                    # Not a numeric ID, check if it's the correct header
                    if first_row != FIELD_NAMES:
                        headers_needed = True
            except StopIteration:
                headers_needed = True

            # Read the rest of the file if it exists
            file_content.extend(row for row in reader if row)

        # Only rewrite the file if we need to add/fix headers
        if headers_needed:
            with CSV_FILE_PATH.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(FIELD_NAMES)
                writer.writerows(file_content)
  
    except Exception as e:
        console.print(f"[error]Error initializing CSV file:[/error] [white]{e}[/white]")
        # Ensure the file exists with correct headers even after error
        try:
            with CSV_FILE_PATH.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
                writer.writeheader()
        except Exception as e:
            console.print(f"[error]Critical error creating CSV file:[/error] [white]{e}[/white]")
            raise


def read_expenses():
    """
    Reads all expense entries from the CSV file.
    
    Returns:
        list: List of dictionaries with expense data.
    """
    expenses = []
    try:
        with CSV_FILE_PATH.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
    except FileNotFoundError:
        pass
    return expenses


def save_expense(expense: Dict[str, str]):
    """
    Saves a single expense entry to the CSV file.

    Args:
        expense (Dict[str, str]): A dictionary representing the expense with keys corresponding to FIELD_NAMES.
    """
    with CSV_FILE_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(expense)


def get_next_expense_id() -> int:
    """
    Retrieves the next available ID for a new expense entry.

    Returns:
        int: The next available ID, incremented from the highest ID found in the file. 
             If the file is empty or doesn't exist, returns 1.
    """
    try:
        expenses = read_expenses()
        ids = [int(row["ID"]) for row in expenses if row["ID"].isdigit()]
        return max(ids, default=0) + 1
    except Exception as e:
        console.print(f"[error]Error retrieving next expense ID:[/error] [white]{e}[/white]")
        return 1


def filter_expenses(reader, target_year, target_month=None, target_category=None):
    """
    Filters expenses by year, month, and category for summary.

    Args:
        reader: CSV reader object with expense data.
        target_year (int): Year to filter by.
        target_month (int, optional): Month (1-12). Defaults to all months.
        target_category (str, optional): Category. Defaults to all categories.

    Returns:
        tuple: (total_expense, filtered_expense, category_summary)
    """
    total_expense = 0.00
    filtered_expense = 0.00
    category_summary = defaultdict(float)

    for row in reader:
        try:
            date = datetime.strptime(row["Date"], "%Y-%m-%d")
            amount = float(row["Amount"])
            category = row["Category"].capitalize()

            total_expense += amount

            matches_year = (target_year is None or date.year == target_year)
            matches_month = (target_month is None or date.month == target_month)

            matches_category = (target_category is None or category == target_category)

            if matches_year and matches_month and matches_category:
                filtered_expense += amount
                category_summary[category] += amount

        except ValueError as e:
            console.print(f"[error]Skipping row due to error:[/error] [white]{e}[/white]")

    return total_expense, filtered_expense, category_summary
