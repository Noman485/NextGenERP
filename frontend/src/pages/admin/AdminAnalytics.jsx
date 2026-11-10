import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { BarChart, LineChart } from '../../components/Charts';
import { Icon } from '../../components/Icons';
import {
  ErrorBlock,
  KpiCard,
  LoadingBlock,
  Pagination,
  Panel,
  SortHeader,
  compactCurrency,
  formatCurrency,
  formatDate,
  formatDateTime,
  formatDay,
  formatNumber,
  formatPercent,
  useAdminResource,
} from './AdminComponents';

const PAGE_SIZE = 20;

const TABS = [
  { id: 'daily', label: 'Daily', icon: 'chart' },
  { id: 'monthly', label: 'Monthly', icon: 'calendar' },
  { id: 'yearly', label: 'Yearly', icon: 'forecast' },
  { id: 'users', label: 'Users', icon: 'users' },
  { id: 'products', label: 'Products', icon: 'box' },
  { id: 'inventory', label: 'Inventory', icon: 'inventory' },
  { id: 'suppliers', label: 'Suppliers', icon: 'truck' },
];

const tableClass = 'min-w-full divide-y divide-stone-200 text-sm';
const headRowClass = 'bg-stone-50/80';
const bodyRowClass = 'border-t border-stone-100 transition hover:bg-stone-50/70';
const cellClass = 'whitespace-nowrap px-3 py-2.5 text-stone-700';
const numberCellClass = `${cellClass} text-right tabular-nums`;

function Growth({ value }) {
  if (value === null || value === undefined) {
    return <span className="text-stone-400">—</span>;
  }
  const positive = Number(value) >= 0;
  return (
    <span className={positive ? 'font-medium text-emerald-700' : 'font-medium text-rose-700'}>
      {formatPercent(value)}
    </span>
  );
}

