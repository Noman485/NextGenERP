from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.connection import engine
from models.inventory_transaction import InventoryTransaction
from models.product import Product
from models.user import User
from schemas.inventory_transaction import (
    InventoryTransactionCreate,
    InventoryTransactionHistory,
)
from services.audit import inventory_state, record_audit
from services.inventory import change_stock


router = APIRouter(
    prefix="/inventory-transactions",
    tags=["Inventory Transactions"],
    dependencies=[Depends(get_current_user)],
)


def get_db():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=InventoryTransactionHistory)
def create_inventory_transaction(
    transaction_data: InventoryTransactionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = (
        db.query(Product)
        .filter(Product.id == transaction_data.product_id)
        .with_for_update()
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    transaction = change_stock(
        db,
        product,
        transaction_data.transaction_type,
        transaction_data.quantity,
        transaction_data.reason,
    )

    try:
        db.flush()
        record_audit(
            db,
            action="inventory.adjust",
            entity_type="inventory_transaction",
            entity_id=transaction.id,
            actor=current_user,
            after=inventory_state(transaction),
            request=request,
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(transaction)
    return {
        "id": transaction.id,
        "product_id": product.id,
        "product_name": product.name,
        "transaction_type": transaction.transaction_type,
        "quantity": transaction.quantity,
        "previous_stock": transaction.previous_stock,
        "new_stock": transaction.new_stock,
        "reason": transaction.reason,
        "created_at": transaction.created_at,
    }


@router.get("/", response_model=list[InventoryTransactionHistory])
def get_inventory_transactions(db: Session = Depends(get_db)):
    transactions = (
        db.query(InventoryTransaction, Product.name)
        .join(Product, InventoryTransaction.product_id == Product.id)
        .order_by(InventoryTransaction.created_at.desc(), InventoryTransaction.id.desc())
        .all()
    )

    return [
        {
            "id": transaction.id,
            "product_id": transaction.product_id,
            "product_name": product_name,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "previous_stock": transaction.previous_stock,
            "new_stock": transaction.new_stock,
            "reason": transaction.reason,
            "created_at": transaction.created_at,
        }
        for transaction, product_name in transactions
    ]


@router.delete("/{transaction_id}")
def delete_inventory_transaction(transaction_id: int):
    """Inventory history is an immutable audit trail."""

    raise HTTPException(
        status_code=405,
        detail="Inventory history records cannot be deleted",
    )
