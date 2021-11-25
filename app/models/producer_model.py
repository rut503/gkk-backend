from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Set, Optional
from enum import Enum
from pydantic.fields import Field

class address_optional(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class address_in(BaseModel):
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
    address: Optional[address_optional]
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
    address: address_in
    
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

# class menu(BaseModel):
#     sunday: Optional[List[int]] = None
#     monday: Optional[List[int]] = None
#     tuesday: Optional[List[int]] = None
#     wednesday: Optional[List[int]] = None
#     thursday: Optional[List[int]] = None
#     friday: Optional[List[int]] = None
#     saturday: Optional[List[int]] = None

# class producer_base(BaseModel):
#     firstName: str 
#     lastName: str
#     phoneNumber: int
#     address: address

# class producer_in(producer_base):
#     pass
    
# class producer_out(producer_base):
#     id: str
#     rating: int
#     active_orders: List[ str ] = []
#     archived_orders: List[ str ] = []
#     food: Optional[List] = None
#     rating: int = 0
#     acceptedOrdersToCreate: Optional[Set[int]] = None
#     pendingOrderForProducer: Optional[Set[int]] = None
#     menu: Optional[menu]
#     date_created: datetime
#     date_updated: datetime
