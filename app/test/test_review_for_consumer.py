from datetime import datetime
from _pytest.fixtures import fixture
from bson.objectid import ObjectId
from app.config.database import review_for_consumer_collection, producer_collection, consumer_collection
from fastapi.testclient import TestClient
from app.main import app
from app.models.review_for_consumer_model import review_for_consumer_response
from pytest_lazyfixture import lazy_fixture
from pytest import mark
from app.test.ids_for_testing import *

client = TestClient(app)

@fixture
def post_producer():
    payload = PAYLOAD_PRODUCER
    post_id = producer_collection.insert_one(payload).inserted_id
    post_doc = producer_collection.find_one({"_id": post_id})
    post_doc["id"] = str(post_doc["_id"])
    
    del post_doc["_id"]
    yield post_doc["id"]

    producer_collection.find_one_and_delete({"_id": ObjectId(post_id)})
@fixture
def post_consumer():
    payload = CONSUMER_PAYLOAD
    post_id = consumer_collection.insert_one(payload).inserted_id
    post_doc = consumer_collection.find_one({"_id": post_id})
    post_doc["id"] = str(post_doc["_id"])
    
    del post_doc["_id"]
    yield post_doc["id"]

    consumer_collection.find_one_and_delete({"_id": ObjectId(post_id)})


