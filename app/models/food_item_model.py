from pydantic import BaseModel
from datetime import datetime
from typing import List

class food_item_base(BaseModel):
    producer_id: str
    diet_preference: str
    description: str
    photo: str
    price: float
    name: str
    portion_size: float
    spicy: int
    allergy: List[str] = []

class food_item_in(food_item_base):
    pass

class food_item_out(food_item_base):
    id: str
    rating: float
    date_created: datetime
    date_updated: datetime
