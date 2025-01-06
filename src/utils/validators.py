import click
from datetime import datetime


def validate_parse_date(date_str: str, allow_future: bool = False, force_full_date: bool = False):
    """
    Parse and validate a date string in the format 'YYYY', 'YYYY-MM', or 'YYYY-MM-DD'.
    Ensures the date isn't in the future unless allow_future is True.
    If force_full_date is True, only 'YYYY-MM-DD' is accepted.
    """
    try:
        if force_full_date and len(date_str) != 10:
            raise click.BadParameter(
                "Only the full date format 'YYYY-MM-DD' is accepted.",
                param_hint="'--date'"
            )
        if len(date_str) == 4:
            if force_full_date:
                raise click.BadParameter(
                    "Only the full date format 'YYYY-MM-DD' is accepted.",
                    param_hint="'--date'"
                )
            year = int(date_str)
            if year < 1900 or year > 2100:
                raise click.BadParameter(
                    "Year must be between 1900 and 2100.",
                    param_hint="'--date'"
                )
            return year, None, None
        elif len(date_str) == 7:
            if force_full_date:
                raise click.BadParameter(
                    "Only the full date format 'YYYY-MM-DD' is accepted.",
                    param_hint="'--date'"
                )
            parsed_date = datetime.strptime(date_str, "%Y-%m")
            if parsed_date.year < 1900 or parsed_date.year > 2100:
                raise click.BadParameter(
                    "Year must be between 1900 and 2100.",
                    param_hint="'--date'"
                )
            return parsed_date.year, parsed_date.month, None
        elif len(date_str) == 10:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            if parsed_date.year < 1900 or parsed_date.year > 2100:
                raise click.BadParameter(
                    "Year must be between 1900 and 2100.",
                    param_hint="'--date'"
                )
            today = datetime.now().date()
            if not allow_future and parsed_date.date() > today:
                raise click.BadParameter(
                    "Please enter a valid past or current date.",
                    param_hint="'--date'"
                )
            return parsed_date.year, parsed_date.month, parsed_date.day
        else:
            raise ValueError
    except ValueError:
        raise click.BadParameter(
            "Invalid date format. Use 'YYYY-MM-DD' and ensure it's a valid date.",
            param_hint="'--date'"
        )


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


def validate_budget_amount(amount: float):
    """
    Validates the budget amount to be greater than $0 and less than or equal to $100,000.
    """
    max_budget = 100000

    if amount <= 0 or amount > max_budget:
        raise click.BadParameter(f"Budget has to be greater than $0 and less than ${max_budget}.", param_hint="'--amount'")

    return round(amount, 2)
