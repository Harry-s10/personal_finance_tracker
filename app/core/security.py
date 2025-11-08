from datetime import UTC, datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import SecretStr

from app.core.config import settings
from app.core.exceptions import InvalidTokenError

oauth2_schemes = OAuth2PasswordBearer("/api/v1/users/login")


class SecurityService:
    """Handles password hashing, JWT creation and validation"""

    def __init__(self):
        self.__secret_key = settings.JWT_SECRET_KEY
        self.__algorithm = settings.JWT_ALGORITHM
        self.__access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.__pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: SecretStr):
        return self.__pwd_content.hash(password.get_secret_value())

    def verify_password(self, plain_password: SecretStr, hashed_password: SecretStr):
        return self.__pwd_content.verify(
            plain_password.get_secret_value(), hashed_password.get_secret_value()
        )

    def create_access_token(self, subject: str):
        expire = datetime.now(UTC) + timedelta(
            minutes=self.__access_token_expire_minutes
        )
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, self.__secret_key, self.__algorithm)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.__secret_key, [self.__algorithm])
        except JWTError:
            raise InvalidTokenError()


_security_service = None


def get_security_service():
    global _security_service
    if _security_service is None:
        _security_service = SecurityService()
    return _security_service
