from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class address_base(BaseModel):
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=25)
    zip_code: str = Field(..., min_length=2, max_length=12)
    
class consumer_base(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15, regex="[0-9]{10,15}")
    address: address_base

class consumer_post(consumer_base):
    pass

class consumer_put(consumer_base):
    pass

class consumer_response(consumer_base):
    id: str = Field(..., min_length=24, max_length=24)
    rating: float = Field(..., ge=0.00, le=5.00)
    active_orders: List[ str ]
    date_created: datetime
    date_updated: datetime
