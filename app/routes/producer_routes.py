from typing import Optional
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Query
from config.database import producer_collection, deactivated_producer_collection
from models.producer_model import address as address_model, filter_fields
from schemas.producer_schema import producer_serializer


producer_router = APIRouter()

# Get a producer by id
@producer_router.get("/{id}")
async def get_producer_by_id(id: str, 
                             address: Optional[bool] = None,
                             food_items: Optional[bool] = None,
                             active_order: Optional[bool] = None,
                             menu: Optional[bool] = None):
    field_to_filter = filter_fields()
    field_to_filter.__setattr__('address', address)
    field_to_filter.__setattr__('food_items', food_items)
    field_to_filter.__setattr__('active_orders', active_order)
    field_to_filter.__setattr__('menu', menu)
    
    # Creates a field_to_filter model 
    fields_to_filer_dict = field_to_filter.dict(exclude_defaults=True) 

    if not ObjectId.is_valid(id):
         raise HTTPException(status_code=404, detail=id + " is not a valid ObjectId type!")

    print(fields_to_filer_dict)

    # Checks if any query parameters were sent in
    if len(fields_to_filer_dict) != 0: 
        producer = producer_collection.find_one({"_id": ObjectId(id)}, fields_to_filer_dict)
        if producer is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)

        producer["id"] = str(producer["_id"])
        del producer["_id"]

        return producer
    else:
        producer = producer_collection.find_one({"_id": ObjectId(id)})
        if producer is None:
            raise HTTPException(status_code=404, detail="Consumer not found with id " + id)

        return producer
    
    