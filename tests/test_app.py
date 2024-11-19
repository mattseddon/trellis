import asyncio

import pytest

from app import app, process_queues, stop_process_queues


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


def process_and_stop_queues(event_loop, task):
    event_loop.run_until_complete(asyncio.sleep(1))
    stop_process_queues()
    event_loop.run_until_complete(task)


def test_request_prime_factorization(client):
    response = client.post(
        "/request_prime_factorization", json={"caller_id": 100, "number": 42}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "request_id" in data
    assert isinstance(data["request_id"], str)


def test_invalid_request_prime_factorization(client):
    response = client.post("/request_prime_factorization", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No number provided"

    response = client.post("/request_prime_factorization", json={"number": 10})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No caller_id provided"

    response = client.post(
        "/request_prime_factorization", json={"number": "a", "caller_id": 100}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Number must be an integer"

    response = client.post(
        "/request_prime_factorization", json={"number": 10, "caller_id": "a"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "caller_id is invalid"


def test_get_prime_factors(client, event_loop):
    task = event_loop.create_task(process_queues())
    response = client.post(
        "/request_prime_factorization", json={"caller_id": 100, "number": 42}
    )
    assert response.status_code == 200
    data = response.get_json()
    request_id = data["request_id"]

    assert request_id
    process_and_stop_queues(event_loop, task)

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

    response = client.get("/prime_factors/a")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid request_id"
