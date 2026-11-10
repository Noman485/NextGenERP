# ML Demand Forecasting Integration

This document describes how the XGBoost demand-forecasting and reorder-recommendation module is integrated into NextGenERP.

## Overview

The ML module adds two capabilities to the ERP:

1. **7-day demand forecast** per trained product, using historical sales plus weather features.
2. **Smart reorder recommendations** using forecast demand, lead time, safety stock, reorder point, target stock, and current inventory.

The backend exposes the results through a single authenticated API endpoint, and the React frontend renders them on the **Forecasting** page.

## Architecture

```text
React Forecasting page
        |
        | GET /ml/insights (Bearer token)
        v
FastAPI routes/ml.py
        |
        +--> ml/service.py
                |
                +--> ml/predict.py   (loads demand_xgb.json + sales.csv, fetches weather)
                +--> ml/reorder.py   (calculates safety stock, reorder point, quantity)
        |
        +--> ERP product table (optional live-stock overlay by product name)
```

## Files added

| Path | Purpose |
| --- | --- |
| `backend/ml/predict.py` | Loads the trained XGBoost model, builds lag/rolling/calendar/weather features, and generates the 7-day forecast |
| `backend/ml/reorder.py` | Calculates safety stock, reorder point, target stock, days left, urgency, and recommended purchase quantity |
| `backend/ml/service.py` | Combines forecast and recommendation output into the API response shape |
| `backend/ml/train_store_item.py` | Reproducible training script: downloads the dataset, selects series, trains candidate objectives, and saves the artifacts below |
| `backend/ml/demand_xgb.json` | Trained XGBoost model artifact |
| `backend/ml/sales.csv` | Historical daily sales used for lag/rolling features and demand variability |
| `backend/ml/inventory.json` | Default stock/lead-time/supplier values generated for the forecasted series |
| `backend/ml/model_metadata.json` | Dataset, split, candidate metrics, feature importance, and selected product metadata |
| `backend/routes/ml.py` | FastAPI router for `GET /ml/insights`; overlays live ERP inventory when a product name matches |
| `frontend/src/pages/Forecasting.jsx` | React page showing summary cards, reorder recommendations, and daily forecast tables |

## Files changed

| Path | Change |
| --- | --- |
| `backend/main.py` | Registers the ML router |
| `backend/requirements.txt` | Adds `numpy`, `pandas`, `requests`, `xgboost`, and `scikit-learn` |
| `frontend/src/App.jsx` | Adds the Forecasting navigation item and route |
| `frontend/vite.config.js` | Proxies `/ml` requests to the backend during local development |
| `frontend/nginx.conf` | Proxies `/ml` requests to the backend in the containerized frontend |

## API

### `GET /ml/insights`

Requires `Authorization: Bearer <token>` like the other business-resource routes.

Response shape:

```json
{
  "summary": {
    "forecast_days": 7,
    "total_products": 20,
    "products_requiring_reorder": 3,
    "weather_source": "Open-Meteo (Live)"
  },
  "forecast": [
    {
      "date": "2026-11-12",
      "product_id": 1,
      "product": "Store 2 / Item 28",
      "rain_prob": 0.35,
      "temp": 27.4,
      "predicted_demand": 42.1
    }
  ],
  "recommendations": [
    {
      "product_id": 1,
      "product": "Store 2 / Item 28",
      "current_stock": 400,
      "forecast_demand": 280.5,
      "demand_lt": 180.2,
      "demand_coverage": 210.4,
      "safety_stock": 25.8,
      "reorder_point": 236.2,
      "target_stock": 306.3,
      "reorder_quantity": 0,
      "days_left": 7,
      "urgent": false,
      "lead_time": 5,
      "supplier": "ABC Traders",
      "order_by": "2026-11-13",
      "erp_product_id": null,
      "erp_sku": null
    }
  ]
}
```

When an ERP catalog product has the same name as a forecasted product, the recommendation uses the ERP product's current `stock_quantity`. In that case `erp_product_id`, `erp_sku`, and optionally `erp_reorder_level` are included.

