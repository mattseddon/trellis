# trellis

## A set of prime factorization endpoints

This take-home assignment was part of the [Trellis](https://runtrellis.com/) interview process. The task is described [here](https://trellis-ai.notion.site/Trellis-Infrastructure-Takehome-11c2aaed8f3e809bb761e273dbe9e130). It had to be completed within 3 hours and was sent to me > 30 minutes into the 3 hour time block I had scheduled to complete it.

## Why is this open-source?

I was ghosted after completing the following steps:

- An initial interview with the CEO.
- A live coding interview with the CTO.
- This take-home assignment.
- Another design patterns interview with a founding engineer.

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