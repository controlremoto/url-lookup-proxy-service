import pytest
from src.services.url_lookup_service import UrlLookupService
from src.models.url import UrlInfo

class DummyRepo:
    def __init__(self, doc=None):
        self.doc = doc
    def find_url(self, hostname, path):
        if self.doc and self.doc['hostname'] == hostname and self.doc['path'] == path:
            return UrlInfo(**self.doc)
        return None

def test_lookup_found():
    repo = DummyRepo({'_id': '1', 'url': 'http://a.com/foo', 'hostname': 'a.com', 'path': 'foo', 'is_malicious': False})
    service = UrlLookupService(repo)
    result = service.lookup('a.com', 'foo')
    assert result is not None
    assert result.url == 'http://a.com/foo'

def test_lookup_not_found():
    repo = DummyRepo()
    service = UrlLookupService(repo)
    result = service.lookup('a.com', 'bar')
    assert result is None
