from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.v1.routes_users import router as user_router
from app.core.exceptions import (
    DatabaseError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.db.mongodb import get_mongodb_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    mongo_client = get_mongodb_client()
    await mongo_client.connect()
    app.state.mongo_client = mongo_client
    try:
        yield
    finally:
        # Shutdown code here
        await mongo_client.close()


app = FastAPI(title="Personal finance tracker API", lifespan=lifespan)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "personal-finance-tracker"}


app.include_router(user_router, prefix="/api/v1")


# Exception handler
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)}
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Database operation failed : {str(exc)}"},
    )
