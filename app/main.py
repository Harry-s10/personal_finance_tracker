from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    await initialize_database()
    yield
    # Shutdown code here
    await close_database_connection()


app = FastAPI(title="Personal finance tracker API", lifespan=lifespan)

app.include_router(user_router, prefix="/app/v1")
