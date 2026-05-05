from fastapi import FastAPI, HTTPException
from src.db.mongo_repository import MongoRepository
from src.services.url_lookup_service import UrlLookupService
from src.models.url import UrlInfo
from src.utils.logger import get_logger

app = FastAPI()
logger = get_logger("urlinfo-api")

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
                "metadata": {"source": "startup-seed"}
            },
            {
                "url": "http://good.com/safe",
                "hostname": "good.com:80",
                "path": "safe",
                "is_malicious": False,
                "metadata": {"source": "startup-seed"}
            }
        ]
        collection.insert_many(seed_data)
        logger.info("Seed data inserted at startup.")
    else:
        logger.info("Collection already populated. Skipping seed.")

# API endpoint to get URL info based on hostname and path
@app.get("/urlinfo/1/{hostname_and_port}/{original_path_and_query_string}")
def get_url_info(hostname_and_port: str, original_path_and_query_string: str):
    hostname = hostname_and_port  # For now, treat as hostname (port parsing can be added)
    path = original_path_and_query_string
    logger.info(f"Lookup request: hostname={hostname}, path={path}")
    url_info = service.lookup(hostname, path)
    if url_info:
        return {"data": url_info.dict(by_alias=True), "error": None}
    else:
        return {"data": None, "error": "URL not found in database"}
