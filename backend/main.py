import logging
import os
import re
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from database.connection import Base, engine
from database.migrations import ensure_schema
from models.audit_log import AuditLog
from models.category import Category
from models.refresh_token import RefreshToken
from models.user import User
from models.product import Product
from models.supplier import Supplier
from models.order import Order
from models.purchase_order import PurchaseOrder
from models.inventory_transaction import InventoryTransaction
from routes.products import router as product_router
from routes.categories import router as category_router
from routes.suppliers import router as supplier_router
from routes.orders import router as order_router
from routes.purchase_orders import router as purchase_order_router
from routes.inventory_transactions import router as inventory_transaction_router
from routes.auth import router as auth_router
from routes.ml import router as ml_router
from routes.assistant import router as assistant_router
from routes.admin import router as admin_router
from security_controls import apply_security_headers
from services.audit import reset_request_id, set_request_id

logger = logging.getLogger(__name__)
_REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{8,64}$")
_environment = os.getenv("ENVIRONMENT", "development").strip().lower()
_docs_enabled = _environment not in {"production", "prod"} or os.getenv(
    "ENABLE_API_DOCS", ""
).strip().lower() in {"1", "true", "yes"}
app = FastAPI(
    docs_url="/docs" if _docs_enabled else None,
    redoc_url="/redoc" if _docs_enabled else None,
    openapi_url="/openapi.json" if _docs_enabled else None,
)


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    apply_security_headers(request, response)
    return response


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Attach a request id to the request, audit trail and response headers."""

    incoming = request.headers.get("x-request-id", "")
    request_id = (
        incoming if _REQUEST_ID_PATTERN.fullmatch(incoming) else uuid.uuid4().hex
    )
    request.state.request_id = request_id
    token = set_request_id(request_id)
    try:
        response = await call_next(request)
    finally:
        reset_request_id(token)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, error: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": list(issue["loc"]),
                    "msg": issue["msg"],
                    "type": issue["type"],
                }
                for issue in error.errors()
            ],
            "request_id": getattr(request.state, "request_id", None),
        },
    )


cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
if "*" in cors_origins:
    raise RuntimeError("CORS_ORIGINS must list explicit origins; wildcards are not allowed.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)

Base.metadata.create_all(bind=engine)
ensure_schema()

from admin_provision import bootstrap_admin_from_env

bootstrap_admin_from_env()

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(order_router)
app.include_router(purchase_order_router)
app.include_router(inventory_transaction_router)
app.include_router(ml_router)
app.include_router(assistant_router)
app.include_router(admin_router)

@app.get("/")
def home():
    return {
        "message": "NextGenERP API is running!"
    }


@app.get("/health")
@app.get("/database-test", include_in_schema=False)
def database_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as error:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from error