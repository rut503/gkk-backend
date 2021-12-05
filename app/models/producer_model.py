from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic.fields import Field

class address_response(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class address_post(BaseModel):
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=25)
    zip_code: str = Field(..., min_length=2, max_length=12)

class filter_fields(BaseModel):
    first_name: Optional[bool] = True
    last_name: Optional[bool] = True
    phone_number: Optional[bool] = True
    address: Optional[bool] = True
    food_items: Optional[bool] = True
    rating: Optional[bool] = True
    active_orders: Optional[bool] = True
    menu: Optional[bool] = True
    date_created: Optional[bool] = True
    date_updated: Optional[bool] = True

class producer_response(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[address_response]
    food_items: Optional[List[str]] = None
    rating: Optional[float] = None
    active_orders: Optional[List[str]] = None
    menu: Optional[dict] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

class producer_post(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name : str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15, regex="[0-9]{10,15}")
    address: address_post

# Used in insert and update calls for menu subdocument
class day(str, Enum):
    sunday = "sunday"
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"

class meal_type(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    
class meal_array_put(BaseModel):
    food_array: List[str]
