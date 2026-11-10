import pandas as pd

from .predict import generate_forecast
from .reorder import generate_reorder_recommendations


def get_ml_results(inventory=None, forecast_df=None):
    if forecast_df is None:
        forecast_df = generate_forecast()

    weather_source = forecast_df.attrs.get("weather_source", "Unknown")
    recommendations = generate_reorder_recommendations(forecast_df, inventory=inventory)

    forecast_records = []
    for row in forecast_df.to_dict(orient="records"):
        forecast_records.append({
            "date": pd.Timestamp(row["date"]).strftime("%Y-%m-%d"),
            "product_id": int(row["product_id"]),
            "product": str(row["product"]),
            "rain_prob": float(row["rain_prob"]),
            "temp": float(row["temp"]),
            "predicted_demand": float(row["predicted_demand"])
        })

    return {
        "summary": {
            "forecast_days": int(forecast_df["date"].nunique()) if not forecast_df.empty else 0,
            "total_products": int(forecast_df["product_id"].nunique()) if not forecast_df.empty else 0,
            "products_requiring_reorder": sum(
                1 for item in recommendations if item["reorder_quantity"] > 0
            ),
            "weather_source": weather_source
        },
        "forecast": forecast_records,
        "recommendations": recommendations
    }
