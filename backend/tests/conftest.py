import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import event
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

_TEST_DATABASE_DIR = Path(tempfile.mkdtemp(prefix="nextgenerp-backend-tests-"))
_TEST_DATABASE_PATH = _TEST_DATABASE_DIR / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DATABASE_PATH.as_posix()}"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-never-use-outside-tests"
os.environ["SECURITY_RATE_LIMIT_ENABLED"] = "0"
os.environ["ENVIRONMENT"] = "test"
os.environ["CORS_ORIGINS"] = (
    "http://localhost:5173,http://localhost:8080,"
    "http://127.0.0.1:8080,https://erp.example.com"
)
# Never let a developer's shell key turn tests into real provider calls.
os.environ["ASSISTANT_LLM_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

from database.connection import Base, engine


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(connection, _record):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


import main


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    with TestClient(main.app) as test_client:
        response = test_client.post(
            "/auth/register",
            json={
                "username": "regression-user",
                "password": "regression-test-password",
            },
        )
        assert response.status_code == 201, response.text
        test_client.headers["Authorization"] = (
            f"Bearer {response.json()['access_token']}"
        )
        yield test_client


@pytest.fixture
def unauthenticated_client():
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture
def admin_client():
    from admin_provision import provision_admin

    with TestClient(main.app) as test_client:
        with Session(engine) as session:
            provision_admin(
                session,
                "test-admin",
                "test-admin-password-123",
                "test-admin@example.test",
            )
        response = test_client.post(
            "/auth/login",
            json={
                "username": "test-admin",
                "password": "test-admin-password-123",
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["user"]["role"] == "ADMIN"
        test_client.headers["Authorization"] = (
            f"Bearer {response.json()['access_token']}"
        )
        yield test_client


@pytest.fixture
def create_category(client):
    def create(name="Test category", description="Regression test category"):
        response = client.post(
            "/categories/",
            params={"name": name, "description": description},
        )
        assert response.status_code == 200, response.text
        return response.json()

    return create


@pytest.fixture
def create_product(client):
    def create(
        name="Test product",
        sku="TEST-SKU",
        stock_quantity=10,
        reorder_level=3,
        category_id=None,
    ):
        payload = {
            "name": name,
            "sku": sku,
            "price": 12.5,
            "stock_quantity": stock_quantity,
            "reorder_level": reorder_level,
            "category_id": category_id,
        }
        response = client.post("/products/", json=payload)
        assert response.status_code == 200, response.text
        return response.json()

    return create


@pytest.fixture
def create_supplier(client):
    def create(name="Test supplier"):
        response = client.post(
            "/suppliers/",
            json={
                "name": name,
                "email": "supplier@example.test",
                "phone": "5550100",
                "address": "Test address",
                "lead_time_days": 5,
                "performance_rating": 4.5,
            },
        )
        assert response.status_code == 200, response.text
        return response.json()

    return create


@pytest.fixture(scope="session")
def frontend_dist():
    """Return the built frontend assets, building them once when absent.

    Artifact checks (source maps, bundled secrets) inspect the real production
    build rather than a mock. The build is cached for the whole test session.
    """

    dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if not dist.is_dir():
        npm = shutil.which("npm")
        assert npm, "npm is required to build frontend/dist for artifact checks"
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=dist.parent,
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert result.returncode == 0, result.stderr[-2000:]
    return dist


@pytest.fixture(scope="session", autouse=True)
def remove_temporary_test_database():
    yield
    engine.dispose()
    shutil.rmtree(_TEST_DATABASE_DIR)
