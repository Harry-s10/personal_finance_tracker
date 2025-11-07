import re
from string import punctuation

from pydantic import SecretStr


def check_password_strength(value: SecretStr | None):
    if not value:
        return value
    password = value.get_secret_value()
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if "password" in password:
        raise ValueError('Password cannot contain the word "password"')
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(rf"{punctuation}", password):
        raise ValueError("Password must contain at least one special character")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")

    return value
