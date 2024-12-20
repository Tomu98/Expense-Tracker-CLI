import click
from datetime import datetime


def validate_date(date: str):
    """
    Validates the date format (YYYY-MM-DD) and ensures it's not in the future.
    """
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.now().date()

        if parsed_date.date() > today:
            raise click.BadParameter(
                "Please enter a valid past or current date.",
                param_hint="'--date'"
            )

        return date

    except ValueError:
        raise click.BadParameter(
            f"Invalid date format or values in '{date}'. Use YYYY-MM-DD and ensure the values are valid.",
            param_hint="'--date'"
        )


def validate_category(category: str):
    """
    Ensures the category is in the list of valid options.
    """
    category = category.capitalize()

    VALID_CATEGORIES = ["Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"]

    if category not in VALID_CATEGORIES:
        valid_options = ", ".join(VALID_CATEGORIES)
        raise click.BadParameter(
            f"'{category}' is not a valid category. The valid ones are: {valid_options}.",
            param_hint="'--category'"
        )

    return category


def validate_description(description: str):
    """
    Validates the description length (3 to 60 characters). Defaults to "..." if empty.
    """
    if not description:
        return "..."

    if len(description) < 3:
        raise click.BadParameter("Description must be at least 3 characters.", param_hint="'--description'")

    if len(description) > 60:
        raise click.BadParameter("Description must be no more than 60 characters.", param_hint="'--description'")

    return description


def validate_amount(amount: float):
    """
    Ensures the amount is positive, below $100,000, and significant after rounding.
    """
    max_value = 100000
    if amount <= 0 or amount > max_value:
        raise click.BadParameter(f"Amount must be positive and not exceed ${max_value}.", param_hint="'--amount'")

    rounded_amount = round(amount, 2)
    if rounded_amount <= 0:
        raise click.BadParameter("Amount must be significant (greater than $0.00 after rounding).", param_hint="'--amount'")

    return rounded_amount


def validate_budget_amount(amount: float):
    """
    Validates the budget amount to be greater than $0 and less than or equal to $100,000.
    """
    max_budget = 100000

    if amount <= 0 or amount > max_budget:
        raise click.BadParameter(f"Budget has to be greater than $0 and less than ${max_budget}.", param_hint="'--amount'")

    return round(amount, 2)
