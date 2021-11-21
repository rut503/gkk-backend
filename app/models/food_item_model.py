from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class diet_preference(str, Enum):
    low_carb = "Low Carb"
    High_protein = "High Protein"
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

class food_item_post(BaseModel):
    producer_id: str = Field(..., min_length=24, max_length=24)
    diet_preference: diet_preference
    description: str = Field(..., min_length=1, max_length=1500)
    photo: HttpUrl
    price: float = Field(..., ge=0.01, le=999.99)
    name: str = Field(..., min_length=1, max_length=200)
    portion_size: float = Field(..., ge=0.01, le=999.99)
    spicy: int = Field(..., ge=0, le=3)
    allergy: List[str] = Field(..., max_items=100)

class food_item_put(BaseModel):
    diet_preference: diet_preference
    description: str = Field(..., min_length=1, max_length=1500)
    photo: HttpUrl
    price: float = Field(..., ge=0.01, le=999.99)
    name: str = Field(..., min_length=1, max_length=200)
    portion_size: float = Field(..., ge=0.01, le=999.99)
    spicy: int = Field(..., ge=0, le=3)
    allergy: List[str] = Field(..., max_items=100)

class food_item_response(BaseModel):
    id: str
    producer_id: str
    diet_preference: diet_preference
    description: str
    photo: HttpUrl
    price: float
    rating: float
    name: str
    portion_size: float
    spicy: int
    allergy: List[str]
    date_updated: datetime
    date_created: datetime
