from fastapi import FastAPI
from routes.grade_routes import grade_router


app = FastAPI()

app.include_router(grade_router)


# class Address(BaseModel):
#     street: str
#     city: str
#     state: str
#     zip: int

# class Menu(BaseModel):
#     sunday: Optional[List[int]] = None
#     monday: Optional[List[int]] = None
#     tuesday: Optional[List[int]] = None
#     wednesday: Optional[List[int]] = None
#     thursday: Optional[List[int]] = None
#     friday: Optional[List[int]] = None
#     saturday: Optional[List[int]] = None

# class Producer(BaseModel):
#     firstName: str 
#     lastName: str
#     phoneNum: int
#     address: Address
#     food: Optional[List] = None
#     averageProducerRating: int = 0
#     acceptedOrdersToCreate: Optional[Set[int]] = None
#     pendingOrderForProducer: Optional[Set[int]] = None
#     menu: Optional[Menu]

# @app.get("/")
# async def root():
#     return {"msg": "Hello Rutvi"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/producers/")
# async def get_producers() -> List[Producer] :
#     return {"producers": "LIST[producers]"}

# @app.get("/producer/{producer_id}")
# async def get_producer(producer_id: int):
#     return {"producers": producer_id}

# @app.post("/producer/")
# async def create_producer(producer: Producer):
#     print(producer)
#     return {"producers": "one producer"}