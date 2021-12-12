from pydantic import BaseModel, Field
from datetime import datetime

class review_for_producer_base(BaseModel):
    rating: float = Field(..., ge=0.00, le=5.00)
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=600)

class review_for_producer_put(review_for_producer_base):
    pass

class review_for_producer_post(review_for_producer_base):
    producer_id: str = Field(..., min_length=24, max_length=24)
    consumer_id: str = Field(..., min_length=24, max_length=24)

class review_for_producer_response(review_for_producer_post):
    id: str = Field(..., min_length=24, max_length=24)
    date_created: datetime
    date_updated: datetime
