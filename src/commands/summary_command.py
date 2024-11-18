import click
import csv
from data_manager import CSV_FILE_PATH
from datetime import datetime


@click.command()
@click.option("--month", type=int, help="Month number to show the summary.")
@click.option("--year", type=int, help="Year to show the summary.")
def summary(month, year):
    total_expense = 0.0
    filtered_expense = 0.0
    current_date = datetime.now()
    target_year = year if year else current_date.year  # Target year (by default, the current year)

    # Determine the month and year when only “--month” is passed
    if month and not year:
        if month > current_date.month:  # Month is greater than the current month, then take last year
            target_year = current_date.year - 1

    # Determine the month and year when passing only “--year”
    if year and not month:
        target_month = None
    elif month:
        target_month = month
    else:
        target_month = current_date.month

    with open(CSV_FILE_PATH, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row["Date"], "%Y-%m-%d")
                amount = float(row["Amount"])

                total_expense += amount

                if (not target_month or date.month == target_month) and date.year == target_year:
                    filtered_expense += amount

            except ValueError as e:
                click.echo(f"Error processing a row: {e}")

    # Show summary
    if month and year:
        month_name = datetime(target_year, month, 1).strftime("%B")
        click.echo(f"Total expenses for {month_name} {target_year}: ${filtered_expense:.2f}")
    elif month:
        month_name = datetime(target_year, month, 1).strftime("%B")
        click.echo(f"Total expenses for {month_name} ({target_year}): ${filtered_expense:.2f}")
    elif year:
        click.echo(f"Total expenses for {target_year}: ${filtered_expense:.2f}")
    else:
        click.echo(f"Total expenses: ${total_expense:.2f}")
