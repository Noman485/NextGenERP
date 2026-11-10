"""Train a demand-forecasting model on the Store Item Demand dataset.

Dataset: Store Item Demand Forecasting Challenge (Kaggle)
Public mirror: https://github.com/jgonzalezab/Store-Item-Demand-Forecasting

The dataset contains 5 years of daily sales for 10 stores x 50 items. This
script selects the highest-volume series, builds lag/rolling/calendar features,
trains several XGBoost objectives with a time-based split, picks the best one by
validation WAPE, evaluates it on a held-out test period, and writes the model,
sales history, metadata, and default inventory used by the API.

Run from the backend directory:
    .\\venv\\Scripts\\python.exe -m ml.train_store_item
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from .predict import FEATURES

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TRAIN_CSV = DATA_DIR / "store_item_train.csv"

SALES_PATH = BASE_DIR / "sales.csv"
MODEL_PATH = BASE_DIR / "demand_xgb.json"
METADATA_PATH = BASE_DIR / "model_metadata.json"
INVENTORY_PATH = BASE_DIR / "inventory.json"

DATASET_URL = (
    "https://raw.githubusercontent.com/jgonzalezab/"
    "Store-Item-Demand-Forecasting/master/Data/train.csv"
)

TOP_SERIES = 20
TRAIN_END = "2017-07-01"
VAL_END = "2017-10-01"


def download_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if TRAIN_CSV.exists() and TRAIN_CSV.stat().st_size > 1_000_000:
        return

    print(f"Downloading dataset from {DATASET_URL} ...")
    response = requests.get(DATASET_URL, timeout=120)
    response.raise_for_status()
    TRAIN_CSV.write_bytes(response.content)
    print(f"Downloaded {TRAIN_CSV.stat().st_size / 1024 / 1024:.1f} MB")


def load_dataset() -> pd.DataFrame:
    download_dataset()
    print("Loading dataset ...")
    data = pd.read_csv(TRAIN_CSV, parse_dates=["date"])
    required = {"date", "store", "item", "sales"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {sorted(missing)}")

    data["store"] = pd.to_numeric(data["store"], errors="coerce")
    data["item"] = pd.to_numeric(data["item"], errors="coerce")
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
    data = data.dropna(subset=["date", "store", "item", "sales"])
    data = data[data["sales"] >= 0]
    return data


def select_series(data: pd.DataFrame):
    totals = (
        data.groupby(["store", "item"])["sales"]
        .agg(total_sales="sum", mean_sales="mean", std_sales="std")
        .reset_index()
    )
    totals["cv"] = totals["std_sales"] / totals["mean_sales"]
    totals = totals[totals["cv"].notna()]
    selected = totals.sort_values("total_sales", ascending=False).head(TOP_SERIES)

    rows = []
    inventory_series = []
    for product_id, record in enumerate(selected.itertuples(index=False), start=1):
        series = (
            data[(data["store"] == record.store) & (data["item"] == record.item)]
            .set_index("date")["sales"]
            .sort_index()
            .astype(float)
        )
        product_name = f"Store {int(record.store)} / Item {int(record.item)}"
        inventory_series.append(
            {
                "product_id": product_id,
                "store": int(record.store),
                "item": int(record.item),
                "product": product_name,
                "total_sales": float(record.total_sales),
                "cv": float(record.cv),
                "last_30_avg": float(series.tail(30).mean()),
            }
        )
        for date, sales in series.items():
            rows.append(
                {
                    "date": date,
                    "product_id": product_id,
                    "product": product_name,
                    "store": int(record.store),
                    "item": int(record.item),
                    "sales": float(sales),
                    "rain_prob": 0.2,
                    "temp": 28.0,
                }
            )

    return pd.DataFrame(rows), inventory_series


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["product_id", "date"]).copy()
    grouped = df.groupby("product_id")["sales"]

    for lag in (1, 3, 7, 14, 21, 28):
        df[f"lag_{lag}"] = grouped.shift(lag)

    df["roll_mean_7"] = grouped.transform(lambda series: series.shift(7).rolling(7).mean())
    df["roll_mean_28"] = grouped.transform(lambda series: series.shift(7).rolling(28).mean())
    df["roll_std_7"] = grouped.transform(lambda series: series.shift(7).rolling(7).std())
    df["roll_std_28"] = grouped.transform(lambda series: series.shift(7).rolling(28).std())
    df["dow"] = df["date"].dt.day_of_week
    df["month"] = df["date"].dt.month
    df["is_weekend"] = (df["dow"] >= 5).astype(int)

    return df.dropna(subset=FEATURES).reset_index(drop=True)


def evaluate(y_true, y_pred):
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "wape": float((y_true - y_pred).abs().sum() / y_true.sum()),
    }


def train_candidates(train, val, test):
    candidates = [
        ("poisson", {"objective": "count:poisson"}, False),
        ("tweedie_1.5", {"objective": "reg:tweedie", "tweedie_variance_power": 1.5}, False),
        ("tweedie_1.2", {"objective": "reg:tweedie", "tweedie_variance_power": 1.2}, False),
        ("log1p_square", {"objective": "reg:squarederror"}, True),
        ("square", {"objective": "reg:squarederror"}, False),
    ]

    results = []
    for name, params, log_target in candidates:
        train_target = np.log1p(train["sales"]) if log_target else train["sales"]
        val_target = np.log1p(val["sales"]) if log_target else val["sales"]

        model = XGBRegressor(
            n_estimators=2000,
            learning_rate=0.03,
            max_depth=7,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            early_stopping_rounds=50,
            **params,
        )
        model.fit(
            train[FEATURES],
            train_target,
            eval_set=[(val[FEATURES], val_target)],
            verbose=False,
        )

        val_pred = np.maximum(model.predict(val[FEATURES]), 0)
        test_pred = np.maximum(model.predict(test[FEATURES]), 0)
        if log_target:
            val_pred = np.maximum(np.expm1(val_pred), 0)
            test_pred = np.maximum(np.expm1(test_pred), 0)

        val_metrics = evaluate(val["sales"], val_pred)
        test_metrics = evaluate(test["sales"], test_pred)
        results.append(
            {
                "name": name,
                "params": params,
                "log_target": log_target,
                "model": model,
                "val": val_metrics,
                "test": test_metrics,
            }
        )
        print(
            f"{name:14s} VAL mae={val_metrics['mae']:7.3f} wape={val_metrics['wape']:6.2%} | "
            f"TEST mae={test_metrics['mae']:7.3f} rmse={test_metrics['rmse']:7.3f} "
            f"r2={test_metrics['r2']:6.3f} wape={test_metrics['wape']:6.2%}"
        )

    return results


def main():
    data = load_dataset()
    print(f"Rows loaded: {len(data):,}")

    sales, selected = select_series(data)
    print(f"Selected {len(selected)} series | rows: {len(sales):,}")
    print(f"Date range: {sales['date'].min().date()} to {sales['date'].max().date()}")

    sales.to_csv(SALES_PATH, index=False)
    print(f"Saved sales history: {SALES_PATH}")

    features = build_features(sales)
    train = features[features["date"] < pd.Timestamp(TRAIN_END)]
    val = features[
        (features["date"] >= pd.Timestamp(TRAIN_END))
        & (features["date"] < pd.Timestamp(VAL_END))
    ]
    test = features[features["date"] >= pd.Timestamp(VAL_END)]

    print(f"Train rows: {len(train):,} | Validation rows: {len(val):,} | Test rows: {len(test):,}")
    if min(len(train), len(val), len(test)) == 0:
        raise ValueError("Time-based split produced an empty dataset")

    baseline_mae = float(mean_absolute_error(test["sales"], test["lag_7"]))

    print("\nTraining candidate models ...")
    results = train_candidates(train, val, test)
    best = min(results, key=lambda result: result["val"]["wape"])

    print(f"\nBest model by validation WAPE: {best['name']}")
    best["model"].save_model(str(MODEL_PATH))
    print(f"Saved model: {MODEL_PATH}")

    importance = pd.Series(
        best["model"].feature_importances_, index=FEATURES
    ).sort_values(ascending=False)

    inventory = {}
    for row in selected:
        lead_time = 3 + (row["product_id"] % 5)
        # Vary stock coverage so the demo shows a mix of healthy and low-stock
        # products instead of every recommendation being "no reorder needed".
        stock_days = 4 + (row["product_id"] * 7) % 26
        inventory[str(row["product_id"])] = {
            "stock": int(np.ceil(max(row["last_30_avg"], 1.0) * stock_days)),
            "lead_time": int(lead_time),
            "supplier": f"Supplier {chr(64 + ((row['product_id'] - 1) % 6) + 1)}",
            "product": row["product"],
        }
    INVENTORY_PATH.write_text(json.dumps(inventory, indent=2), encoding="utf-8")

    metadata = {
        "dataset": {
            "name": "Store Item Demand Forecasting Challenge (Kaggle)",
            "url": DATASET_URL,
            "rows": int(len(data)),
            "date_range": {
                "start": str(sales["date"].min().date()),
                "end": str(sales["date"].max().date()),
            },
            "selection": {"top_series": TOP_SERIES},
        },
        "model": {
            "type": "XGBRegressor",
            "selected_candidate": best["name"],
            "objective": best["params"],
            "log_target": best["log_target"],
            "features": FEATURES,
            "n_estimators": 2000,
            "learning_rate": 0.03,
            "max_depth": 7,
        },
        "split": {
            "train_end": TRAIN_END,
            "validation_start": TRAIN_END,
            "test_start": VAL_END,
        },
        "metrics": {
            "baseline_mae": baseline_mae,
            **best["test"],
            "mae_improvement_pct": float(
                (baseline_mae - best["test"]["mae"]) / baseline_mae * 100
            ),
        },
        "candidates": [
            {
                "name": result["name"],
                "params": result["params"],
                "log_target": result["log_target"],
                "validation": result["val"],
                "test": result["test"],
            }
            for result in results
        ],
        "feature_importance": {key: float(value) for key, value in importance.items()},
        "products": selected,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("FINAL MODEL EVALUATION (held-out test)")
    print("=" * 60)
    print(f"Baseline MAE       : {baseline_mae:.3f}")
    print(f"XGBoost MAE        : {best['test']['mae']:.3f}")
    print(f"RMSE               : {best['test']['rmse']:.3f}")
    print(f"R2 Score           : {best['test']['r2']:.4f}")
    print(f"WAPE               : {best['test']['wape']:.2%}")
    print(f"MAE Improvement    : {(baseline_mae - best['test']['mae']) / baseline_mae * 100:.2f}%")
    print("=" * 60)
    print("\nTop feature importance:")
    print(importance.to_string())
    print(f"\nSaved metadata: {METADATA_PATH}")
    print(f"Saved inventory: {INVENTORY_PATH}")


if __name__ == "__main__":
    main()
