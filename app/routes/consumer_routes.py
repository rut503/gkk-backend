from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path
from pydantic.errors import TupleError
from pydantic.fields import T
from pydantic.utils import Obj, deep_update
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime

from pymongo.message import update
from config.database import consumer_collection, deactivated_consumer_collection
from models.consumer_model import consumer_in, consumer_response
from schemas.consumer_schema import consumer_serializer

consumer_router = APIRouter()

# get data
@consumer_router.get("/{id}", response_model=consumer_response)
async def get_consumer_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail=id + " is not a valid ObjectId type!")
    consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
    if consumer is None:
        raise HTTPException(status_code=404, detail="Consumer not found with id " + id)
    consumer = consumer_serializer(consumer)
    return consumer

@consumer_router.get("/phone_number/{phone_number}", response_model=consumer_response)
async def get_consumer_by_phone_number( phone_number: str = Path(..., min_length=10, max_length=15, regex="[0-9]{10,15}") ):
    consumer = consumer_collection.find_one({ "phone_number": phone_number })
    if consumer is None:
        raise HTTPException(status_code=404, detail="Consumer not found with phone number " + phone_number)
    consumer = consumer_serializer(consumer)
    return consumer


# post data
@consumer_router.post("/", response_model=consumer_response)
async def post_consumer(consumer: consumer_in):

    ######################################################
    # Check if consumer with phone_number already exists #
    ######################################################


    # manually setting required fields to their default values at consumer creation
    consumer = consumer.dict()
    consumer["rating"] = 0
    consumer["active_orders"] = []
    consumer["date_created"] = datetime.today()
    consumer["date_updated"] = datetime.today()

    # inserting the consumer into DB
    inserted_consumer = consumer_collection.insert_one(consumer)
    if not inserted_consumer.inserted_id:
        raise HTTPException(status_code=400, detail="Error while inserting")
    
    # finding that inserted consumer 
    inserted_consumer = consumer_collection.find_one({ "_id": inserted_consumer.inserted_id })
    inserted_consumer = consumer_serializer(inserted_consumer)
    
    # returning inserted consumer back
    return inserted_consumer


# put data
@consumer_router.put("/{id}", response_model=consumer_response)
async def put_consumer(id: str, consumer: consumer_in):
    # manually setting date_updated field to current datetime
    consumer = consumer.dict()
    consumer["date_updated"] = datetime.today()
    
    # finding and updating consumer 
    updated_consumer = consumer_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": consumer },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )
    updated_consumer = consumer_serializer(updated_consumer)
    
    # returning updated consumer
    return updated_consumer


# delete data
@consumer_router.delete("/{id}")
async def delete_consumer(id: str):
    moved_consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
    moved_consumer = deactivated_consumer_collection.insert_one(moved_consumer)
    if not moved_consumer.inserted_id:
        raise HTTPException(status_code=400, detail="Error while deactivating consumer")
    
    deleted_consumer = consumer_collection.delete_one({ "_id": ObjectId(id) })
    if deleted_consumer.deleted_count != 1:
        raise HTTPException(status_code=400, detail="Error while deleting consumer")

    return HTTPException(status_code=200, detail="Successfully deleted a consumer")
