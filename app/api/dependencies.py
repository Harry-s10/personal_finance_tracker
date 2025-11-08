from fastapi import Depends, HTTPException, status

from app.core.exceptions import UserNotFoundError
from app.core.security import SecurityService, get_security_service, oauth2_schemes
from app.models.user_model import UserResponse
from app.services.user_service import UserService, get_user_service


async def get_current_user(
    token: str = Depends(oauth2_schemes),
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Validate JWT and return the authenticated user"""
    try:
        payload = security_service.decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = await user_service.get_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_copy = dict(user)
    user_copy["id"] = str(user_copy.pop("_id"))
    user_copy.pop("password", None)
    return UserResponse(**user_copy)
