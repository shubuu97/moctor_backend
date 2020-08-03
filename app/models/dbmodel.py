from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(default=datetime.utcnow(), alias="createdAt")
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(), alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[int] = None
