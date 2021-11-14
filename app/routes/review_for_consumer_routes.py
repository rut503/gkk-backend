from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
import models
import config
import schemas

review_for_consumer_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

@review_for_consumer_router.get("/{id}", response_model=models.review_for_consumer_return)
async def get_review_for_consumer_by_id(id: Optional[str] = None):
    if id is None:
        raise HTTPException(status_code=404)

    review_for_consumer_collection = config.review_for_consumer_collection    
    review_document_returned = review_for_consumer_collection.find_one({"_id": ObjectId(id)})

    if review_document_returned is None:
        raise HTTPException(status_code=404, detail="Consumer review not found with id of " + id)
    
    serialized_review_document = schemas.review_for_consumer_serializer(review_document_returned)

    return serialized_review_document