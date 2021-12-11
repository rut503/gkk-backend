from fastapi.testclient import TestClient
from starlette import status
from app.main import app
from app.config.database import review_for_consumer_collection

client = TestClient(app)

async def override_dependency(id: str):
     return {"id": id, "skip": 5, "limit": 10}

# #class Test_Review_for_Consumer:
# def test_get_review_for_consumer_by_id():
#     response = client.get("/review_for_consumer/619ef1aee1fce6757d17a7e5")
#     assert response.status_code == 200

# # Unprocessible 
# def test_get_review_for_consumer_by_id2():
#     response = client.get("/review_for_consumer/619ef1aee1fce6757d17a7e55")
#     assert response.status_code == 422

# def test_get_review_for_consumer_by_id3():
#     response = client.get("/review_for_consumer/519ef1aee1fce6757d17a7e5")
#     assert response.status_code == 404

def test_get_review_for_consumer_by_id():
    app.dependency_overrides[review_for_consumer_collection.find_one] = override_dependency
    response = client.get("/review_for_consumer/619ef1aee1fce6757d17a7e5")
    print(response.json())
    assert response.status_code == 200