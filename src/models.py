"""Request validation for expense payloads."""
from datetime import datetime


class ValidationError(Exception):
    """Raised when incoming expense data fails validation."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def validate_expense_payload(data):
    """Validate the JSON body used to create an expense.

    Returns a tuple (title, amount, category, date) on success.
    Raises ValidationError with a human-readable message on failure.
    """
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object.")

    title = data.get("title")
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date")

    if not title or not isinstance(title, str) or not title.strip():
        raise ValidationError("'title' is required and must be a non-empty string.")

    if amount is None or isinstance(amount, bool):
        raise ValidationError("'amount' is required and must be a number.")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValidationError("'amount' must be a number.")
    if amount <= 0:
        raise ValidationError("'amount' must be greater than 0.")

    if not category or not isinstance(category, str) or not category.strip():
        raise ValidationError("'category' is required and must be a non-empty string.")

    if not date or not isinstance(date, str):
        raise ValidationError("'date' is required and must be a string in YYYY-MM-DD format.")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("'date' must be in YYYY-MM-DD format.")

    return title.strip(), amount, category.strip(), date
