from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
import models
import config


review_for_consumer_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

@review_for_consumer_router.get("/{id}", response_model=models.review_for_consumer_out)
async def get_review_for_consumer_by_id(id: Optional[str] = None):
    if id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    review_collection = config.review_for_consumer_collection
    review_document = review_collection.find_one({"_id": ObjectId(id)})
    return review_document