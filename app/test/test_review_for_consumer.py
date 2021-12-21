from datetime import datetime
from _pytest.fixtures import fixture
from bson.objectid import ObjectId
from app.config.database import review_for_consumer_collection, consumer_collection, producer_collection
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.config.database import review_for_consumer_collection
from pytest import mark, raises
from app.models.review_for_consumer_model import review_for_consumer_response
from pytest_lazyfixture import lazy_fixture
client = TestClient(app)

VALID_ID          = "61b6f11a41e7064d92e23641"
UNAVAILABLE_ID    = "111111111111111111111111"
INVALID_OBJECT_ID = "xxxxxxxxxxxxxxxxxxxxxxxx"
TOO_LONG_ID       = "1111111111111111111111111"
CONSUMER_ID       = "61b6f10641e7064d92e2361e"
PRODUCER_ID       = "61b6f10841e7064d92e23621"

# Creates a test document and returns the new document. Deletes the document at the end. 
@fixture
def get_posted_review():   
    payload = {"consumer_id": ObjectId(CONSUMER_ID), "producer_id": ObjectId(PRODUCER_ID), "rating": "2", "title": "This a test post", "description": "This is the test description", "date_created": datetime.utcnow(), "date_updated": datetime.utcnow()}
    post_id = review_for_consumer_collection.insert_one(payload).inserted_id
    post_doc = review_for_consumer_collection.find_one({"_id": post_id})
    post_doc["id"] = str(post_doc["_id"])
    
    print(type(post_doc["producer_id"]))

    del post_doc["_id"]
    yield post_doc
    
    review_for_consumer_collection.find_one_and_delete({"_id": ObjectId(post_id)})

@fixture
def get_posted_producer_id(get_posted_review):
    return str(get_posted_review["producer_id"])

@fixture
def get_posted_consumer_id(get_posted_review):
    return str(get_posted_review["consumer_id"])

class Test_Get_By_Id:
    # Successful call
    def test_get_by_id_in_db(self, get_posted_review):
        response = client.get("/review_for_consumer/" + get_posted_review["id"])
        response_model = review_for_consumer_response(**response.json())
        assert response.status_code == 200

    # Unavailable document
    def test_get_by_id_not_in_db(self):
        response = client.get("/review_for_consumer/" + UNAVAILABLE_ID)
        assert response.status_code == 404
        assert raises(HTTPException)

    # Too long id
    def test_get_by_too_long_id(self):
        response = client.get("/review_for_consumer/" + TOO_LONG_ID)
        assert response.status_code == 422

    # Invalid object Id
    def test_get_by_invalid_id(self):
        response = client.get("/review_for_consumer/" + INVALID_OBJECT_ID)
        assert response.status_code == 400
        assert raises(HTTPException)

    # Empty id
    def test_get_by_empty_id(self):
        response = client.get("/review_for_consumer/")
        assert response.status_code == 405

class Test_Get_By_Consumer_And_Producer:
    #Successful 
    def test_get_by_valid_consumer_id_and_producer_id(self, get_posted_review):
        response = client.get("/review_for_consumer", params={"consumer_id": get_posted_review["consumer_id"], "producer_id": get_posted_review["producer_id"]})
        assert response.status_code == 200
        
        # Validating documents returned
        for document in response.json():
            response_model = review_for_consumer_response(**document)

    # Get reviews from a producer_id or a consumer_id
    @mark.parametrize("id, producer_or_consumer",[
        (lazy_fixture('get_posted_producer_id'), "producer_id"),
        (lazy_fixture('get_posted_consumer_id'), "consumer_id")
    ])
    def test_get_by_consumer_id_and_producer_id_only_one(self, id, producer_or_consumer):
        response = client.get("/review_for_consumer", params={producer_or_consumer: id})
        response_status_code = response.status_code

        assert response_status_code == 200
        # Validating documents returned
        for document in response.json():
            review_for_consumer_response(**document)

    # Valid id that returns an empty list
    @mark.parametrize("producer_or_consumer",[
        ("producer_id"),
        ("consumer_id")
    ])
    def test_get_by_consumer_id_and_producer_id_no_reviews(self, producer_or_consumer):
        response = client.get("/review_for_consumer", params={producer_or_consumer: VALID_ID})
        assert response.status_code == 404 

    # Too long id
    @mark.parametrize("producer_or_consumer, id",[
        ("producer_id", TOO_LONG_ID),
        ("consumer_id", TOO_LONG_ID)
    ])
    def test_get_by_consumer_id_and_producer_id_too_long(self, producer_or_consumer, id):
        response = client.get("/review_for_consumer", params={producer_or_consumer: id})
        assert response.status_code == 422

    # Empty id
    @mark.parametrize("producer_id, consumer_id",[
        (lazy_fixture('get_posted_producer_id'), ""),
        ("", lazy_fixture('get_posted_consumer_id')),
        ("", ""),
    ])
    def test_get_by_consumer_id_and_producer_id_one_is_empty(self, producer_id, consumer_id):
        response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
        assert response.status_code == 422

    # Invalid object id
    def test_get_by_consumer_id_and_producer_id_invalid_ids(self):
        response = client.get("/review_for_consumer", params={"consumer_id": INVALID_OBJECT_ID, "producer_id": INVALID_OBJECT_ID})
        assert response.status_code == 400
        assert raises(HTTPException)


