import click
import csv
from datetime import datetime
from utils.data_manager import CSV_FILE_PATH, filter_expenses
from utils.validators import validate_date, validate_category


@click.command()
@click.option("--month", type=int, help="Month number to show the summary (1-12).")
@click.option("--year", type=int, help="Year to show the summary (e.g., 2024).")
@click.option("--category", help="Filter expenses by a specific category.")
def summary(month, year, category):
    try:
        current_date = datetime.now()
        current_year = current_date.year

        # Validate initial values
        if month is not None and (month <= 0 or month > 12):
            raise click.BadParameter("Month must be between 1 and 12.", param_hint="'--month'")
        if year is not None and (year < 1800 or year > current_year):
            raise click.BadParameter(f"Year must be between 1800 and {current_year}.", param_hint="'--year'")

        # Default values for filters
        target_year = year if year else current_year
        target_month = month
        target_category = category.capitalize() if category else None

        # Validate remaining entries
        if target_month:
            validate_date(f"{target_year}-{target_month:02d}-01")
        if target_category:
            validate_category(target_category)

        # Read and process CSV file
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            total_expense, filtered_expense, category_summary = filter_expenses(
                reader, target_year, target_month, target_category
            )

        # Show results
        if target_month or year or target_category:
            if filtered_expense == 0.00:
                click.echo("No expenses found for the specified filters.")
                return

            filter_desc = []
            if target_month:
                month_name = datetime(target_year, target_month, 1).strftime("%B")
                filter_desc.append(f"{month_name} {target_year}")
            elif year:
                filter_desc.append(f"{target_year}")
            if target_category:
                filter_desc.append(f"category '{target_category}'")

            filter_text = " and ".join(filter_desc)
            click.echo(f"Total expenses for {filter_text}: ${filtered_expense:.2f}")

            # Show breakdown only if no category is specified
            if not target_category:
                click.echo("\nBreakdown by category:")
                for cat, amount in category_summary.items():
                    click.echo(f"- {cat}: ${amount:.2f}")

        else:
            click.echo(f"Total expenses: ${total_expense:.2f}")

    except FileNotFoundError:
        click.echo("Error: No expenses file was found.")



# Añadir información del presupuesto:
# - Que salga la cantidad del presupuesto y lo que queda del mes actual o seleccionado con --month --year
# - Si se coloca tanto --month, --year y --category, que salga la información del presupuesto de la fecha seleccionado pero no importa la categoria
