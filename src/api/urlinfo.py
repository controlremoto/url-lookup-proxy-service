from fastapi import FastAPI, HTTPException, Request, Depends, status
from src.db.mongo_repository import MongoRepository
from src.services.url_lookup_service import UrlLookupService
from src.models.url import UrlInfo
from src.utils.logger import get_logger
from src.utils.rate_limiter import rate_limiter
from src.utils.url_utils import normalize_url
from src.config.constants import URL_LENGTH_LIMIT, SEED_SOURCE, LOGGER_NAME

app = FastAPI()
logger = get_logger(LOGGER_NAME)

# Dependency injection
repository = MongoRepository()
service = UrlLookupService(repository)

# Seed the database with initial data on startup if the collection is empty
@app.on_event("startup")
def startup_event():
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

# API endpoint to get URL info based on hostname and path

@app.get("/urlinfo/1/{hostname_and_port}/{original_path_and_query_string}")
def get_url_info(
    hostname_and_port: str,
    original_path_and_query_string: str,
    request: Request,
    _: None = Depends(rate_limiter)
):
    client_ip = request.client.host
    headers = dict(request.headers)
    logger.info(f"Received request from {client_ip}, headers: {headers}")
    try:
        url = normalize_url(hostname_and_port, original_path_and_query_string)
        if len(url) > URL_LENGTH_LIMIT:
            logger.error(f"URL too long: {url}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="URL too long")
        url_info = service.lookup(hostname_and_port, original_path_and_query_string)
        if url_info:
            return {"data": url_info.dict(by_alias=True), "error": None}
        else:
            return {"data": None, "error": "URL not found in database"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
