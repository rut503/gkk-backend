from typing import Optional
from fastapi import APIRouter
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from config.database import consumer_collection, deactivated_consumer_collection
from models.consumer_model import consumer_in, consumer_out
from schemas.consumer_schema import consumer_serializer, consumers_serializer

consumer_router = APIRouter()

# get data
@consumer_router.get("/", response_model=consumer_out)
async def get_consumer_by_phone_num(id: Optional[str] = None, phone_number: Optional[str] = None):
    if id:
        consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
        consumer = consumer_serializer(consumer)
        return consumer
    elif phone_number:
        consumer = consumer_collection.find_one({ "phone_number": phone_number })
        consumer = consumer_serializer(consumer)
        return consumer
    else:
        return "error bro!"


# post data
@consumer_router.post("/", response_model=consumer_out)
async def post_consumer(consumer: consumer_in):
    # manually setting required fields to their default values at consumer creation
    consumer = consumer.dict()
    consumer["rating"] = 0
    consumer["active_orders"] = []
    consumer["archived_orders"] = []
    consumer["date_created"] = datetime.today()
    consumer["date_updated"] = datetime.today()

    # inserting the consumer into DB
    inserted_consumer = consumer_collection.insert_one(consumer)
    if not inserted_consumer.inserted_id:
        return "Error while inserting"
    
    # finding that inserted consumer 
    inserted_consumer = consumer_collection.find_one({ "_id": inserted_consumer.inserted_id })
    inserted_consumer = consumer_serializer(inserted_consumer)
    
    # returning inserted consumer back
    return inserted_consumer


# put data
@consumer_router.put("/{id}", response_model=consumer_out)
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
    if moved_consumer.inserted_id != ObjectId(id):
        return "Error while deactivating consumer"
    
    deleted_consumer = consumer_collection.delete_one({ "_id": ObjectId(id) })
    if deleted_consumer.deleted_count != 1:
        return "Error while deleting consumer"
    
    return "Successfully deleted!"
