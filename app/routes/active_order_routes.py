from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from starlette.responses import Response

from app.config.database import active_order_collection, archived_order_collection
from app.models.active_order_model import active_order_response
from app.schemas.active_order_schema import active_order_serializer, active_orders_serializer

active_order_router = APIRouter()

'''
    GET : /active_order/{id}
    GET : /active_order ? consumer_id="" & producer_id=""
'''

@active_order_router.get("/{id}", response_model=active_order_response, status_code=status.HTTP_200_OK)
async def get_active_order_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # finding active_order that matches passed in id
    active_order = active_order_collection.find_one({ "_id": ObjectId(id) })
    if active_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Active Order not found with id " + id
        )
    serialized_active_order = active_order_serializer(active_order)
    return serialized_active_order