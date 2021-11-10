import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)

db = client.gkk

consumer_collection = db["consumer"]
producer_collection = db["producer"]

deactivated_consumer_collection = db["deactivated_consumer"]
deactivated_producer_collection = db["deactivated_producer"]

food_item_collection = db["food_item"]

active_order_collection = db["active_order"]
archived_order_collection = db["archived_order"]

review_for_consumer_collection = db["review_for_consumer"]
review_for_producer_collection = db["review_for_producer"]
review_for_food_item_collection = db["review_for_food_item"]
