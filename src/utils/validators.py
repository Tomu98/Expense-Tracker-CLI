import click
from utils.constants import VALID_CATEGORIES


def validate_category(category: str):
    category = category.capitalize()

    if category not in VALID_CATEGORIES:
        valid_options = ", ".join(VALID_CATEGORIES)
        raise click.BadParameter(
            f"'{category}' is not a valid category. The valid ones are: {valid_options}.",
            param_hint="'--category'"
        )

    return category


def validate_description(description: str):
    if not description:
        return "..."

    if len(description) < 3:
        raise click.BadParameter("Description must be at least 3 characters.", param_hint="'--description'")

    if len(description) > 100:
        raise click.BadParameter("Description must be no more than 100 characters.", param_hint="'--description'")

    return description


def validate_amount(amount: float):
    max_value = 100000
    if amount <= 0 or amount > max_value:
        raise click.BadParameter(f"Amount must be positive and not exceed ${max_value}.", param_hint="'--amount'")

    rounded_amount = round(amount, 2)
    if rounded_amount <= 0:
        raise click.BadParameter("Amount must be significant (greater than $0.00 after rounding).", param_hint="'--amount'")

    return rounded_amount