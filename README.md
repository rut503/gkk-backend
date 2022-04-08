# Commands

1. Install pipenv
    - `pip3 install pipenv`
2. Start python virtual environment (gkk-backend)
    - Be inside of app directory (../gkk-backend/app)
    - `pipenv shell`
3. Run server
    - `pipenv run uvicorn main:app --reload`

# Backend Logic Map

## API Endpoints

#### Consumer

- Find consumer
    - `GET : /consumer/{id}`
    - `GET : /consumer/phone_number/{phone_number}`

- Create new consumer
    - `POST : /consumer/`
    ```
        {
            first_name: "Juan",
            last_name: "Lopez",
            phone_number: "8157890123",
            address: {
                street: "656 Glidden Ave",
                city: "DeKalb",
                state: "IL",
                zip_code: "60115"
            }
        }
    ```

- Update consumer
    - `PUT : /consumer/{id}`
    ```
        {
            first_name: "Juan",
            last_name: "Lopez",
            phone_number: "8157890123",
            address: {
                street: "656 Glidden Ave",
                city: "DeKalb",
                state: "IL",
                zip_code: "60115"
            }
        }
    ```

- Delete consumer
    - `DELETE : /consumer/{id}`

#### Producer

- Find producer
    - `GET : /producer/{id}`
    - `GET : /producer/phone_number/{phone_number}`
    - `GET : /producer/filter ? _______` 
        - query parameters
            - consumer_coordinates = ??????
            - distance_radius = 8 (miles, float)

- Create new producer
    - `POST : /producer/`
    ```
        {
            first_name: "Juan",
            last_name: "Lopez",
            phone_number: "8157890123",
            address: {
                street: "656 Glidden Ave",
                city: "DeKalb",
                state: "IL",
                zip_code: "60115"
            }
        }
    ```

- Update producer
    - `PUT : /producer/{id}`
    ```
        {
            first_name: "Juan",
            last_name: "Lopez",
            phone_number: "8157890123",
            address: {
                street: "656 Glidden Ave",
                city: "DeKalb",
                state: "IL",
                zip_code: "60115"
            }
        }
    ```
    - `PUT : /producer/{id}/menu`
    ```
        {
            menu: {
                sunday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                monday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                tuesday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                wednesday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                thursday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                friday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                },
                saturday: {
                    breakfast: [ food_item_id ],
                    lunch: [ food_item_id ],
                    dinner: [ food_item_id ]
                }
            }
        }
    ```
- Delete producer
    - `DELETE : /producer/{id}`

#### Food Item

- Find food item
    - `GET : /food_item/{id}`
    - `GET : /food_item ? producer_id="" `

- Create new food item
    - `POST : /food_item/`
    ```
        {
            producer_id: ObjectId,
            diet_preferance: "Vegan",
            description: "This is a description of Poteto Bhajiyas",
            price: 6.99,
            name: "Potato Bhajiya",
            portion_size: 12,
            spicy: 2,
            allergy: [ "nuts", "gluten" ]
        }
    ```

- Update food item
    - `PUT : /food_item/{id}`
    ```
        {
            diet_preferance: "Vegan",
            description: "This is a description of Poteto Bhajiyas",
            price: 6.99,
            name: "Potato Bhajiya",
            portion_size: 12,
            spicy: 2,
            allergy: [ "nuts", "gluten" ]
        }
    ```

- Delete food item
    - `DELETE : /food_item/{id}`

#### Active Order

- Find active order
    - `GET : /active_order/{id}`
    - `GET : /active_order ? consumer_id="" & producer_id="" `

