from pydantic import BaseModel
from typing import Optional

class review_for_consumer_base(BaseModel):
    rating: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class review_for_consumer_in(review_for_consumer_base):
    pass

class review_for_consumer_out(review_for_consumer_base):
    test: Optional[str] = None
    pass