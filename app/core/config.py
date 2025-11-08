from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    PRODUCTION = "production"
    STAGING = "staging"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    APP_NAME: Annotated[str, Field("Personal Finance Tracker")]
    ENVIRONMENT: Annotated[Environment, Field(Environment.LOCAL)]
    # Log config
    LOG_DIR: Annotated[str, Field("logs")]
    LOG_FILE: Annotated[str, Field("app.log")]
    LOG_FORMAT: Annotated[Literal["json", "text"], Field("text")]
    LOG_LEVEL: Annotated[LogLevel, Field(LogLevel.DEBUG)]
    # Database
    MONGO_URI: str
    DB_NAME: str
    # Required secrets
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: Annotated[str, Field("HS256")]
    ACCESS_TOKEN_EXPIRE_MINUTES: Annotated[int, Field(60)]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str):
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        return v

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_access_token_expire_minutes(cls, v: int):
        if v > 60:
            raise ValueError("Access token expire minutes should not exceed 60 minutes")
        return v


settings = Settings()
