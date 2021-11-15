from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Query
from models.review_for_consumer_model import *
from config.database import review_for_consumer_collection
from schemas.review_for_consumer_schema import review_for_consumer_serializer

review_for_consumer_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

# Get all reviews created by a unique producer
@review_for_consumer_router.get("/producer_id", response_model=List[review_for_consumer_response])
async def get_all_review_for_consumer_by_producer_id(producer_id: str = Query(..., max_length=24)):
    list_of_review_documents = []
    
    if not ObjectId.is_valid(producer_id):
        raise HTTPException(status_code=404, detail=producer_id + "is not a valid ObjectId type")

    review_document_cursor = review_for_consumer_collection.find({"producer_id": ObjectId(producer_id)})

    for review_document in review_document_cursor:
        list_of_review_documents.append(review_for_consumer_serializer(review_document))

    return list_of_review_documents


# Get all reviews created by a unique consumer
@review_for_consumer_router.get("/consumer_id", response_model=List[review_for_consumer_response])
async def get_all_review_for_consumer_by_consumer_id(consumer_id: str = Query(..., max_length=24)):
    list_of_review_documents = []
    
    if not ObjectId.is_valid(consumer_id):
        raise HTTPException(status_code=404, detail=consumer_id + "is not a valid ObjectId type")

    review_document_cursor = review_for_consumer_collection.find({"consumer_id": ObjectId(consumer_id)})

    for review_document in review_document_cursor:
        list_of_review_documents.append(review_for_consumer_serializer(review_document))

    return list_of_review_documents

# Get a unique review
@review_for_consumer_router.get("/{id}", response_model=review_for_consumer_response)
async def get_review_for_consumer_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail=id + "is not a valid ObjectId type")

    review_document_returned = review_for_consumer_collection.find_one({"_id": ObjectId(id)})

    if review_document_returned is None:
        raise HTTPException(status_code=404, detail="Consumer review not found with id of " + id)
    
    serialized_review_document = review_for_consumer_serializer(review_document_returned)

    return serialized_review_document

