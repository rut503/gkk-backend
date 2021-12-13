from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List
from enum import Enum

from app.models.food_item_model import food_item_base

class status_enum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    ready = "ready"
    completed = "completed"
    cancelled_by_consumer = "cancelled_by_consumer"
    cancelled_by_producer = "cancelled_by_producer"

class meal_time_enum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"

class item_base(food_item_base):
    photo: HttpUrl
    rating: float = Field(..., ge=0.00, le=5.00)
    quantity: int = Field(..., ge=1, le=50)

class active_order_response(BaseModel):
    id: str = Field(..., min_length=24, max_length=24)
    consumer_id: str = Field(..., min_length=24, max_length=24)
    producer_id: str = Field(..., min_length=24, max_length=24)
    items: List[item_base] = Field(..., min_items=1, max_items=50)
    total_price: float = Field(..., ge=0.01, le=999.99)
    status: status_enum
    meal_time: meal_time_enum
    message_for_producer: str = Field(..., min_length=0, max_length=600)
    order_due_datetime: datetime
    date_updated: datetime
    date_created: datetime
