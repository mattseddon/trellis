import asyncio
from collections import deque

import sympy
from flask import Flask, jsonify, request

app = Flask(__name__)


data_store: dict[int, dict[str, int]] = {}
request_counter = 1
queues: dict[str, deque[tuple[int, int]]] = {}
stop_event = asyncio.Event()


@app.route("/request_prime_factorization", methods=["POST"])
def request_prime_factorization():
    global request_counter

    valid_callers = [100, 200, 300]

    number = request.json.get("number")
    caller_id = request.json.get("caller_id")

    if number is None:
        return jsonify({"error": "No number provided"}), 400

    if caller_id is None:
        return jsonify({"error": "No caller_id provided"}), 400

    if not isinstance(number, int):
        return jsonify({"error": "Number must be an integer"}), 400

    if caller_id not in valid_callers:
        return jsonify({"error": "caller_id is invalid"}), 400

    request_id = request_counter

    if caller_id in queues:
        queues[caller_id].append((request_id, number))
    else:
        queues[caller_id] = deque([(request_id, number)])

    request_counter += 1

    return jsonify({"request_id": request_id}), 200


@app.route("/prime_factors/<int:request_id>", methods=["GET"])
def get_prime_factorization(request_id):
    if not (number := data_store.get(request_id)):
        return jsonify({"error": "Invalid request_id"}), 404

    return jsonify({"number": number}), 200


def process_oldest_client_item(queue: deque[tuple[int, int]]):
    request_id, number = queue.popleft()
    prime_factors = sympy.factorint(number)
    data_store[request_id] = prime_factors


async def process_queues():
    to_delete = []
    while not stop_event.is_set():
        for caller_id, queue in queues.items():
            if not queue:
                to_delete.append(caller_id)
                continue

            process_oldest_client_item(queue)

        while to_delete:
            caller_id = to_delete.pop()
            del queues[caller_id]

        if not queues:
            await asyncio.sleep(1)


def stop_process_queues():
    stop_event.set()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(process_queues())
    app.run()
    loop.run_until_complete(task)
