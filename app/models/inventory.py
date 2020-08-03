from typing import Optional

from .dbmodel import DBModelMixin, DateTimeModelMixin
from .rwmodel import RWModel


class Inventory(RWModel):
    product: str
    available: Optional[int] = 0
    in_order: Optional[int] = 0
    in_transition: Optional[int] = 0
    delivered: Optional[int] = 0
    incoming_orders: Optional[int] = 0
    returning: Optional[int] = 0
    expired: Optional[int] = 0


class InventoryInDB(DBModelMixin, DateTimeModelMixin, Inventory):
    pass
