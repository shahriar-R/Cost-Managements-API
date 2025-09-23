import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_non_existing_cost():
    """If a cost with a non-existing ID is requested,
    it should return 404 with an error message
    """
    response = client.get("/costs/999")
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "cost with Id 999 not found",
    }


def test_delete_non_existing_cost():
    """If a user tries to delete a non-existing cost,
    it should return 404 with an error message
    """
    response = client.delete("/costs/500")
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "cost with ID 500 not found",
    }


def test_get_existing_cost():
    """If a cost exists, it should return the cost details successfully"""
    response = client.get("/costs/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "amount" in data


def test_delete_existing_cost():
    """If a cost exists, it should be deleted successfully and no longer be retrievable"""

    response = client.get("/costs/1")
    assert response.status_code == 200

    response = client.delete("/costs/1")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "cost deleted"}

    response = client.get("/costs/1")
    assert response.status_code == 404
    assert "cost deleted" in response.json()["message"]
