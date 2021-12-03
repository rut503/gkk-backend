import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)

# from urllib.parse import quote_plus
# uri = "mongodb://%s:%s@%s" % ( quote_plus(user), quote_plus(password), host)
# client = MongoClient(uri)

# from pymongo.errors import ConnectionFailure
# client = MongoClient()
# try:
#     # The ping command is cheap and does not require auth.
#     client.admin.command('ping')
# except ConnectionFailure:
#     print("Server not available")

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
