import pytest
from app import app

# AI usage: test structure suggested by Claude Code

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Top Five" in response.data

def test_submit_valid(client):
    data = {
        "category": "Movies",
        "item1": "Inception",
        "item2": "Interstellar",
        "item3": "The Dark Knight",
        "item4": "Arrival",
        "item5": "Dune",
    }
    response = client.post("/", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Movies" in response.data

def test_submit_missing_item(client):
    # Incomplete form — should not add submission (redirects cleanly)
    data = {"category": "Books", "item1": "Dune", "item2": "", "item3": "", "item4": "", "item5": ""}
    response = client.post("/", data=data, follow_redirects=True)
    assert response.status_code == 200
