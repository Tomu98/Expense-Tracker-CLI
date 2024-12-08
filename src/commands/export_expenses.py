import click
import csv
from datetime import datetime
from pathlib import Path
from utils.budget import get_budget_summary
from utils.data_manager import CSV_FILE_PATH
from utils.export_helpers import write_csv, write_json, write_excel
from utils.validators import validate_date, validate_category


@click.command()
@click.option("--output", type=str, required=True, help="Path to save the exported file (CSV/JSON/Excel).")
@click.option("--month", type=int, help="Filter expenses by month (1-12).")
@click.option("--year", type=int, help="Filter expenses by year (e.g., 2024).")
@click.option("--category", type=str, help="Filter expenses by category.")
@click.option("--include-budget", is_flag=True, help="Include budget information in the export.")
def export(output, month, year, category, include_budget):
    """
    Export expenses to a specified file (CSV, JSON, or Excel), with optional filters by date or category.
    Supports including budget information for the selected month.
    """
    try:
        current_date = datetime.now()
        target_year = year if year else current_date.year
        output_path = Path(output)
        output_format = output_path.suffix.lower()

        # Validate output format
        if output_format not in [".csv", ".json", ".xlsx"]:
            raise click.BadParameter("Supported formats are CSV, JSON, and Excel (.xlsx).", param_hint="'--output'")

        # Validate inputs
        if category:
            category = validate_category(category)
        if year:
            validate_date(f"{target_year}-01-01")
        if month:
            if not (1 <= month <= 12):
                raise click.BadParameter(f"Invalid month '{month}'. Please specify a value between 1 and 12.", param_hint="'--month'")
            validate_date(f"{target_year}-{month:02d}-01")

        # Ensure the directory for the output file exists
        if not output_path.parent.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Read the source CSV file
        with open(CSV_FILE_PATH, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            filtered_expenses = []

            for row in reader:
                try:
                    date = datetime.strptime(row["Date"], "%Y-%m-%d")
                    matches_date = (not month or date.month == month) and date.year == target_year
                    matches_category = not category or row["Category"].capitalize() == category

                    if matches_date and matches_category:
                        filtered_expenses.append(row)

                except ValueError as e:
                    click.echo(f"Skipping row due to error: {e}")

        # Check if there are any expenses
        if not filtered_expenses:
            click.echo("No expenses match the specified filters.")
            return

        # Calculate budget information if necessary
        budget_info = None
        if include_budget and month:
            budget_info = get_budget_summary(year=target_year, month=month)

        # Write the filtered expenses to the output file
        if output_format == ".csv":
            write_csv(output_path, filtered_expenses, budget_info=budget_info)
        elif output_format == ".json":
            write_json(output_path, filtered_expenses, budget_info=budget_info)
        elif output_format == ".xlsx":
            write_excel(output_path, filtered_expenses, budget_info=budget_info)

        click.echo(f"Expenses successfully exported to '{output}'.")

    except FileNotFoundError:
        click.echo("Error: No expenses file was found.")
    except PermissionError:
        click.echo(f"Error: Permission denied to write to '{output}'.")
