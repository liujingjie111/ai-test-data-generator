"""Data validation utilities."""

import re


def validate_email(email: str) -> bool:
    """Validate an email address format.

    Args:
        email: Email address to validate.

    Returns:
        True if email is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate a phone number format (Chinese).

    Args:
        phone: Phone number to validate.

    Returns:
        True if phone is valid, False otherwise.
    """
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_id_card(id_card: str) -> bool:
    """Validate a Chinese ID card number.

    Args:
        id_card: ID card number to validate.

    Returns:
        True if ID card is valid, False otherwise.
    """
    pattern = r"^\d{17}[\dXx]$"
    if not bool(re.match(pattern, id_card)):
        return False

    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

    total = sum(int(id_card[i]) * weights[i] for i in range(17))
    return check_codes[total % 11] == id_card[-1].upper()


def validate_count(count: int, min_count: int = 1, max_count: int = 100000) -> bool:
    """Validate a count value is within the acceptable range.

    Args:
        count: Count value to validate.
        min_count: Minimum allowed value.
        max_count: Maximum allowed value.

    Returns:
        True if count is valid, False otherwise.
    """
    return min_count <= count <= max_count
