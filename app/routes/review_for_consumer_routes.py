from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.review_for_consumer_model import *
from config.database import review_for_consumer_collection
from schemas.review_for_consumer_schema import review_for_consumer_serializer

review_for_consumer_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

@review_for_consumer_router.get("/{id}", response_model=review_for_consumer_response)
async def get_review_for_consumer_by_id(id: Optional[str] = None):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail=id + "is not a valid ObjectId type")

    review_document_returned = review_for_consumer_collection.find_one({"_id": ObjectId(id)})

    if review_document_returned is None:
        raise HTTPException(status_code=404, detail="Consumer review not found with id of " + id)
    
    serialized_review_document = review_for_consumer_serializer(review_document_returned)

    return serialized_review_document