function StatusBadge({ status }) {
  const tones = {
    'In stock': 'border-emerald-200 bg-emerald-50 text-emerald-800',
    'Low stock': 'border-amber-200 bg-amber-50 text-amber-800',
    'Out of stock': 'border-rose-200 bg-rose-50 text-rose-800',
  };
  return (
    <span
      className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] ${
        tones[status] ?? 'border-stone-200 bg-stone-50 text-stone-600'
      }`}
    >
      {status}
    </span>
  );
}

function useListing(initialSort) {
  const [query, setQuery] = useState('');
  const [appliedQuery, setAppliedQuery] = useState('');
  const [sort, setSort] = useState(initialSort);
  const [direction, setDirection] = useState('desc');
  const [page, setPage] = useState(1);

  function applySearch(event) {
    event.preventDefault();
    setAppliedQuery(query.trim());
    setPage(1);
  }

  function onSort(value) {
    if (value === sort) {
      setDirection((current) => (current === 'desc' ? 'asc' : 'desc'));
    } else {
      setSort(value);
      setDirection('desc');
    }
    setPage(1);
  }

  function changeDirection() {
    setDirection((current) => (current === 'desc' ? 'asc' : 'desc'));
    setPage(1);
  }

  return {
    query,
    setQuery,
    appliedQuery,
    sort,
    direction,
    page,
    setPage,
    applySearch,
    onSort,
    changeDirection,
  };
}

function buildPath(base, { appliedQuery, sort, direction, page, extra = '' }) {
  const params = new URLSearchParams();
  if (appliedQuery) params.set('q', appliedQuery);
  params.set('sort', sort);
  params.set('direction', direction);
  params.set('limit', String(PAGE_SIZE));
  params.set('offset', String((page - 1) * PAGE_SIZE));
  return `${base}?${params.toString()}${extra}`;
}

function SearchForm({ query, setQuery, onSubmit, placeholder, children }) {
  return (
    <form onSubmit={onSubmit} className="flex flex-wrap items-center gap-2">
      <label className="relative min-w-[12rem] flex-1">
        <span className="sr-only">Search</span>
        <span className="pointer-events-none absolute inset-y-0 left-2.5 flex items-center text-stone-400">
          <Icon name="search" size={14} />
        </span>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={placeholder}
          maxLength={120}
          className="w-full rounded-lg border border-stone-300 bg-white py-1.5 pl-8 pr-3 text-xs text-stone-800 outline-none placeholder:text-stone-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
        />
      </label>
      <button
        type="submit"
        className="rounded-lg bg-stone-900 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-stone-800"
      >
        Search
      </button>
      {children}
    </form>
  );
}

function DirectionButton({ direction, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="inline-flex items-center gap-1 rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs font-medium text-stone-700 transition hover:bg-stone-50"
      aria-label={`Sort ${direction === 'desc' ? 'descending' : 'ascending'}; switch direction`}
    >
      {direction === 'desc' ? 'Highest first' : 'Lowest first'}
    </button>
  );
}

function DailyPanel() {
  const resource = useAdminResource('/admin/analytics/daily?days=30');

  if (resource.loading && !resource.data) return <LoadingBlock label="Loading daily sales…" />;
  if (resource.error) {
    return <ErrorBlock message={resource.error} onRetry={resource.reload} />;
  }

  const data = resource.data;
  const series = data.series ?? [];

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <KpiCard label="30-day revenue" value={data.totals.revenue} format="currency" />
        <KpiCard label="Orders" value={data.totals.orders} />
        <KpiCard label="Completed" value={data.totals.completed_orders} tone="teal" />
        <KpiCard label="Cancelled" value={data.totals.cancelled_orders} tone="rose" />
        <KpiCard
          label="Average order value"
          value={data.totals.average_order_value}
          format="currency"
          tone="indigo"
        />
      </div>

      {data.undated_orders > 0 && (
        <p className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-900">
          {formatNumber(data.undated_orders)} legacy orders have no creation
          timestamp and cannot be placed on a day. They are excluded from this
          daily series but remain in the overview totals.
        </p>
      )}

      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Revenue by day" subtitle="Last 30 days, UTC calendar dates">
          <LineChart
            data={series}
            xKey="date"
            yKey="revenue"
            label="Daily revenue for the last 30 days"
            formatValue={compactCurrency}
            formatX={formatDay}
            height={230}
          />
        </Panel>
        <Panel title="Orders by day" subtitle="All sales orders created each day">
          <BarChart
            data={series}
            xKey="date"
            yKey="orders"
            label="Daily order count for the last 30 days"
            formatValue={(value) => formatNumber(value)}
            formatX={formatDay}
            height={230}
          />
        </Panel>
      </div>

      <Panel
        title="Daily detail"
        subtitle={`${data.start} to ${data.end}`}
        actions={
          <button
            type="button"
            onClick={resource.reload}
            className="inline-flex items-center gap-1.5 rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs font-medium text-stone-700 hover:bg-stone-50"
          >
            <Icon name="refresh" size={12} />
            Refresh
          </button>
        }
      >
        <div className="overflow-x-auto">
          <table className={tableClass}>
            <thead className={headRowClass}>
              <tr>
                <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Date
                </th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Revenue
                </th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Orders
                </th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Completed
                </th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Cancelled
                </th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                  Avg. order value
                </th>
              </tr>
            </thead>
            <tbody>
              {series.map((day) => (
                <tr key={day.date} className={bodyRowClass}>
                  <td className={cellClass}>{formatDay(day.date)}</td>
                  <td className={numberCellClass}>{formatCurrency(day.revenue)}</td>
                  <td className={numberCellClass}>{formatNumber(day.orders)}</td>
                  <td className={numberCellClass}>{formatNumber(day.completed_orders)}</td>
                  <td className={numberCellClass}>{formatNumber(day.cancelled_orders)}</td>
                  <td className={numberCellClass}>{formatCurrency(day.average_order_value)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}

function MonthlyPanel() {
  const currentYear = new Date().getUTCFullYear();
  const years = useMemo(
    () => Array.from({ length: 7 }, (_, index) => currentYear - index),
    [currentYear],
  );
  const [year, setYear] = useState(currentYear);
  const resource = useAdminResource(`/admin/analytics/monthly?year=${year}`);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs text-stone-500">
          Month-by-month revenue with comparison to the previous month. Missing
          months are shown as zero, not omitted.
        </p>
        <label className="inline-flex items-center gap-2 text-xs font-medium text-stone-600">
          Year
          <select
            value={year}
            onChange={(event) => setYear(Number(event.target.value))}
            className="rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
          >
            {years.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>

      {resource.loading && !resource.data ? (
        <LoadingBlock label={`Loading ${year} monthly sales…`} />
      ) : resource.error ? (
        <ErrorBlock message={resource.error} onRetry={resource.reload} />
      ) : (
        <>
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
            <KpiCard label={`${year} revenue`} value={resource.data.totals.revenue} format="currency" />
            <KpiCard label="Orders" value={resource.data.totals.orders} />
            <KpiCard label="Completed" value={resource.data.totals.completed_orders} tone="teal" />
            <KpiCard label="Cancelled" value={resource.data.totals.cancelled_orders} tone="rose" />
            <KpiCard
              label="Average order value"
              value={resource.data.totals.average_order_value}
              format="currency"
              tone="indigo"
            />
          </div>

          <div className="grid gap-4 xl:grid-cols-2">
            <Panel title="Revenue by month" subtitle={`Calendar year ${year}`}>
              <BarChart
                data={resource.data.series}
                xKey="label"
                yKey="revenue"
                label={`Monthly revenue for ${year}`}
                formatValue={compactCurrency}
                formatX={(value) => String(value).slice(0, 3)}
                height={240}
              />
            </Panel>
            <Panel title="Orders by month" subtitle="Order count per month">
              <LineChart
                data={resource.data.series}
                xKey="label"
                yKey="orders"
                label={`Monthly order count for ${year}`}
                formatValue={(value) => formatNumber(value)}
                formatX={(value) => String(value).slice(0, 3)}
                height={240}
              />
            </Panel>
          </div>

          <Panel title="Monthly detail" subtitle="Revenue, orders and month-over-month growth">
            <div className="overflow-x-auto">
              <table className={tableClass}>
                <thead className={headRowClass}>
                  <tr>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Month</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Revenue</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Orders</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Completed</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Cancelled</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Avg. order value</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Growth</th>
                  </tr>
                </thead>
                <tbody>
                  {resource.data.series.map((month) => (
                    <tr key={month.month} className={bodyRowClass}>
                      <td className={cellClass}>{month.label}</td>
                      <td className={numberCellClass}>{formatCurrency(month.revenue)}</td>
                      <td className={numberCellClass}>{formatNumber(month.orders)}</td>
                      <td className={numberCellClass}>{formatNumber(month.completed_orders)}</td>
                      <td className={numberCellClass}>{formatNumber(month.cancelled_orders)}</td>
                      <td className={numberCellClass}>{formatCurrency(month.average_order_value)}</td>
                      <td className={numberCellClass}>
                        <Growth value={month.previous_month_growth_percent} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {resource.data.undated_orders > 0 && (
              <p className="mt-2 text-[11px] text-stone-500">
                {formatNumber(resource.data.undated_orders)} legacy orders without a
                timestamp are excluded from the monthly breakdown.
              </p>
            )}
          </Panel>
        </>
      )}
    </div>
  );
}

function YearlyPanel() {
  const resource = useAdminResource('/admin/analytics/yearly?years=5');

  if (resource.loading && !resource.data) return <LoadingBlock label="Loading yearly sales…" />;
  if (resource.error) return <ErrorBlock message={resource.error} onRetry={resource.reload} />;

  const data = resource.data;

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <KpiCard label="Revenue, 5-year window" value={data.totals.revenue} format="currency" />
        <KpiCard label="Orders" value={data.totals.orders} />
        <KpiCard label="Completed" value={data.totals.completed_orders} tone="teal" />
        <KpiCard label="Cancelled" value={data.totals.cancelled_orders} tone="rose" />
        <KpiCard
          label="Average order value"
          value={data.totals.average_order_value}
          format="currency"
          tone="indigo"
        />
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Revenue by year" subtitle={`${data.start_year}–${data.end_year}`}>
          <BarChart
            data={data.series}
            xKey="year"
            yKey="revenue"
            label="Yearly revenue"
            formatValue={compactCurrency}
            formatX={(value) => String(value)}
            height={240}
          />
        </Panel>
        <Panel title="Orders by year" subtitle="Order count and year-over-year change">
          <LineChart
            data={data.series}
            xKey="year"
            yKey="orders"
            label="Yearly order count"
            formatValue={(value) => formatNumber(value)}
            formatX={(value) => String(value)}
            height={240}
          />
        </Panel>
      </div>

      <Panel title="Yearly detail" subtitle="Year-over-year comparison">
        <div className="overflow-x-auto">
          <table className={tableClass}>
            <thead className={headRowClass}>
              <tr>
                <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Year</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Revenue</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Orders</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Completed</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Cancelled</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Avg. order value</th>
                <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">YoY growth</th>
              </tr>
            </thead>
            <tbody>
              {data.series.map((year) => (
                <tr key={year.year} className={bodyRowClass}>
                  <td className={cellClass}>{year.year}</td>
                  <td className={numberCellClass}>{formatCurrency(year.revenue)}</td>
                  <td className={numberCellClass}>{formatNumber(year.orders)}</td>
                  <td className={numberCellClass}>{formatNumber(year.completed_orders)}</td>
                  <td className={numberCellClass}>{formatNumber(year.cancelled_orders)}</td>
                  <td className={numberCellClass}>{formatCurrency(year.average_order_value)}</td>
                  <td className={numberCellClass}>
                    <Growth value={year.year_over_year_growth_percent} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}

function UsersPanel() {
  const listing = useListing('revenue');
  const path = buildPath('/admin/analytics/users', listing);
  const resource = useAdminResource(path);
  const data = resource.data;

  return (
    <div className="space-y-4">
      <Panel
        title="User-wise sales"
        subtitle="Realized revenue and order activity per account"
        actions={
          <Link
            to="/admin/users"
            className="rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs font-semibold text-stone-700 transition hover:bg-stone-50"
          >
            Manage users
          </Link>
        }
      >
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <SearchForm
            query={listing.query}
            setQuery={listing.setQuery}
            onSubmit={listing.applySearch}
            placeholder="Search by username or email"
          >
            <label className="inline-flex items-center gap-1.5 text-xs text-stone-600">
              Sort
              <select
                value={listing.sort}
                onChange={(event) => listing.onSort(event.target.value)}
                className="rounded-lg border border-stone-300 bg-white px-2 py-1.5 text-xs text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
              >
                <option value="revenue">Revenue</option>
                <option value="orders">Orders</option>
                <option value="username">Username</option>
                <option value="created_at">Created date</option>
              </select>
            </label>
            <DirectionButton direction={listing.direction} onClick={listing.changeDirection} />
          </SearchForm>
        </div>

        {resource.loading && !data ? (
          <LoadingBlock label="Loading user sales…" />
        ) : resource.error ? (
          <ErrorBlock message={resource.error} onRetry={resource.reload} />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className={tableClass}>
                <thead className={headRowClass}>
                  <tr>
                    <SortHeader label="User" value="username" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} />
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Email</th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Status</th>
                    <SortHeader label="Orders" value="orders" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} align="right" />
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Realized</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Completed</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Cancelled</th>
                    <SortHeader label="Revenue" value="revenue" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} align="right" />
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Avg. order value</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((row) => (
                    <tr key={row.user_id ?? 'unassigned'} className={bodyRowClass}>
                      <td className={cellClass}>
                        <span className="font-medium text-stone-900">{row.username}</span>
                        {row.role && (
                          <span className="ml-1.5 rounded bg-stone-100 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-[0.08em] text-stone-500">
                            {row.role}
                          </span>
                        )}
                      </td>
                      <td className={cellClass}>{row.email || '—'}</td>
                      <td className={cellClass}>
                        {row.is_active === null ? (
                          '—'
                        ) : (
                          <span
                            className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] ${
                              row.is_active
                                ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
                                : 'border-rose-200 bg-rose-50 text-rose-800'
                            }`}
                          >
                            {row.is_active ? 'Active' : 'Inactive'}
                          </span>
                        )}
                      </td>
                      <td className={numberCellClass}>{formatNumber(row.orders)}</td>
                      <td className={numberCellClass}>{formatNumber(row.realized_orders)}</td>
                      <td className={numberCellClass}>{formatNumber(row.completed_orders)}</td>
                      <td className={numberCellClass}>{formatNumber(row.cancelled_orders)}</td>
                      <td className={numberCellClass}>{formatCurrency(row.revenue)}</td>
                      <td className={numberCellClass}>{formatCurrency(row.average_order_value)}</td>
                    </tr>
                  ))}
                  {data.items.length === 0 && (
                    <tr>
                      <td colSpan={9} className="px-3 py-8 text-center text-sm text-stone-500">
                        No user sales match this search.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <Pagination
              page={listing.page}
              pageSize={PAGE_SIZE}
              total={data.total}
              onChange={listing.setPage}
            />
          </>
        )}
      </Panel>
    </div>
  );
}

