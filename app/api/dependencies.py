from uuid import uuid4

from fastapi import Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.exceptions import InvalidTokenError
from app.core.security import SecurityService, get_security_service, oauth2_schemes
from app.models.user_model import UserResponse
from app.services.user_service import UserService, get_user_service


async def get_current_user(
    token: str = Depends(oauth2_schemes),
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Validate JWT and return the authenticated user"""
    payload = security_service.decode_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")

    user = await user_service.get_by_id(user_id)
    user_copy = dict(user)
    user_copy["id"] = str(user_copy.pop("_id"))
    user_copy.pop("password", None)
    return UserResponse(**user_copy)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
