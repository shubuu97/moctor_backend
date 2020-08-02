from typing import List

from ..db.mongodb import AsyncIOMotorClient
from ..models.order import OrderInDB
from ..core.config import database_name, orders_collection_name


async def get_orders_by_user(conn: AsyncIOMotorClient, username: str) -> List[OrderInDB]:
    orders: List[OrderInDB] = []
    order_docs = conn[database_name][orders_collection_name].find(
        {"user": username}, projection={"id": True}
    )
    async for row in order_docs:
        orders.append(
            OrderInDB(
                **row
            )
        )
    return orders


async def get_orders_by_status(
        conn: AsyncIOMotorClient, username: str, status: str
) -> List[OrderInDB]:
    orders: List[OrderInDB] = []
    order_docs = conn[database_name][orders_collection_name].find(
        {"user": username, "status": f"$all: [\"{status}\"]"}, projection={"id": True}
    )
    async for row in order_docs:
        orders.append(
            OrderInDB(
                **row
            )
        )
    return orders
