from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.connection import engine
from ml.predict import generate_forecast
from ml.reorder import load_inventory
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

    The forecast is generated once per request. Recommendations use live ERP
    stock when a catalog product matches a trained product name
    (case-insensitive). Other trained products fall back to the bundled
    inventory snapshot.
    """
    forecast_df = generate_forecast()

    product_names = {
        str(name) for name in forecast_df["product"].dropna().unique()
    }
    matched_products = (
        db.query(Product)
        .filter(
            func.lower(Product.name).in_(
                [name.lower() for name in product_names]
            )
        )
        .all()
        if product_names
        else []
    )
    name_to_product = {
        product.name.lower(): product for product in matched_products
    }

    default_inventory = load_inventory()
    inventory = {}
    for raw_product_id in forecast_df["product_id"].dropna().unique():
        product_id = int(raw_product_id)
        product_rows = forecast_df[forecast_df["product_id"] == product_id]
        if product_rows.empty:
            continue

        product_name = str(product_rows["product"].iloc[0])
        erp_product = name_to_product.get(product_name.lower())
        fallback = default_inventory.get(product_id, {})

        inventory[product_id] = {
            "stock": (
                int(erp_product.stock_quantity or 0)
                if erp_product is not None
                else int(fallback.get("stock", 0))
            ),
            "lead_time": int(fallback.get("lead_time", 3)),
            "supplier": str(fallback.get("supplier", "Default Supplier")),
            "product": product_name,
        }

    results = get_ml_results(inventory=inventory, forecast_df=forecast_df)

    for recommendation in results.get("recommendations", []):
        erp_product = name_to_product.get(
            str(recommendation.get("product", "")).lower()
        )
        recommendation["erp_product_id"] = (
            erp_product.id if erp_product else None
        )
        recommendation["erp_sku"] = erp_product.sku if erp_product else None
        if erp_product is not None and erp_product.reorder_level is not None:
            recommendation["erp_reorder_level"] = int(
                erp_product.reorder_level
            )

    return results
