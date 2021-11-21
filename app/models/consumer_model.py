from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class address_in(BaseModel):
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=25)
    zip_code: str = Field(..., min_length=2, max_length=12)
    
class consumer_in(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15, regex="[0-9]{10,15}")
    address: address_in

# class address_put(BaseModel):
#     street: str = Field(None, min_length=1, max_length=100)
#     city: str = Field(None, min_length=1, max_length=50)
#     state: str = Field(None, min_length=1, max_length=25)
#     zip_code: str = Field(None, min_length=2, max_length=12)

# class consumer_put(BaseModel):
#     first_name: Optional[str] = Field(None, min_length=1, max_length=50)
#     last_name: Optional[str] = Field(None, min_length=1, max_length=50)
#     phone_number: Optional[str] = Field(None, min_length=10, max_length=15, regex="[0-9]{10,15}")
#     address: Optional[address_put] = None

class address_response(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class consumer_response(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    address: address_response
    rating: float
    active_orders: List[ str ]
    date_created: datetime
    date_updated: datetime
