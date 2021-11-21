from datetime import datetime


def address_serializer(address: dict) -> dict:
    return {
        "street": address["street"],
        "city": address["city"],
        "state": address["state"],
        "zip_code": address["zip_code"]
    }

def producer_serializer(producer_document) -> dict:
    producer_document["id"] = producer_document["_id"]
    del producer_document["_id"]
    
    for key, value in producer_document:
        print(key)
        if type(value) is datetime:
            producer_document[key] = str(producer_document[key])
    
    return producer_document