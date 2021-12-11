from os import stat
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Path, Query
from starlette import status

from app.models.review_for_consumer_model import *
from app.config.database import review_for_consumer_collection
from app.schemas.review_for_consumer_schema import review_for_consumer_serializer, reviews_for_consumer_serializer
from datetime import datetime

review_for_consumer_router = APIRouter()

# Get a review by id
@review_for_consumer_router.get("/{id}", response_model=review_for_consumer_response, status_code=status.HTTP_200_OK)
async def get_review_for_consumer_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=id + "is not a valid ObjectId type"
        )

    review_document_returned = review_for_consumer_collection.find_one({ "_id": ObjectId(id) })
    if review_document_returned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer review not found with id of " + id
        )
    
    serialized_review_document = review_for_consumer_serializer(review_document_returned)
    return serialized_review_document

# Get a all reviews between a consumer and producer
@review_for_consumer_router.get("", response_model=List[review_for_consumer_response], status_code=status.HTTP_200_OK)
async def get_all_review_for_consumer_by_user(
    consumer_id: Optional[str] = Query(None, min_length=24, max_length=24),
    producer_id: Optional[str] = Query(None, min_length=24, max_length=24)
) -> list:

    # Find reviews with matching producer_id and consumer_id
    if consumer_id is not None and producer_id is not None:
        if not ObjectId.is_valid(consumer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=consumer_id + "is not a valid ObjectId type"
            )
        if not ObjectId.is_valid(producer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=producer_id + "is not a valid ObjectId type"
            )

        review_document_cursor = review_for_consumer_collection.find({
            "consumer_id": ObjectId(consumer_id), 
            "producer_id": ObjectId(producer_id)
        })
        return reviews_for_consumer_serializer(review_document_cursor)

    # Check if consumer_id is not none
    if consumer_id is not None:
        if not ObjectId.is_valid(consumer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=consumer_id + "is not a valid ObjectId type"
            )
        review_document_cursor = review_for_consumer_collection.find({ "consumer_id": ObjectId(consumer_id) })
        return reviews_for_consumer_serializer(review_document_cursor)

    # Check if producer_id is not none
    if producer_id is not None:
        if not ObjectId.is_valid(producer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=producer_id + "is not a valid ObjectId type"
            )
        review_document_cursor = review_for_consumer_collection.find({ "producer_id": ObjectId(producer_id) })
        return reviews_for_consumer_serializer(review_document_cursor)


# Post a single review
@review_for_consumer_router.post("/", response_model=review_for_consumer_response, status_code=status.HTTP_201_CREATED)
async def post_review_for_consumer(review: review_for_consumer_post):
    review_to_insert = {
        **review.dict(),
        "date_created" : datetime.utcnow(),
        "date_updated" : datetime.utcnow()
    }

    # Convert string to ObjectId
    review_to_insert["producer_id"] = ObjectId(review_to_insert["producer_id"])
    review_to_insert["consumer_id"] = ObjectId(review_to_insert["consumer_id"])

    result = review_for_consumer_collection.insert_one(review_to_insert)

    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error while inserting"
        )

    # Retrieving newly added document
    inserted_review = review_for_consumer_collection.find_one({ "_id": result.inserted_id })
    inserted_review = review_for_consumer_serializer(inserted_review)
    return inserted_review


@review_for_consumer_router.put("/{id}", response_model=review_for_consumer_response, status_code=status.HTTP_200_OK)
async def update_review_for_consumer( *, id: str = Path(..., min_length=24, max_length=24), review: review_for_consumer_put ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    curent_review = review_for_consumer_serializer( review_for_consumer_collection.find_one({ "_id": ObjectId(id) }) )
    
    # Updating date_updated field
    curent_review ['date_updated'] = datetime.utcnow()
    review_identifier = curent_review['id']

    fields_to_change_model = review_for_consumer_put(**curent_review)
    updated_data = review.dict(exclude_unset=True)
    updated_review = fields_to_change_model.copy(update=updated_data)
    
    # Making Basemodel a dict
    updated_review = updated_review.dict()
    # Setting updated time
    updated_review["date_updated"] = datetime.utcnow()

    result = review_for_consumer_collection.update_one(
        { "_id": ObjectId(review_identifier) }, 
        { "$set": updated_review }
    )

    if result.modified_count != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error while updating"
        )

    updated_review_document = review_for_consumer_collection.find_one({ "_id": ObjectId(review_identifier) })
    updated_review_document = review_for_consumer_serializer(updated_review_document)
    return updated_review_document


@review_for_consumer_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_for_consumer( id: str = Path(..., min_length=24, max_length=24) ):
    review_for_consumer_collection.delete_one({ "_id": ObjectId(id) })
