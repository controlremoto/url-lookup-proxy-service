from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends, status
from src.db.mongo_repository import MongoRepository
from src.services.url_lookup_service import UrlLookupService
from src.models.url import UrlInfo
from src.utils.logger import get_logger
from src.utils.rate_limiter import rate_limiter
from src.utils.url_utils import normalize_url, is_url_too_long
from src.config.constants import URL_LENGTH_LIMIT, SEED_SOURCE, LOGGER_NAME

logger = get_logger(LOGGER_NAME)


# Dependency injection
repository = MongoRepository()
service = UrlLookupService(repository)

# Provider function for dependency injection
def get_service() -> UrlLookupService:
    return service

# Seed the database with initial data on startup if the collection is empty
@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = repository.collection
    if collection.count_documents({}) == 0:
        seed_data = [
            {
                "url": "http://malicious.com/bad",
                "hostname": "malicious.com:80",
                "path": "bad",
                "is_malicious": True,
                "metadata": {"source": SEED_SOURCE}
            },
            {
                "url": "http://good.com/safe",
                "hostname": "good.com:80",
                "path": "safe",
                "is_malicious": False,
                "metadata": {"source": SEED_SOURCE}
            }
        ]
        collection.insert_many(seed_data)
        logger.info("Seed data inserted at startup.")
    else:
        logger.info("Collection already populated. Skipping seed.")
    yield

app = FastAPI(lifespan=lifespan)

# API endpoint to get URL info based on hostname and path

@app.get("/urlinfo/1/{hostname_and_port}/{original_path_and_query_string}")
def get_url_info(
    hostname_and_port: str,
    original_path_and_query_string: str,
    request: Request,
    _: None = Depends(rate_limiter),
    service: UrlLookupService = Depends(get_service)
):
    client_ip = request.client.host
    headers = dict(request.headers)
    logger.info(f"Received request from {client_ip}, headers: {headers}")
    try:
        norm_host, norm_path_query = normalize_url(hostname_and_port, original_path_and_query_string)
        if is_url_too_long(norm_host, norm_path_query, URL_LENGTH_LIMIT):
            logger.error(f"URL too long: host={norm_host}, path={norm_path_query}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="URL too long")
        url_info = service.lookup(norm_host, norm_path_query)
        if url_info:
            return {"data": url_info.dict(by_alias=True), "error": None}
        else:
            return {"data": None, "error": "URL not found in database"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
