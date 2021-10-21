import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)
db = client.sample_training
grade_collection = db["grades"]
