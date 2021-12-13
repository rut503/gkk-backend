from pymongo.cursor import Cursor

from app.schemas.active_order_schema import active_order_serializer, active_orders_serializer

def archived_order_serializer(order_document: dict) -> dict:
    return active_order_serializer(order_document)

def archived_orders_serializer(order_document_cursor: Cursor) -> list:
    return active_orders_serializer(order_document_cursor)
