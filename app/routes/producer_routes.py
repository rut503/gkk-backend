from logging import raiseExceptions
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from fastapi.params import Query, Path
from pymongo.collection import ReturnDocument
from starlette.responses import Response
from models.producer_model import *
from config.database import *
from schemas.producer_schema import producer_serializer


producer_router = APIRouter()

@producer_router.get("/{id}", response_model=producer_response)
async def get_producer_by_id(id: str = Path(..., min_length=24, max_length=24),
                             fields: List[str] = Query(None)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail=id + " is not a valid ObjectId type!"
        )
    
    if fields is not None:
        fields_to_return = {key: 1 for key in fields}
        producer = producer_collection.find_one({"_id": ObjectId(id)}, fields_to_return)
    else:
        producer = producer_collection.find_one({"_id": ObjectId(id)})
    

    # Checks if any query parameters were sent in    
    if producer is None:
        raise HTTPException(
            status_code=404,
            detail="Producer not found with id " + id
        )

    return producer_serializer(producer)

# Get call with phone number
@producer_router.get("/phone_number/{phone_number_param}", response_model=producer_response)
async def get_producer_by_phone_number(phone_number_param: str = Path(..., min_length=10, max_length=15, regex="[0-9]{10,15}"),
                            fields: List[str] = Query(None)):
    
    if fields is not None:
        fields_to_return = {key: 1 for key in fields}
        producer = producer_collection.find_one({"phone_number": phone_number_param}, fields_to_return)
    else:
        producer = producer_collection.find_one({"phone_number": phone_number_param})
    

    # Checks if any query parameters were sent in    
    if producer is None:
        raise HTTPException(
            status_code=404,
            detail="Producer not found with phone number of " + phone_number_param
        )

    return producer_serializer(producer)

# post call
@producer_router.post("/", response_model=producer_response)
async def post_producer(producer: producer_post):
    # Checking if the phone number is already associated with a producer
    producer_document = producer_collection.find_one({"phone_number": producer.dict()["phone_number"]})
    if producer_document:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT , 
            detail="Proudcer already exists with phone number, " + producer_document["phone_number"]
        )

    # Creating dict for producer to be inserted
    producer_dict = producer.dict()
    producer_dict["food_items"] = []
    producer_dict["rating"] = float(0)
    producer_dict["active_orders"] = []
    producer_dict["menu"] = menuDict
    producer_dict["date_created"] = datetime.utcnow()
    producer_dict["date_updated"] = datetime.utcnow()    

    # Inserting new producer
    insert_result = producer_collection.insert_one(producer_dict)
    if not insert_result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting"
        )
    
    # Returning new producer
    inserted_producer = producer_collection.find_one({"_id": insert_result.inserted_id})
    
    if inserted_producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="After inserting, Producer not found with id " + insert_result.inserted_id
        )
    inserted_producer = producer_serializer(inserted_producer)

    return inserted_producer

# put operation for first_name, last_name, phone_number and address
@producer_router.put("/{id}/address", response_model=producer_response, response_model_exclude=["rating", "active_orders","food_items", "menu", "date_created", "date_updated"])
async def put_producer_address(*, id: str = Path(..., min_length=24, max_length=24), producer: producer_post):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # Preparing dict for update
    producer = producer.dict()
    producer["date_updated"] = datetime.utcnow()

    updated_producer = producer_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {'$set': producer},
        return_document=ReturnDocument.AFTER
    )

     # checking if the producer update was sucessful
    if updated_producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer to be updated not found with id " + id
        )

    updated_producer = producer_serializer(updated_producer)

    return updated_producer

# Put operation for menu
@producer_router.put("/{id}/menu/{day}/{meal_type}", response_model=producer_response, response_model_exclude=["first_name", "last_name", "phone_number", "address", "rating", "active_orders","food_items", "date_created", "date_updated"])
async def put_producer_menu_items(*, id: str = Path(..., min_length=24, max_length=24), day: day, meal_type: meal_type, meal_doc: meal_array_put):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    meal_subdoc = "menu." + day + "." + meal_type
    
    producer = producer_collection.find_one({"_id": ObjectId(id)}, {meal_subdoc: 1})
    current_food_array = producer["menu"][day][meal_type]

    # Creating new subdocument
    for food_item in meal_doc.food_array:
        current_food_array.append(ObjectId(food_item))
    
    updated_subdoc = producer_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": 
            {
             meal_subdoc: current_food_array,
             "date_updated": datetime.utcnow(),
            }
        },return_document=ReturnDocument.AFTER
    )

    if updated_subdoc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer to be updated not found with id " + id
        )
    updated_subdoc = producer_serializer(updated_subdoc)

    return updated_subdoc

# Remove one menu id
@producer_router.put("/{id}/menu/{day}/{meal_type}/{menu_id}", status_code=200, response_model=producer_response, response_model_exclude=["first_name", "last_name", "phone_number", "address", "rating", "active_orders","food_items", "date_created", "date_updated"])
async def delete_producer_menu_items(*, id: str = Path(..., min_length=24, max_length=24), day: day, meal_type: meal_type, menu_id: str):
    # Checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # Checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(menu_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=menu_id + " is not a valid ObjectId type!"
        )

    # Checking if the producer exists with passed in id
    producer = producer_collection.find_one({ "_id": ObjectId(id) })
    if producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer not found with id " + id
        )
    meal_subdoc = "menu." + day + "." + meal_type
    
    # Checking for food id in producers menu array
    if ObjectId(menu_id) not in producer["menu"][day][meal_type]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food item with id of " + menu_id + " not found in " + day + "'s " + meal_type + " array"
        )

    # Pulling Food id from respective array
    producer_updated = producer_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$pull": 
            {meal_subdoc: 
                ObjectId(menu_id)
            }
        },
        return_document=ReturnDocument.AFTER
    )

    # Producer check
    if producer_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer to be updated not found with id " + id
        )
    producer_updated = producer_serializer(producer_updated)

    return producer_updated

# Delete via id
@producer_router.delete("/{id}",  status_code=200)
async def delete_producer_by_id(id: str):
    # Checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    # Checking if the producer exists with passed in id
    active_producer = producer_collection.find_one({ "_id": ObjectId(id) })
    if active_producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer not found with id " + id
        )

    # Setting fields we don't want to archive to empty
    active_producer["food_items"] = []
    active_producer["menu"] = {}

    # Cancelling active order
    

    # Archiving producer data from producer collection to deactivated_producer collection
    deactive_producer = deactivated_producer_collection.insert_one(active_producer)
    if not deactive_producer.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while deactivating producer"
        )

    # Deleting the consumer from consumer collection 
    deleted_producer = producer_collection.delete_one({ "_id": ObjectId(id) })
    if deleted_producer.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while deleting producer"
        )

    # Deleting associated documents
    food_item_collection.delete_many({"producer_id": ObjectId(id)})
    review_for_consumer_collection.delete_many({ "producer_id": ObjectId(id)})
    review_for_producer_collection.delete_many({ "producer_id": ObjectId(id)})
    review_for_food_item_collection.delete_many({ "producer_id": ObjectId(id)})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
####################################################################################################################################################################################
# 
#                                                                                       Helper Dicts for menu subdocument
#
####################################################################################################################################################################################
mealDict = {'breakfast': [],
            'lunch': [],
            'dinner': []}

menuDict = {'sunday': mealDict,
            'monday': mealDict,
            'tuesday': mealDict,
            'wednesday': mealDict,
            'thursday': mealDict,
            'friday': mealDict,
            'saturday': mealDict}

