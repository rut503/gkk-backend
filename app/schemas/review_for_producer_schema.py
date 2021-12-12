from pymongo.cursor import Cursor

def review_for_producer_serializer(review_document: dict) -> dict:
    return{
        "id": str(review_document["_id"]),
        "producer_id": str(review_document["producer_id"]),
        "consumer_id": str(review_document["consumer_id"]),
        "rating": review_document["rating"],
        "title": review_document["title"],
        "description": review_document["description"],
        "date_created": review_document["date_created"],
        "date_updated": review_document["date_updated"]
    }

def reviews_for_producer_serializer(review_document_cursor: Cursor) -> list:
    return [ review_for_producer_serializer(document) for document in review_document_cursor ]
