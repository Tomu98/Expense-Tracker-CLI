import click
from services import add_expense, delete_expense



@click.group()
@click.version_option(version="0.3.0", prog_name="Expense Tracker CLI")
def cli():
    pass


@click.command()
@click.option("--category", prompt="Category", help="Category of the expense")
@click.option("--description", prompt="Description", help="Expense description")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense")
def add_expense_cli(category, description, amount):
    new_id = add_expense(category, description, amount)
    click.echo(f"Expense added successfully (ID: {new_id})")


@click.command()
@click.option("--id", prompt="ID", help="ID of the expense to delete")
def delete_expense_cli(id):
    if delete_expense(id):
        click.echo(f"Expense with ID {id} has been deleted successfully.")
    else:
        click.echo(f"No expense found with ID {id}.")



cli.add_command(add_expense_cli, name="add")
cli.add_command(delete_expense_cli, name="delete")


if __name__ == '__main__':
    cli()
