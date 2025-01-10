import click
from datetime import datetime
from rich.table import Table
from styles.colors import console
from utils.budget_helpers import initialize_budget_file, read_budget, save_budget, update_budget, calculate_monthly_expenses
from utils.validators import validate_parse_date, validate_budget_amount


# Set budget
@click.command()
@click.option("--amount", type=float, prompt="Budget amount", help="Amount for the budget.")
@click.option("--date", type=str, prompt="Date (YYYY-MM)", help="Date for the budget in 'YYYY-MM' format.")
def set_budget(amount, date):
    """
    Sets a monthly budget for a specific year and month in 'YYYY-MM' format.
    Validates the amount and date, and updates the budget file with the new value.
    """
    initialize_budget_file()

    validate_budget_amount(amount)

    year, month, _ = validate_parse_date(date, allow_future=True)

    # Validate the year
    current_year = datetime.now().year
    if not (2000 <= year <= current_year + 10):
        raise click.BadParameter(
            f"The year must be between 2000 and {current_year + 10}.",
            param_hint="'--date'"
        )

    update_budget(month, year, amount)


# Delete budget
@click.command()
@click.option("--date", type=str, prompt="Date (YYYY-MM)", help="Date for the budget to delete in 'YYYY-MM' format.")
def delete_budget(date):
    """
    Deletes the budget for a specific year and month in 'YYYY-MM' format.
    Validates the date and removes the corresponding budget entry if it exists.
    """
    initialize_budget_file()

    year, month, _ = validate_parse_date(date)

    if month is None:
        raise click.BadParameter("The date must include both year and month (e.g., '2025-01').", param_hint="'--date'")

    budgets = read_budget()

    key = f"{year}-{month:02d}"

    if key in budgets:
        del budgets[key]
        save_budget(budgets)
        console.print(f"\n[success]Budget for [date]{year}-{month:02d}[/date] has been deleted.[/success]\n")
    else:
        console.print(f"\n[error]No budget found for [date]{year}-{month:02d}[/date].[/error]\n")


# View budgets
@click.command()
@click.option("--current", is_flag=True, help="Show the current month's budget.")
@click.option("--all", is_flag=True, help="Show all budgets.")
@click.option("--date", type=str, help="Show the budget for a specific month or year in 'YYYY' or 'YYYY-MM' format.")
def view_budget(current, all, date):
    """
    Displays budget information. Allows viewing the current month's budget, all budgets,
    or a specific budget by month and year in 'YYYY' or 'YYYY-MM' format.
    Shows budget total, current expenses, and the remaining difference.
    """
    budgets = read_budget()

    if not current and not all and not date:
        return console.print("\n[warning]Please specify an option:[/warning] [white][white_dim]--current[/white_dim], [white_dim]--all[/white_dim], or [white_dim]--date 'YYYY-MM'/'YYYY'[/white_dim].[/white]\n")

    if not budgets:
        console.print("\n[error]No budgets found.[/error]\n")
        return

    # Validate and parse date
    if date:
        year, month, _ = validate_parse_date(date)

        if month is None:
            # Show budgets for the entire year
            table = Table(title=f"\nBudgets for {year}", row_styles=["none", "dim"])
            table.add_column("Date", justify="center", style="date", min_width=9)
            table.add_column("Budget Total", justify="center", style="budget", min_width=15)
            table.add_column("Current Expenses", justify="center", style="amount", min_width=15)
            table.add_column("Difference", justify="center", min_width=15)

            budgets_found = False

            for key, budget_amount in budgets.items():
                budget_year, budget_month = map(int, key.split("-"))

                if budget_year == year:
                    budgets_found = True
                    current_expenses = calculate_monthly_expenses(budget_year, budget_month)
                    difference = budget_amount - current_expenses
                    difference_color = "budget2" if difference >= 0 else "amount2"

                    table.add_row(
                        key,
                        f"${budget_amount:.2f}",
                        f"${current_expenses:.2f}",
                        f"[{difference_color}]${difference:.2f}[/{difference_color}]",
                    )

            if budgets_found:
                console.print(table)
            else:
                console.print(f"\n[warning]No budgets found for the year [date]{year}[/date].[/warning]\n")

            return

        # Show budget for a specific month
        key = f"{year}-{month:02d}"
        if key not in budgets:
            console.print(f"\n[warning]No budget found for [date]{key}[/date].[/warning]\n")
            return

        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(year, month)
        difference = budget_amount - current_expenses
        difference_color = "budget2" if difference >= 0 else "amount2"

        table = Table(title=f"\nBudget for {key}")
        table.add_column("Date", justify="center", style="date", min_width=9)
        table.add_column("Budget Total", justify="center", style="budget", min_width=15)
        table.add_column("Current Expenses", justify="center", style="amount", min_width=15)
        table.add_column("Difference", justify="center", min_width=15)

        table.add_row(
            key,
            f"${budget_amount:.2f}",
            f"${current_expenses:.2f}",
            f"[{difference_color}]${difference:.2f}[/{difference_color}]",
        )

        console.print(table)
        return

    # Show current budget
    if current:
        current_year = datetime.now().year
        current_month = datetime.now().month
        key = f"{current_year}-{current_month:02d}"

        if key not in budgets:
            console.print(f"\n[warning]No budget found for [date]{current_year}-{current_month:02d}[/date].[/warning]\n")
            return

        budget_amount = budgets[key]
        current_expenses = calculate_monthly_expenses(current_year, current_month)
        difference = budget_amount - current_expenses
        difference_color = "budget2" if difference >= 0 else "amount2"

        table = Table(title=f"\nBudget for {current_year}-{current_month:02d}")
        table.add_column("Date", justify="center", style="date", min_width=9)
        table.add_column("Budget Total", justify="center", style="budget", min_width=15)
        table.add_column("Current Expenses", justify="center", style="amount", min_width=15)
        table.add_column("Difference", justify="center", min_width=15)

        table.add_row(
            f"{current_year}-{current_month:02d}",
            f"${budget_amount:.2f}",
            f"${current_expenses:.2f}",
            f"[{difference_color}]${difference:.2f}[/{difference_color}]",
        )

        console.print(table)

    # Show all budgets
    if all:
        table = Table(title="\nAll Budgets", row_styles=["none", "dim"])
        table.add_column("Date", justify="center", style="date", min_width=9)
        table.add_column("Budget Total", justify="center", style="budget", min_width=15)
        table.add_column("Current Expenses", justify="center", style="amount", min_width=15)
        table.add_column("Difference", justify="center", min_width=15)

        for key, budget_amount in budgets.items():
            year, month = map(int, key.split("-"))
            current_expenses = calculate_monthly_expenses(year, month)
            difference = budget_amount - current_expenses
            difference_color = "budget2" if difference >= 0 else "amount2"

            table.add_row(
                key,
                f"${budget_amount:.2f}",
                f"${current_expenses:.2f}",
                f"[{difference_color}]${difference:.2f}[/{difference_color}]",
            )

        console.print(table)
