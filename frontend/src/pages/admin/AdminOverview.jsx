import { useMemo } from 'react';
import { LineChart, BarChart } from '../../components/Charts';
import { Icon } from '../../components/Icons';
import {
  ErrorBlock,
  KpiCard,
  LoadingBlock,
  Panel,
  compactCurrency,
  formatCurrency,
  formatDay,
  formatNumber,
  useAdminResource,
} from './AdminComponents';

const STATUS_COLORS = {
  Pending: '#f59e0b',
  Confirmed: '#0ea5e9',
  Shipped: '#6366f1',
  Delivered: '#0f766e',
  Cancelled: '#e11d48',
};

export default function AdminOverview() {
  const overview = useAdminResource('/admin/overview');
  const daily = useAdminResource('/admin/analytics/daily?days=30');

  const statusSeries = useMemo(() => {
    if (!overview.data) return [];
    return [
      { label: 'Pending', value: overview.data.pending_orders },
      { label: 'Confirmed', value: overview.data.confirmed_orders },
      { label: 'Shipped', value: overview.data.shipped_orders },
      { label: 'Delivered', value: overview.data.completed_orders },
      { label: 'Cancelled', value: overview.data.cancelled_orders },
    ];
  }, [overview.data]);

  if (overview.loading && !overview.data) {
    return <LoadingBlock label="Loading business overview…" />;
  }

  if (overview.error && !overview.data) {
    return (
      <ErrorBlock
        message={`The business overview could not be loaded. ${overview.error}`}
        onRetry={overview.reload}
      />
    );
  }

  const data = overview.data;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs text-stone-500">
          Realized revenue counts Confirmed, Shipped and Delivered sales orders.
          Pending orders are shown separately; cancelled orders are excluded.
        </p>
        <button
          type="button"
          onClick={() => {
            overview.reload();
            daily.reload();
          }}
          className="inline-flex items-center gap-1.5 rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 transition hover:bg-stone-50"
        >
          <Icon name="refresh" size={13} />
          Refresh
        </button>
      </div>

      {overview.error && (
        <ErrorBlock message={overview.error} onRetry={overview.reload} />
      )}

      <section aria-label="Sales performance" className="space-y-2">
        <h2 className="text-[10px] font-semibold uppercase tracking-[0.24em] text-stone-500">
          Sales performance
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <KpiCard
            label="Realized revenue"
            value={data.total_sales_revenue}
            format="currency"
            detail="Confirmed, Shipped and Delivered orders"
          />
          <KpiCard
            label="Realized orders"
            value={data.total_sales}
            detail={`${formatNumber(data.total_orders)} total sales orders`}
          />
          <KpiCard
            label="Average order value"
            value={data.average_order_value}
            format="currency"
            detail="Based on realized orders"
          />
          <KpiCard
            label="Pending pipeline"
            value={data.pipeline_revenue}
            format="currency"
            detail={`${formatNumber(data.pending_orders)} pending orders, not revenue`}
            tone="amber"
          />
          <KpiCard
            label="Completed orders"
            value={data.completed_orders}
            detail="Delivered orders"
            tone="teal"
          />
          <KpiCard
            label="Pending orders"
            value={data.pending_orders}
            detail="Awaiting confirmation"
            tone="amber"
          />
          <KpiCard
            label="Cancelled orders"
            value={data.cancelled_orders}
            detail={`${formatCurrency(data.cancelled_value)} excluded from revenue`}
            tone="rose"
          />
          <KpiCard
            label="Cancelled value"
            value={data.cancelled_value}
            format="currency"
            detail="Never counted as revenue"
            tone="rose"
          />
        </div>
      </section>

      <div className="grid gap-4 xl:grid-cols-[1.35fr_1fr]">
        <Panel
          title="Daily realized revenue"
          subtitle="Last 30 days, based on order creation date (UTC)"
          actions={
            daily.loading ? (
              <span className="text-[11px] text-stone-400">Loading chart…</span>
            ) : null
          }
        >
          {daily.error ? (
            <ErrorBlock message={daily.error} onRetry={daily.reload} />
          ) : (
            <LineChart
              data={daily.data?.series ?? []}
              xKey="date"
              yKey="revenue"
              label="Daily realized revenue for the last 30 days"
              formatValue={compactCurrency}
              formatX={formatDay}
              height={230}
            />
          )}
        </Panel>

        <Panel
          title="Orders by status"
          subtitle="Current distribution of all sales orders"
        >
          <BarChart
            data={statusSeries}
            xKey="label"
            yKey="value"
            label="Sales orders by status"
            formatValue={(value) => formatNumber(value)}
            height={230}
          />
          <ul className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-[10px] text-stone-500">
            {statusSeries.map((item) => (
              <li key={item.label} className="inline-flex items-center gap-1.5">
                <span
                  className="h-2 w-2 rounded-full"
                  style={{ backgroundColor: STATUS_COLORS[item.label] }}
                />
                {item.label}: {formatNumber(item.value)}
              </li>
            ))}
          </ul>
        </Panel>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Accounts" subtitle="Registered and active users">
          <div className="grid gap-3 sm:grid-cols-2">
            <KpiCard label="Total registered users" value={data.total_users} />
            <KpiCard
              label="Active users"
              value={data.active_users}
              detail="Accounts allowed to sign in"
              tone="indigo"
            />
          </div>
        </Panel>

        <Panel title="Catalog and inventory" subtitle="Current stock position">
          <div className="grid gap-3 sm:grid-cols-2">
            <KpiCard label="Products" value={data.total_products} />
            <KpiCard label="Suppliers" value={data.total_suppliers} tone="indigo" />
            <KpiCard
              label="Inventory units"
              value={data.total_inventory_units}
              detail="Total units across products"
            />
            <KpiCard
              label="Inventory value"
              value={data.inventory_value_at_selling_price}
              format="currency"
              detail="At selling price; cost is not stored"
            />
            <KpiCard
              label="Low-stock products"
              value={data.low_stock_products}
              tone="amber"
            />
            <KpiCard
              label="Out-of-stock products"
              value={data.out_of_stock_products}
              tone="rose"
            />
          </div>
        </Panel>
      </div>

      <Panel
        title="Purchasing"
        subtitle="Received purchase orders are expenditure; open orders are commitments"
      >
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <KpiCard label="Purchase orders" value={data.purchase_orders} />
          <KpiCard
            label="Received purchase orders"
            value={data.received_purchase_orders}
            detail="Included in expenditure"
            tone="teal"
          />
          <KpiCard
            label="Purchase expenditure"
            value={data.purchase_expenditure}
            format="currency"
            detail="Received orders only"
          />
          <KpiCard
            label="Pending purchase value"
            value={data.pending_purchase_value}
            format="currency"
            detail={`${formatNumber(data.pending_purchase_orders)} pending orders`}
            tone="amber"
          />
        </div>
        <p className="mt-3 text-[11px] leading-relaxed text-stone-500">
          {data.purchase_expenditure_note} {data.inventory_value_note}
        </p>
      </Panel>

      <Panel title="Data notes" subtitle="How these numbers are produced">
        <ul className="space-y-1.5 text-xs leading-relaxed text-stone-600">
          <li>• {data.revenue_definition}</li>
          <li>
            • Cancelled sales orders are excluded from revenue and reported as a
            separate value.
          </li>
          <li>
            • No order is counted twice: each order contributes once to its
            current status bucket.
          </li>
          <li>
            • Dates use the stored UTC timestamp; days are grouped by UTC calendar
            date.
          </li>
        </ul>
      </Panel>
    </div>
  );
}
