from pydantic import BaseModel
from datetime import datetime
from typing import List

class food_item_base(BaseModel):
    description: str
    photo: str
    price: float
    portion_size: float
    spicy: int
    allergy: List[str] = []

class food_item_in(food_item_base):
    producer_id: str
    diet_preference: str
    name: str

class food_item_update(food_item_base):
    pass

class food_item_out(food_item_base):
    id: str
    rating: float
    date_created: datetime
    date_updated: datetime
