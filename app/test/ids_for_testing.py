from datetime import date, datetime
from bson.objectid import ObjectId

VALID_ID          = "61b6f11a41e7064d92e23641"
UNAVAILABLE_ID    = "111111111111111111111111"
INVALID_OBJECT_ID = "xxxxxxxxxxxxxxxxxxxxxxxx"
TOO_LONG_ID       = "1111111111111111111111111"
CONSUMER_ID       = "61b6f10641e7064d92e2361a"
PRODUCER_ID       = "51b6f10841e7064d92e23621"
OBJ = "61c4f5eb13f7d8c68f9b0972"
POST_RATING = 2.0
POST_TITLE = "This is a test for posting a review for consumer"
POST_DESCRIPTION = "This is the test description"

mealDict = {'breakfast': [],
            'lunch': [],
            'dinner': []}

menuDict = {'sunday': mealDict,
            'monday': mealDict,
            'tuesday': mealDict,
            'wednesday': mealDict,
            'thursday': mealDict,
            'friday': mealDict,
            'saturday': mealDict}
            
PAYLOAD_PRODUCER = {
    "_id": ObjectId(PRODUCER_ID),
    "first_name": "Peter",
    "last_name": "Griffin",
    "phone_number": "8157625852",
    "email_address": "peter@gmail.com",
    "photo": "https://en.wikipedia.org/wiki/Peter_Griffin#/media/File:Peter_Griffin.png",
    "bio": "Peanut butter jelly time",
    "address": {
        "street": "636 Yorkshire Dr",
        "city": "Dekalb",
        "state": "IL",
        "zip_code": "60115"
    },
    "food_items": [],
    "rating": float(0),
    "active_orders": [],
    "menu": menuDict,
    "date_created": datetime.utcnow(),
    "date_updated": datetime.utcnow()
}
CONSUMER_PAYLOAD = {
    "_id": ObjectId(CONSUMER_ID),
    "first_name": "Brian",
    "last_name": "Griffin",
    "phone_number": "8157625851",
    "email_address": "brian@gmail.com",
    "photo": "https://familyguy.fandom.com/wiki/Brian_Griffin?file=FamilyGuy_Single_BrianWriter_R7.jpg",
    "bio": "I'm snoopy",
    "address": {
        "street": "636 Yorkshire Dr",
        "city": "Dekalb",
        "state": "IL",
        "zip_code": "60115"
    },
    "rating": float(0),
    "active_orders": [],
    "date_created": datetime.utcnow(),
    "date_updated": datetime.utcnow()
}


