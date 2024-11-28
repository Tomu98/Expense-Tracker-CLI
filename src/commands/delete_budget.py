import click
from datetime import datetime
from data_manager import initialize_budget_file, read_budget, save_budget


@click.command()
@click.option("--month", type=int, prompt="Month (1-12)", help="Month for the budget to delete (1-12).")
@click.option("--year", type=int, prompt="Year", help="Year for the budget to delete.")
def delete_budget(month, year):
    initialize_budget_file()

    if not (1 <= month <= 12):
        raise click.BadParameter("The month must be between 1 and 12.", param_hint="'--month'")

    current_year = datetime.now().year
    if not (2000 <= year <= current_year + 5):
        raise click.BadParameter(
            f"The year must be between 2000 and {current_year + 5}.",
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
