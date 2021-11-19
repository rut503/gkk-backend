from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Query
from models.review_for_consumer_model import *
from config.database import review_for_consumer_collection
from schemas.review_for_consumer_schema import review_for_consumer_serializer, reviews_for_consumer_serializer

review_for_consumer_router = APIRouter()

dummyData = {
    "1": {"rating": "5", "title": "Test", "description": "Description"}
}

@review_for_consumer_router.get("/by_user", response_model=List[review_for_consumer_response])
async def get_all_review_for_consumer_by_user(consumer_id: Optional[str] = Query(None, max_length=24),
                                              producer_id: Optional[str] = Query(None, max_length=24)) -> list:
    # Find reviews with matching producer_id and consumer_id
    if consumer_id is not None and producer_id is not None:
        if not ObjectId.is_valid(consumer_id):
            raise HTTPException(status_code=404, detail=consumer_id + "is not a valid ObjectId type")
        if not ObjectId.is_valid(producer_id):
            raise HTTPException(status_code=404, detail=producer_id + "is not a valid ObjectId type")

        review_document_cursor = review_for_consumer_collection.find({"consumer_id": ObjectId(consumer_id), "producer_id": ObjectId(producer_id)})
        return reviews_for_consumer_serializer(review_document_cursor)

    # Check if consumer_id is not none
    if consumer_id is not None:
        if not ObjectId.is_valid(consumer_id):
            raise HTTPException(status_code=404, detail=consumer_id + "is not a valid ObjectId type")

        review_document_cursor = review_for_consumer_collection.find({"consumer_id": ObjectId(consumer_id)})
        return reviews_for_consumer_serializer(review_document_cursor)

    # Check if producer_id is not none
    if producer_id is not None:
        if not ObjectId.is_valid(producer_id):
            raise HTTPException(status_code=404, detail=producer_id + "is not a valid ObjectId type")
        
        review_document_cursor = review_for_consumer_collection.find({"producer_id": ObjectId(producer_id)})
        return reviews_for_consumer_serializer(review_document_cursor)
    

# Get a unique review
@review_for_consumer_router.get("/id/{id}", response_model=review_for_consumer_response)
async def get_review_for_consumer_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail=id + "is not a valid ObjectId type")

    review_document_returned = review_for_consumer_collection.find_one({"_id": ObjectId(id)})

    if review_document_returned is None:
        raise HTTPException(status_code=404, detail="Consumer review not found with id of " + id)
    
    serialized_review_document = review_for_consumer_serializer(review_document_returned)

    return serialized_review_document

# Post a review
@review_for_consumer_router.post("/", response_model=review_for_consumer_response)
async def post_review_for_consumer(review: review_for_consumer_post):
    review_to_insert = {"date_created" : datetime.today(), "date_updated" : datetime.today(), **review.dict()}
    result = review_for_consumer_collection.insert_one(review_to_insert)

    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Error while inserting")

    # This does an extra query for every insert
    # inserted_review = review_for_consumer_collection.find_one({"_id": result.inserted_id})
    # inserted_review = review_for_consumer_serializer(inserted_review)

    #print(type(result.inserted_id.__str__()))
    #return inserted_review

    # This way doesn't use a query
    review_to_insert["id"] = result.inserted_id.__str__()

    return review_to_insert