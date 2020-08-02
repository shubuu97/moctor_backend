from typing import List

from ..db.mongodb import AsyncIOMotorClient
from ..models.tags import TagInDB
from ..core.config import database_name, tags_collection_name


async def fetch_all_tags(conn: AsyncIOMotorClient) -> List[TagInDB]:
    tags = []
    rows = conn[database_name][tags_collection_name].find()
    async for row in rows:
        tags.append(TagInDB(**row))

    return tags


async def create_tags_that_not_exist(conn: AsyncIOMotorClient, tags: List[str]):
    await conn[database_name][tags_collection_name].insert_many([{"tag": tag} for tag in tags])
