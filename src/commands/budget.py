import click
from rich.table import Table
from rich.console import Console
from datetime import datetime
from utils.budget import initialize_budget_file, read_budget, save_budget, update_budget, calculate_monthly_expenses
from utils.validators import validate_budget_amount


# Set budget
@click.command()
@click.option("--amount", type=float, prompt="Budget amount", help="Amount for the budget.")
@click.option("--month", type=int, prompt="Month (1-12)", help="Month for the budget (1-12).")
@click.option("--year", type=int, prompt="Year", help="Year for the budget.")
def set_budget(amount, month, year):
    initialize_budget_file()

    validate_budget_amount(amount)

    if not (1 <= month <= 12):
        raise click.BadParameter("The month must be between 1 and 12.", param_hint="'--month'")

    current_year = datetime.now().year
    if not (2000 <= year <= current_year + 10):
        raise click.BadParameter(
            f"The year must be between 2000 and {current_year + 10}.",
            param_hint="'--year'"
        )

    update_budget(month, year, amount)


# Delete budget
@click.command()
@click.option("--month", type=int, prompt="Month (1-12)", help="Month for the budget to delete (1-12).")
@click.option("--year", type=int, prompt="Year", help="Year for the budget to delete.")
def delete_budget(month, year):
    initialize_budget_file()

    if not (1 <= month <= 12):
        raise click.BadParameter("The month must be between 1 and 12.", param_hint="'--month'")

    current_year = datetime.now().year
    if not (2000 <= year <= current_year + 10):
        raise click.BadParameter(
            f"The year must be between 2000 and {current_year + 10}.",
            param_hint="'--year'"
        )

    budgets = read_budget()

    key = f"{year}-{month:02d}"

    if key in budgets:
        del budgets[key]
        save_budget(budgets)
        click.echo(f"Budget for {year}-{month:02d} has been deleted.")
    else:
        click.echo(f"No budget found for {year}-{month:02d}.")


# View budgets
@click.command()
@click.option("--current", is_flag=True, help="Show the current month's budget.")
@click.option("--all", is_flag=True, help="Show all budgets.")
@click.option("--specific", type=str, help="Show the budget for a specific month in 'YYYY-MM' format.")
def budget(current, all, specific):
    console = Console()
    budgets = read_budget()

    if not budgets:
        console.print("[bold red]No budgets found.[/bold red]")
        return

    if not current and not all and not specific:
        console.print("[bold yellow]Please specify an option: --current, --all, or --specific 'YYYY-MM'.[/bold yellow]")
        return

    if specific:
        # Validate format "YYYY-MM"
        try:
            specific_date = datetime.strptime(specific, "%Y-%m")
            year, month = specific_date.year, specific_date.month
        except ValueError:
            console.print("[bold red]Invalid date format. Use 'YYYY-MM'.[/bold red]")
            return

        # Search budget for the specific date
        key = f"{year}-{month:02d}"
        if key not in budgets:
            console.print(f"[bold red]No budget found for {key}.[/bold red]")
            return

        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(year, month)
        difference = budget_amount - current_expenses

        table = Table(title=f"Budget for {key}")
        table.add_column("Month", justify="center")
        table.add_column("Budget Total", justify="center")
        table.add_column("Current Expenses", justify="center")
        table.add_column("Difference", justify="center")

        difference_color = "green" if difference >= 0 else "red"
        table.add_row(
            key,
            f"${budget_amount:.2f}",
            f"${current_expenses:.2f}",
            f"[{difference_color}]${difference:.2f}[/{difference_color}]",
        )

        console.print(table)
        return

    if current:
        # Show current budget
        current_year = datetime.now().year
        current_month = datetime.now().month
        key = f"{current_year}-{current_month:02d}"

        if key not in budgets:
            console.print(f"[bold red]No budget found for {current_year}-{current_month:02d}.[/bold red]")
            return

        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(current_year, current_month)
        difference = budget_amount - current_expenses

        table = Table(title=f"Budget for {current_year}-{current_month:02d}")
        table.add_column("Month", justify="center")
        table.add_column("Budget Total", justify="center")
        table.add_column("Current Expenses", justify="center")
        table.add_column("Difference", justify="center")

        difference_color = "green" if difference >= 0 else "red"
        table.add_row(
            f"{current_year}-{current_month:02d}",
            f"${budget_amount:.2f}",
            f"${current_expenses:.2f}",
            f"[{difference_color}]${difference:.2f}[/{difference_color}]",
        )

        console.print(table)

    if all:
        # Show all budgets
        table = Table(title="All Budgets")
        table.add_column("Month", justify="center")
        table.add_column("Budget Total", justify="center")
        table.add_column("Current Expenses", justify="center")
        table.add_column("Difference", justify="center")

        for key, budget_amount in budgets.items():
            year, month = map(int, key.split("-"))
            current_expenses = calculate_monthly_expenses(year, month)
            difference = budget_amount - current_expenses
            difference_color = "green" if difference >= 0 else "red"

            table.add_row(
                key,
                f"${budget_amount:.2f}",
                f"${current_expenses:.2f}",
                f"[{difference_color}]${difference:.2f}[/{difference_color}]",
            )

        console.print(table)


# Asegurarse que todos los demás comandos funcionen bien con esta función
# y que si hace falta, agregar referencias del presupuesto y su monto, como en list, summary, update