function ProductsPanel() {
  const listing = useListing('revenue');
  const path = buildPath('/admin/analytics/products', listing);
  const resource = useAdminResource(path);
  const data = resource.data;

  return (
    <div className="space-y-4">
      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Best-selling products" subtitle="Ranked by realized revenue">
          {resource.loading && !data ? (
            <LoadingBlock label="Loading products…" />
          ) : (
            <ol className="space-y-1.5">
              {(data?.best_sellers ?? []).slice(0, 6).map((item, index) => (
                <li
                  key={item.product_id}
                  className="flex items-center gap-2 rounded-lg border border-stone-100 bg-stone-50/60 px-2.5 py-1.5 text-xs"
                >
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-white text-[10px] font-semibold text-stone-500">
                    {index + 1}
                  </span>
                  <span className="min-w-0 flex-1 truncate font-medium text-stone-800">{item.name}</span>
                  <span className="shrink-0 tabular-nums text-stone-600">{formatCurrency(item.revenue)}</span>
                </li>
              ))}
              {(data?.best_sellers ?? []).length === 0 && (
                <li className="text-xs text-stone-500">No realized product sales yet.</li>
              )}
            </ol>
          )}
        </Panel>

        <Panel title="Slow-moving products" subtitle="No realized sales in the last 30 days">
          {resource.loading && !data ? (
            <LoadingBlock label="Loading products…" />
          ) : (
            <ol className="space-y-1.5">
              {(data?.slow_moving ?? []).slice(0, 6).map((item) => (
                <li
                  key={item.product_id}
                  className="flex items-center gap-2 rounded-lg border border-amber-100 bg-amber-50/60 px-2.5 py-1.5 text-xs"
                >
                  <span className="min-w-0 flex-1 truncate font-medium text-stone-800">{item.name}</span>
                  <span className="shrink-0 tabular-nums text-stone-600">
                    {formatNumber(item.stock_quantity)} in stock
                  </span>
                </li>
              ))}
              {(data?.slow_moving ?? []).length === 0 && (
                <li className="text-xs text-stone-500">Every product had realized sales in the last 30 days.</li>
              )}
            </ol>
          )}
        </Panel>
      </div>

      <Panel title="Product sales and stock" subtitle="Revenue, units sold and current stock position">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <SearchForm
            query={listing.query}
            setQuery={listing.setQuery}
            onSubmit={listing.applySearch}
            placeholder="Search by product name or SKU"
          >
            <label className="inline-flex items-center gap-1.5 text-xs text-stone-600">
              Sort
              <select
                value={listing.sort}
                onChange={(event) => listing.onSort(event.target.value)}
                className="rounded-lg border border-stone-300 bg-white px-2 py-1.5 text-xs text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
              >
                <option value="revenue">Revenue</option>
                <option value="units">Units sold</option>
                <option value="name">Name</option>
                <option value="stock">Stock</option>
              </select>
            </label>
            <DirectionButton direction={listing.direction} onClick={listing.changeDirection} />
          </SearchForm>
        </div>

        {resource.loading && !data ? (
          <LoadingBlock label="Loading product sales…" />
        ) : resource.error ? (
          <ErrorBlock message={resource.error} onRetry={resource.reload} />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className={tableClass}>
                <thead className={headRowClass}>
                  <tr>
                    <SortHeader label="Product" value="name" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} />
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">SKU</th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Stock</th>
                    <SortHeader label="Units sold" value="units" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} align="right" />
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Realized units</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Orders</th>
                    <SortHeader label="Revenue" value="revenue" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} align="right" />
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Avg. order value</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((item) => (
                    <tr key={item.product_id} className={bodyRowClass}>
                      <td className={cellClass}>
                        <span className="font-medium text-stone-900">{item.name}</span>
                        {item.slow_moving_last_30_days && (
                          <span className="ml-1.5 rounded bg-amber-50 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-[0.08em] text-amber-700">
                            Slow
                          </span>
                        )}
                      </td>
                      <td className={cellClass}>{item.sku}</td>
                      <td className={cellClass}>
                        <div className="flex items-center gap-1.5">
                          <span className="tabular-nums">{formatNumber(item.stock_quantity)}</span>
                          <StatusBadge status={item.stock_status} />
                        </div>
                      </td>
                      <td className={numberCellClass}>{formatNumber(item.units_sold)}</td>
                      <td className={numberCellClass}>{formatNumber(item.realized_units)}</td>
                      <td className={numberCellClass}>{formatNumber(item.orders)}</td>
                      <td className={numberCellClass}>{formatCurrency(item.revenue)}</td>
                      <td className={numberCellClass}>{formatCurrency(item.average_order_value)}</td>
                    </tr>
                  ))}
                  {data.items.length === 0 && (
                    <tr>
                      <td colSpan={8} className="px-3 py-8 text-center text-sm text-stone-500">
                        No products match this search.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <Pagination
              page={listing.page}
              pageSize={PAGE_SIZE}
              total={data.total}
              onChange={listing.setPage}
            />
          </>
        )}
      </Panel>
    </div>
  );
}