## Model and data

- **Dataset:** [Store Item Demand Forecasting Challenge](https://www.kaggle.com/competitions/demand-forecasting-kernels-only) (Kaggle), loaded from a public GitHub mirror so no Kaggle login is required. It contains 5 years (2013–2017) of daily sales for 10 stores × 50 items.
- **Selection:** the 20 highest-volume store/item series are used; `sales.csv` contains their daily history.
- **Features:** short and long lags (`lag_1`, `lag_3`, `lag_7`, `lag_14`, `lag_21`, `lag_28`), rolling means/standard deviations, day-of-week, month, and weekend flag.
- **Model:** XGBoost with a time-based split (train before 2017-07-01, validation Jul–Sep 2017, test Oct–Dec 2017). Several objectives (Poisson, Tweedie, squared error, log-target) are compared and the best by validation WAPE is saved.
- **Held-out test metrics:** MAE **9.155**, RMSE **11.550**, R² **0.744**, WAPE **8.42%**, and **32.28%** lower MAE than the lag-7 baseline (MAE 13.518).
- **Weather:** fetched from Open-Meteo for the next 7 days. The training dataset has no weather signal, so `rain_prob`/`temp` have zero feature importance; they are kept for API/UI compatibility. If the weather request fails, the service falls back to `rain_prob = 0.2`, `temp = 28.0` and reports `weather_source: "Fallback"`.
- **Forecasting method:** predictions are generated recursively day by day, so short lags (`lag_1`, `lag_3`) are available for later days in the 7-day horizon.

## Reorder logic

For each forecasted product:

- `safety_stock = 1.65 × daily_sales_std × √lead_time`
- `reorder_point = demand_coverage + safety_stock`
- `target_stock = total_forecast_demand + safety_stock`
- `reorder_quantity = ceil(target_stock − current_stock)` when stock is at or below the reorder point, otherwise `0`
- `days_left` is the first forecast day on which cumulative demand exceeds current stock
- `urgent` is true when `days_left <= lead_time + review_period` (review period = 1 day)

## Local development

### Backend

```powershell
cd backend
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m ml.train_store_item   # optional: retrain the model
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

The training script downloads the dataset to `backend/ml/data/` (ignored by Git), trains the candidate models, and overwrites `demand_xgb.json`, `sales.csv`, `inventory.json`, and `model_metadata.json`.

The backend requires `DATABASE_URL` and `JWT_SECRET_KEY` (at least 32 characters). For a quick local run without PostgreSQL, `backend/.env` can use:

```env
DATABASE_URL=sqlite:///./nextgenerp.db
JWT_SECRET_KEY=<random-secret-at-least-32-characters>
```

### Frontend

```powershell
cd frontend
npm ci
npm run dev
```

Open <http://localhost:5173>, sign in, and choose **Forecasting** in the sidebar.

## Verification

- Backend tests: `.\venv\Scripts\python.exe -m pytest -q`
- API smoke test: sign in, then request `/ml/insights` with the bearer token.
- Frontend build: `npm run build`

## Limitations

- The model is trained on a public store/item dataset, not on this ERP's own sales history. It is not automatically retrained from ERP sales orders.
- Live inventory overlay matches ERP products by name, not by a stored model-product mapping. The dataset product names (`Store X / Item Y`) will not normally match ERP catalog names.
- Default inventory in `inventory.json` is generated for demo purposes; replace it with real stock, lead times, and suppliers for production.
- Forecast generation loads the model and fetches weather on each request; there is no cache yet.
- Retrain on real ERP data before using recommendations for actual purchasing decisions.

## Future improvements

- Store a product-to-model mapping instead of matching by name.
- Retrain from ERP sales orders and inventory transactions on a schedule.
- Cache forecast results for the day to reduce latency.
- Add confidence intervals and backtesting metrics to the Forecasting page.
- Generate purchase-order drafts directly from reorder recommendations.
