# TICKETS API

A microservice to manage tickets

## Current features

- TDB


## Development

### Setup python environment

#### Pre requisites:

- [pyenv](https://github.com/pyenv/pyenv-installer)

- Python 3.10.0
  - Check lastest with: `$ pyenv install --list | grep " 3.10.0"`
  - Install with `$ pyenv install 3.10.x`

#### Install and setup virtualenv:

At project root directory:

```
$ pyenv virtualenv 3.10.x tickets-api
$ pyenv local tickets-api
```

### Install requirements

```
$ pip install -r requirements-dev.txt
$ pre-commit install
```

### Start the server locally

`$ uvicorn main:app --reload`

The server should start running on port 8000. A healthcheck endpoint is available via
HTTP **GET** at `http://localhost:8000/api/healthcheck/`

### Start the server with docker

At `dockerfiles` repo root directory:

`$ docker-compose -f docker-compose.extras.yml up -d tickets-api-service`

The server should start running on a docker container named `tickets-api`.
A healthcheck endpoint is available via HTTP **GET** at `http://tickets-api.docker/api/healthcheck/`

### Testing

Run `pytest -v` in project's root directory.


### Debugging

[Check FastAPI docs for debugging](https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger)
