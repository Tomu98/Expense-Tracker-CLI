import click
from commands.add_expense import add_expense
from commands.budget import set_budget, delete_budget, view_budget
from commands.delete_expense import delete_expense
from commands.export_expenses import export
from commands.list_expenses import list_expenses
from commands.summary_expenses import summary
from commands.update_expense import update_expense


@click.group()
@click.version_option(version="0.16.27", prog_name="Expense Tracker CLI")
def cli():
    pass


# Registering commands
cli.add_command(add_expense, name="add")
cli.add_command(set_budget, name="set-budget")
cli.add_command(delete_budget, name="delete-budget")
cli.add_command(view_budget, name="view-budget")
cli.add_command(delete_expense, name="delete")
cli.add_command(export, name="export")
cli.add_command(list_expenses, name="list")
cli.add_command(summary, name="summary")
cli.add_command(update_expense, name="update")


if __name__ == '__main__':
    cli()
