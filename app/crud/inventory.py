from typing import List

from ..models.inventory import Inventory, InventoryInDB
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import inventory_collection_name, database_name


async def get_inventory_for_product(
    conn: AsyncIOMotorClient, product_name: str
) -> InventoryInDB:
    inventory_doc = conn[database_name][inventory_collection_name].find({"product": product_name})
    inventory = InventoryInDB(**inventory_doc)
    return inventory


async def get_inventory_for_products(
    conn: AsyncIOMotorClient, product_names: str
) -> InventoryInDB:
    inventories: List[InventoryInDB] = []
    inventory_docs = conn[database_name][inventory_collection_name].find(
        {"product": f"$all: {product_names}"}
    )
    for row in inventory_docs:
        inventories.append(**row)
    return inventories


async def create_inventory(
    conn: AsyncIOMotorClient, inventory: Inventory
) -> InventoryInDB:
    inventory_doc = inventory.dict()
    await conn[database_name][inventory_collection_name].insert_one(inventory_doc)
    return InventoryInDB(**inventory_doc)


async def update_inventory(conn: AsyncIOMotorClient, inventory: Inventory) -> InventoryInDB:
    db_inventory = await get_inventory_for_product(conn, inventory.product)

    db_inventory.available = inventory.available or db_inventory.available
    db_inventory.in_order = inventory.in_order or db_inventory.in_order
    db_inventory.in_transition = inventory.in_transition or db_inventory.in_transition
    db_inventory.delivered = inventory.delivered or db_inventory.delivered
    db_inventory.incoming_orders = inventory.incoming_orders or db_inventory.incoming_orders
    db_inventory.returning = inventory.returning or db_inventory.returning
    db_inventory.expired = inventory.expired or db_inventory.expired

    updated_at = await conn[database_name][inventory_collection_name] \
        .update_one({"product": db_inventory.product}, {'$set': db_inventory.dict()})
    db_inventory.updated_at = updated_at
    return db_inventory