RATING = 2
TITLE = "This is a test for posting a review for consumer"
DESCRIPTION = "This is the test description"
class Test_Post_Review_For_Consumer:

    # This fixture will delete reviews that have matching test fields after all the tests in this class have finished. 
    # Eg RATING = 2, TITLE = "This is a test for posting a review for consumer" ,DESCRIPTION = "This is the test description"
    @fixture(autouse=True)
    def delete_post(self):
        yield
        review_for_consumer_collection.delete_many({"title": TITLE, "description": DESCRIPTION})

    # Post with all fields passed
    def test_post_valid_all_fields(self, get_posted_consumer_id, get_posted_producer_id):
        payload = {"consumer_id": get_posted_consumer_id, "producer_id": get_posted_producer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)

        response_status_code = response.status_code
        response = review_for_consumer_response(**(response.json()))
        response = response.dict()

        assert response_status_code == 201
        assert response["producer_id"] == get_posted_producer_id
        assert response["consumer_id"] == get_posted_consumer_id
        assert response["rating"] == RATING
        assert response["title"] == TITLE
        assert response["description"] == DESCRIPTION
    
    
    @mark.parametrize("rating, title, description", [
        ("", TITLE, DESCRIPTION),
        (RATING, "", DESCRIPTION),
        (RATING, TITLE, "")
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
        payload = {producer_or_consumer: id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)
        assert response.status_code == 422

    # Post with invalid object Id
    @mark.parametrize("producer_id, consumer_id",[
        (INVALID_OBJECT_ID, lazy_fixture('get_posted_consumer_id')),
        (lazy_fixture('get_posted_producer_id'), INVALID_OBJECT_ID)
    ])
    def test_post_invalid_id(self, producer_id, consumer_id):
        payload = {"producer_id": producer_id, "consumer_id": consumer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
        response = client.post("/review_for_consumer/", json=payload)
        assert response.status_code == 400

    # Post with empty id's
    @mark.parametrize("producer_id, consumer_id",[
        (lazy_fixture('get_posted_producer_id'), ""),
        ("", lazy_fixture('get_posted_consumer_id')),
        ("", "")
    ])
    def test_post_empty_ids(self, producer_id, consumer_id):
        payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
        response = client.post("review_for_consumer/", json=payload)
        assert response.status_code == 422

    @mark.parametrize("producer_id, consumer_id", [
        (lazy_fixture('get_posted_producer_id'), lazy_fixture('get_posted_producer_id')),
        (lazy_fixture('get_posted_consumer_id'), lazy_fixture('get_posted_consumer_id'))
    ])
    # Post with id's that aren't in any documents
    def test_post_no_document_with_matching_id(self, producer_id, consumer_id):
        payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
        response = client.post("/review_for_consumer/", json=payload)
        assert response.status_code == 404
        
        
class Test_Put_Review_For_Consumer:
    @fixture
    def get_payload(self):
        return {"rating": "5", "title": "New updated review", "description": "New updated description"}

    # Successful update
    def test_put(self, get_posted_review):
        new_rating = 5
        new_title = "This a update post sent from Test_Put_Review_For_Consumer"
        new_description = "This is the updated description"

        updated_payload = {"rating": new_rating, "title": new_title, "description": new_description}
        response = client.put("/review_for_consumer/" + get_posted_review["id"], json=updated_payload)
        
        assert response.status_code == 200
        
        response = review_for_consumer_response(**(response.json()))
        response = response.dict()
        assert response["rating"] == new_rating
        assert response["title"] == new_title
        assert response["description"] == new_description

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

class Test_Delete_Review_For_Consumer:
    def test_delete_user_id(self, get_posted_review):
        response = client.delete("/review_for_consumer/" + get_posted_review["id"])
        assert response.status_code == 204

    def test_delete_user_invalid_id(self):
        response = client.delete("/review_for_consumer/" + INVALID_OBJECT_ID)
        assert response.status_code == 400

    def test_delete_user_unavailable_id(self):
        response = client.delete("/review_for_consumer/" + UNAVAILABLE_ID)
        assert response.status_code == 404
