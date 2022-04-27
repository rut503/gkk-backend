from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path, Query
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from starlette.responses import Response

from config.database import active_order_collection, archived_order_collection, producer_collection, consumer_collection
from models.active_order_model import active_order_post, active_order_put, active_order_response
from schemas.active_order_schema import active_order_serializer, active_orders_serializer
from schemas.archived_order_schema import archived_order_serializer

active_order_router = APIRouter()


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


@active_order_router.get("", response_model=List[active_order_response], status_code=status.HTTP_200_OK)
async def get_all_active_orders_by_user(
    consumer_id: Optional[str] = Query(None, min_length=24, max_length=24),
    producer_id: Optional[str] = Query(None, min_length=24, max_length=24)
):
    find_order_query = {}

    # checking if consumer_id is passed in
    if consumer_id:
        # checking if consumer_id is valid ObjectId type
        if ObjectId.is_valid(consumer_id):
            find_order_query["consumer_id"] = ObjectId(consumer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=consumer_id + " consumer_id is not a valid ObjectId type!"
            )
    
    # checking if producer_id is passed in
    if producer_id:
        # checking if producer_id is valid ObjectId type
        if ObjectId.is_valid(producer_id):
            find_order_query["producer_id"] = ObjectId(producer_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=producer_id + " producer_id is not a valid ObjectId type!"
            )

    # checking if find_order_query has any value
    if find_order_query:
        active_order_document_cursor = active_order_collection.find(find_order_query)
        serialized_active_order_documents = active_orders_serializer(active_order_document_cursor)
        # checking if active_orders were not found
        if len(serialized_active_order_documents) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Active Order(s) not found with passed in id(s)"
            )
        return serialized_active_order_documents
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Need to pass in at least consumer_id and/or producer_id"
            )


@active_order_router.post("/", response_model=active_order_response, status_code=status.HTTP_201_CREATED)
async def post_active_order(order: active_order_post):
    # checking if passed in producer_id and consumer_id is valid ObjectId type
    if not ObjectId.is_valid(order.producer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=order.producer_id + " is not a valid ObjectId type for producer_id"
        )
    if not ObjectId.is_valid(order.consumer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=order.consumer_id + " is not a valid ObjectId type for consumer_id"
        )
    
    # converting producer_id and consumer_id to ObjectId type
    producer_id = ObjectId(order.producer_id)
    consumer_id = ObjectId(order.consumer_id)
    
    # checking if the prodcuer and consumer exists with their passed in ids 
    producer_count = producer_collection.count_documents({ "_id": producer_id })
    if producer_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer not found with id " + order.producer_id
        )
    consumer_count = consumer_collection.count_documents({ "_id": consumer_id })
    if consumer_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer not found with id " + order.consumer_id
        )

    # calculating total price of order based on quantity and price of item(s)
    total_price = 0
    for item in order.items:
        total_price += (item.price * item.quantity)
    
    # checking if total_price is between allowed values
    if total_price < 0.01 or total_price > 999.99:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Total order price " + str(total_price) + " is not between $0.01 and $999.99"
        )

    # converting order model to dictionary for insert and setting updated and created dates and status
    order_to_insert = order.dict()
    order_to_insert["status"] = "pending"
    order_to_insert["total_price"] = total_price
    order_to_insert["date_updated"] = datetime.utcnow()
    order_to_insert["date_created"] = datetime.utcnow()
    
    # setting producer_id and consumer_id fields to their value converted to ObjectId type
    order_to_insert["producer_id"] = producer_id
    order_to_insert["consumer_id"] = consumer_id

    result = active_order_collection.insert_one(order_to_insert)
    active_order_id = result.inserted_id
    if not active_order_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error while inserting Active Order"
        )
    # Retrieving newly added document
    inserted_order = active_order_collection.find_one({ "_id": active_order_id })
    if inserted_order is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Can't find order after inserting into active order with id " + active_order_id
        )
    
    # update producer's active_orders array field with new active_order id pushed into it
    updated_producer = producer_collection.update_one(
        { "_id": producer_id },
        { "$push": { "active_orders": active_order_id } }
    )
    # checking if the producer update was sucessful
    if updated_producer.modified_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producer to be updated with id " + producer_id + " didn't update."
        )
    
    # update consumer's active_orders array field with new active_order id pushed into it
    updated_consumer = consumer_collection.update_one(
        { "_id": consumer_id },
        { "$push": { "active_orders": active_order_id } }
    )
    # checking if the consumer update was sucessful
    if updated_consumer.modified_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Consumer to be updated with id " + consumer_id + " didn't update."
        )

    return active_order_serializer(inserted_order)


@active_order_router.put("/{id}", response_model=active_order_response, status_code=status.HTTP_200_OK)
async def update_review_for_consumer( *, id: str = Path(..., min_length=24, max_length=24), order: active_order_put ):
    # checking if passed in id is valid ObjectId type
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=id + " is not a valid ObjectId type!"
        )

    if order.status == "pending" or order.status == "accepted" or order.status == "ready":
        # manually setting date_updated field to current datetime 
        order_to_update = order.dict()
        order_to_update["date_updated"] = datetime.utcnow()

        # finding and updating review_for_consumer
        updated_order = active_order_collection.find_one_and_update(
            { "_id": ObjectId(id) },
            { "$set": order_to_update },
            return_document=ReturnDocument.AFTER    # this will return updated document after update happens 
        )

        # checking if the active_order update was sucessful
        if updated_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Active Order to be updated not found with id " + id
            )

        # returning updated order 
        return active_order_serializer(updated_order)
    
    elif order.status == "completed" or order.status == "cancelled_by_consumer" or order.status == "cancelled_by_producer":
        order_id = ObjectId(id)

        # checking if the order exists with passed in id
        active_order = active_order_collection.find_one({ "_id": order_id })
        if active_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Active Order not found with id " + id
            )
        
        producer_id = active_order["producer_id"]
        consumer_id = active_order["consumer_id"]
        
        # updating order with new status and updated date
        active_order["status"] = order.status
        active_order["date_updated"] = datetime.utcnow()

        # inserting order from active_order collection to archived_order collection
        archived_order = archived_order_collection.insert_one(active_order)
        if not archived_order.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error while moving active order to archived order"
            )
        
        # finding archived_order that was inseted 
        archived_order = archived_order_collection.find_one({ "_id": order_id })
        if archived_order is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Can't find order after inserting into archived order with id " + id
            )
        
        # deleting order from active order collection
        result = active_order_collection.delete_one({ "_id": order_id })
        if result.deleted_count != 1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error while removing order from active order with id " + id
            )

        # update producer's active_orders array field by removing active_order_id 
        updated_producer = producer_collection.update_one(
            { "_id": producer_id },
            { "$pull": { "active_orders": order_id } }
        )
        # checking if the producer update was sucessful
        if updated_producer.modified_count != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Producer to be updated with id " + producer_id + " didn't update."
            )
        
        # update consumer's active_orders array field by removing active_order_id 
        updated_consumer = consumer_collection.update_one(
            { "_id": consumer_id },
            { "$pull": { "active_orders": order_id } }
        )
        # checking if the consumer update was sucessful
        if updated_consumer.modified_count != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Consumer to be updated with id " + consumer_id + " didn't update."
            )
        
        # returning archived order
        return archived_order_serializer(archived_order)
    
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Status of '" + order.status + "' is not allowed"
            )