from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth.dependencies import require_admin
from database.connection import engine
from models.order import Order
from models.user import User
from schemas.admin import UserStatusUpdate
from services import analytics

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(require_admin)],
)


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/overview")
def admin_overview(db: Session = Depends(get_db)):
    return analytics.overview(db)


@router.get("/analytics/daily")
def admin_daily_sales(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return analytics.daily_sales(db, days=days)


@router.get("/analytics/monthly")
def admin_monthly_sales(
    year: int | None = Query(None, ge=2000, le=2100),
    db: Session = Depends(get_db),
):
    selected_year = year or datetime.now(timezone.utc).year
    return analytics.monthly_sales(db, year=selected_year)


@router.get("/analytics/yearly")
def admin_yearly_sales(
    years: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    return analytics.yearly_sales(db, years=years)


@router.get("/analytics/users")
def admin_user_sales(
    q: str | None = Query(None, max_length=120),
    sort: Literal["revenue", "orders", "username", "created_at"] = "revenue",
    direction: Literal["asc", "desc"] = "desc",
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return analytics.user_sales(
        db,
        query=q,
        sort=sort,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.get("/analytics/products")
def admin_product_sales(
    q: str | None = Query(None, max_length=120),
    sort: Literal["revenue", "units", "name", "stock"] = "revenue",
    direction: Literal["asc", "desc"] = "desc",
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return analytics.product_sales(
        db,
        query=q,
        sort=sort,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.get("/analytics/inventory")
def admin_inventory_analytics(db: Session = Depends(get_db)):
    return analytics.inventory_analytics(db)


@router.get("/analytics/suppliers")
def admin_supplier_purchases(
    q: str | None = Query(None, max_length=120),
    sort: Literal["purchase_expenditure", "orders", "name", "received"] = (
        "purchase_expenditure"
    ),
    direction: Literal["asc", "desc"] = "desc",
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return analytics.supplier_purchases(
        db,
        query=q,
        sort=sort,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.get("/users")
def admin_users(
    q: str | None = Query(None, max_length=120),
    sort: Literal["revenue", "orders", "username", "created_at"] = "revenue",
    direction: Literal["asc", "desc"] = "desc",
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return analytics.user_sales(
        db,
        query=q,
        sort=sort,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.get("/users/{user_id}")
def admin_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    summary = analytics.user_sales_summary(db, user.id)
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    orders.sort(
        key=lambda order: order.created_at
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    recent_orders = [
        {
            "id": order.id,
            "product_id": order.product_id,
            "product_name": order.product.name if order.product else None,
            "quantity": order.quantity,
            "total_amount": analytics.money(order.total_amount),
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }
        for order in orders[:20]
    ]

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role or "USER",
            "is_active": bool(user.is_active),
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login_at": (
                user.last_login_at.isoformat() if user.last_login_at else None
            ),
        },
        "sales_summary": summary
        or {
            "orders": 0,
            "realized_orders": 0,
            "completed_orders": 0,
            "cancelled_orders": 0,
            "revenue": 0.0,
            "average_order_value": 0.0,
        },
        "recent_orders": recent_orders,
    }


@router.put("/users/{user_id}/status")
def admin_set_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id and not payload.is_active:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own administrator account",
        )

    if user.role == "ADMIN" and not payload.is_active:
        active_admins = (
            db.query(User)
            .filter(User.role == "ADMIN", User.is_active.is_(True))
            .count()
        )
        if active_admins <= 1:
            raise HTTPException(
                status_code=400,
                detail="At least one active administrator account is required",
            )

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role or "USER",
        "is_active": bool(user.is_active),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
