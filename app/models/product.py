from typing import List, Optional
from pydantic import AnyUrl
from enum import Enum

from .rwmodel import RWModel
from .dbmodel import DBModelMixin, DateTimeModelMixin


class ProductFilterParams(RWModel):
    tag: str = ""
    category: str = ""
    manufacturer: str = ""
    limit: int = 20
    offset: int = 0


class ProductType(str, Enum):
    tablet = 'tablet'
    bottle = 'bottle'
    capsule = 'capsule'
    other = 'other'


class AdviceType(str, Enum):
    alcohol = 'alcohol'
    pregnancy = 'pregnancy'
    breastfeeding = 'breastfeeding'
    driving = 'driving'
    kidney = 'kidney'


class SafetyType(str, Enum):
    conditional = 'conditional'
    caution = 'caution'
    consult = 'consult'
    safe = 'safe'
    unsafe = 'unsafe'
    unknown = 'unknown'


class Advice(RWModel):
    type: AdviceType
    is_safe: bool
    advice: str


class ProductMin(RWModel):
    tags: Optional[List[str]] = None
    name: str
    categories: List[str]
    manufacturer: str
    mrp: str
    prescription_required: bool
    salt_composition: List[str]
    storage_info: str
    type: ProductType


class Product(ProductMin):
    images: Optional[List[AnyUrl]] = None
    quantity_in_one_unit: Optional[int] = None
    alternatives: Optional[List[str]] = None
    about: Optional[str] = None
    usage: Optional[str] = None
    side_effects: Optional[str] = None
    cope_side_effects: Optional[str] = None
    how_to_use: Optional[str] = None
    working: Optional[str] = None
    safety_advice: Optional[Advice] = None


class ProductsInResponse(RWModel):
    products: List[Product]


class ProductInDB(DBModelMixin, DateTimeModelMixin, Product):
    pass
