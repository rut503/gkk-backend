from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path, Query
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime

from config.database import food_item_collection
from models.food_item_model import food_item_post, food_item_put, food_item_response
from schemas.food_item_schema import food_item_serializer, food_items_serializer

food_item_router = APIRouter()

'''
- path param
- query param
- HTTP Exceptions
- HTTP Codes
- Param Validations
'''

# get data
@food_item_router.get("/{id}", response_model=food_item_response)
async def get_food_item( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # finding food_item that matches passed in id
    food_item = food_item_collection.find_one({ "_id": ObjectId(id) })
    if food_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with id " + id
        )
    
    food_item = food_item_serializer(food_item)
    return food_item


@food_item_router.get("", response_model=List[food_item_response])
async def get_food_item_by_producer_id( producer_id: str = Query(..., min_length=24, max_length=24) ):
    # checking if passed in producer_id is valid ObjectId type
    if not ObjectId.is_valid(producer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=producer_id + " is not a valid ObjectId type!"
        )
    
    # finding all food_items that matches passed in producer_id
    food_items = food_item_collection.find({ "producer_id": ObjectId(producer_id) })
    if food_items.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Items not found with producer_id " + producer_id
        )
    
    food_items = food_items_serializer(food_items)
    return food_items


# post data
@food_item_router.post("/", response_model=food_item_response)
async def post_food_item(food_item: food_item_post):
    # manually setting required fields to their default values at food_item creation
    food_item = food_item.dict()
    food_item["rating"] = 0
    food_item["date_created"] = datetime.today()
    food_item["date_updated"] = datetime.today()

    # inserting the food_item into DB
    inserted_food_item = food_item_collection.insert_one(food_item)
    if not inserted_food_item.inserted_id:
        return "Error while inserting"
    
    # finding that inserted food_item 
    inserted_food_item = food_item_collection.find_one({ "_id": inserted_food_item.inserted_id })
    inserted_food_item = food_item_serializer(inserted_food_item)

    # returning inserted food_item back
    return inserted_food_item    


# put data
@food_item_router.put("/{id}", response_model=food_item_response)
async def put_food_item(id: str, food_item: food_item_put):
    # manually setting date_updated field to current datetime and rating to 0 since 
    #   we will remove all the ratings from this food_item if it's updated
    food_item = food_item.dict()
    food_item["rating"] = 0
    food_item["date_updated"] = datetime.today()

    # finding and updating food_item 
    updated_food_item = food_item_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": food_item },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )
    updated_food_item = food_item_serializer(updated_food_item)

    # returning updated food_item
    return updated_food_item


# # delete data
# @food_item_router.delete("/{id}")
# async def delete_food_item(id: str):
#     # moved_consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
#     # moved_consumer = deactivated_consumer_collection.insert_one(moved_consumer)
#     # if moved_consumer.inserted_id != ObjectId(id):
#     #     return "Error while deactivating consumer"
    
#     # deleted_consumer = consumer_collection.delete_one({ "_id": ObjectId(id) })
#     # if deleted_consumer.deleted_count != 1:
#     #     return "Error while deleting consumer"
    
#     return "Successfully deleted!"
