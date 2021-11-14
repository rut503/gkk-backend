from typing import Optional
from fastapi import APIRouter
import models

consumer_review_router = APIRouter()

@consumer_review_router.get("/consumer_review/{id}")
async def get_consumer_review_by_id(id: Optional[str] = None):
    return "test"