from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.exceptions import DatabaseError


class MongoDBClient:
    def __init__(self, uri: str | None = None, db_name: str | None = None):
        if getattr(self, "_initialized", False):
            return
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None
        self._uri = uri or settings.MONGO_URI
        self._db_name = db_name or settings.DATABASE_NAME
        self._initialized = True

    async def connect(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(self._uri)
            self._db = self._client[self._db_name]
            # Create unique index on email to prevent race conditions
            await self._db["users"].create_index("email", unique=True)
            print(f"Connected to MongoDB: {self._db_name}")

    async def close(self):
        if self._client:
            self._client.close()
            self._db = None
            self._client = None
            print("MongoDB connection closed")

    def get_collection(self, name: str):
        if not isinstance(self._db, AsyncIOMotorDatabase):
            raise DatabaseError("Database is not instantiated")
        return self._db[name]


_mongodb_client = None


def get_mongodb_client():
    global _mongodb_client
    if _mongodb_client is None:
        _mongodb_client = MongoDBClient()
    return _mongodb_client
