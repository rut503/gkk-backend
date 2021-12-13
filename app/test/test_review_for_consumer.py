from datetime import time
from logging import error
from _pytest.mark import param
from _pytest.monkeypatch import resolve
from _pytest.python_api import raises
from bson import ObjectId, errors
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException, RequestValidationError, WebSocketRequestValidationError
from pymongo import response
from starlette import status
from app.main import app
from app.config.database import review_for_consumer_collection
from pytest import mark, raises
from app.models.review_for_consumer_model import review_for_consumer_response
client = TestClient(app)

VALID_ID          = "61b6f11a41e7064d92e23641"
UNAVAILABLE_ID    = "111111111111111111111111"
INVALID_OBJECT_ID = "xxxxxxxxxxxxxxxxxxxxxxxx"
TOO_LONG_ID       = "1111111111111111111111111"
CONSUMER_ID       = "61b6f10641e7064d92e2361e"
PRODUCER_ID       = "61b6f10841e7064d92e23621"

class Test_Get_By_Id:
     # Successful call
     def test_get_by_id_in_db(self):
          response = client.get("/review_for_consumer/" + VALID_ID)
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
          assert raises(RequestValidationError)

     # Invalid object Id
     def test_get_by_invalid_id(self):
          response = client.get("/review_for_consumer/" + INVALID_OBJECT_ID)
          assert response.status_code == 400
          assert raises(HTTPException)

     # Empty id
     def test_get_by_empty_id(self):
          response = client.get("/review_for_consumer/")
          assert response.status_code == 405
          assert raises(WebSocketRequestValidationError)

class Test_Get_By_Consumer_And_Producer:
     #Successful 
     def test_get_by_valid_consumer_id_and_producer_id(self):
          response = client.get("/review_for_consumer", params={"consumer_id": CONSUMER_ID, "producer_id": PRODUCER_ID})
          assert response.status_code == 200
          
          # Validating documents returned
          for document in response.json():
               response_model = review_for_consumer_response(**document)

     # Get reviews from a producer_id or a consumer_id
     @mark.parametrize("id, producer_or_consumer",[
          (PRODUCER_ID, "producer_id"),
          (CONSUMER_ID, "consumer_id")
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
          assert raises(RequestValidationError)
          assert response.status_code == 422

     # Empty id
     @mark.parametrize("producer_id, consumer_id",[
          (PRODUCER_ID, ""),
          ("", CONSUMER_ID),
          ("", ""),
     ])
     def test_get_by_consumer_id_and_producer_id_one_is_empty(self, producer_id, consumer_id):
          response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
          assert response.status_code == 422
          assert raises(RequestValidationError)

     # Invalid object id
     def test_get_by_consumer_id_and_producer_id_invalid_ids(self):
          response = client.get("/review_for_consumer", params={"consumer_id": INVALID_OBJECT_ID, "producer_id": INVALID_OBJECT_ID})
          assert response.status_code == 400
          assert raises(HTTPException)


RATING = 2
TITLE = "This is a test for posting a review for consumer"
DESCRIPTION = "This is the test description"

class Test_Post_Review_For_Consumer:
     # Post with all fields passed
     def test_post_valid_all_fields(self):
          payload = {"consumer_id": CONSUMER_ID, "producer_id": PRODUCER_ID, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
          response = client.post("review_for_consumer/", json=payload)

          response_status_code = response.status_code
          response = review_for_consumer_response(**(response.json()))
          response = response.dict()

          assert response_status_code == 201
          assert response["producer_id"] == PRODUCER_ID
          assert response["consumer_id"] == CONSUMER_ID
          assert response["rating"] == RATING
          assert response["title"] == TITLE
          assert response["description"] == DESCRIPTION
     
     # Only one id passed, need a producer AND consumer id for posting a review
     @mark.parametrize("id, producer_or_consumer",[
          (PRODUCER_ID, "producer_id"),
          (CONSUMER_ID, "consumer_id")
     ])
     def test_post_only_one_id(self, id, producer_or_consumer):
          payload = {producer_or_consumer: id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
          response = client.post("review_for_consumer/", json=payload)
          assert response.status_code == 422
          assert raises(RequestValidationError)

          # Only one id passed, need a producer AND consumer id for posting a review
     @mark.parametrize("producer_id, consumer_id",[
          (INVALID_OBJECT_ID, CONSUMER_ID),
          (PRODUCER_ID, INVALID_OBJECT_ID)
     ])
     def test_post_invalid_id(self, producer_id, consumer_id):
          payload = {"producer_id": producer_id, "consumer_id": consumer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
          response = client.post("review_for_consumer/", json=payload)
          assert response.status_code == 400
          assert raises(HTTPException)

     # Post with empty id's
     @mark.parametrize("producer_id, consumer_id",[
          (PRODUCER_ID, ""),
          ("", CONSUMER_ID),
          ("", "")
     ])
     def test_post_empty_ids(self, producer_id, consumer_id):
          payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": RATING, "title": TITLE, "description": DESCRIPTION}
          response = client.post("review_for_consumer/", json=payload)
          assert response.status_code == 422
          assert raises(RequestValidationError)



# class Test_Review_for_Consumer:
#      # Get operation via id. Validating status code
#      @mark.parametrize("id, status, exception", [
#      (valid_id, 200, None),
#      (TOO_LONG_ID, 422, RequestValidationError),
#      (invalid_id, 404, HTTPException)])
#      def test_get_review_for_consumer_by_id(self, id, status, exception):
#           response = client.get("/review_for_consumer/"+id)
#           assert response.status_code == status
#           assert raises(exception)