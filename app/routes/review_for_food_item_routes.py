from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Path, Query
from starlette import status
from datetime import datetime
from pymongo import ReturnDocument
from starlette.responses import Response

from app.models.review_for_food_item_model import review_for_food_item_post, review_for_food_item_put, review_for_food_item_response
from app.config.database import review_for_food_item_collection, consumer_collection, food_item_collection
from app.schemas.review_for_food_item_schema import review_for_food_item_serializer, reviews_for_food_item_serializer

review_for_food_item_router = APIRouter()


@review_for_food_item_router.get("/{id}", response_model=review_for_food_item_response, status_code=status.HTTP_200_OK)
async def get_review_for_food_item_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # finding review_for_food_item that matches passed in id
    review_document_returned = review_for_food_item_collection.find_one({ "_id": ObjectId(id) })
    if review_document_returned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Food Item not found with review id " + id
        )
    serialized_review_document = review_for_food_item_serializer(review_document_returned)
    return serialized_review_document


@review_for_food_item_router.get("", response_model=List[review_for_food_item_response], status_code=status.HTTP_200_OK)
async def get_all_review_for_food_item_by_user(
    consumer_id: Optional[str] = Query(None, min_length=24, max_length=24),
    food_item_id: Optional[str] = Query(None, min_length=24, max_length=24)
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
    
    # checking if food_item_id is passed in
    if food_item_id:
        # checking if food_item_id is valid ObjectId type
        if ObjectId.is_valid(food_item_id):
            find_review_query["food_item_id"] = ObjectId(food_item_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=food_item_id + " food_item_id is not a valid ObjectId type!"
            )

    # checking if find_review_query has any value
    if find_review_query:
        review_document_cursor = review_for_food_item_collection.find(find_review_query)
        serialized_review_documents = reviews_for_food_item_serializer(review_document_cursor)
        # checking if review_for_food_item were not found
        if len(serialized_review_documents) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Review for Food Item not found with passed in id(s)"
            )
        return serialized_review_documents
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Need to pass in at least consumer_id and/or food_item_id"
            )


@review_for_food_item_router.post("/", response_model=review_for_food_item_response, status_code=status.HTTP_201_CREATED)
async def post_review_for_food_item(review: review_for_food_item_post):
    # checking if passed in food_item_id and consumer_id is valid ObjectId type
    if not ObjectId.is_valid(review.food_item_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=review.food_item_id + " is not a valid ObjectId type for food_item_id"
        )
    if not ObjectId.is_valid(review.consumer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=review.consumer_id + " is not a valid ObjectId type for consumer_id"
        )
    
    # checking if the food_item and consumer exists with their passed in ids 
    food_item_count = food_item_collection.count_documents({ "_id": ObjectId(review.food_item_id) })
    if food_item_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Item not found with id " + review.food_item_id
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
    review_to_insert["food_item_id"] = ObjectId(review_to_insert["food_item_id"])
    review_to_insert["consumer_id"] = ObjectId(review_to_insert["consumer_id"])

    result = review_for_food_item_collection.insert_one(review_to_insert)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting Review for Food Item"
        )

    # Retrieving newly added document
    inserted_review = review_for_food_item_collection.find_one({ "_id": result.inserted_id })
    inserted_review = review_for_food_item_serializer(inserted_review)
    return inserted_review


@review_for_food_item_router.put("/{id}", response_model=review_for_food_item_response, status_code=status.HTTP_200_OK)
async def update_review_for_food_item( *, id: str = Path(..., min_length=24, max_length=24), review: review_for_food_item_put ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # manually setting date_updated field to current datetime 
    review = review.dict()
    review["date_updated"] = datetime.utcnow()

    # finding and updating review_for_food_item
    updated_review = review_for_food_item_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": review },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )

    # checking if the review_for_food_item update was sucessful
    if updated_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Food Item to be updated not found with id " + id
        )

    # returning updated review 
    serialized_updated_review = review_for_food_item_serializer(updated_review)
    return serialized_updated_review


@review_for_food_item_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_for_food_item( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # deleting review_for_food_item if it exists with passed in id 
    deleted_review = review_for_food_item_collection.find_one_and_delete({ "_id": ObjectId(id) })
    if deleted_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review for Food Item to be deleted was not found with id " + id
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
