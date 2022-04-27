from fastapi import FastAPI
from routes.consumer_routes import consumer_router
from routes.producer_routes import producer_router
from routes.food_item_routes import food_item_router
from routes.active_order_routes import active_order_router
from routes.archived_order_routes import archived_order_router
from routes.review_for_consumer_routes import review_for_consumer_router
from routes.review_for_producer_routes import review_for_producer_router
from routes.review_for_food_item_routes import review_for_food_item_router

app = FastAPI()

#consumer routes
app.include_router(
    consumer_router,
    prefix="/consumer",
    tags=["Consumer"]
)

# producer routes
app.include_router(
    producer_router,
    prefix="/producer",
    tags=["Producer"]
)

# food_item routes
app.include_router(
    food_item_router,
    prefix="/food_item",
    tags=["Food Item"]
)

# active_order routes
app.include_router(
    active_order_router,
    prefix="/active_order",
    tags=["Active Order"]
)

# archived_order routes
app.include_router(
    archived_order_router,
    prefix="/archived_order",
    tags=["Archived Order"]
)

# review_for_consumer routes
app.include_router(
    review_for_consumer_router,
    prefix="/review_for_consumer",
    tags=["Review for Consumer"]
)

# review_for_producer routes
app.include_router(
    review_for_producer_router,
    prefix="/review_for_producer",
    tags=["Review for Producer"]
)

# review_for_food_item routes
app.include_router(
    review_for_food_item_router,
    prefix="/review_for_food_item",
    tags=["Review for Food Item"]
)