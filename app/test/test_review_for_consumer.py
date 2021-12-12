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

valid_id         = "61b5d4c7ca41dca5232ac59b"
invalid_id       = "111111111111111111111111"
unprocessable_id = "1111111111111111111111111"
consumer_id = "61b5d4b3ca41dca5232ac579"
producer_id = "61b5d4b8ca41dca5232ac57c"

class Test_Get_By_Id:
     # Successful call
     def test_get_by_id_in_db(self):
          response = client.get("/review_for_consumer/" + valid_id)
          response_model = review_for_consumer_response(**response.json())
          assert response.status_code == 200

     # Unavailable document
     def test_get_by_id_not_in_db(self):
          response = client.get("/review_for_consumer/" + invalid_id)
          assert response.status_code == 404
          assert raises(HTTPException)

     # Unprocessible id param
     def test_get_by_unprocessable_id(self):
          response = client.get("/review_for_consumer/" + unprocessable_id)
          assert response.status_code == 422
          assert raises(RequestValidationError)

     # Invalid Id
     def test_get_by_invalid_id(self):
          response = client.get("/review_for_consumer/xxxxxxxxxxxxxxxxxxxxxxxx")
          assert response.status_code == 400
          assert raises(HTTPException)

     # Empty
     def test_get_by_empty_id(self):
          response = client.get("/review_for_consumer/")
          assert response.status_code == 405
          assert raises(WebSocketRequestValidationError)

class Test_Get_By_Consumer_And_Producer:
     def test_get_by_valid_consumer_id_and_producer_id(self):
          response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
          assert response.status_code == 200
          
          # Validating documents returned
          response = response.json()
          for document in response:
               response_model = review_for_consumer_response(**document)

     @mark.parametrize("id, producer_or_consumer",[
          (producer_id, "producer_id"),
          (consumer_id, "consumer_id")
     ])
     # fix this test, you can only pass one producer or consumer 
     def test_get_by_consumer_id_and_producer_id_only_one(self, id, producer_or_consumer):
          response = client.get("/review_for_consumer", params={producer_or_consumer: id})
          print(response.url)
          assert response.status_code == 422
          assert raises(RequestValidationError)

     @mark.parametrize("producer_id, consumer_id",[
          (producer_id, ""),
          ("", consumer_id),
          ("", "")
     ])
     def test_get_by_consumer_id_and_producer_id_one_is_empty(self, producer_id, consumer_id):
          response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
          assert response.status_code == 422
          assert raises(RequestValidationError)

     # send a valid id which returns an empty list

rating = 2
title = "This is a test for posting a review for consumer"
description = "This is the test description"

class Test_Post_Review_For_Consumer:
     def test_post(self):
          payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": rating, "title": title, "description": description}
          response = client.post("review_for_consumer/", json=payload)

          response_status_code = response.status_code
          response = review_for_consumer_response(**(response.json()))
          response = response.dict()

          assert response_status_code == 201
          assert response["producer_id"] == producer_id
          assert response["consumer_id"] == consumer_id
          assert response["rating"] == rating
          assert response["title"] == title
          assert response["description"] == description
     
     @mark.parametrize("id, producer_or_consumer",[
          (producer_id, "producer_id"),
          (consumer_id, "consumer_id")
     ])
     def test_post_only_one_id(self, id, producer_or_consumer):
          payload = {producer_or_consumer: id, "rating": rating, "title": title, "description": description}
          response = client.post("review_for_consumer/", json=payload)
          assert response.status_code == 422
          assert raises(RequestValidationError)

     @mark.parametrize("producer_id, consumer_id",[
          (producer_id, ""),
          ("", consumer_id),
          ("", "")
     ])
     def test_post_empty(self, producer_id, consumer_id):
          payload = {"consumer_id": consumer_id, "producer_id": producer_id, "rating": rating, "title": title, "description": description}
          response = client.post("review_for_consumer/", json=payload)
          assert raises(RequestValidationError)
          assert response.status_code == 422
         
# class Test_Review_for_Consumer:
#      # Get operation via id. Validating status code
#      @mark.parametrize("id, status, exception", [
#      (valid_id, 200, None),
#      (unprocessable_id, 422, RequestValidationError),
#      (invalid_id, 404, HTTPException)])
#      def test_get_review_for_consumer_by_id(self, id, status, exception):
#           response = client.get("/review_for_consumer/"+id)
#           assert response.status_code == status
#           assert raises(exception)