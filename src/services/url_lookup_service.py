from src.db.mongo_repository import MongoRepository
from src.models.url import UrlInfo
from typing import Optional

class UrlLookupService:
    def __init__(self, repository: MongoRepository):
        self.repository = repository

    def lookup(self, hostname: str, path: str) -> Optional[UrlInfo]:
        return self.repository.find_url(hostname, path)
