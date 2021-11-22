from datetime import datetime


def address_serializer(address: dict) -> dict:
    return {
        "street": address["street"],
        "city": address["city"],
        "state": address["state"],
        "zip_code": address["zip_code"]
    }

# Serializes Object(id) fields
def producer_serializer(producer_document) -> dict:
    list_of_keys = list(producer_document)
    
    # _id
    if "_id" in list_of_keys:
        producer_document["id"] = str(producer_document["_id"])
        del producer_document["_id"]
    
    # Serizalizing food id's
    if "food_items" in list_of_keys:
        len_of_food_list = len(producer_document["food_items"])
        for i in range(len_of_food_list):
            producer_document["food_items"][i] = str(producer_document["food_items"][i])

    # Serizalizing active_orders id's 
    if "active_orders" in list_of_keys:
        len_of_active_orders_list = len(producer_document["active_orders"])
        for i in range(len_of_active_orders_list):
            producer_document["active_orders"][i] = str(producer_document["active_orders"][i])
    
    # Serizalizing the food id's of the menu
    if "menu" in list_of_keys:
        for day_of_week in producer_document["menu"]:
            for time_of_day in producer_document["menu"][day_of_week]:
                for i in range(len(producer_document["menu"][day_of_week][time_of_day])):
                    producer_document["menu"][day_of_week][time_of_day][i] = str(producer_document["menu"][day_of_week][time_of_day][i])

    return producer_document