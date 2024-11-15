import csv
import click
from rich.console import Console
from rich.table import Table
from datetime import datetime
from data_manager import *



# Commands
@click.group()
@click.version_option(version="0.6.3", prog_name="Expense Tracker CLI")
def cli():
    pass


VALID_CATEGORIES = ["Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"]


# Add expense
@click.command()
@click.option("--category", type=str, prompt="Category", help="Category of the expense.")
@click.option("--description", default=None, help="Expense description.")
@click.option("--amount", type=float, prompt="Amount", help="Amount of the expense.")
def add_expense(category, description, amount):
    initialize_csv()

    # Validate category
    category = category.capitalize()
    if category not in VALID_CATEGORIES:
        click.echo("Invalid category. Choose from: " + ", ".join(VALID_CATEGORIES))
        return

    # Validate amount
    try:
        if amount <= 0:
            raise ValueError("Amount must be a positive number and higher than 0.")
        if amount > 100000:
            raise ValueError(f"Amount exceeds the maximum limit of $100000.")
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    # Validate description
    if description:
        if len(description) < 3:
            click.echo(f"Error: Description must be at least 3 characters.")
            return
        elif len(description) > 100:
            click.echo(f"Error: Description must be no more than 100 characters.")
            return
    else:
        description = "..."

    # Generate new expense ID and date
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

    click.echo(f"Expense added successfully (ID: {new_id}, Category: '{category}', Amount: ${amount:.2f})")



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
@click.option("--id", help="ID of the expense to delete.", required=False)
@click.option("--all", is_flag=True, help="Delete all expenses.")
def delete_expense(id, all):
    if all:
        while True:
            confirmation = click.prompt(
                "Are you sure you want to delete all expenses? (y/n)", 
                type=str, 
                default="n"
            ).lower()

            if confirmation in ["y", "yes"]:
                try:
                    with open(CSV_FILE_PATH, "w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
                        writer.writeheader()
                    click.echo("All expenses have been deleted successfully.")
                except Exception as e:
                    click.echo(f"Error when deleting all expenses: {e}")
                return
            elif confirmation in ["n", "no"]:
                click.echo("Deletion cancelled.")
                return
            else:
                click.echo("Please enter a valid response: 'y' or 'n' (or 'yes'/'no').")

    if not id:
        click.echo("Error: You must provide an ID with --id or use --all to delete all expenses.")
        return

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
@click.option("--year", type=int, help="Year to show the summary.")
def summary(month, year):
    total_expense = 0.0
    filtered_expense = 0.0
    current_date = datetime.now()
    target_year = year if year else current_date.year  # Target year (by default, the current year)

    # Determine the month and year when only “--month” is passed
    if month and not year:
        if month > current_date.month:  # Month is greater than the current month, then take last year
            target_year = current_date.year - 1

    # Determine the month and year when passing only “--year”
    if year and not month:
        target_month = None
    elif month:
        target_month = month
    else:
        target_month = current_date.month

    with open(CSV_FILE_PATH, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row["Date"], "%Y-%m-%d")
                amount = float(row["Amount"])

                total_expense += amount

                if (not target_month or date.month == target_month) and date.year == target_year:
                    filtered_expense += amount

            except ValueError as e:
                click.echo(f"Error processing a row: {e}")

    # Show summary
    if month and year:
        month_name = datetime(target_year, month, 1).strftime("%B")
        click.echo(f"Total expenses for {month_name} {target_year}: ${filtered_expense:.2f}")
    elif month:
        month_name = datetime(target_year, month, 1).strftime("%B")
        click.echo(f"Total expenses for {month_name} ({target_year}): ${filtered_expense:.2f}")
    elif year:
        click.echo(f"Total expenses for {target_year}: ${filtered_expense:.2f}")
    else:
        click.echo(f"Total expenses: ${total_expense:.2f}")



cli.add_command(add_expense, name="add")
cli.add_command(update_expense, name="update")
cli.add_command(delete_expense, name="delete")
cli.add_command(list_expenses, name="list")
cli.add_command(summary, name="summary")



if __name__ == '__main__':
    cli()


# Falta para filtrar gastos por categoria
# Falta para permitir a los usuarios establecer un presupuesto para cada mes
# y mostrar una advertencia cuando el usuario supere el presupuesto
# Falta permitir a los usuarios exportar gastos a un archivo CSV

# Ver si puedo modularizar más el código
# Agregar tests
# Agregar estilos con rich


# Update expense:
# - Comprobar posibles fallos
# - Hacer que lo de actulizar lo que sea del gasto sea opcional y preguntando si está seguro de actualizar
# - Asegurar que tengan las mismas validaciones de los datos en amount, description, category y date
# 

# Delete expense:
# - Comprobar que todo esté bien
# - posiblemente agregar para borrar por fecha

# List
# - Comprobar que todo esté bien
# - Le podria agregar que filtre por categoria, fecha o monto especifico

# Summary
# - Comprobar que todo esté bien
