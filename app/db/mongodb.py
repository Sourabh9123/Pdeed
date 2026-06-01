from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class MongoDB:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongodb = MongoDB()


async def connect_to_mongo() -> None:
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb.database = mongodb.client[settings.MONGODB_DATABASE]
    await mongodb.client.admin.command("ping")
    logger.info("Connected to MongoDB database: %s", settings.MONGODB_DATABASE)


async def close_mongo_connection() -> None:
    if mongodb.client:
        mongodb.client.close()
        logger.info("Closed MongoDB connection")


async def ping_mongo() -> bool:
    if not mongodb.client:
        return False

    try:
        await mongodb.client.admin.command("ping")
        return True
    except Exception as exc:
        logger.warning("MongoDB health check failed: %s", exc)
        return False
