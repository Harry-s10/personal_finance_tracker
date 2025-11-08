from fastapi import status


class AppBaseError(Exception):
    """Base class for all custom application errors"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details

    def to_dict(self):
        return {"error": {"message": self.message, "details": self.details}}


# ---- User related error ----
class UserNotFoundError(AppBaseError):
    """Raised when a user is not found in the database"""

    def __init__(self):
        super().__init__("User not found", status.HTTP_404_NOT_FOUND)


class InvalidCredentialsError(AppBaseError):
    """Raised when login credentials is invalid"""

    def __init__(self):
        super().__init__("Invalid email or password", status.HTTP_401_UNAUTHORIZED)


class InvalidTokenError(AppBaseError):
    """Raised when token is invalid"""

    def __init__(self, message: str | None = None):
        super().__init__(
            "Invalid token or expired token" if message is None else message,
            status.HTTP_401_UNAUTHORIZED,
        )


class UnauthorizedAccessError(AppBaseError):
    """Raised when unauthorized accesss"""

    def __init__(self):
        super().__init__("Unauthorized access", status.HTTP_403_FORBIDDEN)


class ResourceNotFoundError(AppBaseError):
    """Raise when resource not found"""

    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", status.HTTP_404_NOT_FOUND)


class DuplicateResourceError(AppBaseError):
    """Raise when duplicate resource detected"""

    def __init__(self, resource: str):
        super().__init__(f"{resource} already exists", status.HTTP_409_CONFLICT)


# ---- Other common error ----
class DatabaseConnectionError(AppBaseError):
    """Raised when database connection fails"""

    def __init__(self):
        super().__init__(
            "Database connection error", status.HTTP_503_SERVICE_UNAVAILABLE
        )


class DatabaseError(AppBaseError):
    """Raised when database operation fails"""

    def __init__(self, message: str):
        super().__init__(
            f"Database error : {message}", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ValidationError(AppBaseError):
    """Raised when data validation fails at a business level"""

    def __init__(self, details: dict):
        super().__init__(
            "Validation failed", status.HTTP_422_UNPROCESSABLE_CONTENT, details
        )
