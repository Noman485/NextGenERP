"""Application-level security controls shared by the API.

The module is intentionally dependency-free so it can be imported from route
modules and from tests without pulling in the rest of the application.
"""

from __future__ import annotations

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


@dataclass
class _Window:
    started_at: float
    count: int


_windows: dict[str, _Window] = {}
_lock = threading.Lock()


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
    """Raise HTTP 429 when ``identity`` exceeds the rule for ``scope``.

    This is a fixed-window in-process limiter. It protects a single backend
    process; multi-worker deployments need a shared store (see the security
    report's residual risks).
    """

    if not _enabled():
        return

    limit, window = _rule(scope)
    key = f"{scope}:{identity or client_ip(request)}"
    now = time.monotonic()

    with _lock:
        entry = _windows.get(key)
        if entry is None or now - entry.started_at >= window:
            _windows[key] = _Window(started_at=now, count=1)
            return
        entry.count += 1
        if entry.count <= limit:
            return
        retry_after = max(1, int(window - (now - entry.started_at)) + 1)

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Too many requests. Please try again later.",
        headers={"Retry-After": str(retry_after)},
    )


def reset_rate_limits() -> None:
    """Clear the limiter store (used by tests and by deliberate operations)."""

    with _lock:
        _windows.clear()
