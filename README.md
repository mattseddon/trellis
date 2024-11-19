# trellis

## A set of prime factorization endpoints

### Routes 
#### /request_prime_factorization 

Accepts a POST request with a JSON body containing the caller's ID and a number to be prime factorized.

#### /prime_factors/<int:request_id> 

Accepts a GET request with a request_id and returns the prime factors of the number associated with that request_id.


### Setup instructions

In order to run, clone this repository and run the following commands from the foot directory:

```bash
❯ python3.12 -m venv .env
❯ source .env/bin/activate
❯ pip install "."
❯ flask --app src/app.py run
```

#### Testing

This repository is tested with pytest. To run the tests, run the following commands from the root directory:

```bash
❯ source .env/bin/activate
❯ pip install -e ".[tests]"
❯ pytest tests
```