import pytest
import time
from fastapi.testclient import TestClient
from src.api.urlinfo import app, get_service

def test_lookup_success():
    class DummyUrlInfo:
        def dict(self, by_alias=True):
            return {'_id': '1', 'url': 'http://a.com/foo', 'hostname': 'a.com', 'path': 'foo', 'is_malicious': False}
    class DummyService:
        def lookup(self, h, p):
            return DummyUrlInfo()
    app.dependency_overrides[get_service] = lambda: DummyService()
    with TestClient(app) as client:
        response = client.get('/urlinfo/1/a.com/foo')
        assert response.status_code == 200
        assert response.json()['data']['url'] == 'http://a.com/foo'
    app.dependency_overrides = {}

def test_lookup_not_found():
    class DummyService:
        def lookup(self, h, p):
            return None
    app.dependency_overrides[get_service] = lambda: DummyService()
    with TestClient(app) as client:
        response = client.get('/urlinfo/1/a.com/bar')
        assert response.status_code == 200
        assert response.json()['data'] is None
    app.dependency_overrides = {}

def test_url_too_long():
    with TestClient(app) as client:
        long_path = 'a' * 2100
        response = client.get(f'/urlinfo/1/a.com/{long_path}')
        assert response.status_code == 400
        assert 'URL too long' in response.text


def test_unexpected_exception():
    # Override the service to raise an Exception to test the generic exception handler
    class FailingService:
        def lookup(self, h, p):
            raise Exception("Simulated unexpected error")
    app.dependency_overrides[get_service] = lambda: FailingService()
    with TestClient(app) as client:
        response = client.get('/urlinfo/1/a.com/foo')
        assert response.status_code == 500
        assert 'Simulated unexpected error' in response.text
    app.dependency_overrides = {}


def test_rate_limiter_exceeded(monkeypatch):
    # Patch _visits to simulate hitting the rate limit
    from src.utils import rate_limiter as rl_mod
    ip = 'test-ip'
    rl_mod._visits[ip] = [int(time.time())] * rl_mod.RATE_LIMIT
    class DummyRequest:
        client = type('obj', (), {'host': ip})
        headers = {}
        url = type('obj', (), {'path': '/urlinfo/1/a.com/foo'})
    with pytest.raises(Exception) as excinfo:
        rl_mod.rate_limiter(DummyRequest())
    assert excinfo.value.status_code == 429
    assert 'Rate limit exceeded' in str(excinfo.value.detail)
    rl_mod._visits.clear()
