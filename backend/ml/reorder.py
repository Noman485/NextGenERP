import numpy as np
import pandas as pd

from .predict import SALES_PATH

DEFAULT_INVENTORY = {
    1: {"stock": 400, "lead_time": 5, "supplier": "ABC Traders"},
    2: {"stock": 150, "lead_time": 3, "supplier": "XYZ Stationers"},
    3: {"stock": 150, "lead_time": 2, "supplier": "Cool Foods"},
}

SERVICE_Z = 1.65
HORIZON = 7
REVIEW_PERIOD = 1


def calculate_reorder(stock, forecast, daily_sales_std, lead_time):
    forecast = np.array(forecast, dtype=float)

    safety = SERVICE_Z * daily_sales_std * np.sqrt(lead_time)

    coverage_days = min(
        lead_time + REVIEW_PERIOD,
        len(forecast)
    )

    demand_lt = forecast[:lead_time].sum()
    demand_coverage = forecast[:coverage_days].sum()

    reorder_point = demand_coverage + safety
    target_stock = forecast.sum() + safety

    qty = (
        max(0, int(np.ceil(target_stock - stock)))
        if stock <= reorder_point
        else 0
    )

    cumulative_demand = np.cumsum(forecast)
    exhausted_days = np.where(cumulative_demand > stock)[0]

    days_left = (
        int(exhausted_days[0] + 1)
        if len(exhausted_days) > 0
        else len(forecast)
    )

    urgent = days_left <= lead_time + REVIEW_PERIOD

    return {
        "forecast_demand": float(forecast.sum()),
        "demand_lt": float(demand_lt),
        "demand_coverage": float(demand_coverage),
        "safety_stock": float(safety),
        "reorder_point": float(reorder_point),
        "target_stock": float(target_stock),
        "reorder_quantity": int(qty),
        "days_left": int(days_left),
        "urgent": bool(urgent)
    }


def generate_reorder_recommendations(forecast_df, inventory=None):
    if inventory is None:
        inventory = DEFAULT_INVENTORY

    today = pd.Timestamp.today().normalize()
    sales_history = pd.read_csv(SALES_PATH, parse_dates=["date"])

    recommendations = []

    for pid, info in inventory.items():
        product_data = forecast_df[
            forecast_df["product_id"] == pid
        ].sort_values("date")

        if product_data.empty:
            continue

        predictions = product_data["predicted_demand"].to_numpy()

        lead_time = int(info.get("lead_time", 3))
        if len(predictions) < lead_time:
            continue

        past_sales = (
            sales_history[sales_history["product_id"] == pid]
            .sort_values("date")["sales"]
            .tail(60)
        )

        daily_std = past_sales.std()
        if pd.isna(daily_std):
            daily_std = 0

        result = calculate_reorder(
            int(info.get("stock", 0)),
            predictions,
            float(daily_std),
            lead_time
        )

        order_by = today + pd.Timedelta(
            days=max(
                0,
                result["days_left"] - lead_time - REVIEW_PERIOD
            )
        )

        result.update({
            "product_id": int(pid),
            "product": str(info.get("product") or product_data["product"].iloc[0]),
            "current_stock": int(info.get("stock", 0)),
            "lead_time": lead_time,
            "supplier": str(info.get("supplier", "Default Supplier")),
            "order_by": order_by.strftime("%Y-%m-%d"),
        })

        recommendations.append(result)

    return recommendations
