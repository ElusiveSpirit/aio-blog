import motor.motor_asyncio

from app.utils import settings


def connect_db() -> tuple:
    """
    MongoDB connection function

    :param settings: Application settings. Sets db attr after initializing
    :return: (client, db) tuple
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]
    settings.db = db

    return client, db
