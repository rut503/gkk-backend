from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path, Query
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from starlette.responses import Response

from app.config.database import food_item_collection, producer_collection, review_for_food_item_collection
from app.models.food_item_model import food_item_post, food_item_put, food_item_response
from app.schemas.food_item_schema import food_item_serializer, food_items_serializer

food_item_router = APIRouter()


# get data
@food_item_router.get("/{id}", response_model=food_item_response, status_code=status.HTTP_200_OK)
async def get_food_item( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type"
        )
    
    # finding food_item that matches passed in id
    food_item = food_item_collection.find_one({ "_id": ObjectId(id) })
    if food_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Item not found with id " + id
        )
    
    food_item = food_item_serializer(food_item)
    return food_item


@food_item_router.get("", response_model=List[food_item_response], status_code=status.HTTP_200_OK)
async def get_food_item_by_producer_id( producer_id: str = Query(..., min_length=24, max_length=24) ):
    # checking if passed in producer_id is valid ObjectId type
    if not ObjectId.is_valid(producer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=producer_id + " is not a valid ObjectId type"
        )
    
    # finding all food_items that matches passed in producer_id
    food_items = food_item_collection.find({ "producer_id": ObjectId(producer_id) })
    food_items = food_items_serializer(food_items)

    # checking if any food_items were not found
    if len(food_items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Items not found with producer_id " + producer_id
        )
    return food_items


# post data
@food_item_router.post("/", response_model=food_item_response, status_code=status.HTTP_201_CREATED)
async def post_food_item(food_item: food_item_post):
    # checking if passed in producer_id is valid ObjectId type
    if not ObjectId.is_valid(food_item.producer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=food_item.producer_id + " is not a valid ObjectId type for producer_id"
        )
    
    # checking if the producer with the passed in producer_id exists
    producer = producer_collection.find_one({ "_id": ObjectId(food_item.producer_id) })
    if producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer not found with id " + food_item.producer_id
        )
    
    # manually setting required fields to their default values at food_item creation
    food_item = food_item.dict()
    food_item["rating"] = 0
    food_item["date_updated"] = datetime.utcnow()
    food_item["date_created"] = datetime.utcnow()

    # converting id type from sting to ObjectId for database
    producer_id_object_id = ObjectId(food_item["producer_id"])
    food_item["producer_id"] = producer_id_object_id

    #############################################################################
    # TODO: Do something about photo upload here and get the URL to store in DB #
    #############################################################################
    food_item["photo"] = "https://www.photos.com/path"

    # inserting the food_item into DB
    inserted_food_item = food_item_collection.insert_one(food_item)
    inserted_food_item_id = inserted_food_item.inserted_id
    if not inserted_food_item_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting Food Item"
        )
    
    # update producer's food_items array field with new food_item id pushed into it
    updated_producer = producer_collection.find_one_and_update(
        { "_id": producer_id_object_id },
        { "$push": { "food_items": inserted_food_item_id } },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )

    # checking if the producer update was sucessful
    if updated_producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer to be updated not found with id " + id
        )
    
    # finding that inserted food_item 
    inserted_food_item = food_item_collection.find_one({ "_id": inserted_food_item.inserted_id })
    if inserted_food_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="After inserting, Food Item not found with id " + inserted_food_item.inserted_id
        )
    inserted_food_item = food_item_serializer(inserted_food_item)

    # returning inserted food_item back
    return inserted_food_item    



# put data
@food_item_router.put("/{id}", response_model=food_item_response, status_code=status.HTTP_200_OK)
async def put_food_item( *, id: str = Path(..., min_length=24, max_length=24), food_item: food_item_put ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # manually setting date_updated field to current datetime and rating to 0 since 
    #   we will remove all the ratings from this food_item if it's updated
    food_item = food_item.dict()
    food_item["rating"] = 0
    food_item["date_updated"] = datetime.utcnow()

    #############################################################################
    # TODO: Do something about photo upload here and get the URL to store in DB #
    #############################################################################

    # finding and updating food_item 
    updated_food_item = food_item_collection.find_one_and_update(
        { "_id": ObjectId(id) },
        { "$set": food_item },
        return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
    )

    # checking if the food_item update was sucessful
    if updated_food_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Item to be updated not found with id " + id
        )
    updated_food_item = food_item_serializer(updated_food_item)

    # cascade delete all the reviews for food item since food_item was updated
    review_for_food_item_collection.delete_many({ "food_item_id": ObjectId(id)})

    # returning updated food_item
    return updated_food_item


# delete data
@food_item_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # checking if the food_item exists with passed in id
    food_item = food_item_collection.find_one_and_delete({ "_id": ObjectId(id) })
    if food_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food Item to be deleted was not found with id " + id
        )

    # cascade deleting all the reviews that are associated with deleted food_item
    review_for_food_item_collection.delete_many({ "food_item_id": ObjectId(id)})

    # remove food_item id that was deleted from food_items field and menu.*.* fields in producer
    producer_collection.update_one(
        { "food_items": ObjectId(id) },
        { "$pull": { 
            "food_items": ObjectId(id),

            "menu.sunday.breakfast": ObjectId(id),
            "menu.sunday.lunch": ObjectId(id),
            "menu.sunday.dinner": ObjectId(id),

            "menu.monday.breakfast": ObjectId(id),
            "menu.monday.lunch": ObjectId(id),
            "menu.monday.dinner": ObjectId(id),

            "menu.tuesday.breakfast": ObjectId(id),
            "menu.tuesday.lunch": ObjectId(id),
            "menu.tuesday.dinner": ObjectId(id),

            "menu.wednesday.breakfast": ObjectId(id),
            "menu.wednesday.lunch": ObjectId(id),
            "menu.wednesday.dinner": ObjectId(id),

            "menu.thursday.breakfast": ObjectId(id),
            "menu.thursday.lunch": ObjectId(id),
            "menu.thursday.dinner": ObjectId(id),

            "menu.friday.breakfast": ObjectId(id),
            "menu.friday.lunch": ObjectId(id),
            "menu.friday.dinner": ObjectId(id),

            "menu.saturday.breakfast": ObjectId(id),
            "menu.saturday.lunch": ObjectId(id),
            "menu.saturday.dinner": ObjectId(id),
        }}
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
