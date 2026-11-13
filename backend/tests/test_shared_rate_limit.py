"""Tests for the shared rate-limit backend abstraction."""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import security_controls
from security_controls import (
    MemoryBackend,
    RateLimitUnavailable,
    RedisBackend,
    check_rate_limit,
    set_rate_limit_backend,
)


class FakeRedis:
    """Minimal stand-in for the Lua fixed-window command used in production."""

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}
        self.ttls: dict[str, int] = {}
        self.keys: list[str] = []
        self.fail = False

    def eval(self, _script, _numkeys, key, window):
        self.keys.append(key)
        if self.fail:
            raise ConnectionError("redis unavailable")
        count = self.counts.get(key, 0) + 1
        self.counts[key] = count
        ttl = self.ttls.get(key, int(window))
        if count == 1:
            self.ttls[key] = int(window)
        return [count, ttl]


@pytest.fixture(autouse=True)
def reset_backend():
    yield
    set_rate_limit_backend(None)


def make_request(ip="203.0.113.10") -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/auth/login",
            "headers": [],
            "client": (ip, 12345),
            "scheme": "http",
            "server": ("testserver", 80),
            "query_string": b"",
        }
    )


def test_memory_backend_enforces_boundary():
    backend = MemoryBackend()
    assert backend.hit("scope:user", 2, 60) == (True, 0)
    assert backend.hit("scope:user", 2, 60) == (True, 0)
    allowed, retry_after = backend.hit("scope:user", 2, 60)
    assert allowed is False
    assert retry_after >= 1
    # A different identity has its own window.
    assert backend.hit("scope:other", 2, 60) == (True, 0)


def test_redis_backends_share_windows_across_workers():
    fake = FakeRedis()
    worker_a = RedisBackend(fake)
    worker_b = RedisBackend(fake)

    assert worker_a.hit("login:alice", 3, 60)[0] is True
    assert worker_a.hit("login:alice", 3, 60)[0] is True
    assert worker_b.hit("login:alice", 3, 60)[0] is True
    allowed, retry_after = worker_b.hit("login:alice", 3, 60)
    assert allowed is False
    assert retry_after >= 1


def test_redis_keys_do_not_expose_identity():
    fake = FakeRedis()
    backend = RedisBackend(fake)
    backend.hit("login:alice@example.com:203.0.113.10", 5, 60)

    assert fake.keys
    stored_key = fake.keys[0]
    assert stored_key.startswith(security_controls.REDIS_KEY_PREFIX)
    assert "alice" not in stored_key
    assert "203.0.113.10" not in stored_key
    assert len(stored_key.split(":")[-1]) == 64


def test_redis_failure_falls_back_to_memory():
    fake = FakeRedis()
    fake.fail = True
    backend = RedisBackend(fake, fallback=MemoryBackend(), required=False)

    assert backend.hit("login:alice", 1, 60)[0] is True
    allowed, retry_after = backend.hit("login:alice", 1, 60)
    assert allowed is False
    assert retry_after >= 1


def test_redis_failure_can_fail_closed():
    fake = FakeRedis()
    fake.fail = True
    backend = RedisBackend(fake, required=True)
    with pytest.raises(RateLimitUnavailable):
        backend.hit("login:alice", 10, 60)


def test_check_rate_limit_returns_429_with_retry_after(monkeypatch):
    monkeypatch.setenv("SECURITY_RATE_LIMIT_ENABLED", "1")
    monkeypatch.setitem(security_controls.DEFAULT_RULES, "login", (1, 60))
    set_rate_limit_backend(MemoryBackend())
    request = make_request()

    check_rate_limit(request, "login", identity="alice")
    with pytest.raises(HTTPException) as error:
        check_rate_limit(request, "login", identity="alice")

    assert error.value.status_code == 429
    assert "Retry-After" in error.value.headers
    assert int(error.value.headers["Retry-After"]) >= 1


def test_check_rate_limit_returns_503_when_required_store_is_down(monkeypatch):
    monkeypatch.setenv("SECURITY_RATE_LIMIT_ENABLED", "1")
    fake = FakeRedis()
    fake.fail = True
    set_rate_limit_backend(RedisBackend(fake, required=True))

    with pytest.raises(HTTPException) as error:
        check_rate_limit(make_request(), "login", identity="alice")

    assert error.value.status_code == 503
    assert "temporarily unavailable" in error.value.detail.lower()
