from fastapi import APIRouter, Depends

from ....core.jwt import get_current_user_authorizer
from ....crud.order import get_orders_by_user
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.order import OrdersInResponse
from ....models.user import User

router = APIRouter()


@router.get("/orders", response_model=OrdersInResponse, tags=["orders"])
async def get_all_orders(
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    username = user.username
    orders = await get_orders_by_user(db, username)
    return OrdersInResponse(orders=orders)
