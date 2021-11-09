import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)

db = client.gkk
consumer_collection = db["consumer"]
deactivated_consumer_collection = db["deactivated_consumer"]

db2 = client.sample_training
grade_collection = db2["grades"]

