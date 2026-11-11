"""Shared format validation for contact fields.

Both the HTTP schemas and the provisioning scripts use these helpers so that a
value accepted in one entry point is accepted everywhere, and the same rules
are applied in the browser.
"""

from __future__ import annotations

import re

MAX_EMAIL_LENGTH = 255
MAX_PHONE_LENGTH = 20
MIN_PHONE_DIGITS = 7
MAX_PHONE_DIGITS = 15

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*"
    r"\.[A-Za-z]{2,63}$"
)

# Optional leading "+" or area-code parentheses, digits, and the separators
# people normally type in a phone number. The digit count is checked separately.
PHONE_PATTERN = re.compile(
    r"^\+?(?:\([0-9]{1,6}\)\s?)?[0-9][0-9\s().-]{3,17}[0-9]$"
)


def normalize_email(email: str | None) -> str | None:
    """Trim and lowercase an email, returning None for a blank value.

    Raises:
        ValueError: when the value is not a valid email address.
    """
    if email is None:
        return None
    cleaned = email.strip().lower()
    if not cleaned:
        return None
    if len(cleaned) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.match(cleaned):
        raise ValueError("Enter a valid email address")
    return cleaned


def normalize_phone(phone: str | None) -> str | None:
    """Trim a phone number, returning None for a blank value.

    Accepts international numbers with an optional leading ``+`` and common
    separators (spaces, dots, hyphens, parentheses). The number must contain
    between 7 and 15 digits.

    Raises:
        ValueError: when the value is not a valid phone number.
    """
    if phone is None:
        return None
    cleaned = phone.strip()
    if not cleaned:
        return None
    digits = sum(character.isdigit() for character in cleaned)
    if (
        len(cleaned) > MAX_PHONE_LENGTH
        or not PHONE_PATTERN.match(cleaned)
        or not MIN_PHONE_DIGITS <= digits <= MAX_PHONE_DIGITS
    ):
        raise ValueError("Enter a valid phone number")
    return cleaned
