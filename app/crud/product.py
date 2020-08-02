from typing import List

from ..db.mongodb import AsyncIOMotorClient
from ..models.product import ProductInDB, ProductFilterParams
from ..core.config import database_name, products_collection_name


async def get_all_products(
        conn: AsyncIOMotorClient, limit=20, offset=0
) -> List[ProductInDB]:
    products: List[ProductInDB] = []
    product_docs = await conn[database_name][products_collection_name].find({},
                                                                            limit=limit,
                                                                            skip=offset)
    async for row in product_docs:
        products.append(
            ProductInDB(
                **row
            )
        )
    return products


async def get_products_with_filter(
        conn: AsyncIOMotorClient, filters: ProductFilterParams
) -> List[ProductInDB]:
    products: List[ProductInDB] = []
    base_query = {}

    if filters.tag:
        base_query["tags"] = f"$all: [\"{filters.tag}\"]"

    if filters.category:
        base_query["category"] = f"$all: [\"{filters.category}\"]"

    if filters.manufacturer:
        base_query["manufacturer"] = f"$in: [\"{filters.manufacturer}]\""

    rows = conn[database_name][products_collection_name].find(base_query,
                                                              limit=filters.limit,
                                                              skip=filters.offset)
    async for row in rows:
        products.append(
            ProductInDB(
                **row
            )
        )
    return products
