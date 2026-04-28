from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
database = None


async def connect_to_mongo() -> None:
    global client, database
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]


async def close_mongo_connection() -> None:
    global client
    if client:
        client.close()


def get_db():
    return database