function InventoryPanel() {
  const resource = useAdminResource('/admin/analytics/inventory');

  if (resource.loading && !resource.data) return <LoadingBlock label="Loading inventory analytics…" />;
  if (resource.error) return <ErrorBlock message={resource.error} onRetry={resource.reload} />;

  const data = resource.data;
  const movements = data.stock_movements_last_30_days;
  const movementSeries = [
    { label: 'Stock In', value: movements.stock_in_units },
    { label: 'Stock Out', value: movements.stock_out_units },
  ];

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-6">
        <KpiCard label="Products" value={data.total_products} />
        <KpiCard label="Units in stock" value={data.total_units} />
        <KpiCard
          label="Inventory value"
          value={data.inventory_value_at_selling_price}
          format="currency"
          detail="At selling price"
          tone="indigo"
        />
        <KpiCard label="Low stock" value={data.low_stock_count} tone="amber" />
        <KpiCard label="Out of stock" value={data.out_of_stock_count} tone="rose" />
        <KpiCard
          label="Transactions, 30 days"
          value={movements.transactions}
          detail={`Net ${formatNumber(movements.net_units)} units`}
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Stock movement, last 30 days" subtitle="Units added and removed">
          <BarChart
            data={movementSeries}
            xKey="label"
            yKey="value"
            label="Stock in and stock out units over the last 30 days"
            formatValue={(value) => formatNumber(value)}
            height={220}
          />
        </Panel>
        <Panel title="Inventory valuation" subtitle={data.inventory_value_note}>
          <p className="text-3xl font-semibold tracking-tight text-stone-900">
            {formatCurrency(data.inventory_value_at_selling_price)}
          </p>
          <p className="mt-1 text-xs text-stone-500">
            {formatNumber(data.total_units)} units across {formatNumber(data.total_products)} products.
            This is not purchase cost; cost data is not stored per product.
          </p>
          <div className="mt-4 grid grid-cols-2 gap-2 text-center text-xs">
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-2">
              <p className="font-semibold text-emerald-800">{formatNumber(movements.stock_in_units)}</p>
              <p className="text-emerald-700">units in</p>
            </div>
            <div className="rounded-lg border border-rose-200 bg-rose-50 p-2">
              <p className="font-semibold text-rose-800">{formatNumber(movements.stock_out_units)}</p>
              <p className="text-rose-700">units out</p>
            </div>
          </div>
        </Panel>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Low-stock products" subtitle="At or below reorder level, but not empty">
          {data.low_stock_products.length === 0 ? (
            <p className="text-sm text-stone-500">No products are low on stock.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className={tableClass}>
                <thead className={headRowClass}>
                  <tr>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Product</th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">SKU</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Stock</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Reorder level</th>
                  </tr>
                </thead>
                <tbody>
                  {data.low_stock_products.map((item) => (
                    <tr key={item.product_id} className={bodyRowClass}>
                      <td className={cellClass}>{item.name}</td>
                      <td className={cellClass}>{item.sku}</td>
                      <td className={`${numberCellClass} font-medium text-amber-800`}>{formatNumber(item.stock_quantity)}</td>
                      <td className={numberCellClass}>{formatNumber(item.reorder_level)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>

        <Panel title="Out-of-stock products" subtitle="Stock quantity is zero">
          {data.out_of_stock_products.length === 0 ? (
            <p className="text-sm text-stone-500">No products are out of stock.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className={tableClass}>
                <thead className={headRowClass}>
                  <tr>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Product</th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">SKU</th>
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Reorder level</th>
                  </tr>
                </thead>
                <tbody>
                  {data.out_of_stock_products.map((item) => (
                    <tr key={item.product_id} className={bodyRowClass}>
                      <td className={cellClass}>{item.name}</td>
                      <td className={cellClass}>{item.sku}</td>
                      <td className={numberCellClass}>{formatNumber(item.reorder_level)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
      </div>

      <Panel title="Recent stock movements" subtitle="Latest inventory transactions">
        {data.recent_movements.length === 0 ? (
          <p className="text-sm text-stone-500">No inventory transactions recorded yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className={tableClass}>
              <thead className={headRowClass}>
                <tr>
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">When</th>
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Product</th>
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Type</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Quantity</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Before</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">After</th>
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Reason</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_movements.map((movement) => (
                  <tr key={movement.id} className={bodyRowClass}>
                    <td className={cellClass}>{formatDateTime(movement.created_at)}</td>
                    <td className={cellClass}>{movement.product_name || `#${movement.product_id}`}</td>
                    <td className={cellClass}>{movement.transaction_type}</td>
                    <td className={numberCellClass}>{formatNumber(movement.quantity)}</td>
                    <td className={numberCellClass}>{formatNumber(movement.previous_stock)}</td>
                    <td className={numberCellClass}>{formatNumber(movement.new_stock)}</td>
                    <td className={`${cellClass} max-w-[16rem] truncate`} title={movement.reason}>
                      {movement.reason}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </div>
  );
}

function SuppliersPanel() {
  const listing = useListing('purchase_expenditure');
  const path = buildPath('/admin/analytics/suppliers', listing);
  const resource = useAdminResource(path);
  const data = resource.data;

  return (
    <Panel title="Supplier and purchase analytics" subtitle="Received orders are expenditure; open orders are commitments">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <SearchForm
          query={listing.query}
          setQuery={listing.setQuery}
          onSubmit={listing.applySearch}
          placeholder="Search by supplier name or email"
        >
          <label className="inline-flex items-center gap-1.5 text-xs text-stone-600">
            Sort
            <select
              value={listing.sort}
              onChange={(event) => listing.onSort(event.target.value)}
              className="rounded-lg border border-stone-300 bg-white px-2 py-1.5 text-xs text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
            >
              <option value="purchase_expenditure">Expenditure</option>
              <option value="orders">Purchase orders</option>
              <option value="received">Received</option>
              <option value="name">Name</option>
            </select>
          </label>
          <DirectionButton direction={listing.direction} onClick={listing.changeDirection} />
        </SearchForm>
      </div>

      {resource.loading && !data ? (
        <LoadingBlock label="Loading supplier analytics…" />
      ) : resource.error ? (
        <ErrorBlock message={resource.error} onRetry={resource.reload} />
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className={tableClass}>
              <thead className={headRowClass}>
                <tr>
                  <SortHeader label="Supplier" value="name" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} />
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Lead time</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Rating</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Purchase orders</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Pending</th>
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Received</th>
                  <SortHeader label="Expenditure" value="purchase_expenditure" sort={listing.sort} direction={listing.direction} onSort={listing.onSort} align="right" />
                  <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Pending value</th>
                  <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">Last purchase</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((row) => (
                  <tr key={row.supplier_id} className={bodyRowClass}>
                    <td className={cellClass}>
                      <span className="font-medium text-stone-900">{row.name}</span>
                      {row.email && (
                        <span className="block text-[11px] text-stone-500">{row.email}</span>
                      )}
                    </td>
                    <td className={cellClass}>{formatNumber(row.lead_time_days)} days</td>
                    <td className={numberCellClass}>
                      {row.performance_rating === null || row.performance_rating === undefined
                        ? '—'
                        : Number(row.performance_rating).toFixed(1)}
                    </td>
                    <td className={numberCellClass}>{formatNumber(row.purchase_orders)}</td>
                    <td className={numberCellClass}>{formatNumber(row.pending_purchases)}</td>
                    <td className={numberCellClass}>{formatNumber(row.received_purchases)}</td>
                    <td className={numberCellClass}>{formatCurrency(row.purchase_expenditure)}</td>
                    <td className={numberCellClass}>{formatCurrency(row.pending_value)}</td>
                    <td className={cellClass}>{formatDate(row.last_purchase_at)}</td>
                  </tr>
                ))}
                {data.items.length === 0 && (
                  <tr>
                    <td colSpan={9} className="px-3 py-8 text-center text-sm text-stone-500">
                      No suppliers match this search.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <Pagination
            page={listing.page}
            pageSize={PAGE_SIZE}
            total={data.total}
            onChange={listing.setPage}
          />
        </>
      )}
    </Panel>
  );
}

export default function AdminAnalytics() {
  const [tab, setTab] = useState('daily');

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <div
          role="tablist"
          aria-label="Analytics views"
          className="flex flex-wrap gap-1 rounded-xl border border-stone-200 bg-[#fffdf9] p-1"
        >
          {TABS.map((item) => (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={tab === item.id}
              onClick={() => setTab(item.id)}
              className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                tab === item.id
                  ? 'bg-stone-900 text-white'
                  : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900'
              }`}
            >
              <Icon name={item.icon} size={13} />
              {item.label}
            </button>
          ))}
        </div>
        <p className="text-[11px] text-stone-500">
          Realized revenue: Confirmed, Shipped and Delivered orders only.
        </p>
      </div>

      {tab === 'daily' && <DailyPanel />}
      {tab === 'monthly' && <MonthlyPanel />}
      {tab === 'yearly' && <YearlyPanel />}
      {tab === 'users' && <UsersPanel />}
      {tab === 'products' && <ProductsPanel />}
      {tab === 'inventory' && <InventoryPanel />}
      {tab === 'suppliers' && <SuppliersPanel />}
    </div>
  );
}
