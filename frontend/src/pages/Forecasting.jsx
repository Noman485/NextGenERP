import { useEffect, useMemo, useState } from 'react';
import { apiFetch } from '../api';
import { Icon } from '../components/Icons';
import BarChart3D from '../components/BarChart3D';

function formatNumber(value, digits = 0) {
  const n = Number(value);
  if (!Number.isFinite(n)) return '-';
  return n.toLocaleString('en-IN', {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function formatDay(dateValue) {
  const date = new Date(dateValue);
  if (Number.isNaN(date.getTime())) return { label: dateValue, short: dateValue };
  return {
    label: date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }),
    short: date.toLocaleDateString('en-IN', { weekday: 'short' }),
  };
}

function KpiCard({ label, value, detail, icon, tone = 'teal' }) {
  const tones = {
    teal: 'bg-teal-50 text-teal-700 ring-teal-100',
    amber: 'bg-amber-50 text-amber-700 ring-amber-100',
    rose: 'bg-rose-50 text-rose-700 ring-rose-100',
    stone: 'bg-stone-100 text-stone-600 ring-stone-200',
  };

  return (
    <div className="relative overflow-hidden rounded-xl border border-stone-200/80 bg-[#fffdf9] p-4 shadow-[0_1px_2px_rgba(28,25,23,0.04)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_16px_30px_-24px_rgba(28,25,23,0.55)]">
      <div className="flex items-start justify-between gap-2">
        <p className="text-[9px] font-semibold uppercase tracking-[0.18em] text-stone-500">{label}</p>
        <span className={`rounded-md p-1.5 ring-1 ${tones[tone] ?? tones.teal}`}>
          <Icon name={icon} size={14} />
        </span>
      </div>
      <p className="mt-3 text-2xl font-semibold leading-none tracking-tight text-stone-900 tabular-nums">
        {value}
      </p>
      <p className="mt-1.5 text-[11px] leading-tight text-stone-500">{detail}</p>
    </div>
  );
}

export default function Forecasting() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [onlyReorder, setOnlyReorder] = useState(false);

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
  const recommendations = useMemo(() => data?.recommendations || [], [data]);
  const forecast = useMemo(() => data?.forecast || [], [data]);

  const dailyTotals = useMemo(() => {
    const totals = new Map();
    forecast.forEach((row) => {
      const key = row.date;
      totals.set(key, (totals.get(key) || 0) + Number(row.predicted_demand || 0));
    });

    return [...totals.entries()]
      .sort(([first], [second]) => String(first).localeCompare(String(second)))
      .map(([date, value]) => {
        const day = formatDay(date);
        return { label: day.label, short: day.short, value };
      });
  }, [forecast]);

  const forecastByProduct = useMemo(() => {
    const grouped = new Map();
    forecast.forEach((row) => {
      const key = row.product || `Product ${row.product_id}`;
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(row);
    });
    return [...grouped.entries()];
  }, [forecast]);

  const totals = useMemo(() => {
    const horizonTotal = dailyTotals.reduce((sum, day) => sum + day.value, 0);
    const reorderNeeded = recommendations.filter((item) => Number(item.reorder_quantity) > 0);
    return {
      horizonTotal,
      averageDaily: dailyTotals.length ? horizonTotal / dailyTotals.length : 0,
      reorderNeeded: reorderNeeded.length,
      urgent: reorderNeeded.filter((item) => item.urgent).length,
    };
  }, [dailyTotals, recommendations]);

  const visibleRecommendations = onlyReorder
    ? recommendations.filter((item) => Number(item.reorder_quantity) > 0)
    : recommendations;

  return (
    <div className="space-y-5">
      <section className="animate-rise relative overflow-hidden rounded-2xl border border-white/5 bg-[radial-gradient(130%_130%_at_0%_0%,#16312e_0%,#101a1c_48%,#0a1011_100%)] p-5 text-stone-100 shadow-[0_30px_70px_-52px_rgba(12,20,22,0.95)] sm:p-6">
        <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full bg-cyan-400/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 left-1/4 h-56 w-56 rounded-full bg-teal-400/[0.08] blur-3xl" />

        <div className="relative grid items-center gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-teal-300/20 bg-teal-400/10 px-2.5 py-1 text-[9px] font-semibold uppercase tracking-[0.2em] text-teal-200">
              <Icon name="chip" size={11} />
              ML module · XGBoost
            </span>

            <h1 className="mt-3 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
              Demand forecast &amp; reorder
            </h1>
            <p className="mt-2 max-w-xl text-sm leading-relaxed text-stone-400">
              A 7-day demand forecast with smart reorder recommendations, driven by lag,
              rolling, calendar and weather features.
            </p>

            <div className="mt-4 flex flex-wrap gap-2 text-[10px]">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1 text-stone-300">
                <Icon name="clock" size={11} className="text-teal-300" />
                {summary.forecast_days || 0}-day horizon
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1 text-stone-300">
                <Icon name="box" size={11} className="text-teal-300" />
                {summary.total_products || 0} products
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1 text-stone-300">
                <Icon name="cloud" size={11} className="text-teal-300" />
                {summary.weather_source || 'Unknown'}
              </span>
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={loadInsights}
                disabled={loading}
                className="inline-flex items-center gap-2 rounded-lg bg-teal-300 px-3.5 py-2 text-sm font-semibold text-[#06201d] shadow-[0_10px_30px_-14px_rgba(45,212,191,0.9)] transition hover:bg-teal-200 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Icon name="refresh" size={15} className={loading ? 'animate-spin' : ''} />
                {loading ? 'Refreshing…' : 'Refresh insights'}
              </button>
              <span className="text-[10px] uppercase tracking-[0.18em] text-stone-500">
                Hover the bars for daily detail
              </span>
            </div>
          </div>

          <div className="h-60 sm:h-64 lg:h-72">
            {dailyTotals.length > 0 ? (
              <BarChart3D data={dailyTotals} className="h-full w-full" />
            ) : (
              <div className="flex h-full items-center justify-center rounded-xl border border-dashed border-white/10 text-[10px] uppercase tracking-[0.22em] text-stone-500">
                {loading ? 'Loading forecast…' : 'No forecast data'}
              </div>
            )}
          </div>
        </div>
      </section>

      {error && (
        <div
          role="alert"
          className="flex flex-col gap-2 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800 sm:flex-row sm:items-center sm:justify-between"
        >
          <span className="flex items-center gap-2">
            <Icon name="alert" size={15} />
            {error}
          </span>
          <button
            type="button"
            onClick={loadInsights}
            className="w-fit rounded-md border border-rose-300 px-2.5 py-1 text-xs font-semibold text-rose-800 hover:bg-rose-100"
          >
            Try again
          </button>
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          label="Horizon demand"
          value={loading ? '—' : `${formatNumber(totals.horizonTotal)} u`}
          detail="predicted units across all products"
          icon="layers"
        />
        <KpiCard
          label="Average per day"
          value={loading ? '—' : `${formatNumber(totals.averageDaily)} u`}
          detail="mean daily demand in horizon"
          icon="forecast"
        />
        <KpiCard
          label="Need reorder"
          value={loading ? '—' : formatNumber(totals.reorderNeeded)}
          detail="products below reorder point"
          icon="cart"
          tone="amber"
        />
        <KpiCard
          label="Urgent"
          value={loading ? '—' : formatNumber(totals.urgent)}
          detail="order before lead time runs out"
          icon="alert"
          tone="rose"
        />
      </div>

      <section className="overflow-hidden rounded-xl border border-stone-200 bg-[#fffdf9] shadow-sm">
        <div className="flex flex-col gap-3 border-b border-stone-200 p-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-50 text-teal-700 ring-1 ring-teal-100">
              <Icon name="cart" size={16} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-stone-900">Smart reorder recommendations</h2>
              <p className="text-xs text-stone-500">
                Forecasted demand + lead time + safety stock vs current inventory
              </p>
            </div>
          </div>

          <div className="inline-flex rounded-lg border border-stone-200 bg-stone-50 p-0.5 text-xs font-medium">
            <button
              type="button"
              onClick={() => setOnlyReorder(false)}
              className={`rounded-md px-3 py-1.5 transition ${
                onlyReorder ? 'text-stone-500 hover:text-stone-700' : 'bg-white text-stone-900 shadow-sm'
              }`}
            >
              All ({recommendations.length})
            </button>
            <button
              type="button"
              onClick={() => setOnlyReorder(true)}
              className={`rounded-md px-3 py-1.5 transition ${
                onlyReorder ? 'bg-white text-stone-900 shadow-sm' : 'text-stone-500 hover:text-stone-700'
              }`}
            >
              Needs reorder ({totals.reorderNeeded})
            </button>
          </div>
        </div>

        <div className="max-h-[30rem] overflow-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="sticky top-0 z-10 bg-stone-50 text-[10px] uppercase tracking-[0.12em] text-stone-500">
              <tr>
                <th className="px-4 py-3 font-semibold">Product</th>
                <th className="px-4 py-3 text-right font-semibold">Stock</th>
                <th className="px-4 py-3 text-right font-semibold">7d forecast</th>
                <th className="px-4 py-3 text-right font-semibold">Safety</th>
                <th className="px-4 py-3 text-right font-semibold">Reorder pt</th>
                <th className="px-4 py-3 text-right font-semibold">Recommended</th>
                <th className="px-4 py-3 font-semibold">Order by</th>
                <th className="px-4 py-3 font-semibold">Supplier</th>
                <th className="px-4 py-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {visibleRecommendations.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-stone-500" colSpan="9">
                    {onlyReorder
                      ? 'No products need a reorder right now — inventory is healthy.'
                      : 'No recommendations available.'}
                  </td>
                </tr>
              ) : (
                visibleRecommendations.map((item) => {
                  const needsReorder = Number(item.reorder_quantity) > 0;
                  return (
                    <tr
                      key={item.product_id}
                      className={`transition hover:bg-stone-50/80 ${
                        needsReorder && item.urgent ? 'bg-rose-50/40' : ''
                      }`}
                    >
                      <td className="px-4 py-3 font-medium text-stone-900">
                        <span className="flex items-center gap-2">
                          <span className="flex h-6 w-6 items-center justify-center rounded-md bg-stone-100 text-stone-500">
                            <Icon name="box" size={12} />
                          </span>
                          <span className="truncate">{item.product}</span>
                          {item.erp_sku ? (
                            <span className="font-mono text-[10px] text-stone-400">({item.erp_sku})</span>
                          ) : null}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums">{formatNumber(item.current_stock)}</td>
                      <td className="px-4 py-3 text-right tabular-nums">{formatNumber(item.forecast_demand)}</td>
                      <td className="px-4 py-3 text-right tabular-nums text-stone-500">
                        {formatNumber(item.safety_stock, 1)}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums text-stone-500">
                        {formatNumber(item.reorder_point, 1)}
                      </td>
                      <td className="px-4 py-3 text-right font-semibold tabular-nums text-stone-900">
                        {formatNumber(item.reorder_quantity)}
                      </td>
                      <td className="px-4 py-3 text-xs tabular-nums text-stone-600">{item.order_by || '-'}</td>
                      <td className="px-4 py-3 text-stone-600">{item.supplier}</td>
                      <td className="px-4 py-3">
                        {needsReorder ? (
                          <span
                            className={`inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium ring-1 ${
                              item.urgent
                                ? 'bg-rose-50 text-rose-700 ring-rose-100'
                                : 'bg-amber-50 text-amber-800 ring-amber-100'
                            }`}
                          >
                            <span
                              className={`h-1.5 w-1.5 rounded-full ${
                                item.urgent ? 'bg-rose-500' : 'bg-amber-500'
                              }`}
                            />
                            {item.urgent ? 'Urgent' : 'Reorder'}
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700 ring-1 ring-emerald-100">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                            OK
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-stone-100 text-stone-700 ring-1 ring-stone-200">
            <Icon name="forecast" size={16} />
          </span>
          <div>
            <h2 className="text-base font-semibold text-stone-900">7-day demand forecast</h2>
            <p className="text-xs text-stone-500">
              Daily predicted demand per trained product, with weather features
            </p>
          </div>
        </div>

        {loading ? (
          <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {Array.from({ length: 6 }).map((_, index) => (
              <div
                key={index}
                className="h-32 animate-pulse rounded-lg border border-stone-200 bg-stone-100/60"
              />
            ))}
          </div>
        ) : forecastByProduct.length === 0 ? (
          <p className="mt-4 text-sm text-stone-500">No forecast data available.</p>
        ) : (
          <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {forecastByProduct.map(([product, rows]) => {
              const series = [...rows].sort((first, second) =>
                String(first.date).localeCompare(String(second.date)),
              );
              const total = series.reduce((sum, row) => sum + Number(row.predicted_demand || 0), 0);
              const peak = Math.max(...series.map((row) => Number(row.predicted_demand || 0)), 1);

              return (
                <div
                  key={product}
                  className="group rounded-lg border border-stone-200 bg-white p-3 transition hover:border-teal-300 hover:shadow-[0_16px_30px_-26px_rgba(13,148,136,0.7)]"
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="truncate text-sm font-medium text-stone-800">{product}</p>
                    <span className="shrink-0 rounded-full bg-teal-50 px-2 py-0.5 text-[10px] font-semibold text-teal-700 tabular-nums">
                      {formatNumber(total)} u
                    </span>
                  </div>

                  <div className="mt-3 flex h-16 items-end gap-1">
                    {series.map((row) => {
                      const value = Number(row.predicted_demand || 0);
                      const height = Math.max((value / peak) * 100, 6);
                      return (
                        <div key={`${row.product_id}-${row.date}`} className="group/bar relative flex-1">
                          <div
                            className="w-full rounded-t-[3px] bg-gradient-to-t from-teal-500/70 to-teal-300 transition group-hover/bar:from-teal-600 group-hover/bar:to-teal-400"
                            style={{ height: `${height}%`, minHeight: '4px' }}
                            title={`${row.date}: ${formatNumber(value, 1)} units`}
                          />
                        </div>
                      );
                    })}
                  </div>

                  <div className="mt-1.5 flex justify-between text-[9px] uppercase tracking-[0.08em] text-stone-400">
                    {series.map((row) => (
                      <span key={`label-${row.product_id}-${row.date}`} className="flex-1 text-center">
                        {formatDay(row.date).short.slice(0, 2)}
                      </span>
                    ))}
                  </div>

                  <div className="mt-2 flex items-center justify-between border-t border-stone-100 pt-2 text-[10px] text-stone-500">
                    <span>Rain {formatNumber(Number(series[0]?.rain_prob) * 100, 0)}%</span>
                    <span>{formatNumber(series[0]?.temp, 1)}°C</span>
                    <span className="tabular-nums">Peak {formatNumber(peak)} u</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
