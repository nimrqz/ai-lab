import pytest, requests
from ailab import llm


class Resp:
    def __init__(self, data, status=200): self._d, self.status = data, status
    def raise_for_status(self):
        if self.status >= 400: raise requests.HTTPError("boom")
    def json(self): return self._d


def test_generate_returns_response(monkeypatch):
    seen = {}
    def fake_post(url, json, timeout):
        seen.update(url=url, json=json)
        return Resp({"response": "oi"})
    monkeypatch.setattr(llm.requests, "post", fake_post)
    assert llm.generate("p", json_mode=True, system="s") == "oi"
    assert seen["url"].endswith("/api/generate")
    assert seen["json"]["format"] == "json" and seen["json"]["system"] == "s"
    assert seen["json"]["stream"] is False


def test_generate_wraps_errors(monkeypatch):
    monkeypatch.setattr(llm.requests, "post", lambda *a, **k: Resp({}, 500))
    with pytest.raises(llm.LLMError):
        llm.generate("p")
