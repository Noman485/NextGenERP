from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.connection import engine
from ml.service import get_ml_results
from models.product import Product

router = APIRouter(
    prefix="/ml",
    tags=["ML Forecasting"],
    dependencies=[Depends(get_current_user)],
)


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/insights")
def get_ml_insights(db: Session = Depends(get_db)):
    """Return demand forecast and reorder recommendations.

    Recommendations are generated for the trained ML products. When a product with
    the same name exists in the ERP catalog, its current stock and reorder level are
    used to make the recommendation reflect live inventory.
    """
    # Baseline forecast from the ML model/training products
    base = get_ml_results()
    forecast_product_names = {item["product"] for item in base.get("recommendations", [])}

    # Overlay ERP inventory for matching products
    inventory = {}
    matched_products = (
        db.query(Product)
        .filter(Product.name.in_(list(forecast_product_names)))
        .all()
        if forecast_product_names
        else []
    )

    name_to_product = {p.name.lower(): p for p in matched_products}

    for rec in base.get("recommendations", []):
        pname = rec.get("product", "")
        erp = name_to_product.get(str(pname).lower())
        pid = rec.get("product_id")
        if erp:
            inventory[pid] = {
                "stock": int(erp.stock_quantity or 0),
                "lead_time": int(rec.get("lead_time", 3)),
                "supplier": rec.get("supplier", "Default Supplier"),
                "product": pname,
            }
        else:
            inventory[pid] = {
                "stock": int(rec.get("current_stock", 0)),
                "lead_time": int(rec.get("lead_time", 3)),
                "supplier": rec.get("supplier", "Default Supplier"),
                "product": pname,
            }

    if inventory:
        base = get_ml_results(inventory=inventory)
        # attach ERP linkage info
        for rec in base.get("recommendations", []):
            erp = name_to_product.get(str(rec.get("product", "")).lower())
            rec["erp_product_id"] = erp.id if erp else None
            rec["erp_sku"] = erp.sku if erp else None
            if erp and erp.reorder_level is not None:
                rec["erp_reorder_level"] = int(erp.reorder_level)

    return base
