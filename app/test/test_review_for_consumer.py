from _pytest.mark import param
from _pytest.monkeypatch import resolve
from _pytest.python_api import raises
from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette import status
from app.main import app
from app.config.database import review_for_consumer_collection
from pytest import mark, raises
from app.models.review_for_consumer_model import review_for_consumer_response
client = TestClient(app)

valid_id         = "61b465deae919a6d715cac2a"
invalid_id       = "111111111111111111111111"
unprocessable_id = "1111111111111111111111111"
consumer_id = "61b465c4ae919a6d715cac08"
producer_id = "61b465caae919a6d715cac0b"

class Test_Review_for_Consumer_Get_By_Id:
     # Successful call
     def test_get_review_for_consumer_by_id_in_db(self):
          response = client.get("/review_for_consumer/" + valid_id)
          response_model = review_for_consumer_response(**response.json())
          assert response.status_code == 200

     # Unavailable document
     def test_get_review_for_consumer_by_not_db(self):
          response = client.get("/review_for_consumer/" + invalid_id)
          assert response.status_code == 404
          assert raises(HTTPException)

     # Unprocessible id param
     def test_get_review_for_consumer_by_id_unprocessable(self):
          response = client.get("/review_for_consumer/" + unprocessable_id)
          assert response.status_code == 422
          assert raises(RequestValidationError)

class Test_Review_for_Consumer_Get_By_Consumer_And_Producer:
     def test_get_review_for_consumer_by_consumer_id_and_producer_id_valid(self):
          response = client.get("/review_for_consumer", params={"consumer_id": consumer_id, "producer_id": producer_id})
          assert response.status_code == 200

     @mark.parametrize("id, producer_or_consumer",[
          (producer_id, "producer_id"),
          (consumer_id, "consumer_id")
     ])
     def test_get_review_for_consumer_by_consumer_id_and_producer_id_only_one(self, id, producer_or_consumer):
          response = client.get("/review_for_consumer", params={producer_or_consumer: id})
          assert response.status_code == 422
          assert raises(RequestValidationError)

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