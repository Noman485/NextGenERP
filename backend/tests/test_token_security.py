"""Regression tests for refresh-token rotation, revocation and reuse detection."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.orm import Session

from auth.tokens import hash_refresh_token
from database.connection import engine
from models.audit_log import AuditLog
from models.refresh_token import RefreshToken
from models.user import User

USERNAME = "regression-user"
PASSWORD = "regression-test-password"


def login_tokens(http):
    response = http.post(
        "/auth/login",
        json={"username": USERNAME, "password": PASSWORD},
    )
    assert response.status_code == 200, response.text
    return response.json()


def refresh(http, token):
    return http.post("/auth/refresh", json={"refresh_token": token})


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def audit_actions(**filters):
    with Session(engine) as session:
        query = session.query(AuditLog)
        for key, value in filters.items():
            query = query.filter(getattr(AuditLog, key) == value)
        return [row.action for row in query.order_by(AuditLog.id).all()]


def test_login_returns_refresh_metadata(client):
    body = login_tokens(client)
    assert body["token_type"].lower() == "bearer"
    assert body["expires_in"] == 1800
    assert len(body["access_token"].split(".")) == 3
    assert isinstance(body["refresh_token"], str)
    assert len(body["refresh_token"]) >= 40
    assert body["refresh_token"] != body["access_token"]


def test_refresh_rotates_and_reuse_revokes_family(client):
    first = login_tokens(client)
    rotated = refresh(client, first["refresh_token"])
    assert rotated.status_code == 200, rotated.text
    second = rotated.json()
    assert second["refresh_token"] != first["refresh_token"]
    assert second["access_token"] != first["access_token"]

    assert client.get("/auth/me", headers=bearer(second["access_token"])).status_code == 200

    reuse = refresh(client, first["refresh_token"])
    assert reuse.status_code == 401

    # Reuse detection must revoke the child token and the bound access token.
    assert refresh(client, second["refresh_token"]).status_code == 401
    assert client.get("/auth/me", headers=bearer(second["access_token"])).status_code == 401
    assert "auth.refresh_reuse_detected" in audit_actions(outcome="denied")


def test_logout_revokes_access_and_refresh_tokens(client):
    body = login_tokens(client)
    access_token = body["access_token"]
    refresh_token = body["refresh_token"]

    response = client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert response.status_code == 200, response.text

    assert client.get("/auth/me", headers=bearer(access_token)).status_code == 401
    assert refresh(client, refresh_token).status_code == 401

    # Idempotent: repeating logout is not an error and does not reveal state.
    assert (
        client.post("/auth/logout", json={"refresh_token": refresh_token}).status_code
        == 200
    )
    assert "auth.logout" in audit_actions()


def test_unknown_refresh_token_is_rejected_and_audited(unauthenticated_client):
    response = refresh(unauthenticated_client, "unknown-token-" + "x" * 50)
    assert response.status_code == 401
    assert "Invalid or expired refresh token" in response.json()["detail"]
    assert "auth.refresh_failed" in audit_actions(outcome="failure")


def test_expired_refresh_token_is_rejected(client):
    body = login_tokens(client)
    with Session(engine) as session:
        entry = (
            session.query(RefreshToken)
            .filter(RefreshToken.token_hash == hash_refresh_token(body["refresh_token"]))
            .one()
        )
        entry.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        session.commit()

    assert refresh(client, body["refresh_token"]).status_code == 401


def test_deactivated_user_cannot_refresh(client):
    body = login_tokens(client)
    with Session(engine) as session:
        user = session.query(User).filter(User.username == USERNAME).one()
        user.is_active = False
        session.commit()

    assert refresh(client, body["refresh_token"]).status_code == 401


def test_refresh_token_is_stored_only_as_a_hash(client):
    body = login_tokens(client)
    raw = body["refresh_token"]
    with Session(engine) as session:
        entry = (
            session.query(RefreshToken)
            .filter(RefreshToken.token_hash == hash_refresh_token(raw))
            .one()
        )
        assert entry.token_hash != raw
        assert len(entry.token_hash) == 64
        for column in (
            entry.token_hash,
            entry.family_id,
            entry.user_agent,
            entry.ip_address,
        ):
            assert column is None or raw not in str(column)


def test_legacy_access_token_without_sid_remains_valid(client):
    """Document the compatibility window for tokens minted before rotation."""

    user_id = client.get("/auth/me").json()["id"]
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=5),
        },
        os.environ["JWT_SECRET_KEY"],
        algorithm="HS256",
    )
    response = client.get("/auth/me", headers=bearer(token))
    assert response.status_code == 200, response.text


def test_refresh_request_rejects_malformed_values(client):
    assert client.post("/auth/refresh", json={"refresh_token": ""}).status_code == 422
    assert client.post("/auth/refresh", json={"refresh_token": "short"}).status_code == 422
    assert client.post("/auth/refresh", json={}).status_code == 422
