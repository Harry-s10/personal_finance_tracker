from contextlib import asynccontextmanager

from fastapi import FastAPI

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

app.include_router(user_router, prefix="/app/v1")
