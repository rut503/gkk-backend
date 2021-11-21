from datetime import datetime


def address_serializer(address: dict) -> dict:
    return {
        "street": address["street"],
        "city": address["city"],
        "state": address["state"],
        "zip_code": address["zip_code"]
    }

def producer_serializer(producer_document) -> dict:
    list_of_keys = list(producer_document)
    
    if "_id" in list_of_keys:
        producer_document["id"] = str(producer_document["_id"])
        del producer_document["_id"]
    
    if "food_items" in list_of_keys:
        len_of_food_list = len(producer_document["food_items"])
        for i in range(len_of_food_list):
            producer_document["food_items"][i] = str(producer_document["food_items"][i])

    
    # for key, value in producer_document:
    #     print(key)
    #     if type(value) is datetime:
    #         producer_document[key] = str(producer_document[key])
    
    return producer_document