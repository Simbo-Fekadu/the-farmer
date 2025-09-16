from motor.motor_asyncio import AsyncIOMotorDatabase
from ..main import db

async def get_database() -> AsyncIOMotorDatabase:
    return db