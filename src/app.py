import asyncio
from collections import deque

import sympy
from flask import Flask, jsonify, request

app = Flask(__name__)

data_store: dict[str, dict[str, int]] = {}
request_counter = 1
queues: dict[str, deque] = {}
stop_event = asyncio.Event()


@app.route("/request_prime_factorization", methods=["POST"])
def request_prime_factorization():
    global request_counter

    number = request.json.get("number")
    caller_id = request.json.get("caller_id")
    if number is None:
        return jsonify({"error": "No number provided"}), 400

    if caller_id is None:
        return jsonify({"error": "No caller_id provided"}), 400

    request_id = request_counter

    if caller_id in queues:
        queues[caller_id].append((request_id, number))
    else:
        queues[caller_id] = deque([(request_id, number)])

    request_counter += 1

    return jsonify({"request_id": request_id}), 200


@app.route("/prime_factors/<int:request_id>", methods=["GET"])
def get_prime_factorization(request_id):
    number = data_store.get(request_id)
    if number is None:
        return jsonify({"error": "Invalid request_id"}), 404

    return jsonify({"number": number}), 200


async def process_queues():
    while not stop_event.is_set():
        for queue in queues.values():
            # take first item from each of the queues
            request_id, number = queue.popleft()
            prime_factors = sympy.factorint(number)
            data_store[request_id] = prime_factors
        await asyncio.sleep(1)


def stop_process_queues():
    stop_event.set()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(process_queues())
    app.run()
    loop.run_until_complete(task)
