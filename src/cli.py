import click
from commands.add_command import add_expense
from commands.update_command import update_expense
from commands.delete_command import delete_expense
from commands.list_command import list_expenses
from commands.summary_command import summary
from commands.export_command import export
from commands.set_budget_command import set_budget


@click.group()
@click.version_option(version="0.12.0", prog_name="Expense Tracker CLI")
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


if __name__ == '__main__':
    cli()


# Agregar estilos con rich
# Agregar tests
# Agregar Docstrings
