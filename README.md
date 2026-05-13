![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/controlremoto/url-lookup-proxy-service/ci.yml)
![Static Badge](https://img.shields.io/badge/python-v3.11-yellow?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/Docker-24.x-blue?style=flat&logo=docker)
![Static Badge](https://img.shields.io/badge/Mongodb-v6-green?style=flat&logo=mongodb)
![GitHub forks](https://img.shields.io/github/forks/controlremoto/url-lookup-proxy-service)


# URL Lookup Service

An HTTP proxy python API that scans traffic looking for malware URLs before allowing HTTP connections to be made. This proxy asks a service that maintains several databases of malware URLs if the resource being requested is known to contain malware.

## Features

- FastAPI-based REST API
- MongoDB backend
- SOLID, Clean Architecture
- Logging & error handling
- Containerized (Docker, Docker Compose)
- Follows PEP8 and project guidelines

## Requirements

- **Python**: 3.11 (see Dockerfile) 
- **Docker**: 24.x or newer (recommended)
- **Docker Compose**: v2.x (Compose V2 syntax)
- **MongoDB**: 6.0 (see docker-compose.yml)

> For local (non-Docker) development, you must have Python and MongoDB installed on your system.

## Quickstart

### Prerequisites

- Docker & Docker Compose (see above for versions)

### Environment Variables

| Variable              | Required | Default                  | Description                                 |
|-----------------------|----------|--------------------------|---------------------------------------------|
| MONGO_URI             | Yes      | mongodb://mongo:27017    | MongoDB connection string                   |
| MONGO_DB_NAME         | No       | urllookup                | MongoDB database name                       |
| MONGO_COLLECTION_NAME | No       | urls                     | MongoDB collection name                     |
| MONGO_USERNAME        | No       | (empty)                  | MongoDB username (if using auth)            |
| MONGO_PASSWORD        | No       | (empty)                  | MongoDB password (if using auth)            |
| API_PORT              | No       | 8000                     | API server port                             |
| LOG_LEVEL             | No       | INFO                     | Logging level (DEBUG, INFO, WARNING, etc.)  |
| RATE_LIMIT            | No       | 10                       | Requests per window (rate limiter)          |
| RATE_LIMIT_WINDOW     | No       | 60                       | Rate limit window (seconds)                 |
| ENV_NAME              | No       | local                    | Environment name (local, uat, prod, etc.)   |

---

## Running Locally Without Docker

You can run the API directly on your machine using a Python virtual environment. **MongoDB must be running and accessible.**

1. Install Python 3.11 and MongoDB 6.0 (or use a remote MongoDB instance).
2. Clone this repository and enter the project directory.
3. Create and activate a virtual environment:

   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

5. Copy and edit your environment variables:

   ```sh
   cp .env.example .env
   # Edit .env as needed (set MONGO_URI, etc.)
   ```

6. Ensure MongoDB is running and accessible at the URI you set in `.env`.
7. Start the API:

   ```sh
   uvicorn src.api.urlinfo:app --host 0.0.0.0 --port 8000
   ```

8. The API will be available at [http://localhost:8000](http://localhost:8000)

---

### Local Development

1. Copy the `.env.example` to `.env` and edit as needed (especially MONGO_URI if not using Docker).
2. Start the stack:

   ```sh
   cp .env.example .env
   docker compose up --build #Optionally add -d for detached mode
   ```

3. The API will be available at [http://localhost:8000](http://localhost:8000)

### UAT/Production

- Set environment variables via your CI/CD pipeline or GitHub Secrets (do not use `.env` in production).
- Use the same variable names as above.

---

## Automated Testing

This project uses `pytest` for automated tests. You can run all tests with one of the following commands:

**With Docker Compose (recommended for full integration):**

```sh
docker compose run --rm app pytest --cov=src --cov-report=term-missing
```

**Locally (virtualenv recommended):**

```sh
pytest --cov=src --cov-report=term-missing
```

> MongoDB must be running and accessible for integration tests. Unit tests do not require a live database.

---

## API Usage & Testing

### Endpoint

`GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}`

#### Example URLs (after seeding)

- [http://localhost:8000/urlinfo/1/malicious.com:80/bad](http://localhost:8000/urlinfo/1/malicious.com:80/bad)
- [http://localhost:8000/urlinfo/1/good.com:80/safe](http://localhost:8000/urlinfo/1/good.com:80/safe)

### Example: Test with curl

```sh
curl -i http://localhost:8000/urlinfo/1/malicious.com:80/bad
```

**Expected response:**

```json
HTTP/1.1 200 OK
date: Wed, 06 May 2026 17:33:22 GMT
server: uvicorn
content-length: 189
content-type: application/json

{"data":{"_id":"69fb74e2ca83e0e6abb7351f","url":"http://malicious.com/bad","hostname":"malicious.com:80","path":"bad","is_malicious":true,"metadata":{"source":"startup-seed"}},"error":null}
```

#### Not found example

```sh
curl -i http://localhost:8000/urlinfo/1/unknown.com:80/unknown
```

**Expected response:**

```json
HTTP/1.1 200 OK
date: Wed, 06 May 2026 17:34:28 GMT
server: uvicorn
content-length: 49
content-type: application/json

{"data":null,"error":"URL not found in database"}
```

### Browser Testing

- Open [http://localhost:8000/urlinfo/1/malicious.com:80/bad](http://localhost:8000/urlinfo/1/malicious.com:80/bad) in your browser.
- You should see a JSON response with the URL info if seeded, or `null` if not found.

---

## Data Model

MongoDB documents in the `urls` collection have the following structure:

```json
{
   "_id": "ObjectId",
   "url": "string",           // Full URL
   "hostname": "string",     // Hostname and port (e.g., "malicious.com:80")
   "path": "string",         // Path (e.g., "bad")
   "is_malicious": true,      // Boolean flag
   "metadata": {              // Optional metadata
      "source": "startup-seed"
   }
}
```

See `src/models/url.py` for the authoritative Pydantic model.

---

## Seed Data Behavior

- On API startup, if the MongoDB collection is empty, two records are inserted:
   - `http://malicious.com/bad` (malicious)
   - `http://good.com/safe` (not malicious)
- Both have a `metadata.source` field set to `startup-seed`.
- This seed data is intended **only for local/demo use**. In production, the collection should be pre-populated or managed externally.
- See `src/api/urlinfo.py` for the seeding logic.

---

## Tradeoffs & Unfinished Areas

- Rate limiting is basic and in-memory (not distributed or persistent).
- Error handling is present but not exhaustive for all edge cases.
- No authentication or authorization is implemented.
- Seed data is for demo/local only; production data management is not included.
- No admin UI or management endpoints.

---

## Multi-Environment & Secret Management

- **Local**: Uses `.env` file (never commit secrets!).
- **UAT/Prod**: Use GitHub Secrets or CI/CD to inject environment variables.
- **MongoDB Auth**: Set `MONGO_USERNAME` and `MONGO_PASSWORD` for secure deployments.

See the table above for all supported environment variables.
