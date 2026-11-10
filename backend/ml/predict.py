import numpy as np
import pandas as pd
import requests
from pathlib import Path
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "demand_xgb.json"
SALES_PATH = BASE_DIR / "sales.csv"

FEATURES = [
    "product_id", "lag_7", "lag_14", "lag_28",
    "roll_mean_7", "roll_mean_28", "dow", "month",
    "is_weekend", "rain_prob", "temp"
]

HORIZON = 7


def get_weather(lat=21.1458, lon=79.0882, days=HORIZON):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_probability_max,temperature_2m_mean",
        "timezone": "Asia/Kolkata",
        "forecast_days": days
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()["daily"]

        weather = pd.DataFrame({
            "date": pd.to_datetime(data["time"]),
            "rain_prob": np.array(
                data["precipitation_probability_max"],
                dtype=float
            ) / 100,
            "temp": data["temperature_2m_mean"]
        })

        weather.attrs["weather_source"] = "Open-Meteo (Live)"
        return weather

    except Exception:
        weather = pd.DataFrame({
            "date": pd.date_range(
                pd.Timestamp.now().normalize(),
                periods=days
            ),
            "rain_prob": [0.2] * days,
            "temp": [28.0] * days
        })

        weather.attrs["weather_source"] = "Fallback"
        return weather


def generate_forecast(lat=21.1458, lon=79.0882, days=HORIZON):
    model = XGBRegressor()
    model.load_model(str(MODEL_PATH))

    hist = pd.read_csv(SALES_PATH, parse_dates=["date"])

    names = (
        hist.drop_duplicates("product_id")
        .set_index("product_id")["product"]
        .to_dict()
    )

    yesterday = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)

    hist["date"] = hist["date"] + (yesterday - hist["date"].max())

    weather = get_weather(lat, lon, days)
    weather_source = weather.attrs.get("weather_source", "Unknown")

    rows = []

    for pid, group in hist.groupby("product_id"):
        sales = group.set_index("date")["sales"].sort_index()

        for _, weather_row in weather.iterrows():
            date = weather_row["date"]

            rows.append({
                "date": date,
                "product_id": pid,
                "product": names[pid],
                "lag_7": sales.loc[date - pd.Timedelta(days=7)],
                "lag_14": sales.loc[date - pd.Timedelta(days=14)],
                "lag_28": sales.loc[date - pd.Timedelta(days=28)],
                "roll_mean_7": sales.loc[
                    date - pd.Timedelta(days=13):
                    date - pd.Timedelta(days=7)
                ].mean(),
                "roll_mean_28": sales.loc[
                    date - pd.Timedelta(days=34):
                    date - pd.Timedelta(days=7)
                ].mean(),
                "dow": date.day_of_week,
                "month": date.month,
                "is_weekend": int(date.day_of_week >= 5),
                "rain_prob": weather_row["rain_prob"],
                "temp": weather_row["temp"]
            })

    forecast = pd.DataFrame(rows)

    predictions = np.maximum(model.predict(forecast[FEATURES]), 0)

    forecast["predicted_demand"] = predictions

    forecast = forecast[
        [
            "date",
            "product_id",
            "product",
            "rain_prob",
            "temp",
            "predicted_demand"
        ]
    ]

    forecast.attrs["weather_source"] = weather_source
    return forecast
