from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path
from pymongo import ReturnDocument
from bson import ObjectId
from datetime import datetime
from starlette.responses import Response

from app.config.database import archived_order_collection, active_order_collection 
from app.models.archived_order_model import archived_order_response
from app.schemas.archived_order_schema import archived_order_serializer, archived_orders_serializer

archived_order_router = APIRouter()


'''
    GET : /archived_order/{id}
'''

'''
    GET : /archived_order ? consumer_id="" & producer_id=""
'''