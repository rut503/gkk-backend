from pymongo.cursor import Cursor

def food_item_serializer(food_item) -> dict:
    return {
        "diet_preference": food_item["diet_preference"],
        "description": food_item["description"],
        "photo": food_item["photo"],
        "price": food_item["price"],
        "rating": food_item["rating"],
        "name": food_item["name"],
        "portion_size": food_item["portion_size"],
        "spicy": food_item["spicy"],
        "allergy": food_item["allergy"],
        "quantity": food_item["quantity"]
    }

def active_order_serializer(order_document: dict) -> dict:
    return{
        "id": str(order_document["_id"]),
        "consumer_id": str(order_document["consumer_id"]),
        "producer_id": str(order_document["producer_id"]),
        "items": [ food_item_serializer(subdocument) for subdocument in order_document["items"] ],
        "total_price": order_document["total_price"],
        "status": order_document["status"],
        "meal_time": order_document["meal_time"],
        "message_for_producer": order_document["message_for_producer"],
        "order_due_datetime": order_document["order_due_datetime"],
        "date_created": order_document["date_created"],
        "date_updated": order_document["date_updated"]
    }

def active_orders_serializer(order_document_cursor: Cursor) -> list:
    return [ active_order_serializer(document) for document in order_document_cursor ]
