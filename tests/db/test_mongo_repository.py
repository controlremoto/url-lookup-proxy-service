from src.db.mongo_repository import MongoRepository
from pymongo.errors import ServerSelectionTimeoutError
import pytest
from src.models.url import UrlInfo

def test_find_url_server_selection_timeout(monkeypatch):
    repo = MongoRepository(uri="mongodb://localhost:27017", db_name="testdb", collection="testcol")
    # Patch collection.find_one to raise ServerSelectionTimeoutError
    class DummyCollection:
        def find_one(self, query):
            raise ServerSelectionTimeoutError("timed out")
    repo.collection = DummyCollection()
    result = repo.find_url("host", "path")
    assert result is None


def test_find_url_pymongo_error():
    from pymongo.errors import PyMongoError
    repo = MongoRepository(uri="mongodb://localhost:27017", db_name="testdb", collection="testcol")
    class DummyCollection:
        def find_one(self, query):
            raise PyMongoError("simulated pymongo error")
    repo.collection = DummyCollection()
    result = repo.find_url("host", "path")
    assert result is None

class DummyCollection:
    def __init__(self, doc=None):
        self.doc = doc
    def find_one(self, query):
        if self.doc and self.doc['hostname'] == query['hostname'] and self.doc['path'] == query['path']:
            return self.doc
        return None

class DummyClient:
    def __getitem__(self, db_name):
        return { 'urls': DummyCollection(self.doc) }
    def __init__(self, doc=None):
        self.doc = doc


def test_find_url_found(monkeypatch):
    repo = MongoRepository()
    repo.client = DummyClient({'_id': '1', 'url': 'http://a.com/foo', 'hostname': 'a.com', 'path': 'foo', 'is_malicious': False})
    repo.collection = repo.client['urllookup']['urls']
    result = repo.find_url('a.com', 'foo')
    assert isinstance(result, UrlInfo)
    assert result.url == 'http://a.com/foo'

def test_find_url_not_found(monkeypatch):
    repo = MongoRepository()
    repo.client = DummyClient()
    repo.collection = repo.client['urllookup']['urls']
    result = repo.find_url('a.com', 'bar')
    assert result is None
