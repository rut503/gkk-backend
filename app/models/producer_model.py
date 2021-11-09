from pydantic import BaseModel
from datetime import datetime
from typing import List, Set, Optional















# class address(BaseModel):
#     street: str
#     city: str
#     state: str
#     zip_code: str

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
#     phoneNum: int
#     address: address

# class producer_in(producer_base):
#     pass
    
# class producer_out(producer_base):
#     id: str
#     average_consumer_rating: int
#     active_orders: List[ str ] = []
#     archived_orders: List[ str ] = []
#     food: Optional[List] = None
#     rating: int = 0
#     acceptedOrdersToCreate: Optional[Set[int]] = None
#     pendingOrderForProducer: Optional[Set[int]] = None
#     menu: Optional[menu]
#     date_created: datetime
#     date_updated: datetime
