from fastapi.testclient import TestClient
from main import app,  Item
from database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends


client = TestClient(app)

def test_create_item(db: Session = Depends(get_db)):
    item = {"name": "Test Item", "description": "This is a test item"}
    response = client.post("/items/", json=item)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == item["name"]
    assert created_item["description"] == item["description"]
    assert created_item in db

""" def test_read_item():
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "description": "This is a test item"}

def test_delete_item():
    response = client.delete("/items/0")
    assert response.status_code == 200
    deleted_item = response.json()
    assert deleted_item == {"name": "Updated Item", "description": "This item has been updated"}
    assert db == [] """

# Optional: Clean up after all tests are done
def teardown_function():
    db.clear()