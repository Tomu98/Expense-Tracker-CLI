import csv
import click
from rich.console import Console
from rich.table import Table
from datetime import datetime
from data_manager import *



@click.group()
@click.version_option(version="0.5.0", prog_name="Expense Tracker CLI")
def cli():
    pass



# Add expense
@click.command()
@click.option("--category", prompt="Category", help="Category of the expense.")
@click.option("--description", prompt="Description", help="Expense description.")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
def add_expense(category, description, amount):
    initialize_csv()

    new_id = get_expenses_count() + 1
    expense_date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "ID": str(new_id),
        "Date": expense_date,
        "Category": category,
        "Description": description,
        "Amount": f"{amount:.2f}"
    }

    save_expense(expense)
    click.echo(f"Expense added successfully (ID: {new_id})")



# Update expense
@click.command()
@click.argument("expense_id")
@click.option("--new-date", type=str, help="New date (YYYYY-MM-DD).")
@click.option("--new-category", type=str, help="New category.")
@click.option("--new-description", type=str, help="New description.")
@click.option("--new-amount", type=float, help="New amount.")
def update_expense(expense_id, new_date, new_category, new_description, new_amount):
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)

        expense_found = False
        for expense in expenses:
            if expense["ID"] == expense_id:
                expense_found = True
                if new_date:
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        expense["Date"] = new_date
                    except ValueError:
                        click.echo("Invalid date format. Use YYYY-MM-DD.")
                        return

                if new_category:
                    expense["Category"] = new_category
                if new_description:
                    expense["Description"] = new_description
                if new_amount is not None:
                    expense["Amount"] = f"{new_amount:.2f}"
                break

        if not expense_found:
            click.echo(f"The expense with the ID {expense_id} has not been found.")
            return

        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(expenses)

        click.echo(f"Expense with ID {expense_id} successfully updated.")
    
    except FileNotFoundError:
        click.echo("Error: Expense file not found.")
    except Exception as e:
        click.echo(f"Error updating expense: {e}")



# Delete expense
@click.command()
@click.option("--id", prompt="ID", help="ID of the expense to delete")
def delete_expense(id):
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
        
        updated_expenses = [expense for expense in expenses if expense["ID"] != id]

        if len(updated_expenses) == len(expenses):
            click.echo(f"No expense found with ID {id}.")
            return

        with open(CSV_FILE_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            writer.writerows(updated_expenses)

        click.echo(f"Expense with ID {id} has been deleted successfully.")
    
    except FileNotFoundError:
        click.echo("Error: Expense file not found.")
    except Exception as e:
        click.echo(f"Error when eliminating expense: {e}")



# List expenses
@click.command()
def list_expenses():
    try:
        with open(CSV_FILE_PATH, "r", newline="") as file:
            reader = csv.DictReader(file)
            expenses = [row for row in reader]
    except FileNotFoundError:
        click.echo("Error: No expenses file was found.")
        return
    except Exception as e:
        click.echo(f"Error reading file: {e}")
        return

    if not expenses:
        click.echo("No expenses recorded.")
        return

    # Create table
    table = Table(title="Expenses")

    table.add_column("ID", style="dim", width=6)
    table.add_column("Date", justify="center", width=12)
    table.add_column("Description", justify="left", width=20)
    table.add_column("Category", justify="left", width=15)
    table.add_column("Amount", justify="right", width=10)

    for expense in expenses:
        table.add_row(
            expense["ID"], 
            expense["Date"], 
            expense["Description"],
            expense["Category"],
            f"${expense['Amount']}"
        )

    console = Console()
    console.print(table)



# Summary expenses
@click.command()
@click.option("--month", type=int, help="Month number to show the summary.")
def summary(month):
    total_expense = 0.0
    month_expense = 0.0
    month_name = ""

    with open(CSV_FILE_PATH, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row["date"], "%Y-%m-%d")
                amount = float(row["amount"])

                total_expense += amount

                if month and date.month == month:
                    month_expense += amount
                    month_name = date.strftime("%B")
            except ValueError as e:
                click.echo(f"Error processing a row: {e}")

    if month:
        click.echo(f"Total expenses for {month_name}: ${month_expense:.2f}")
    else:
        click.echo(f"Total expenses: ${total_expense:.2f}")



cli.add_command(add_expense, name="add")
cli.add_command(update_expense, name="update")
cli.add_command(delete_expense, name="delete")
cli.add_command(list_expenses, name="list")
cli.add_command(summary, name="summary")



if __name__ == '__main__':
    cli()


# Poner categorias disponibles para que no pongan cualquier cosa
# Lo mismo con la descripcion y el monto
# El id falla, como si al haber cambiado todo no se sumo o algo...
