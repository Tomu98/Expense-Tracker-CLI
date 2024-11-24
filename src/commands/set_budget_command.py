import click
from data_manager import initialize_budget_file, update_budget


@click.command()
@click.option("--month", type=int, prompt="Month (1-12)", help="Month for the budget (1-12).")
@click.option("--year", type=int, prompt="Year", help="Year for the budget.")
@click.option("--amount", type=float, prompt="Budget amount", help="Amount for the budget.")
def set_budget(month, year, amount):
    initialize_budget_file()

    if not (1 <= month <= 12):
        raise click.BadParameter("The month must be between 1 and 12.", param_hint="'--month'")

    if amount <= 0:
        raise click.BadParameter("The budget amount must be greater than 0.", param_hint="'--amount'")

    update_budget(month, year, amount)

# Comprobar que todo esté bien
# Asegurarse que todos los demás comandos funcionen bien con esta función
# y que si hace falta, agregar referencias del presupuesto y su monto, como en list, summary, update
# Comprobar que esten bien y sean justas y necesarias las demás funciones relacionadas a este comando
# Comprobar que el proyecto siga bien organizado
# Comprobar si "data_manager.py" no lo debería mover a otro archivo para mejor organización
