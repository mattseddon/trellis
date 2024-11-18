import sympy
from flask import Flask, jsonify, request

app = Flask(__name__)

data_store = {}
request_counter = 1


@app.route("/request_prime_factorization/", methods=["POST"])
def request_prime_factorization():
    global request_counter
    number = request.json.get("number")
    if number is None:
        return jsonify({"error": "No number provided"}), 400

    request_id = request_counter
    prime_factors = sympy.factorint(number)
    data_store[request_id] = prime_factors
    request_counter += 1

    return jsonify({"request_id": request_id}), 200


@app.route("/prime_factors/<int:request_id>", methods=["GET"])
def get_prime_factorization(request_id):
    number = data_store.get(request_id)
    if number is None:
        return jsonify({"error": "Invalid request_id"}), 404

    return jsonify({"number": number}), 200


if __name__ == "__main__":
    app.run()
