from datetime import UTC, datetime

from bson import ObjectId
from fastapi import Depends

from app.core.exceptions import (
    DuplicateResourceError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.core.security import SecurityService, get_security_service
from app.db.mongodb import MongoDBClient, get_mongodb_client
from app.models.user_model import UserCreate, UserLogin, UserResponse, UserUpdate


class UserService:
    """Business logic layer for user operations."""

    def __init__(self, mongo_client: MongoDBClient, security_service: SecurityService):
        self._collection = mongo_client.get_collection("users")
        self._security = security_service

    async def create(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.get_by_email(user_data.email)
        if existing_user:
            raise DuplicateResourceError("email")

        user_dict = user_data.model_dump()
        user_dict["password"] = self._security.hash_password(user_data.password)
        user_dict["created_at"] = datetime.now(UTC)
        user_dict["updated_at"] = datetime.now(UTC)

        result = await self._collection.insert_one(user_dict)
        user = await self.get_by_id(result.inserted_id)
        return self._build_user_response(user)

    async def get_by_id(self, id: str):
        if not ObjectId.is_valid(id):
            raise UserNotFoundError()
        user = await self._collection.find_one({"_id": ObjectId(id)})
        if not user:
            raise UserNotFoundError()
        return user

    async def get_by_email(self, email: str):
        return await self._collection.find_one({"email": email})

    async def update(self, id: str, updates: UserUpdate):
        await self.get_by_id(id)
        update_data = updates.model_dump(exclude_unset=True)
        if "password" in update_data and updates.password is not None:
            update_data["password"] = self._security.hash_password(updates.password)
        update_data["updated_at"] = datetime.now(UTC)
        await self._collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        updated_user = await self.get_by_id(id)
        return self._build_user_response(updated_user)

    async def delete(self, id: str):
        if not ObjectId.is_valid(id):
            raise UserNotFoundError()
        result = await self._collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise UserNotFoundError()
        return True

    async def authenticate_user(self, user_data: UserLogin):
        user = await self.get_by_email(user_data.email)
        if not user or not self._security.verify_password(
            user_data.password, user["password"]
        ):
            raise InvalidCredentialsError()
        token = self._security.create_access_token(str(user["_id"]))
        return dict(
            access_token=token,
            token_type="bearer",
            user=self._build_user_response(user),
        )

    def _build_user_response(self, user: dict):
        if not user:
            return None
        user["id"] = str(user.pop("_id"))
        user.pop("password", None)
        return UserResponse(**user)


def get_user_service(
    mongo_client: MongoDBClient = Depends(get_mongodb_client),
    security_service: SecurityService = Depends(get_security_service),
):
    return UserService(mongo_client, security_service)
