def address_serializer(address) -> dict:
    return {
        "street": address["street"],
        "city": address["city"],
        "state": address["state"],
        "zip_code": address["zip_code"]
    }

def consumer_serializer(consumer) -> dict:
    return {
        "id": str(consumer["_id"]),
        "first_name": consumer["first_name"],
        "last_name": consumer["last_name"],
        "phone_num": consumer["phone_num"],
        "address": address_serializer(consumer["address"]),
        "average_consumer_rating": consumer["average_consumer_rating"],
        "active_orders": [ str(id) for id in consumer["active_orders"] ],
        "archived_orders": [ str(id) for id in consumer["archived_orders"] ],
        "date_created": consumer["date_created"],
        "date_updated": consumer["date_updated"]
    }

def consumers_serializer(consumers) -> list:
    return [ consumer_serializer(consumer) for consumer in consumers ]
