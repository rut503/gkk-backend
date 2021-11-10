def food_item_serializer(food_item) -> dict:
    return {
        "id": str(food_item["_id"]),
        "producer_id": str(food_item["producer_id"]),
        "diet_preference": food_item["diet_preference"],
        "description": food_item["description"],
        "photo": food_item["photo"],
        "price": food_item["price"],
        "rating": food_item["rating"],
        "name": food_item["name"],
        "portion_size": food_item["portion_size"],
        "spicy": food_item["spicy"],
        "allergy": food_item["allergy"],
        "date_created": food_item["date_created"],
        "date_updated": food_item["date_updated"]
    }

def food_items_serializer(food_items) -> list:
    return [ food_item_serializer(food_item) for food_item in food_items ]
