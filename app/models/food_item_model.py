from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class food_item_post(BaseModel):
    producer_id: str
    diet_preference: str
    description: str
    photo: str
    price: float
    name: str
    portion_size: float
    spicy: int
    allergy: List[str]

class food_item_put(BaseModel):
    diet_preference: Optional[str] = None
    description: Optional[str] = None
    photo: Optional[str] = None
    price: Optional[float] = None
    name: Optional[str] = None
    portion_size: Optional[float] = None
    spicy: Optional[int] = None
    allergy: Optional[List[str]] = None

class food_item_response(BaseModel):
    id: str
    producer_id: str
    diet_preference: str
    description: str
    photo: str
    price: float
    rating: float
    name: str
    portion_size: float
    spicy: int
    allergy: List[str]
    date_created: datetime
    date_updated: datetime
