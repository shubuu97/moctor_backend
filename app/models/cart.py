from typing import List

from .dbmodel import DBModelMixin, DateTimeModelMixin
from .rwmodel import RWModel


class CartItem(RWModel):
    user: str
    product: str
    status: str


class CartItemInDB(DBModelMixin, DateTimeModelMixin, RWModel):
    pass


class CartItems(RWModel):
    items: List[CartItem]
