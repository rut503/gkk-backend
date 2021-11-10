from pydantic import BaseModel
from datetime import datetime
from typing import List


class address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class consumer_base(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: address
    
class consumer_in(consumer_base):
    pass

class consumer_out(consumer_base):
    id: str
    rating: float
    active_orders: List[ str ] = []
    archived_orders: List[ str ] = []
    date_created: datetime
    date_updated: datetime
