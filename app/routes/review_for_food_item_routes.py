from typing import Optional, List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.params import Path, Query
from starlette import status
from datetime import datetime
from pymongo import ReturnDocument
from starlette.responses import Response

from app.models.review_for_food_item_model import review_for_food_item_post, review_for_food_item_put, review_for_food_item_response
from app.config.database import review_for_food_item_collection, consumer_collection
from app.schemas.review_for_food_item_schema import review_for_food_item_serializer, reviews_for_food_item_serializer

review_for_food_item_router = APIRouter()
