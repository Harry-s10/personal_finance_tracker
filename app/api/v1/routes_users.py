from fastapi import APIRouter, Depends, Request, status

from app.api.dependencies import get_current_user
from app.models.response_model import SuccessResponse
from app.models.user_model import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService, get_user_service
from app.util.response_builder import build_success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(
    user_data: UserCreate,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    new_user = await user_service.create(user_data)
    return build_success_response(request, new_user, "User created successfully")


@router.post(
    "/login",
    response_model=SuccessResponse,
    summary="Authenticate user and generate JWT token",
)
async def login_user(
    user_data: UserLogin,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    result = await user_service.authenticate_user(user_data)
    return build_success_response(request, result, "User Authenticated")


@router.get(
    "/me", response_model=UserResponse, summary="Get current logged-in user details"
)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_user),
):
    return current_user


@router.put("/me/update", response_model=SuccessResponse, summary="Update user details")
async def update_user(
    request: Request,
    updates: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    result = await user_service.update(str(current_user.id), updates)
    return build_success_response(request, result, "Update successful")
