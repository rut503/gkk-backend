from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    
class consumer_post(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: address

class consumer_put(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[address] = None

class consumer_response(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    address: address
    rating: float
    active_orders: List[ str ]
    archived_orders: List[ str ]
    date_created: datetime
    date_updated: datetime
