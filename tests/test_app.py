import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_request_prime_factorization(client):
    response = client.post("/request_prime_factorization", json={"number": 42})
    assert response.status_code == 200
    data = response.get_json()
    assert "request_id" in data
    assert isinstance(data["request_id"], int)


def test_invalid_request_prime_factorization(client):
    response = client.post("/request_prime_factorization", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No number provided"


def test_get_prime_factors(client):
    response = client.post("/request_prime_factorization", json={"number": 42})
    assert response.status_code == 200
    data = response.get_json()
    request_id = data["request_id"]

    assert request_id
    response = client.get(f"/prime_factors/{request_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "number" in data
    assert data["number"] == {"2": 1, "3": 1, "7": 1}


def test_invalid_get_prime_factors_request_id(client):
    response = client.get("/prime_factors/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid request_id"
