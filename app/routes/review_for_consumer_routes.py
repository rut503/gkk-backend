from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Path, Query
from starlette import status
from datetime import datetime
from pymongo import ReturnDocument
from starlette.responses import Response

from models.review_for_consumer_model import review_for_consumer_post, review_for_consumer_put, review_for_consumer_response
from config.database import review_for_consumer_collection, consumer_collection, producer_collection
from schemas.review_for_consumer_schema import review_for_consumer_serializer, reviews_for_consumer_serializer

review_for_consumer_router = APIRouter()


@review_for_consumer_router.get("/{id}", response_model=review_for_consumer_response, status_code=status.HTTP_200_OK)
async def get_review_for_consumer_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # finding review_for_consumer that matches passed in id
    review_document_returned = review_for_consumer_collection.find_one({ "_id": ObjectId(id) })
    if review_document_returned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Consumer not found with review id " + id
        )
    serialized_review_document = review_for_consumer_serializer(review_document_returned)
    return serialized_review_document


@review_for_consumer_router.get("", response_model=List[review_for_consumer_response], status_code=status.HTTP_200_OK)
async def get_all_review_for_consumer_by_user(
    consumer_id: Optional[str] = Query(None, min_length=24, max_length=24),
    producer_id: Optional[str] = Query(None, min_length=24, max_length=24)
):
    find_review_query = {}

    # checking if consumer_id is passed in
    if consumer_id:
        # checking if consumer_id is valid ObjectId type
        if ObjectId.is_valid(consumer_id):
            find_review_query["consumer_id"] = ObjectId(consumer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=consumer_id + " consumer_id is not a valid ObjectId type!"
            )
    
    # checking if producer_id is passed in
    if producer_id:
        # checking if producer_id is valid ObjectId type
        if ObjectId.is_valid(producer_id):
            find_review_query["producer_id"] = ObjectId(producer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=producer_id + " producer_id is not a valid ObjectId type!"
            )

    # checking if find_review_query has any value
    if find_review_query:
        review_document_cursor = review_for_consumer_collection.find(find_review_query)
        serialized_review_documents = reviews_for_consumer_serializer(review_document_cursor)
        # checking if review_for_consumer were not found
        if len(serialized_review_documents) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Review for Consumer not found with passed in id(s)"
            )
        return serialized_review_documents
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Need to pass in at least consumer_id and/or producer_id"
            )


@review_for_consumer_router.post("/", response_model=review_for_consumer_response, status_code=status.HTTP_201_CREATED)
async def post_review_for_consumer(review: review_for_consumer_post):
    # checking if passed in producer_id and consumer_id is valid ObjectId type
    if not ObjectId.is_valid(review.producer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=review.producer_id + " is not a valid ObjectId type for producer_id"
        )
    if not ObjectId.is_valid(review.consumer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=review.consumer_id + " is not a valid ObjectId type for consumer_id"
        )
    
    # checking if the producer and consumer exists with their passed in ids 
    producer_count = producer_collection.count_documents({ "_id": ObjectId(review.producer_id) })
    if producer_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer not found with id " + review.producer_id
        )
    consumer_count = consumer_collection.count_documents({ "_id": ObjectId(review.consumer_id) })
    if consumer_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with id " + review.consumer_id
        )
    
    # converting review model to dictionary for insert and setting updated and created dates
    review_to_insert = review.dict()
    review_to_insert["date_updated"] = datetime.utcnow()
    review_to_insert["date_created"] = datetime.utcnow()

    # Convert string ids to ObjectIds
    review_to_insert["producer_id"] = ObjectId(review_to_insert["producer_id"])
    review_to_insert["consumer_id"] = ObjectId(review_to_insert["consumer_id"])

    result = review_for_consumer_collection.insert_one(review_to_insert)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting Reveiw for Consumer"
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
    
    # manually setting date_updated field to current datetime 
    review = review.dict()
    review["date_updated"] = datetime.utcnow()

    # finding and updating review_for_consumer
    updated_review = review_for_consumer_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": review },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )

    # checking if the review_for_consumer update was sucessful
    if updated_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Consumer to be updated not found with id " + id
        )

    # returning updated review 
    serialized_updated_review = review_for_consumer_serializer(updated_review)
    return serialized_updated_review


@review_for_consumer_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_for_consumer( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # deleting review_for_consumer if it exists with passed in id 
    deleted_review = review_for_consumer_collection.find_one_and_delete({ "_id": ObjectId(id) })
    if deleted_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Consumer to be deleted was not found with id " + id
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
