import click
from commands.add_expense import add_expense
from commands.update_expense import update_expense
from commands.delete_expense import delete_expense
from commands.list_expenses import list_expenses
from commands.summary_expenses import summary
from commands.export_expenses import export
from commands.budget import set_budget, delete_budget, budget


@click.group()
@click.version_option(version="0.16.14", prog_name="Expense Tracker CLI")
def cli():
    pass


# Registering commands
cli.add_command(add_expense, name="add")
cli.add_command(update_expense, name="update")
cli.add_command(delete_expense, name="delete")
cli.add_command(list_expenses, name="list")
cli.add_command(summary, name="summary")
cli.add_command(export, name="export")
cli.add_command(set_budget, name="set-budget")
cli.add_command(delete_budget, name="delete-budget")
cli.add_command(budget, name="budget")


if __name__ == '__main__':
    cli()

# Agregar tests
# Ver si hacer que los comandos que reciben "--month" y "--year" sean directamente juntos como "--date" y que se pueda pasar solo 2024 o 2024-01
# Los que contienen esas opciones de fecha son:
# - src/commands/export_expenses.py: export
# - src/commands/summary_expenses.py: summary
# Con esto, ver si las funciones auxiliares como filter_expenses y otras que usan estas opciones de fecha se pueden simplificar
# Comprobar que --category y otras opciones de filtro funcionen correctamente
# Con todo esto, ver si se pueden simplificar las funciones auxiliares de export_helpers.py y data_manager.py
# y editar los tests para que pasen con los cambios
