import click
import csv
from datetime import datetime
from collections import defaultdict
from data_manager import CSV_FILE_PATH
from utils.validators import validate_date, validate_category


@click.command()
@click.option("--month", type=int, help="Month number to show the summary (1-12).")
@click.option("--year", type=int, help="Year to show the summary (e.g., 2024).")
@click.option("--category", help="Filter expenses by a specific category.")
def summary(month, year, category):
    try:
        current_date = datetime.now()
        total_expense = 0.00
        filtered_expense = 0.00
        category_summary = defaultdict(float)

        # Validate inputs
        if category:
            category = validate_category(category)

        target_year = year if year else current_date.year
        if year:
            validate_date(f"{target_year}-01-01")

        if month:
            if not (1 <= month <= 12):
                raise click.BadParameter("Month must be between 1 and 12.", param_hint="'--month'")
            validate_date(f"{target_year}-{month:02d}-01")

        # Read and process the CSV file
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    date = datetime.strptime(row["Date"], "%Y-%m-%d")
                    amount = float(row["Amount"])
                    total_expense += amount

                    matches_date = (not month or date.month == month) and date.year == target_year
                    matches_category = not category or row["Category"].capitalize() == category

                    if matches_date and matches_category:
                        filtered_expense += amount
                        category_summary[row["Category"].capitalize()] += amount

                except ValueError as e:
                    click.echo(f"Skipping row due to error: {e}")

        # Display the summary
        if month or year or category:
            if filtered_expense == 0.00:
                click.echo("No expenses found for the specified filters.")
                return

            if month:
                month_name = datetime(target_year, month, 1).strftime("%B")
                click.echo(f"Total expenses for {month_name} {target_year}: ${filtered_expense:.2f}")
            elif year:
                click.echo(f"Total expenses for {target_year}: ${filtered_expense:.2f}")
            elif category:
                click.echo(f"Total expenses for category '{category}': ${filtered_expense:.2f}")

            # Display breakdown only if not filtered by category
            if not category:
                click.echo("\nBreakdown by category:")
                for cat, amount in category_summary.items():
                    click.echo(f"  {cat}: ${amount:.2f}")

        else:
            click.echo(f"Total expenses: ${total_expense:.2f}")

    except FileNotFoundError:
        click.echo("Error: No expenses file was found.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")
