from pydantic import BaseModel, Field
from datetime import datetime

class review_for_food_item_base(BaseModel):
    rating: float = Field(..., ge=0.00, le=5.00)
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=600)

class review_for_food_item_put(review_for_food_item_base):
    pass

class review_for_food_item_post(review_for_food_item_base):
    consumer_id: str = Field(..., min_length=24, max_length=24)
    food_item_id: str = Field(..., min_length=24, max_length=24)

class review_for_food_item_response(review_for_food_item_post):
    id: str = Field(..., min_length=24, max_length=24)
    date_created: datetime
    date_updated: datetime
