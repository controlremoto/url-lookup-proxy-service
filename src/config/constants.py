import os
# Environment
ENV_NAME_ENV = "ENV_NAME"  # local, uat, prod

# Database
MONGO_URI_ENV = "MONGO_URI"
MONGO_DB_NAME_ENV = "MONGO_DB_NAME"
MONGO_COLLECTION_NAME_ENV = "MONGO_COLLECTION_NAME"
MONGO_USERNAME_ENV = "MONGO_USERNAME"
MONGO_PASSWORD_ENV = "MONGO_PASSWORD"
DB_TIMEOUT_MS = 3000


# API
API_PORT = int(os.getenv("API_PORT", 8000))
URL_LENGTH_LIMIT = 2048


# Rate Limiter
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))  # seconds


# Seed Data
SEED_SOURCE = "startup-seed"


# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGER_NAME = "urlinfo-api"