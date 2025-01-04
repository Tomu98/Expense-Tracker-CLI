import click
from pathlib import Path
from styles.colors import console
from src.utils.budget_helpers import get_budget_summary
from utils.data_manager import read_expenses
from utils.export_helpers import write_csv, write_json, write_excel, generate_unique_filename, filter_expenses
from utils.validators import validate_parse_date, validate_category


@click.command()
@click.option("--output", type=str, prompt="Name file", required=True, help="Name of the exported file (e.g., expenses.csv, expenses.json).")
@click.option("--date", type=str, help="Filter expenses by year (e.g., 2025) or year and month (e.g., 2025-01).")
@click.option("--category", type=str, help="Filter expenses by category.")
@click.option("--include-budget", is_flag=True, help="Include budget information in the export. Requires --date with year and month.")
def export(output, date, category, include_budget):
    """
    Export expenses to a file (CSV, JSON, or Excel) in the 'exports' directory, with optional filters by date or category.
    Supports including budget information for the selected date.
    """
    try:
        # Ensure the exports directory exists
        exports_dir = Path("exports")
        exports_dir.mkdir(parents=True, exist_ok=True)

        # Create full output path in the exports directory
        output_path = exports_dir / output
        output_format = output_path.suffix.lower()

        # Validate output format
        while output_format not in [".csv", ".json", ".xlsx"]:
            console.print("\n[error]Invalid output format:[/error] [warning]Supported formats are '.csv', '.json' and '.xlsx' (Excel).[/warning]")
            output = console.input("[white]Enter the name of the exported file [white_dim](e.g. 'expenses.json')[/white_dim]:[/white]")
            output_path = exports_dir / output
            output_format = output_path.suffix.lower()

        # Handle duplicate file names by appending a unique suffix
        output_path = generate_unique_filename(output_path)

        # Validate inputs
        year = None
        month = None

        if date:
            year, month, _ = validate_parse_date(date)

        if category:
            category = validate_category(category)

        # Ensure --date includes both year and month if --include-budget is used
        if include_budget and (not year or not month):
            raise click.UsageError("--include-budget requires --date with both year and month specified.")

        # Read the source CSV file
        expenses = read_expenses()

        # Filter expenses
        filtered_expenses = filter_expenses(
            expenses=expenses,
            year=year,
            month=month,
            category=category
        )

        if not filtered_expenses:
            console.print("\n[warning]No expenses match the specified filters.[/warning]\n")
            return

        # Budget information
        budget_info = None
        if include_budget:
            budget_info = get_budget_summary(year=year, month=month)
            if not budget_info["budget_set"]:
                console.print(f"\n[warning]No budget found for {year}-{month:02d}.[/warning] [white]Exporting expenses without budget information.[/white]")
                budget_info = None

        # Write the filtered expenses to the output file
        if output_format == ".csv":
            write_csv(output_path, filtered_expenses, budget_info=budget_info)
        elif output_format == ".json":
            write_json(output_path, filtered_expenses, budget_info=budget_info)
        elif output_format == ".xlsx":
            write_excel(output_path, filtered_expenses, budget_info=budget_info)

        console.print(f"\n[success]Expenses successfully exported to [white_dim]'{output_path}'[/white_dim].[/success]\n")

    except FileNotFoundError:
        console.print("\n[error]Error:[/error] No expenses file was found.\n")
    except PermissionError:
        console.print(f"\n[error]Error:[/error] Permission denied to write to [white_dim]'{output_path}'[/white_dim].\n")
    except Exception as e:
        console.print(f"\n[error]Unexpected error:[/error] [white]{e}[/white]\n")
