from fastapi import APIRouter

from .endpoints.user import router as user_router
from .endpoints.authentication import router as auth_router
from .endpoints.order import router as order_router
from .endpoints.inventory import router as inventory_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(order_router)
router.include_router(inventory_router)
