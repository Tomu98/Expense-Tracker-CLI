import click
from commands.add_expense import add_expense
from commands.update_expense import update_expense
from commands.delete_expense import delete_expense
from commands.list_expenses import list_expenses
from commands.summary_expenses import summary
from commands.export_expenses import export
from commands.budget import set_budget, delete_budget, budget


@click.group()
@click.version_option(version="0.16.19", prog_name="Expense Tracker CLI")
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

# Asegurarse que todos los errores de cada comando esten cubiertos por Exception y "unexpected error" o similar,
# y que tengan sus mensajes con sus estilos como en algunos comandos como summary


# dos tipos de formatos para --date: uno con formato YYYY-MM-DD y otro con formato YYYY-MM.
# hay otro de "list_expenses" que es "start_date" y "end_date", pero su formato es YYYY-MM-DD

# Formato YYYY-MM-DD:
# - Comandos: add_expense, update_expense, list_expenses
# - Funciones: validate_date

# Formato YYYY-MM:
# - Comandos: budget.py (set_budget, delete_budget, budget), export_expenses, summary_expenses
# - Funciones:
# --- utils/budget: read_budget(), save_budget(), update_budget(), calculate_monthly_expenses(), check_budget_warning(), get_budget_summary()
# --- utils/data_manager: parse_date(), filter_expenses()
# --- utils/export_helpers: filter_expenses()
# - otro: date/budgets.json
 