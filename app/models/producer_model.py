from pydantic import BaseModel, HttpUrl, EmailStr
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

class producer_response(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[EmailStr] = None
    bio: Optional[str] = None
    photo: Optional[HttpUrl] = None
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
    email_address: EmailStr
    bio: str = Field(..., min_length=0, max_length=2000)
    photo: HttpUrl
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
