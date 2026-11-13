"""Application-level security controls shared by the API.

The module is intentionally dependency-free so it can be imported from route
modules and from tests without pulling in the rest of the application.
"""

from __future__ import annotations

import hashlib
import logging
import os
import threading
import time
from dataclasses import dataclass

from fastapi import HTTPException, Request, status

# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

BASELINE_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(self), geolocation=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
}

API_CONTENT_SECURITY_POLICY = (
    "default-src 'self'; frame-ancestors 'none'; base-uri 'self'; "
    "object-src 'none'; form-action 'self'"
)

DOCS_PATHS = {"/docs", "/redoc", "/openapi.json"}


def apply_security_headers(request: Request, response) -> None:
    """Attach baseline headers to an outgoing response.

    The Swagger/Redoc HTML pages are excluded from the restrictive CSP because
    they load their own inline bootstrap assets. All API responses still get
    the non-CSP baseline headers.
    """

    for name, value in BASELINE_SECURITY_HEADERS.items():
        response.headers.setdefault(name, value)

    if request.url.path not in DOCS_PATHS:
        response.headers.setdefault(
            "Content-Security-Policy", API_CONTENT_SECURITY_POLICY
        )

    forwarded_proto = request.headers.get("x-forwarded-proto", "").lower()
    if request.url.scheme == "https" or forwarded_proto == "https":
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

DEFAULT_RULES = {
    # scope: (max requests, window in seconds)
    "login": (10, 60),
    "login_ip": (30, 60),
    "register": (5, 300),
    "register_ip": (20, 300),
    "assistant": (20, 60),
}

_ENV_OVERRIDES = {
    "login": "SECURITY_LOGIN_LIMIT",
    "login_ip": "SECURITY_LOGIN_IP_LIMIT",
    "register": "SECURITY_REGISTER_LIMIT",
    "register_ip": "SECURITY_REGISTER_IP_LIMIT",
    "assistant": "SECURITY_ASSISTANT_LIMIT",
}

REDIS_KEY_PREFIX = "nextgenerp:ratelimit:"

# Atomic fixed-window increment. The TTL is set on the first hit and repaired
# if a key somehow lost its expiry. Returning the TTL lets the API send an
# accurate Retry-After header.
REDIS_FIXED_WINDOW_SCRIPT = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
    return {current, tonumber(ARGV[1])}
end
local ttl = redis.call('TTL', KEYS[1])
if ttl < 0 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
    ttl = tonumber(ARGV[1])
