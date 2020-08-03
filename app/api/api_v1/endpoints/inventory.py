from fastapi import APIRouter, Depends

from ....crud.inventory import get_inventory_for_product
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.inventory import InventoryInDB

router = APIRouter()


@router.get("/inventory", response_model=InventoryInDB, tags=["inventories"])
async def get_product_inventory(
        product_name: str,
        db: AsyncIOMotorClient = Depends(get_database)
):
    inventory = await get_inventory_for_product(db, product_name)
    return inventory
