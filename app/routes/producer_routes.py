from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Query, Path
from models.producer_model import *
from config.database import producer_collection, deactivated_producer_collection
from schemas.producer_schema import producer_serializer


producer_router = APIRouter()

# Get a producer by id
@producer_router.get("/{id}", response_model=producer_response, response_model_exclude_none=True)
async def get_producer_by_id(id: str,
                             first_name: bool = True,
                             last_name: bool = True,
                             phone_number: bool = True,
                             address: bool = True,
                             food_items: bool = True,
                             rating: bool = True,
                             active_orders: bool = True,
                             menu: bool = True,
                             date_created: bool = True,
                             date_updated: bool = True):
    
    if not ObjectId.is_valid(id):
         raise HTTPException(status_code=404, detail=id + " is not a valid ObjectId type!")
    
    field_to_filter = filter_fields()
    field_to_filter.__setattr__('first_name', first_name)
    field_to_filter.__setattr__('last_name', last_name)
    field_to_filter.__setattr__('phone_number', phone_number)
    field_to_filter.__setattr__('address', address)
    field_to_filter.__setattr__('food_items', food_items)
    field_to_filter.__setattr__('rating', rating)
    field_to_filter.__setattr__('active_orders', active_orders)
    field_to_filter.__setattr__('menu', menu)
    field_to_filter.__setattr__('date_created', date_created)
    field_to_filter.__setattr__('date_updated', date_updated)
    
    # Creates a field_to_filter model 
    fields_to_filer_dict = field_to_filter.dict(exclude_defaults=True) 

    # Checks if any query parameters were sent in
    if len(fields_to_filer_dict) != 0: 
        producer_dict = producer_collection.find_one({"_id": ObjectId(id)}, fields_to_filer_dict)
        if producer_dict is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)

        return producer_serializer(producer_dict)

    else:
        producer_dict = producer_collection.find_one({"_id": ObjectId(id)})
        if producer_dict is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)
        
        return producer_serializer(producer_dict)

@producer_router.get("/phone_number/{phone_number_param}", response_model=producer_response, response_model_exclude_none=True)
async def get_producer_by_phone_number(phone_number_param: str = Path(..., min_length=10, max_length=15, regex="[0-9]{10,15}"),
                             first_name: bool = True,
                             last_name: bool = True,
                             phone_number: bool = True,
                             address: bool = True,
                             food_items: bool = True,
                             rating: bool = True,
                             active_orders: bool = True,
                             menu: bool = True,
                             date_created: bool = True,
                             date_updated: bool = True):
    
    field_to_filter = filter_fields()
    field_to_filter.__setattr__('first_name', first_name)
    field_to_filter.__setattr__('last_name', last_name)
    field_to_filter.__setattr__('phone_number', phone_number)
    field_to_filter.__setattr__('address', address)
    field_to_filter.__setattr__('food_items', food_items)
    field_to_filter.__setattr__('rating', rating)
    field_to_filter.__setattr__('active_orders', active_orders)
    field_to_filter.__setattr__('menu', menu)
    field_to_filter.__setattr__('date_created', date_created)
    field_to_filter.__setattr__('date_updated', date_updated)
    
    # Creates a field_to_filter model 
    fields_to_filer_dict = field_to_filter.dict(exclude_defaults=True) 

    # Checks if any query parameters were sent in
    if len(fields_to_filer_dict) != 0: 
        producer_dict = producer_collection.find_one({"phone_number": phone_number_param}, fields_to_filer_dict)
        if producer_dict is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)

        return producer_serializer(producer_dict)

    else:
        producer_dict = producer_collection.find_one({"phone_number": phone_number_param})
        if producer_dict is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)
        
        return producer_serializer(producer_dict)

# @producer_router.post("/", response_model=producer_response)
# async def post_producer(producer: producer_post):
#     producer_to_insert = producer_collection.insert_one({})