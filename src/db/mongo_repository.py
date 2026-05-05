import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Optional
from src.models.url import UrlInfo

class MongoRepository:
    def __init__(self, uri: Optional[str] = None, db_name: str = "urllookup", collection: str = "urls"):
        self.uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = db_name
        self.collection_name = collection
        self.client = MongoClient(self.uri)
        self.collection = self.client[self.db_name][self.collection_name]

    def find_url(self, hostname: str, path: str) -> Optional[UrlInfo]:
        try:
            doc = self.collection.find_one({"hostname": hostname, "path": path})
            if doc:
                return UrlInfo(**doc)
            return None
        except PyMongoError as e:
            # Logging will be added later
            return None