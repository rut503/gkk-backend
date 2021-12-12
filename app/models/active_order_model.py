from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime
from typing import List
from enum import Enum

from app.models.food_item_model import diet_preference_enum

'''
    items.*.quantity : 1 - 99
    order_total : 0.01 - 999.99 float
    status : drop down menu
    meal_time : drop down menu
    order_due_datetime : ISO date
    message_for_producer : 600 character string
'''
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

class food_item_base(BaseModel):
    diet_preference: List[diet_preference_enum]
    description: str = Field(..., min_length=1, max_length=1500)
    price: float = Field(..., ge=0.01, le=999.99)
    name: str = Field(..., min_length=1, max_length=200)
    portion_size: float = Field(..., ge=0.01, le=999.99)
    spicy: int = Field(..., ge=0, le=3)
    allergy: List[str] = Field(..., max_items=100)

class item_base(BaseModel):
    food_item: food_item_base
    quantity: int = Field(..., ge=1, le=99)

class active_order_base(BaseModel):
    id: str = Field(..., min_length=24, max_length=24)
    consumer_id: str = Field(..., min_length=24, max_length=24)
    producer_id: str = Field(..., min_length=24, max_length=24)
    items: List[item_base] = NOT_SURE
    total_price: float = Field(..., ge=0.01, le=999.99)
    status: status_enum
    meal_time: meal_time_enum
    message_for_producer: str = Field(..., min_length=0, max_length=600)
    order_due_datetime: datetime
    date_updated: datetime
    date_created: datetime