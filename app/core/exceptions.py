class AppBaseError(Exception):
    """Base class for all custom application errors"""

    pass


# ---- User related error ----
class UserNotFoundError(AppBaseError):
    """Raised when a user is not found in the database"""

    pass


class UserAlreadyExistsError(AppBaseError):
    """Raised when a user exists in the database"""

    pass


class InvalidCredentialsError(AppBaseError):
    """Raised when login credentials is invalid"""

    pass


# ---- Other common error ----
class DatabaseError(AppBaseError):
    """Raised when database operation fails"""

    pass


class ValidationError(AppBaseError):
    """Raised when data validation fails at a business level"""

    pass
