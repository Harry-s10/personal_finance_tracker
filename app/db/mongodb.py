from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.exceptions import DatabaseError


class MongoDBClient:
    def __init__(self):
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None
        self._uri = settings.MONGO_URI
        self._db_name = settings.DATABASE_NAME

    async def connect(self):
        self._client = AsyncIOMotorClient(self._uri)
        self._db = self._client[self._db_name]
        print(f"Connected to MongoDB: {self._db_name}")

    async def close(self):
        if self._client:
            self._client.close()
            print("MongoDB connection closed")

    async def get_collection(self, name: str):
        if not isinstance(self._db, AsyncIOMotorDatabase):
            raise DatabaseError("Database is not instantiated")
        return self._db[name]


def get_mongodb_client():
    return MongoDBClient()