end
return {current, ttl}
"""


@dataclass
class _Window:
    started_at: float
    count: int


class RateLimitUnavailable(RuntimeError):
    """Raised when a required shared limiter cannot be reached."""


class MemoryBackend:
    """Thread-safe fixed-window limiter for one process."""

    def __init__(self) -> None:
        self._windows: dict[str, _Window] = {}
        self._lock = threading.Lock()

    def hit(self, key: str, limit: int, window: int) -> tuple[bool, int]:
        now = time.monotonic()
        with self._lock:
            entry = self._windows.get(key)
            if entry is None or now - entry.started_at >= window:
                self._windows[key] = _Window(started_at=now, count=1)
                return True, 0
            entry.count += 1
            if entry.count <= limit:
                return True, 0
            retry_after = max(1, int(window - (now - entry.started_at)) + 1)
        return False, retry_after

    def reset(self) -> None:
        with self._lock:
            self._windows.clear()


class _UnavailableRedisClient:
    def eval(self, *_args, **_kwargs):
        raise ConnectionError("Redis client is not available")


class RedisBackend:
    """Shared fixed-window limiter backed by Redis.

    On a store failure the limiter either falls back to the in-process window
    (default, preserves availability while a single worker still limits) or
    fails closed when ``RATE_LIMIT_REDIS_REQUIRED`` is true. The choice is
    explicit and logged so operators can detect the degraded mode.
    """

    def __init__(
        self,
        client,
        *,
        fallback: MemoryBackend | None = None,
        required: bool = False,
    ) -> None:
        self._client = client
        self._fallback = fallback
        self._required = required

    def hit(self, key: str, limit: int, window: int) -> tuple[bool, int]:
        # Hash identities so account names and IP addresses are not written to
        # the shared store as plaintext keys.
        redis_key = REDIS_KEY_PREFIX + hashlib.sha256(key.encode("utf-8")).hexdigest()
        try:
            count, ttl = self._client.eval(
                REDIS_FIXED_WINDOW_SCRIPT, 1, redis_key, int(window)
            )
            count = int(count)
            ttl = int(ttl)
        except Exception:
            logger.warning(
                "Shared rate-limit store unavailable; %s",
                "failing closed (RATE_LIMIT_REDIS_REQUIRED is set)"
                if self._required
                else "using in-process fallback",
            )
            if self._required:
                raise RateLimitUnavailable from None
            if self._fallback is None:
                self._fallback = MemoryBackend()
            return self._fallback.hit(key, limit, window)

        if count <= limit:
            return True, 0
        return False, max(1, ttl if ttl > 0 else window)

    def reset(self) -> None:
        # Never delete shared production counters from request code. Tests that
        # inject a fake Redis backend can reset it directly.
        if self._fallback is not None:
            self._fallback.reset()


_backend: MemoryBackend | RedisBackend | None = None
_backend_lock = threading.Lock()


def _redis_required() -> bool:
    value = os.getenv("RATE_LIMIT_REDIS_REQUIRED", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _build_backend():
    url = os.getenv("RATE_LIMIT_REDIS_URL", "").strip()
    if not url:
        return MemoryBackend()

    memory = MemoryBackend()
    try:
        import redis  # type: ignore[import-not-found]

        client = redis.Redis.from_url(
            url,
            socket_connect_timeout=1,
            socket_timeout=1,
            decode_responses=True,
        )
    except Exception:
        logger.error(
            "RATE_LIMIT_REDIS_URL is set but the Redis client is unavailable; %s",
            "rate limiting will fail closed"
            if _redis_required()
            else "using the in-process fallback",
        )
        client = _UnavailableRedisClient()

    return RedisBackend(client, fallback=memory, required=_redis_required())


def get_rate_limit_backend():
    global _backend
    with _backend_lock:
        if _backend is None:
            _backend = _build_backend()
        return _backend


def set_rate_limit_backend(backend) -> None:
    """Replace the limiter backend (tests and controlled operations)."""

    global _backend
    with _backend_lock:
        _backend = backend


def _enabled() -> bool:
    value = os.getenv("SECURITY_RATE_LIMIT_ENABLED", "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def _rule(scope: str) -> tuple[int, int]:
    limit, window = DEFAULT_RULES[scope]
    override = os.getenv(_ENV_OVERRIDES.get(scope, ""), "").strip()
    if override.isdigit() and int(override) > 0:
        limit = int(override)
    return limit, window


def client_ip(request: Request) -> str:
    """Return the direct client address.

    Forwarded headers are deliberately not trusted: the deployment terminates
    traffic at a local reverse proxy, and trusting X-Forwarded-For without a
    configured trusted-proxy list would let callers forge their identity.
    """

    return request.client.host if request.client else "unknown"


def check_rate_limit(
    request: Request,
    scope: str,
    identity: str | None = None,
) -> None:
    """Raise HTTP 429 when ``identity`` exceeds the rule for ``scope``."""

    if not _enabled():
        return

    limit, window = _rule(scope)
    key = f"{scope}:{identity or client_ip(request)}"

    try:
        allowed, retry_after = get_rate_limit_backend().hit(key, limit, window)
    except RateLimitUnavailable:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rate limiting is temporarily unavailable. Please try again later.",
        ) from None

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(max(1, retry_after))},
        )


def reset_rate_limits() -> None:
    """Clear the active limiter store (used by tests and deliberate operations)."""

    backend = get_rate_limit_backend()
    reset = getattr(backend, "reset", None)
    if reset is not None:
        reset()
