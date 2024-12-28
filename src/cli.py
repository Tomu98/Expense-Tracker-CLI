import click
from commands.add_expense import add_expense
from commands.update_expense import update_expense
from commands.delete_expense import delete_expense
from commands.list_expenses import list_expenses
from commands.summary_expenses import summary
from commands.export_expenses import export
from commands.budget import set_budget, delete_budget, budget


@click.group()
@click.version_option(version="0.16.6", prog_name="Expense Tracker CLI")
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

# Asegurarse que los colores en los mensajes blancos tengan el [white] y [/white] correspondiente, lo mismo con los demás colores
# Reacomodar el orden de los datos al mostrarse en la terminal, como por ejemplo: ID, Category, Amount, Date en un orden más lógico
# Dar color a los mensajes de badparameter, usageerror, etc.
# Que al agregar --description ayudar a que el usuario tenga que poner comillas simples o dobles para que no haya problemas con el comando al poner espacios
# Color y tamaños a la tabla de budget
