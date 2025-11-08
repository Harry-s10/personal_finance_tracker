from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

from app.models.objectid_model import PyObjectID
from app.util.validation import check_password_strength


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class UserBase(BaseModelConfig):
    full_name: Annotated[
        str,
        Field(
            ...,
            min_length=3,
            max_length=30,
            description="User full name",
            examples=["John Doe"],
        ),
    ]
    email: Annotated[
        EmailStr, Field(..., description="User email ID", examples=["john@example.com"])
    ]
    is_active: Annotated[bool, Field(True)]

    @field_validator("email")
    @classmethod
    def normalise_email(cls, v: EmailStr):
        return v.strip().lower()


class UserCreate(UserBase):
    password: Annotated[SecretStr, Field(..., description="User password")]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr):
        return check_password_strength(v)


class UserLogin(BaseModelConfig):
    email: Annotated[
        EmailStr,
        Field(
            ..., description="User's registered email id", examples=["john@example.com"]
        ),
    ]
    password: Annotated[SecretStr, Field(..., description="User's registered password")]

    @field_validator("email")
    @classmethod
    def normalise_email(cls, value: EmailStr):
        return value.strip().lower()


class UserUpdate(BaseModelConfig):
    full_name: Annotated[
        str | None,
        Field(
            None,
            min_length=3,
            max_length=30,
            description="Updated full name",
            examples=["John Doe"],
        ),
    ]
    password: Annotated[SecretStr | None, Field(None, description="Updated password")]

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr | None):
        return check_password_strength(value)


class UserResponse(BaseModelConfig):
    id: Annotated[
        PyObjectID, Field(..., alias="_id", description="MongoDB document ID")
    ]
    full_name: Annotated[str, Field(..., description="User's full name")]
    email: Annotated[EmailStr, Field(..., description="User's email ID")]
    created_at: Annotated[
        datetime | None, Field(None, description="Account creation date (ISO format)")
    ]
    updated_at: Annotated[
        datetime | None, Field(None, description="Last updated timestamp (ISO format)")
    ]

    model_config = ConfigDict(
        extra="forbid", from_attributes=True, str_strip_whitespace=True
    )


class TokenResponse(BaseModelConfig):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[str, Field("bearer", description="Token type")]
    user: Annotated[UserResponse, Field(..., description="User details")]
