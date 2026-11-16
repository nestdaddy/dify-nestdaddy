"""Tests for the NestDaddy Dify plugin.
Unit tests mock HTTP. Live tests run only when NESTDADDY_API_KEY is set:  pytest -q tests"""
import os
import sys

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import _client  # noqa: E402
from tools.news_search import NestDaddyNewsSearchTool  # noqa: E402
from tools.web_search import NestDaddyWebSearchTool  # noqa: E402


class FakeResp:
    def __init__(self, status, data):
        self.status_code, self._data = status, data

    def json(self):
        return self._data


def run(tool_cls, key, params):
    tool = tool_cls.from_credentials({"nestdaddy_api_key": key})
    return list(tool.invoke(tool_parameters=params))


def texts(msgs):
    return "\n".join(str(getattr(m.message, "text", "")) for m in msgs)


def jsons(msgs):
    return [m.message.json_object for m in msgs if hasattr(m.message, "json_object")]


def test_web_search_formats_results(monkeypatch):
    seen = {}

    def fake_get(url, params, timeout, headers):
        seen.update(url=url, params=params, headers=headers)
        return FakeResp(200, {"results": [{"title": "Python", "url": "https://python.org", "snippet": "Hi",
                                           "domain": "python.org", "extra": "x"}]})
    monkeypatch.setattr(_client.requests, "get", fake_get)
    msgs = run(NestDaddyWebSearchTool, "k1", {"query": " python ", "max_results": 500})
    assert seen["url"] == "https://nestdaddy.com/api/v1/search"
    assert seen["params"] == {"q": "python", "limit": 50}          # clamped
    assert seen["headers"]["X-API-Key"] == "k1"
    assert jsons(msgs)[0]["results"] == [{"title": "Python", "url": "https://python.org", "snippet": "Hi",
                                          "domain": "python.org"}]
    assert "https://python.org" in texts(msgs)


def test_news_search_params_and_bad_country(monkeypatch):
    seen = {}

    def fake_get(url, params, timeout, headers):
        seen.update(url=url, params=params)
        return FakeResp(200, {"results": []})
    monkeypatch.setattr(_client.requests, "get", fake_get)
    msgs = run(NestDaddyNewsSearchTool, "k1", {"query": "rates", "country": "usa; drop", "days": 0})
    assert seen["url"] == "https://nestdaddy.com/api/v1/news/search"
    assert seen["params"] == {"q": "rates", "days": 1, "limit": 10}  # bad country dropped, days clamped
    assert "No news" in texts(msgs)


def test_errors_are_readable_and_hide_the_key(monkeypatch):
    monkeypatch.setattr(_client.requests, "get",
                        lambda *a, **k: FakeResp(401, {"error": "invalid_api_key"}))
    out = texts(run(NestDaddyWebSearchTool, "secret-key-123", {"query": "x"}))
    assert "not valid" in out and "secret-key-123" not in out

    def boom(*a, **k):
        raise requests.Timeout("slow")
    monkeypatch.setattr(_client.requests, "get", boom)
    assert "did not answer in time" in texts(run(NestDaddyNewsSearchTool, "k", {"query": "x"}))


def test_empty_query_and_missing_key():
    assert "key words" in texts(run(NestDaddyWebSearchTool, "k", {"query": "  "}))
    assert "missing" in texts(run(NestDaddyWebSearchTool, "", {"query": "python"}))


LIVE_KEY = os.environ.get("NESTDADDY_API_KEY")


@pytest.mark.skipif(not LIVE_KEY, reason="no NESTDADDY_API_KEY")
def test_live_web_and_news():
    web = run(NestDaddyWebSearchTool, LIVE_KEY, {"query": "python programming", "max_results": 3})
    assert jsons(web)[0]["count"] >= 1
    news = run(NestDaddyNewsSearchTool, LIVE_KEY, {"query": "AI", "days": 7, "max_results": 3})
    assert jsons(news)[0]["count"] >= 1
