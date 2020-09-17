from fastapi import APIRouter, Depends, Body
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY

from ....crud.inventory import get_inventory_for_product, create_inventory, update_inventory
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.inventory import InventoryInDB, InventoriesInResponse, Inventory

router = APIRouter()


@router.get("/product-inventory", response_model=InventoryInDB, tags=["inventories"])
async def get_product_inventory(
        product_name: str,
        db: AsyncIOMotorClient = Depends(get_database)
):
    inventory = await get_inventory_for_product(db, product_name)
    return inventory


@router.get("/products-inventories", response_model=InventoriesInResponse, tags=["inventories"])
async def get_product_inventory(
        product_names: str,
        db: AsyncIOMotorClient = Depends(get_database)
):
    inventories = await get_inventory_for_product(db, product_names)
    return InventoriesInResponse(inventories=inventories)


@router.post("/inventory", response_model=InventoryInDB, tags=["inventories"], status_code=HTTP_201_CREATED)
async def create_product_inventory(
        inventory: Inventory = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)
):
    inventory_by_product = await get_inventory_for_product(
        db, inventory.product
    )
    if inventory_by_product:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"inventory already exists. name={inventory_by_product.product}"
        )
    db_inventory = await create_inventory(db, inventory)
    return db_inventory


@router.put("/inventory", response_model=InventoryInDB, tags=["inventories"], status_code=HTTP_201_CREATED)
async def update_product_inventory(
        inventory: Inventory = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)
):
    inventory_by_product = await get_inventory_for_product(
        db, inventory.product
    )
    if not inventory_by_product:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"inventory does not exists. Create first. name={inventory_by_product.product}"
        )
    db_inventory = await update_inventory(db, inventory)
    return db_inventory
