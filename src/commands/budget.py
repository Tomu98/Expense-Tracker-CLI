import click
from datetime import datetime
from utils.budget import initialize_budget_file, update_budget, read_budget, save_budget
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
    if not (2000 <= year <= current_year + 5):
        raise click.BadParameter(
            f"The year must be between 2000 and {current_year + 5}.",
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


# Comprobar que todo esté bien
# Asegurarse que todos los demás comandos funcionen bien con esta función
# y que si hace falta, agregar referencias del presupuesto y su monto, como en list, summary, update
# Comprobar que esten bien y sean justas y necesarias las demás funciones relacionadas a este comando