# Creates a test document and returns the new document. Deletes the document at the end. 
@fixture
def get_posted_review(post_producer, post_consumer):   
    payload = {"consumer_id": ObjectId(CONSUMER_ID), "producer_id": ObjectId(PRODUCER_ID), "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION, "date_created": datetime.utcnow(), "date_updated": datetime.utcnow()}
    post_id = review_for_consumer_collection.insert_one(payload).inserted_id
    post_doc = review_for_consumer_collection.find_one({"_id": post_id})
    post_doc["id"] = str(post_doc["_id"])
    
    del post_doc["_id"]
    yield post_doc
    
    review_for_consumer_collection.find_one_and_delete({"_id": ObjectId(post_id)})

@fixture
def get_posted_producer_id(get_posted_review):
    return str(get_posted_review["producer_id"])

@fixture
def get_posted_consumer_id(get_posted_review):
    return str(get_posted_review["consumer_id"])

#######################################################################################################################################################################################################################################
#
#                                                                       Get by id
#
#######################################################################################################################################################################################################################################
class Test_Get_By_Id:
    # Successful call
    def test_get_by_id_in_db(self, get_posted_review):
        response = client.get("/review_for_consumer/" + get_posted_review["id"])
        response_model = review_for_consumer_response(**response.json()).dict()
        assert response_model["consumer_id"] == CONSUMER_ID
        assert response_model["producer_id"] == PRODUCER_ID
        assert response_model["rating"] == POST_RATING
        assert response_model["title"] == POST_TITLE
        assert response_model["description"] == POST_DESCRIPTION
        assert response.status_code == 200

    # Unavailable document
    def test_get_by_id_not_in_db(self):
        response = client.get("/review_for_consumer/" + UNAVAILABLE_ID)
        assert response.status_code == 404

    # Too long id
    def test_get_by_too_long_id(self):
        response = client.get("/review_for_consumer/" + TOO_LONG_ID)
        assert response.status_code == 422

    # Invalid object Id
    def test_get_by_invalid_id(self):
        response = client.get("/review_for_consumer/" + INVALID_OBJECT_ID)
        assert response.status_code == 400

    # Empty id
    def test_get_by_empty_id(self):
        response = client.get("/review_for_consumer/")
        assert response.status_code == 405

#######################################################################################################################################################################################################################################
#
#                                                                       Get by consumer or producer id
#
#######################################################################################################################################################################################################################################
class Test_Get_By_Consumer_And_Producer:
    # Successful 
    def test_get_by_valid_consumer_id_and_producer_id(self, get_posted_review):
        response = client.get("/review_for_consumer", params={"consumer_id": get_posted_review["consumer_id"], "producer_id": get_posted_review["producer_id"]})
        
        # Validating documents returned
        for document in response.json():
            response_model = review_for_consumer_response(**document)
        assert response.status_code == 200

    # Get reviews from a producer_id or a consumer_id
    @mark.parametrize("id, producer_or_consumer",[
        (lazy_fixture('get_posted_producer_id'), "producer_id"),
        (lazy_fixture('get_posted_consumer_id'), "consumer_id")
    ])
    def test_get_by_consumer_id_and_producer_id_only_one(self, id, producer_or_consumer):
        response = client.get("/review_for_consumer", params={producer_or_consumer: id})
        response_status_code = response.status_code

        # Validating documents returned
        for document in response.json():
            review_for_consumer_response(**document)
        assert response_status_code == 200

    # Valid id that returns an empty list
    @mark.parametrize("producer_or_consumer",[
        ("producer_id"),
        ("consumer_id")
    ])
    def test_get_by_consumer_id_and_producer_id_no_reviews(self, producer_or_consumer):
        response = client.get("/review_for_consumer", params={producer_or_consumer: VALID_ID})
        assert response.status_code == 404 

    # Testing with an invalid ObjectId
    @mark.parametrize("producer_or_consumer, id",[
        ("producer_id", TOO_LONG_ID),
        ("consumer_id", TOO_LONG_ID)
    ])
    def test_get_by_consumer_id_and_producer_id_too_long(self, producer_or_consumer, id):
        response = client.get("/review_for_consumer", params={producer_or_consumer: id})
        assert response.status_code == 422

    # Testing with empty id's passed in
    @mark.parametrize("producer_id, consumer_id",[
        (lazy_fixture('get_posted_producer_id'), ""),
        ("", lazy_fixture('get_posted_consumer_id')),
        ("", ""),
    ])
    def test_get_by_consumer_id_and_producer_id_one_is_empty(self, producer_id, consumer_id):
        response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
        assert response.status_code == 422

    # Testing with an invalid object id
    def test_get_by_consumer_id_and_producer_id_invalid_ids(self):
        response = client.get("/review_for_consumer", params={"consumer_id": INVALID_OBJECT_ID, "producer_id": INVALID_OBJECT_ID})
        assert response.json()["detail"] == INVALID_OBJECT_ID + " consumer_id is not a valid ObjectId type!"
        assert response.status_code == 400

#######################################################################################################################################################################################################################################
#
#                                                                       Post operations
#
#######################################################################################################################################################################################################################################
class Test_Post_Review_For_Consumer:
    # This fixture will delete reviews that have matching test fields after all the tests in this class have finished. 
    # Eg TITLE = "This is a test for posting a review for consumer" ,DESCRIPTION = "This is the test description"
    @fixture(autouse=True)
    def delete_post(self):
        yield
        review_for_consumer_collection.delete_many({"title": POST_TITLE, "description": POST_DESCRIPTION})

    # Post with all fields passed
    def test_post_valid_all_fields(self, get_posted_consumer_id, get_posted_producer_id):
        payload = {"consumer_id": get_posted_consumer_id, "producer_id": get_posted_producer_id, "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)

        response_status_code = response.status_code
        response = review_for_consumer_response(**(response.json()))
        response = response.dict()

        assert response["producer_id"] == get_posted_producer_id
        assert response["consumer_id"] == get_posted_consumer_id
        assert response["rating"] == POST_RATING
        assert response["title"] == POST_TITLE
        assert response["description"] == POST_DESCRIPTION  
        assert response_status_code == 201
    
    # Test with not sending the required fields
    @mark.parametrize("rating, title, description", [
        ("", POST_TITLE, POST_DESCRIPTION),
        (POST_RATING, "", POST_DESCRIPTION),
        (POST_RATING, POST_TITLE, "")
    ])
    def test_post_missing_fields(self, rating, title, description, get_posted_consumer_id, get_posted_producer_id):
        payload = {"consumer_id": get_posted_consumer_id, "producer_id": get_posted_producer_id, "rating": rating, "title": title, "description": description}
        response = client.post("review_for_consumer/", json=payload)
        assert response.status_code == 422
        
    # Only one id passed, need a producer AND consumer id for posting a review
    @mark.parametrize("id, producer_or_consumer",[
        (lazy_fixture('get_posted_producer_id'), "producer_id"),
        (lazy_fixture('get_posted_consumer_id'), "consumer_id")
    ])
    def test_post_only_one_id(self, id, producer_or_consumer):
        payload = {producer_or_consumer: id, "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)
        assert response.status_code == 422

    # Post with invalid object Id
    @mark.parametrize("producer_id, consumer_id",[
        (INVALID_OBJECT_ID, lazy_fixture('get_posted_consumer_id')),
        (lazy_fixture('get_posted_producer_id'), INVALID_OBJECT_ID)
    ])
    def test_post_invalid_id(self, producer_id, consumer_id):
        payload = {"producer_id": producer_id, "consumer_id": consumer_id, "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION}
        response = client.post("/review_for_consumer/", json=payload)
        assert response.status_code == 400

    # Test with empty id's
    @mark.parametrize("producer_id, consumer_id",[
        (lazy_fixture('get_posted_producer_id'), ""),
        ("", lazy_fixture('get_posted_consumer_id')),
        ("", "")
    ])
    def test_post_empty_ids(self, producer_id, consumer_id):
        payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)
        assert response.status_code == 422

    # Test with same id for consumer and producer
    @mark.parametrize("producer_id, consumer_id", [
        (lazy_fixture('get_posted_producer_id'), lazy_fixture('get_posted_producer_id')),
        (lazy_fixture('get_posted_consumer_id'), lazy_fixture('get_posted_consumer_id'))
    ])
    def test_post_no_document_with_matching_id(self, producer_id, consumer_id):
        payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": POST_RATING, "title": POST_TITLE, "description": POST_DESCRIPTION}
        response = client.post("/review_for_consumer/", json=payload)
        assert response.status_code == 404
        
#######################################################################################################################################################################################################################################
#
#                                                                       Put opeartions
#
#######################################################################################################################################################################################################################################
class Test_Put_Review_For_Consumer:
    @fixture
    def get_payload(self):
        return {"rating": "5", "title": "New updated review", "description": "New updated description"}

    # Successful update
    def test_successful_put(self, get_posted_review):
        new_rating = 5
        new_title = "This a update post sent from Test_Put_Review_For_Consumer"
        new_description = "This is the updated description"

        updated_payload = {"rating": new_rating, "title": new_title, "description": new_description}
        response = client.put("/review_for_consumer/" + get_posted_review["id"], json=updated_payload)
        
        response_model = review_for_consumer_response(**(response.json())).dict()

        assert response_model["rating"] == new_rating
        assert response_model["title"] == new_title
        assert response_model["description"] == new_description
        assert response.status_code == 200

    # Invald id
    def test_put_invalid_id(self, get_payload):
        response = client.put("/review_for_consumer/" + INVALID_OBJECT_ID, json=get_payload)
        assert response.status_code == 400

    # Id doesn't exist in db
    def test_put_unavailable_id(sel, get_payload):
        response = client.put("/review_for_consumer/" + UNAVAILABLE_ID, json=get_payload)
        assert response.status_code == 404

    # Empty id
    def test_put_unavailable_id(sel, get_payload):
        response = client.put("/review_for_consumer/" + "", json=get_payload)
        assert response.status_code == 405

#######################################################################################################################################################################################################################################
#
#                                                                       Delete operations
#
#######################################################################################################################################################################################################################################
class Test_Delete_Review_For_Consumer:
    def test_delete_review_By_id(self, get_posted_review):
        response = client.delete("/review_for_consumer/" + get_posted_review["id"])
        assert response.status_code == 204

    def test_delete_review_invalid_id(self):
        response = client.delete("/review_for_consumer/" + INVALID_OBJECT_ID)
        assert response.status_code == 400

    def test_delete_review_unavailable_id(self):
        response = client.delete("/review_for_consumer/" + UNAVAILABLE_ID)
        assert response.status_code == 404

    def test_delete_review_empty_String(self):
        response = client.delete("/review_for_consumer/" + "")
        assert response.status_code == 405





