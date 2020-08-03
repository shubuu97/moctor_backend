from fastapi import APIRouter, Query, Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from starlette.exceptions import HTTPException

from ....models.product import Product, ProductInDB, ProductsInResponse, ProductFilterParams
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....crud.product import get_products_with_filter, get_product_by_name, create_product


router = APIRouter()


@router.get("/products", response_model=ProductsInResponse, tags=["products"])
async def get_products(
        tag: str = "",
        category: str = "",
        manufacturer: str = "",
        limit: int = Query(20, gt=0),
        offset: int = Query(0, gt=0),
        db: AsyncIOMotorClient = Depends(get_database),
):
    filters = ProductFilterParams(
        tag=tag, category=category, manufacturer=manufacturer, limit=limit, offset=offset
    )
    db_products = await get_products_with_filter(
        db, filters
    )
    return ProductsInResponse(products=db_products)


@router.post("/products", response_model=ProductInDB, tags=["products"], status_code=HTTP_201_CREATED)
async def create_new_product(
        product: Product = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)
):
    product_by_name = await get_product_by_name(
        db, product.name
    )
    if product_by_name:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"product already exists. name={product_by_name.name}"
        )
    db_product = await create_product(db, product)
    return db_product
