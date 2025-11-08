import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppBaseError
from app.core.logging_config import logger


def register_exception_handler(app: FastAPI):
    """Attach all custom exception handlers to FastAPI app"""

    @app.exception_handler(AppBaseError)
    async def handle_app_exceptions(request: Request, exc: AppBaseError):
        logger.warning(
            exc.message,
            extra={"request_path": str(request.url.path), "method": request.method},
        )
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exceptions(request: Request, exc: StarletteHTTPException):
        logger.warning(
            exc.detail,
            extra={"request_path": str(request.url.path), "method": request.method},
        )
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        details = [{"field": err["loc"], "msg": err["msg"]} for err in exc.errors()]
        logger.error(
            "Validation failed",
            extra={
                "request_path": str(request.url.path),
                "method": request.method,
                "details": details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=details
        )

    @app.exception_handler(PyMongoError)
    async def handle_mongo_exception(request: Request, exc: PyMongoError):
        details = {"error": {"message": "Database error", "details": str(exc)}}
        logger.error(
            "Database error",
            extra={
                "request_path": str(request.url.path),
                "method": request.method,
                "details": details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=details
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception):
        details = {"error": {"message": "Internal server error"}}
        logger.error(
            "Unexpected error",
            extra={
                "request_path": str(request.url.path),
                "method": request.method,
                "details": details,
                "traceback": traceback.format_exc(),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=details
        )
