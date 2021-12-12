from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import List
from enum import Enum

class diet_preference_enum(str, Enum):
    low_carb = "Low Carb"
    high_protein = "High Protein"
    low_no_sodium = "Low/No Sodium"
    diabetic = "Diabetic"
    gluten_free = "Gluten Free"
    lactose_free = "Lactose Free"
    vegetarian = "Vegetarian"
    non_vegetarian = "Non-Vegetarian"
    paleo = "Paleo"
    vegan = "Vegan"
    pescetarian = "Pescetarian"
    eggitarian = "Eggitarian"
    nut_free = "Nut Free"
    other = "Other"

class food_item_base(BaseModel):
    diet_preference: List[diet_preference_enum]
    description: str = Field(..., min_length=1, max_length=1500)
    price: float = Field(..., ge=0.01, le=999.99)
    name: str = Field(..., min_length=1, max_length=200)
    portion_size: float = Field(..., ge=0.01, le=999.99)
    spicy: int = Field(..., ge=0, le=3)
    allergy: List[str] = Field(..., max_items=100)

class food_item_put(food_item_base):
    pass

class food_item_post(food_item_base):
    producer_id: str = Field(..., min_length=24, max_length=24)

class food_item_response(food_item_post):
    id: str = Field(..., min_length=24, max_length=24)
    photo: HttpUrl
    rating: float = Field(..., ge=0.00, le=5.00)
    date_updated: datetime
    date_created: datetime
