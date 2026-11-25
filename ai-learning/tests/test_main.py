"""
LESSON 3: Testing with pytest (like xUnit).

Run all tests:   uv run pytest
More detail:     uv run pytest -v

Rules: test files start with "test_", test functions start with "test_",
and you check results with a plain "assert" (no Assert.Equal needed).
"""

import pytest
import app.main as main
from fastapi.testclient import TestClient

from app.main import app, surveys

client = TestClient(app)   # like WebApplicationFactory in ASP.NET tests


@pytest.fixture(autouse=True)
def clear_surveys():
    """Runs before every test, so each test starts with an empty list."""
    surveys.clear()
    main.next_id = 1     # ← reset the ID counter too

def test_list_is_empty_at_start():
    response = client.get("/surveys")
    assert response.status_code == 200
    assert response.json() == []


def test_create_survey():
    response = client.post("/surveys", json={"office": "Cebu", "rating": 5, "comment": "Fast service"})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["office"] == "Cebu"


def test_rating_out_of_range_is_rejected():
    response = client.post("/surveys", json={"office": "Cebu", "rating": 9})
    assert response.status_code == 422   # validation error, like a 400 from ModelState

def test_stats_average():
    client.post("/surveys", json={"office": "Cebu", "rating": 5})
    client.post("/surveys", json={"office": "Manila", "rating": 2})
    response = client.get("/stats")
    assert response.json() == {"count": 2, "average_rating": 3.5}

def test_low_rated_surveys():
    client.post("/surveys", json={"office": "Cebu", "rating": 5})
    client.post("/surveys", json={"office": "Manila", "rating": 2})
    response = client.get("/low-rated-surveys")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["office"] == "Manila"    

def test_delete_survey():
    client.post("/surveys", json={"office": "Cebu", "rating": 5})
    client.post("/surveys", json={"office": "Manila", "rating": 2})
    response = client.delete("/surveys/1")
    assert response.status_code == 200
    response = client.get("/surveys")
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 2    


def test_get_missing_survey_returns_404():
    response = client.get("/surveys/999")
    assert response.status_code == 404

def test_delete_missing_survey_returns_404():
    response = client.delete("/surveys/999")
    assert response.status_code == 404