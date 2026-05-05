# URL Lookup Service

A production-ready, containerized Python API for malware URL lookups, using MongoDB for persistence.

## Features
- FastAPI-based REST API
- MongoDB backend
- SOLID, Clean Architecture
- Logging & error handling
- Containerized (Docker, Docker Compose)
- 80%+ test coverage (pytest)
- Follows PEP8 and project guidelines

## Quickstart

### Prerequisites
- Docker & Docker Compose

### Run Locally
```sh
git clone <your-repo-url>
cd url-lookup-proxy-service
docker-compose up --build
```

API will be available at http://localhost:8000

### Run Tests
```sh
docker-compose run --rm app pytest --cov=src
```

## Project Structure
```
src/
  api/        # FastAPI endpoints
  db/         # MongoDB access
  models/     # Pydantic models
  services/   # Business logic
  utils/      # Logging, exceptions

tests/
  unit/
  integration/
  fixtures/
```

## Configuration
- Environment variables (see `docker-compose.yml`)
- `MONGO_URI` for MongoDB connection

## Linting & Formatting
```sh
black src
flake8 src
isort src
```

## Security
- Run `pip-audit` to check for vulnerabilities

## License
MIT
