from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

MONGO_URL = settings.MONGODB_URI
DATABASE_NAME = settings.DB_NAME

client: AsyncIOMotorClient = None


def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGO_URL)
    return client


def get_database() -> AsyncIOMotorDatabase:
    return get_client()[DATABASE_NAME]