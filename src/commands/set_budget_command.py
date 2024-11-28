import click
from datetime import datetime
from data_manager import initialize_budget_file, update_budget
from utils.validators import validate_budget_amount


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

# Comprobar que todo esté bien
# Asegurarse que todos los demás comandos funcionen bien con esta función
# y que si hace falta, agregar referencias del presupuesto y su monto, como en list, summary, update
# Comprobar que esten bien y sean justas y necesarias las demás funciones relacionadas a este comando
# Comprobar que el proyecto siga bien organizado
# Comprobar si "data_manager.py" no lo debería mover a otro archivo para mejor organización
