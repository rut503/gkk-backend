# Commands 

1. Be in a python virtual environment (gkk-backend)
2. Be inside of app directory (../gkk-backend/app)
3. Run `pipenv run uvicorn main:app --reload`

# Backend Logic Map

## API Endpoints 

#### Consumer
- Find consumer 
    - GET : `/consumer ? id="" & phone_num="" ` 
- Create a new consumer (need ALL required data, rest are set to their default values)
    - POST : `/consumer/`
    ``` 
    {
        firstName: "Juan", 
        lastName: "Lopez",
        phoneNum: "8157890123",
        address: {
            street: "656 Glidden Ave",
            city: "DeKalb",
            state: "IL",
            zip: "60115"
        }
    }
    ```
- Update consumer (only update data that's allowed to be changed by consumer)
    - PUT : `/consumer/{id}`
    ```
    {
        firstName: "Juan", 
        lastName: "Lopez",
        phoneNum: "8157890123",
        address: {
            street: "656 Glidden Ave",
            city: "DeKalb",
            state: "IL",
            zip: "60115"
        }
    }
    ```
- Delete consumer (move consumer to deactivated_user collection)
    - DELETE : `/consumer/{id}`

#### Producer
- Find producer 
    - GET : `/producer/{phoneNum}` 
    - GET : `/producer/{id}` 
    - GET : `/producer/{location_range}` this will require some location logic to find prducers in cirtain radius of consumer location who's doing the look up
- Create a new producer (need ALL required data, rest are set to their default values)
    - POST : `/producer/`
    ``` 
    {
        firstName: "Juan", 
        lastName: "Lopez",
        phoneNum: "8157890123",
        address: {
            street: "656 Glidden Ave",
            city: "DeKalb",
            state: "IL",
            zip: "60115"
        }
    }
    ```
- Update producer (only update data that's allowed to be changed by producer)
    - PUT : `/producer/{id}`
    ```
    {
        firstName: "Juan", 
        lastName: "Lopez",
        phoneNum: "8157890123",
        address: {
            street: "656 Glidden Ave",
            city: "DeKalb",
            state: "IL",
            zip: "60115"
        },
        food: [ food_id ],
        currentOrders: [ order_id ],
        archivedOrders: [ order_id ],
        menu: {
            sunday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            monday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            tuesday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            wednesday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            thursday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            friday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            },
            saturday: {
                breakfast: [ food_id ],
                lunch: [ food_id ],
                dinner: [ food_id ]
            }
        }
    }
    ```
- Delete producer (move producer to deactivated_user collection)
    - DELETE : `/producer/{id}` 

#### Food Item
- Find food item
    - GET : `/food_item/` 
        - query parameters
            - location_range
            - dietPreferance
            - price_range
            - rating_range
            - spicy
    - GET : `/food_item/{id}` 
- Create a new food item (need ALL required data, rest are set to their default values)
    - POST : `/food_item/`
    ``` 
    {
        producerId: ObjectId,
        dietPreferance: "Vegan", 
        description: "This is a description of Poteto Bhajiyas",
        photo: PhotoBinaryData
        price: 6.99,
        name: "Potato Bhajiya",
        portionSize: 12,
        spicy: 2
    }
    ```
- Update food item (only update data that's allowed to be changed by producer and only allow updates to the food item if it's not already in the producer menu and if no one has ordered it yet.)
    - PUT : `/food_item/{id}`
    ```
    {
        description: "This is a description of Poteto Bhajiyas",
        photo: PhotoBinaryData,
        price: 6.99,
        portionSize: 12,
        spicy: 2
    }
    ```
- Delete food item
    - DELETE : `/food_item/{id}`

#### Active Order
- Find active order
    - GET : `/active_order/{producerId}` 
    - GET : `/active_order/{consumerId}` 
    - GET : `/active_order/{id}` 
- Create a new active order (need ALL required data, rest are set to their default values)
    - POST : `/active_order/`
    ``` 
    {
        consumerId: ObjectId,
        producerId: ObjectId,
        items: [
            {
                foodId: ObjectId,
                quantity: 3
            },
            {
                foodId: ObjectId,
                quantity: 5
            },
        ],
        amount: 45.32,
        status: "pending",
        mealTime: "breakfast",
        pickUpDateTime: Date
    }
    ```
- Update food item (only update data that's allowed to be changed by producer and consumer. If status is pending, allow updates to items field, else don't allow that update. Allow status change only by consumer or producer on the status they're allowed to change, Ex accept status can only be set by producer.)
    - PUT : `/active_order/{id}`
    ```
    {
        items: [
            {
                foodId: ObjectId,
                quantity: 3
            },
            {
                foodId: ObjectId,
                quantity: 5
            },
        ],
        amount: 45.32,
        status: "pending",
        pickUpDateTime: Date
    }
    ```

#### Archived Order
- Find archived order
    - GET : `/archived_order/{producerId}` 
    - GET : `/archived_order/{consumerId}` 
    - GET : `/archived_order/{id}` 

#### Review For Consumer
- Find review for consumer
    - GET : `/review_for_consumer/{consumerId}` 
    - GET : `/review_for_consumer/{id}` 
- Create a new review for consumer (need ALL required data, rest are set to their default values)
    - POST : `/review_for_consumer/`
    ``` 
    {
        consumerId: ObjectId,
        producerId: ObjectId,
        rating: 4,
        title: "Pleasure doing business with you",
        description: "was on time",
    }
    ```
- Delete review for consumer (allow deletes by producer only)
    - DELETE : `/review_for_consumer/{id}`

#### Review For Producer
- Find review for producer
    - GET : `/review_for_producer/{producerId}` 
    - GET : `/review_for_producer/{id}` 
- Create a new review for producer (need ALL required data, rest are set to their default values)
    - POST : `/review_for_producer/`
    ``` 
    {
        consumerId: ObjectId,
        producerId: ObjectId,
        rating: 4,
        title: "Pleasure doing business with you",
        description: "was on time",
    }
    ```
- Delete review for producer (allow deletes by consumer only)
    - DELETE : `/review_for_producer/{id}`

#### Review For Food
- Find review for food
    - GET : `/review_for_food/{foodId}` 
    - GET : `/review_for_food/{id}` 
- Create a new review for food (need ALL required data, rest are set to their default values)
    - POST : `/review_for_food/`
    ``` 
    {
        consumerId: ObjectId,
        foodId: ObjectId,
        rating: 4,
        title: "Good food",
        description: "very good food",
    }
    ```
- Delete review for food (allow deletes by consumer only)
    - DELETE : `/review_for_food/{id}`

#### Special Routes