- Create new active order
    - `POST : /active_order/`
    ```
        {
            consumer_id: ObjectId,
            producer_id: ObjectId,
            items: [
                {
                    diet_preference: [ "Vegetarian" ],
                    description: "Apple or Pumpkin flavor",
                    photo: "http://www.photo.com",
                    price: 5.25,
                    rating: 0,
                    name: "Pie",
                    portion_size: 3,
                    spicy: 0,
                    allergy: [ "Dairy", "Soy" ],
                    quantity: 3
                },
                {
                    diet_preference: [ "Vegetarian" ],
                    description: "Peanut Butter Jelly",
                    photo: "http://www.photo.com",
                    price: 2.45,
                    rating: 0,
                    name: "Peanut Butter Jeally",
                    portion_size: 1.8,
                    spicy: 0,
                    allergy: [ "Peanut Butter", "Dairy", "Soy" ],
                    quantity: 5
                }
            ],
            total_price: 45.32,
            status: "pending",
            meal_time: "breakfast",
            message_for_producer: "Make it delicious please",
            order_due_datetime: Date
        }
    ```

- Update food item
    - `PUT : /active_order/{id}`
    ```
        {
            status: "accepted",
        }
    ```

#### Archived Order

- Find archived order
    - `GET : /archived_order/{id}`
    - `GET : /archived_order ? consumer_id="" & producer_id="" `

#### Review For Consumer

- Find review for consumer
    - `GET : /review_for_consumer/{id}`
    - `GET : /review_for_consumer ? consumer_id="" & producer_id="" `

- Create new review for consumer
    - `POST : /review_for_consumer/`
    ```
        {
            consumer_id: ObjectId,
            producer_id: ObjectId,
            rating: 4,
            title: "Pleasure doing business with you",
            description: "was on time",
        }
    ```

- Update review for consumer
    - `PUT : /review_for_consumer/{id}`
    ```
        {
            rating: 4,
            title: "Pleasure doing business with you",
            description: "was on time",
        }
    ```

- Delete review for consumer
  - `DELETE : /review_for_consumer/{id}`

#### Review For Producer

- Find review for producer
    - `GET : /review_for_producer/{id}`
    - `GET : /review_for_producer ? consumer_id="" & producer_id="" `

- Create new review for producer
    - `POST : /review_for_producer/`
    ```
        {
            consumer_id: ObjectId,
            producer_id: ObjectId,
            rating: 4,
            title: "Pleasure doing business with you",
            description: "was on time",
        }
    ```

- Update review for producer
    - `PUT : /review_for_producer/{id}`
    ```
        {
            rating: 4,
            title: "Pleasure doing business with you",
            description: "was on time",
        }
    ```

- Delete review for producer
    - `DELETE : /review_for_producer/{id}`

#### Review For Food

- Find review for food
    - `GET : /review_for_food_item/{id}`
    - `GET : /review_for_food_item ? consumer_id="" & food_item_id="" `

- Create new review for food
    - POST : `/review_for_food_item/`
    ```
        {
            consumer_id: ObjectId,
            food_id: ObjectId,
            rating: 4,
            title: "Good food",
            description: "very good food",
        }
    ```

- Update review for food
    - `PUT : /review_for_food_item/{id}`
    ```
        {
            rating: 4,
            title: "Pleasure doing business with you",
            description: "was on time",
        }
    ```

- Delete review for food
    - `DELETE : /review_for_food_item/{id}`

#### Special Routes

- Search for food items 
    - `GET : /search/food_item ? ______ `
        - Query Parameters
        ```
            time = [ "breakfast", "lunch", "dinner" ] (3 values, list)
            diet_preference = [ "Low Carb",      "High Protein",
                                "Low/No Sodium", "Diabetic",
                                "Gluten Free",   "Lactose Free",
                                "Vegetarian",    "Non-Vegetarian",
                                "Paleo",         "Vegan",
                                "Pescetarian",   "Eggitarian",
                                "Nut Free",      "Other"
                              ] (14 values, list)
            min_price = 4.99 ($, float)
            max_price = 14.99 ($, float)
            consumer_coordinates = ??????
            distance_radius = 8 (miles, float)
            ratings = 4 (stars, int)
            spicy_level = 3 (pepers, int)
            chef_name = "ritu shah" (chef, str)
        ```