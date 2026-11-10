import { useEffect, useState } from 'react';
import { apiFetch } from '../api';

function formatNumber(value, digits = 0) {
  const n = Number(value);
  if (!Number.isFinite(n)) return '-';
  return n.toLocaleString('en-IN', { maximumFractionDigits: digits, minimumFractionDigits: digits });
}

export default function Forecasting() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadInsights() {
    setLoading(true);
    setError('');
    try {
      const response = await apiFetch('/ml/insights');
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.detail || `Failed to load ML insights (HTTP ${response.status}).`);
      }
      setData(payload);
    } catch (err) {
      setError(err.message || 'Failed to load ML insights.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInsights();
  }, []);

  const summary = data?.summary || {};
  const recommendations = data?.recommendations || [];
  const forecast = data?.forecast || [];

  // group forecast by product
  const forecastByProduct = forecast.reduce((acc, row) => {
    const key = row.product || `Product ${row.product_id}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(row);
    return acc;
  }, {});

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-teal-700">ML Module</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-stone-900">Demand Forecast & Reorder</h1>
          <p className="mt-1 text-sm text-stone-600">
            7-day demand forecast and smart reorder recommendations powered by the integrated XGBoost model.
          </p>
        </div>
        <button
          type="button"
          onClick={loadInsights}
          className="rounded-md bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800"
        >
          Refresh insights
        </button>
      </div>

      {error && (
        <div className="rounded-md border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>
      )}

      {loading ? (
        <div className="rounded-lg border border-stone-200 bg-white p-6 text-sm text-stone-600">Loading ML insights...</div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="rounded-lg border border-stone-200 bg-white p-4">
              <p className="text-xs uppercase tracking-wide text-stone-500">Forecast horizon</p>
              <p className="mt-2 text-2xl font-semibold text-stone-900">{summary.forecast_days || 0} days</p>
            </div>
            <div className="rounded-lg border border-stone-200 bg-white p-4">
              <p className="text-xs uppercase tracking-wide text-stone-500">Products forecasted</p>
              <p className="mt-2 text-2xl font-semibold text-stone-900">{summary.total_products || 0}</p>
            </div>
            <div className="rounded-lg border border-stone-200 bg-white p-4">
              <p className="text-xs uppercase tracking-wide text-stone-500">Need reorder</p>
              <p className="mt-2 text-2xl font-semibold text-amber-700">{summary.products_requiring_reorder || 0}</p>
            </div>
            <div className="rounded-lg border border-stone-200 bg-white p-4">
              <p className="text-xs uppercase tracking-wide text-stone-500">Weather source</p>
              <p className="mt-2 text-lg font-semibold text-stone-900">{summary.weather_source || 'Unknown'}</p>
            </div>
          </div>

          <section className="rounded-lg border border-stone-200 bg-white">
            <div className="border-b border-stone-200 px-4 py-3">
              <h2 className="text-base font-semibold text-stone-900">Smart reorder recommendations</h2>
              <p className="text-sm text-stone-500">Uses forecasted demand, lead time, safety stock, and current inventory.</p>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-stone-50 text-xs uppercase tracking-wide text-stone-500">
                  <tr>
                    <th className="px-4 py-3">Product</th>
                    <th className="px-4 py-3">Current stock</th>
                    <th className="px-4 py-3">7d forecast</th>
                    <th className="px-4 py-3">Safety stock</th>
                    <th className="px-4 py-3">Reorder point</th>
                    <th className="px-4 py-3">Recommended qty</th>
                    <th className="px-4 py-3">Order by</th>
                    <th className="px-4 py-3">Supplier</th>
                    <th className="px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {recommendations.length === 0 ? (
                    <tr><td className="px-4 py-4 text-stone-500" colSpan="9">No recommendations available.</td></tr>
                  ) : recommendations.map((item) => (
                    <tr key={item.product_id}>
                      <td className="px-4 py-3 font-medium text-stone-900">
                        {item.product}
                        {item.erp_sku ? <span className="ml-2 text-xs text-stone-500">({item.erp_sku})</span> : null}
                      </td>
                      <td className="px-4 py-3">{formatNumber(item.current_stock)}</td>
                      <td className="px-4 py-3">{formatNumber(item.forecast_demand)}</td>
                      <td className="px-4 py-3">{formatNumber(item.safety_stock, 1)}</td>
                      <td className="px-4 py-3">{formatNumber(item.reorder_point, 1)}</td>
                      <td className="px-4 py-3 font-semibold text-stone-900">{formatNumber(item.reorder_quantity)}</td>
                      <td className="px-4 py-3">{item.order_by || '-'}</td>
                      <td className="px-4 py-3">{item.supplier}</td>
                      <td className="px-4 py-3">
                        {item.reorder_quantity > 0 ? (
                          <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${item.urgent ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'}`}>
                            {item.urgent ? 'Urgent' : 'Reorder'}
                          </span>
                        ) : (
                          <span className="inline-flex rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-700">OK</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="rounded-lg border border-stone-200 bg-white">
            <div className="border-b border-stone-200 px-4 py-3">
              <h2 className="text-base font-semibold text-stone-900">7-day demand forecast</h2>
              <p className="text-sm text-stone-500">Daily predicted demand per trained product (with weather features).</p>
            </div>
            <div className="space-y-4 p-4">
              {Object.keys(forecastByProduct).length === 0 ? (
                <p className="text-sm text-stone-500">No forecast data available.</p>
              ) : Object.entries(forecastByProduct).map(([product, rows]) => (
                <div key={product} className="rounded-md border border-stone-200">
                  <div className="flex items-center justify-between border-b border-stone-200 bg-stone-50 px-3 py-2">
                    <h3 className="font-medium text-stone-900">{product}</h3>
                    <span className="text-xs text-stone-600">7-day total: {formatNumber(rows.reduce((s, r) => s + Number(r.predicted_demand || 0), 0))} units</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="min-w-full text-left text-sm">
                      <thead className="text-xs uppercase tracking-wide text-stone-500">
                        <tr>
                          <th className="px-3 py-2">Date</th>
                          <th className="px-3 py-2">Rain prob</th>
                          <th className="px-3 py-2">Temp (°C)</th>
                          <th className="px-3 py-2">Predicted demand</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-stone-100">
                        {rows.map((row) => (
                          <tr key={`${row.product_id}-${row.date}`}>
                            <td className="px-3 py-2">{row.date}</td>
                            <td className="px-3 py-2">{formatNumber(Number(row.rain_prob) * 100, 0)}%</td>
                            <td className="px-3 py-2">{formatNumber(row.temp, 1)}</td>
                            <td className="px-3 py-2 font-medium">{formatNumber(row.predicted_demand, 1)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
