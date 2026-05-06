import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from typing import Optional
from src.models.url import UrlInfo
from src.utils.logger import get_logger, log_json
from src.config.constants import MONGO_URI_ENV, DB_NAME, COLLECTION_NAME, DB_TIMEOUT_MS, LOGGER_NAME
import inspect

logger = get_logger(LOGGER_NAME)

class MongoRepository:
    def __init__(self, uri: Optional[str] = None, db_name: str = DB_NAME, collection: str = COLLECTION_NAME):
        self.uri = uri or os.getenv(MONGO_URI_ENV)
        self.db_name = db_name
        self.collection_name = collection
        self.client = MongoClient(self.uri, serverSelectionTimeoutMS=DB_TIMEOUT_MS)
        self.collection = self.client[self.db_name][self.collection_name]

    def find_url(self, hostname: str, path: str) -> Optional[UrlInfo]:
        try:
            doc = self.collection.find_one({"hostname": hostname, "path": path})
            if doc:
                url_info = UrlInfo(**doc)
                logger.info(f"MongoRepository.find_url: Found document for hostname={hostname}, path={path}")
                event = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
                log_json(
                    level="info",
                    service=LOGGER_NAME,
                    event=event,
                    hostname=hostname,
                    path=path,
                    document=url_info.model_dump(by_alias=True)
                )
                return url_info
            logger.warning(f"MongoRepository.find_url: No document found for hostname={hostname}, path={path}")
            return None
        except ServerSelectionTimeoutError as timeout_exc:
            logger.error(f"MongoDB query timed out after {DB_TIMEOUT_MS}ms for hostname={hostname}, path={path}: {timeout_exc}")
            return None
        except PyMongoError as e:
            logger.error(f"MongoDB error in find_url for hostname={hostname}, path={path}: {e}")
            return None