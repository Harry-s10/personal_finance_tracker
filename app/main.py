from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import RequestIDMiddleware
from app.api.v1.routes_users import router as user_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handler
from app.core.logging_config import logger
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


def create_app():
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(user_router, prefix="/api/v1")
    register_exception_handler(app)
    app.add_middleware(RequestIDMiddleware)
    logger.info(f"{settings.APP_NAME} started in {settings.ENVIRONMENT.upper()} mode")
    return app


app = create_app()
