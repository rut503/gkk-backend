from fastapi import FastAPI
from routes.consumer_routes import consumer_router
from routes.food_item_routes import food_item_router
from routes.review_for_consumer_routes import review_for_consumer_router

app = FastAPI()

# consumer routes
app.include_router(
    consumer_router,
    prefix="/consumer",
    tags=["Consumer"]
)

# producer routes


# food_item routes
app.include_router(
    food_item_router,
    prefix="/food_item",
    tags=["Food Item"]
)

app.include_router(
    review_for_consumer_router,
    prefix="/review_for_consumer"
)