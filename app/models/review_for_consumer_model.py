from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class review_for_consumer_post(BaseModel):
    consumer_id: str
    producer_id: str
    title: str
    rating: int
    description: str

class review_for_consumer_put(BaseModel):
    rating: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class review_for_consumer_response(BaseModel):
    id: str
    consumer_id: str
    producer_id: str
    title: str
    rating: int
    description: str
    date_created: datetime
    date_updated: datetime