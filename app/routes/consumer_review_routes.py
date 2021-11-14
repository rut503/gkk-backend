from typing import Optional
from fastapi import APIRouter
from bson import ObjectId
import models
import config


consumer_review_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

@consumer_review_router.get("/consumer_review/{id}", response_model=models.consumer_review_out)
async def get_consumer_review_by_id(id: Optional[str] = None):
    review_collection = config.review_for_consumer_collection
    review_document = review_collection.find_one({"_id": ObjectId(id)})
    return review_document