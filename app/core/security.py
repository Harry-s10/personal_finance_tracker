from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UserNotFoundError

oauth2_schemes = OAuth2PasswordBearer("/users/login")


class SecurityService:
    """Handles password hashing, JWT creation and validation"""

    def __init__(self):
        self.__secret_key = settings.JWT_SECRET_KEY
        self.__algorithm = settings.JWT_ALGORITHM
        self.__access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.__pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str):
        return self.__pwd_content.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.__pwd_content.verify(plain_password, hashed_password)

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
            raise ValueError("Invalid or expired token")

    async def get_current_user(
        self,
        token: str = Depends(oauth2_schemes),
        user_services: UserService = Depends(get_user_service),
    ):
        """Validate JWT and return the authenticated user object"""
        payload = self.decode_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user = await user_services.get_by_id(user_id)
        except UserNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return user


def get_security_service():
    return SecurityService()
