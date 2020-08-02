from typing import List, Optional
from pydantic import AnyUrl

from .rwmodel import RWModel
from .dbmodel import DBModelMixin


class Category(RWModel):
    tags: Optional[List[str]] = None
    name: str
    image: Optional[AnyUrl]


class Categories(RWModel):
    categories: List[Category]


class CategoryInDB(DBModelMixin, Category):
    pass
