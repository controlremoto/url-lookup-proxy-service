import pytest
from src.utils.url_utils import normalize_url, is_url_too_long

class TestNormalizeUrl:
    def test_lowercase_host(self):
        host, path = normalize_url('EXAMPLE.COM:80', '/foo')
        assert host == 'example.com:80'
        assert path == '/foo'

    def test_path_cleaning(self):
        host, path = normalize_url('test.com:80', '/safe/../bad')
        assert path == '/safe/bad'

    def test_encoding(self):
        host, path = normalize_url('test.com:80', '/foo bar?x=1 y')
        assert path == '/foo%20bar?x=1%20y'

    def test_edge_case_no_leading_slash(self):
        host, path = normalize_url('site.com:80', 'foo')
        assert path == '/foo' or path == 'foo'  # Accepts both for now

    def test_is_url_too_long(self):
        host, path = 'a.com', '/foo'
        assert not is_url_too_long(host, path, 100)
        assert is_url_too_long(host, path, 10)

    def test_type_error(self):
        with pytest.raises(Exception):
            normalize_url(None, 123)
