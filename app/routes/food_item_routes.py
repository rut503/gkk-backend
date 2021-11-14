from os import device_encoding
from typing import List, Optional
from fastapi import APIRouter
from pydantic.utils import Obj
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime

from pymongo.message import update

from config.database import food_item_collection
from models.food_item_model import food_item_in, food_item_out
from schemas.food_item_schema import food_item_serializer, food_items_serializer

food_item_router = APIRouter()

# get data
@food_item_router.get("/", response_model=food_item_out)
async def get_food_item(id: str):
    food_item = food_item_collection.find_one({ "_id": ObjectId(id) })
    food_item = food_item_serializer(food_item)
    return food_item

"""
- time = [ "breakfast", "lunch", "dinner" ] (3 values, list)
- diet_preference = [ "Low Carb",      "High Protein", 
                        "Low/No Sodium", "Diabetic", 
                        "Gluten Free",   "Lactose Free", 
                        "Vegetarian",    "Non-Vegetarian", 
                        "Paleo",         "Vegan", 
                        "Pescetarian",   "Eggitarian", 
                        "Nut Free",      "Other" 
                    ] (14 values, list)
- min_price = 4.99 ($, float)
- max_price = 14.99 ($, float)
- consumer_coordinates = _____
- distance_radius = 8 (miles, float)
- ratings = 4 (stars, int)
- spicy_level = 3 (pepers, int)
- chef_name = "ritu shah" (chef, str)
"""
@food_item_router.get("/filter/", response_model=List[food_item_out])
async def get_food_item_by_filters( 
                                  ):
    return []
# @consumer_router.get("/", response_model=consumer_out)
# async def get_consumer_by_phone_num(id: Optional[str] = None, phone_num: Optional[str] = None):
#     if id:
#         consumer = consumer_collection.find_one({ "_id": ObjectId(id) })
#         consumer = consumer_serializer(consumer)
#         return consumer
#     elif phone_num:
#         consumer = consumer_collection.find_one({ "phone_num": phone_num })
#         consumer = consumer_serializer(consumer)
#         return consumer
#     else:
#         return "error bro!"


# post data
@food_item_router.post("/", response_model=food_item_out)
async def post_food_item(food_item: food_item_in):
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
@food_item_router.put("/{id}", response_model=food_item_out)
async def put_food_item(id: str, food_item: food_item_in):
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
