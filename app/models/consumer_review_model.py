from pydantic import BaseModel
from typing import Optional

class consumer_review_base(BaseModel):
    rating: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class consumer_review_in(consumer_review_base):
    pass