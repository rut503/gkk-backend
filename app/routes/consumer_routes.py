from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from starlette.responses import Response

from app.config.database import ( 
    consumer_collection, 
    deactivated_consumer_collection, 
    review_for_consumer_collection, 
    review_for_producer_collection, 
    review_for_food_item_collection
)
from app.models.consumer_model import consumer_post, consumer_put, consumer_response
from app.schemas.consumer_schema import consumer_serializer

consumer_router = APIRouter()

# get data
@consumer_router.get("/{id}", response_model=consumer_response, status_code=status.HTTP_200_OK)
async def get_consumer_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # finding consumer that matches passed in id
    consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
    if consumer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with id " + id
        )
    consumer = consumer_serializer(consumer)
    return consumer

@consumer_router.get("/phone_number/{phone_number}", response_model=consumer_response, status_code=status.HTTP_200_OK)
async def get_consumer_by_phone_number( phone_number: str = Path(..., min_length=10, max_length=15, regex="[0-9]{10,15}") ):
    # finding consumer that matches passed in phone_number
    consumer = consumer_collection.find_one({ "phone_number": phone_number })
    if consumer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with phone number " + phone_number
        )
    consumer = consumer_serializer(consumer)
    return consumer


# post data
@consumer_router.post("/", response_model=consumer_response, status_code=status.HTTP_201_CREATED)
async def post_consumer(consumer: consumer_post):
    # checking if consumer with phone_number already exists 
    existing_consumer = consumer_collection.find_one({ "phone_number": consumer.phone_number })
    if existing_consumer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Consumer with phone number " + consumer.phone_number + " already exists"
        )

    # manually setting required fields to their default values at consumer creation
    consumer = consumer.dict()
    consumer["rating"] = 0
    consumer["active_orders"] = []
    consumer["date_created"] = datetime.utcnow()
    consumer["date_updated"] = datetime.utcnow()

    #############################################################################
    # TODO: Do something about photo upload here and get the URL to store in DB #
    #############################################################################

    # inserting the consumer into DB
    inserted_consumer = consumer_collection.insert_one(consumer)
    if not inserted_consumer.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting"
        )
    
    # finding that inserted consumer 
    inserted_consumer = consumer_collection.find_one({ "_id": inserted_consumer.inserted_id })
    if inserted_consumer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="After inserting, Consumer not found with id " + inserted_consumer.inserted_id
        )
    inserted_consumer = consumer_serializer(inserted_consumer)
    
    # returning inserted consumer back
    return inserted_consumer


# put data
@consumer_router.put("/{id}", response_model=consumer_response, status_code=status.HTTP_200_OK)
async def put_consumer( *, id: str = Path(..., min_length=24, max_length=24), consumer: consumer_put ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # manually setting date_updated field to current datetime
    consumer = consumer.dict()
    consumer["date_updated"] = datetime.utcnow()

    #############################################################################
    # TODO: Do something about photo upload here and get the URL to store in DB #
    #############################################################################
    
    # finding and updating consumer 
    updated_consumer = consumer_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": consumer },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )

    # checking if the consumer update was sucessful
    if updated_consumer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer to be updated not found with id " + id
        )
    updated_consumer = consumer_serializer(updated_consumer)
    
    # returning updated consumer
    return updated_consumer


# delete data
@consumer_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consumer(id: str = Path(..., min_length=24, max_length=24)):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # checking if the consumer exists with passed in id
    moved_consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
    if moved_consumer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with id " + id
        )
    
    # adding consumer data from consumer collection to deactivated_consumer collection
    moved_consumer = deactivated_consumer_collection.insert_one(moved_consumer)
    if not moved_consumer.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while deactivating consumer"
        )
    
    # deleting the consumer from consumer collection 
    deleted_consumer = consumer_collection.delete_one({ "_id": ObjectId(id) })
    if deleted_consumer.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while deleting consumer"
        )

    # cascade deleting all the reviews that are associated with deleted consumer
    review_for_consumer_collection.delete_many({ "consumer_id": ObjectId(id)})
    review_for_producer_collection.delete_many({ "consumer_id": ObjectId(id)})
    review_for_food_item_collection.delete_many({ "consumer_id": ObjectId(id)})

    return Response(status_code=status.HTTP_204_NO_CONTENT)
