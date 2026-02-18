from fastapi.testclient import TestClient
from main import app

client = TestClient(app, follow_redirects=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text

def test_add_todo():
    response = client.post("/add", data={"title": "Test Task"})
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    
    response = client.get("/")
    assert "Test Task" in response.text

def test_complete_todo():
    # Add a task first
    client.post("/add", data={"title": "Task to Complete"})
    
    # Assuming it's the second task (if test_add_todo ran) or first. 
    # Let's find its ID by checking the list or just use global state knowledge.
    # In-memory storage is shared in these tests.
    
    response = client.get("/complete/1")
    assert response.status_code == 303
    
def test_delete_todo():
    client.post("/add", data={"title": "Task to Delete"})
    response = client.get("/delete/1")
    assert response.status_code == 303
