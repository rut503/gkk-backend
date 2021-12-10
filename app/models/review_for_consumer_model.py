from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic.fields import Field

class review_for_consumer_post(BaseModel):
    consumer_id: str
    producer_id: str
    rating: Optional[int] = Field(None, ge=0, le=5)
    title: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(..., min_length=1, max_length=600)

class review_for_consumer_put(BaseModel):
    rating: Optional[int] = Field(None, ge=0, le=5)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=600)

class review_for_consumer_response(BaseModel):
    id: str
    consumer_id: str
    producer_id: str
    rating: int
    title: str
    description: str
    date_created: datetime
    date_updated: datetime