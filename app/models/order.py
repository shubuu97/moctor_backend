from enum import Enum
from typing import List

from .dbmodel import DBModelMixin, DateTimeModelMixin
from .rwmodel import RWModel


class OrderStatus(str, Enum):
    placed = 'placed'
    accepted = 'accepted'
    rejected = 'rejected'
    hold = 'hold'
    failed = 'failed'
    processing = 'processing'
    cancelled = 'cancelled'
    completed = 'completed'
    refunded = 'refunded'


class ChargesType(str, Enum):
    delivery = 'delivery'
    tax = 'tax'
    other = 'other'


class Charges(RWModel):
    type: ChargesType
    amount: float


class Address(RWModel):
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    country: str
    pin: str


class Order(RWModel):
    user: str
    status: List[OrderStatus]
    products: List[str]
    product_prices: List[float]
    address: Address
    amount: float
    discount: float
    charges: List[Charges]
    total_amount: float


class OrderInDB(DBModelMixin, DateTimeModelMixin, Order):
    pass
