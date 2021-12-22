from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path, Query
from bson import ObjectId

from app.config.database import archived_order_collection
from app.models.archived_order_model import archived_order_response
from app.schemas.archived_order_schema import archived_order_serializer, archived_orders_serializer

archived_order_router = APIRouter()


@archived_order_router.get("/{id}", response_model=archived_order_response, status_code=status.HTTP_200_OK)
async def get_archived_order_by_id( id: str = Path(..., min_length=24, max_length=24) ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )
    
    # finding archived_order that matches passed in id
    archived_order = archived_order_collection.find_one({ "_id": ObjectId(id) })
    if archived_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Archived Order not found with id " + id
        )
    serialized_archived_order = archived_order_serializer(archived_order)
    return serialized_archived_order


@archived_order_router.get("", response_model=List[archived_order_response], status_code=status.HTTP_200_OK)
async def get_all_archived_orders_by_user(
    consumer_id: Optional[str] = Query(None, min_length=24, max_length=24),
    producer_id: Optional[str] = Query(None, min_length=24, max_length=24)
):
    find_archived_order_query = {}

    # checking if consumer_id is passed in
    if consumer_id:
        # checking if consumer_id is valid ObjectId type
        if ObjectId.is_valid(consumer_id):
            find_archived_order_query["consumer_id"] = ObjectId(consumer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=consumer_id + " consumer_id is not a valid ObjectId type!"
            )
    
    # checking if producer_id is passed in
    if producer_id:
        # checking if producer_id is valid ObjectId type
        if ObjectId.is_valid(producer_id):
            find_archived_order_query["producer_id"] = ObjectId(producer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=producer_id + " producer_id is not a valid ObjectId type!"
            )

    # checking if find_archived_order_query has any value
    if find_archived_order_query:
        archived_order_document_cursor = archived_order_collection.find(find_archived_order_query)
        serialized_archived_order_documents = archived_orders_serializer(archived_order_document_cursor)
        # checking if archived_orders were not found
        if len(serialized_archived_order_documents) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Archived Order(s) not found with passed in id(s)"
            )
        return serialized_archived_order_documents
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Need to pass in at least consumer_id and/or producer_id"
            )
