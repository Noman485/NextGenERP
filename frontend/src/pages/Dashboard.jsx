import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiFetch } from '../api';
import { Icon } from '../components/Icons';
import Warehouse3D from '../components/Warehouse3D';

const API_ENDPOINTS = [
  { key: 'products', label: 'Products', path: '/products/' },
  { key: 'categories', label: 'Categories', path: '/categories/' },
  { key: 'suppliers', label: 'Suppliers', path: '/suppliers/' },
  { key: 'orders', label: 'Sales orders', path: '/orders/' },
  { key: 'purchaseOrders', label: 'Purchase orders', path: '/purchase-orders/' },
];

const emptyDashboardData = {
  products: [],
  categories: [],
  suppliers: [],
  orders: [],
  purchaseOrders: [],
};

const numberFormatter = new Intl.NumberFormat('en-IN');
const quickActions = [
  { label: 'Add Product', path: '/products', icon: 'plus' },
  { label: 'New Sale', path: '/sales-orders', icon: 'cart' },
  { label: 'New Purchase Order', path: '/purchase-orders', icon: 'clipboard' },
  { label: 'Add Supplier', path: '/suppliers', icon: 'users' },
];

async function requestCollection(endpoint) {
  const response = await apiFetch(endpoint.path, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(`${endpoint.label} request failed (HTTP ${response.status}).`);
  }

  const data = await response.json();
  if (!Array.isArray(data)) {
    throw new Error(`${endpoint.label} returned an unexpected response.`);
  }
  return data;
}

async function requestDashboardData() {
  const results = await Promise.allSettled(
    API_ENDPOINTS.map((endpoint) => requestCollection(endpoint)),
  );
  const data = {};
  const errors = {};

  results.forEach((result, index) => {
    const endpoint = API_ENDPOINTS[index];
    if (result.status === 'fulfilled') {
      data[endpoint.key] = result.value;
    } else {
      errors[endpoint.key] =
        result.reason instanceof Error
          ? result.reason.message
          : `${endpoint.label} request failed.`;
    }
  });

  return { data, errors };
}

function getProductQuantity(product) {
  const quantity = Number(product.stock_quantity);
  return Number.isFinite(quantity) ? quantity : 0;
}

function getProductReorderLevel(product) {
  const reorderLevel = Number(product.reorder_level);
  return Number.isFinite(reorderLevel) ? reorderLevel : 0;
}

function getOrderStatusCount(orders, status) {
  return orders.filter((order) => order.status === status).length;
}

function getAttentionSummaries(data, failedSections = {}) {
  const productsUnavailable = Boolean(failedSections.products);
  const ordersUnavailable = Boolean(failedSections.orders);
  const purchaseOrdersUnavailable = Boolean(failedSections.purchaseOrders);
  const lowStockProducts = data.products.filter((product) => {
    const quantity = getProductQuantity(product);
    return quantity > 0 && quantity <= getProductReorderLevel(product);
  });
  const outOfStockProducts = data.products.filter(
    (product) => getProductQuantity(product) === 0,
  );
  const pendingOrders = data.orders.filter((order) => order.status === 'Pending');
  const pendingPurchaseOrders = data.purchaseOrders.filter(
    (order) => order.status === 'Pending',
  );

  return [
    {
      title: 'Low-stock products',
      records: lowStockProducts,
      unavailable: productsUnavailable,
      detail: productsUnavailable
        ? 'Stock levels are unavailable right now.'
        : lowStockProducts.length
          ? lowStockProducts.map((product) => `${product.name} (${product.stock_quantity} units)`).join(', ')
          : 'No products need reorder review.',
      tone: 'amber',
    },
    {
      title: 'Out-of-stock products',
      records: outOfStockProducts,
      unavailable: productsUnavailable,
      detail: productsUnavailable
        ? 'Stock levels are unavailable right now.'
        : outOfStockProducts.length
          ? outOfStockProducts.map((product) => product.name).join(', ')
          : 'No products are out of stock.',
      tone: 'red',
    },
    {
      title: 'Pending sales orders',
      records: pendingOrders,
      unavailable: ordersUnavailable,
      detail: ordersUnavailable
        ? 'Sales orders are unavailable right now.'
        : pendingOrders.length
          ? pendingOrders.map((order) => `#${order.id} · ${order.customer_name}`).join(', ')
          : 'No sales orders are pending.',
      tone: 'amber',
    },
    {
      title: 'Pending purchase orders',
      records: pendingPurchaseOrders,
      unavailable: purchaseOrdersUnavailable,
      detail: purchaseOrdersUnavailable
        ? 'Purchase orders are unavailable right now.'
        : pendingPurchaseOrders.length
          ? pendingPurchaseOrders
              .map((order) => `#${order.id} · supplier ${order.supplier_id}`)
              .join(', ')
          : 'No purchase orders are pending.',
      tone: 'amber',
    },
  ];
}

function getLatestById(records) {
  return [...records]
    .sort((first, second) => Number(second.id) - Number(first.id))
    .slice(0, 3);
}

const TONE_STYLES = {
  teal: {
    text: 'text-stone-900',
    bar: 'from-teal-300 via-teal-400 to-emerald-500',
    chip: 'bg-teal-50 text-teal-700',
  },
  amber: {
    text: 'text-amber-900',
    bar: 'from-amber-200 via-amber-300 to-orange-400',
    chip: 'bg-amber-50 text-amber-700',
  },
  red: {
    text: 'text-red-900',
    bar: 'from-rose-300 via-rose-400 to-red-500',
    chip: 'bg-rose-50 text-rose-700',
  },
};

function StatCard({ label, value, detail, tone = 'teal', icon, loading, unavailable }) {
  const styles = TONE_STYLES[tone] ?? TONE_STYLES.teal;
  const pending = loading || unavailable;

  return (
    <div className="group relative overflow-hidden rounded-xl border border-stone-200/80 bg-[#fffdf9] p-4 shadow-[0_1px_2px_rgba(28,25,23,0.04)] transition duration-300 hover:-translate-y-0.5 hover:border-stone-300 hover:shadow-[0_16px_30px_-24px_rgba(28,25,23,0.55)]">
      <div className={`absolute inset-x-0 top-0 h-[3px] bg-gradient-to-r ${styles.bar}`} />
      <div className="flex items-start justify-between gap-2">
        <p className="text-[9px] font-semibold uppercase leading-snug tracking-[0.18em] text-stone-500">
          {label}
        </p>
        {icon && (
          <span className={`rounded-md p-1.5 ${styles.chip}`}>
            <Icon name={icon} size={14} />
          </span>
        )}
      </div>
      <p
        className={`mt-3 text-2xl font-semibold leading-none tracking-tight tabular-nums ${styles.text}`}
        aria-live="polite"
      >
        {pending ? '—' : numberFormatter.format(value)}
      </p>
      <p className="mt-1.5 text-[11px] leading-tight text-stone-500">
        {unavailable ? 'Unavailable right now' : detail}
      </p>
    </div>
  );
}

function SectionHeading({ icon, title }) {
  return (
    <h2 className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.24em] text-stone-500">
      <span className="flex h-6 w-6 items-center justify-center rounded-md border border-stone-200 bg-[#fffdf9] text-teal-700">
        <Icon name={icon} size={12} />
      </span>
      {title}
    </h2>
  );
}

function Dashboard() {
  const [data, setData] = useState(null);
  const [failedSections, setFailedSections] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  async function loadDashboard(isRefresh = false) {
    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    try {
      const result = await requestDashboardData();
      setData((current) => ({
        ...(current ?? emptyDashboardData),
        ...result.data,
      }));
      setFailedSections(result.errors);
    } catch {
      setFailedSections(
        Object.fromEntries(
          API_ENDPOINTS.map((endpoint) => [
            endpoint.key,
            'Dashboard services could not be reached.',
          ]),
        ),
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let active = true;
    requestDashboardData()
      .then((result) => {
        if (!active) return;
        setData((current) => ({
          ...(current ?? emptyDashboardData),
          ...result.data,
        }));
        setFailedSections(result.errors);
      })
      .catch(() => {
        if (!active) return;
        setFailedSections(
          Object.fromEntries(
            API_ENDPOINTS.map((endpoint) => [
              endpoint.key,
              'Dashboard services could not be reached.',
            ]),
          ),
        );
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const dashboardData = data ?? emptyDashboardData;
  const failedEntries = API_ENDPOINTS.filter(
    (endpoint) => failedSections[endpoint.key],
  );
  const productsUnavailable = Boolean(failedSections.products);
  const categoriesUnavailable = Boolean(failedSections.categories);
  const suppliersUnavailable = Boolean(failedSections.suppliers);
  const ordersUnavailable = Boolean(failedSections.orders);
  const purchaseOrdersUnavailable = Boolean(failedSections.purchaseOrders);
  const showInitialPlaceholders = loading || !data;

  const lowStockProducts = useMemo(
    () =>
      dashboardData.products
        .filter(
          (product) =>
            getProductQuantity(product) <= getProductReorderLevel(product),
        )
        .sort(
          (first, second) =>
            getProductQuantity(first) - getProductQuantity(second),
        ),
    [dashboardData.products],
  );

  const metrics = useMemo(() => {
    const lowStockCount = dashboardData.products.filter((product) => {
      const quantity = getProductQuantity(product);
      return quantity > 0 && quantity <= getProductReorderLevel(product);
    }).length;
    const outOfStockCount = dashboardData.products.filter(
      (product) => getProductQuantity(product) === 0,
    ).length;

    return {
      lowStockCount,
      outOfStockCount,
      totalUnits: dashboardData.products.reduce(
        (total, product) => total + getProductQuantity(product),
        0,
      ),
      pendingOrders: getOrderStatusCount(dashboardData.orders, 'Pending'),
      confirmedOrders: getOrderStatusCount(dashboardData.orders, 'Confirmed'),
      deliveredOrders: getOrderStatusCount(dashboardData.orders, 'Delivered'),
      pendingPurchaseOrders: getOrderStatusCount(dashboardData.purchaseOrders, 'Pending'),
      receivedPurchaseOrders: getOrderStatusCount(dashboardData.purchaseOrders, 'Received'),
    };
  }, [dashboardData]);

  const inventoryHealth = useMemo(() => {
    const groups = [
      {
        label: 'In Stock',
        tone: 'teal',
        products: dashboardData.products.filter((product) => {
          const quantity = getProductQuantity(product);
          return quantity > getProductReorderLevel(product);
        }),
      },
      {
        label: 'Low Stock',
        tone: 'amber',
        products: dashboardData.products.filter((product) => {
          const quantity = getProductQuantity(product);
          return quantity > 0 && quantity <= getProductReorderLevel(product);
        }),
      },
      {
        label: 'Out of Stock',
        tone: 'red',
        products: dashboardData.products.filter(
          (product) => getProductQuantity(product) === 0,
        ),
      },
    ];
    const productCount = dashboardData.products.length;

    return groups.map((group) => {
      const units = group.products.reduce(
        (total, product) => total + getProductQuantity(product),
        0,
      );

      return {
        ...group,
        value: productCount
          ? `${Math.round((group.products.length / productCount) * 100)}%`
          : '0%',
        amount: `${numberFormatter.format(group.products.length)} ${group.products.length === 1 ? 'product' : 'products'} · ${numberFormatter.format(units)} units`,
      };
    });
  }, [dashboardData]);

  const attentionSummaries = useMemo(
    () => getAttentionSummaries(dashboardData, failedSections),
    [dashboardData, failedSections],
  );
  const recentSalesOrders = useMemo(
    () => getLatestById(dashboardData.orders),
    [dashboardData.orders],
  );
  const recentPurchaseOrders = useMemo(
    () => getLatestById(dashboardData.purchaseOrders),
    [dashboardData.purchaseOrders],
  );

  const warehouseItems = useMemo(
    () =>
      [...dashboardData.products]
        .sort((first, second) => getProductQuantity(second) - getProductQuantity(first))
        .slice(0, 12)
        .map((product) => {
          const quantity = getProductQuantity(product);
          const reorderLevel = getProductReorderLevel(product);
          const tone = quantity <= 0 ? 'red' : quantity <= reorderLevel ? 'amber' : 'teal';
          return { id: product.id, label: product.name, value: quantity, tone };
        }),
    [dashboardData.products],
  );

  const inventoryStats = [
    { label: 'Total Products', value: dashboardData.products.length, detail: 'products in catalog', tone: 'teal', icon: 'box', unavailable: productsUnavailable },
    { label: 'Total Categories', value: dashboardData.categories.length, detail: 'categories tracked', tone: 'teal', icon: 'tag', unavailable: categoriesUnavailable },
    { label: 'Low Stock', value: metrics.lowStockCount, detail: 'products to review', tone: 'amber', icon: 'clock', unavailable: productsUnavailable },
    { label: 'Out of Stock', value: metrics.outOfStockCount, detail: 'products unavailable', tone: 'red', icon: 'alert', unavailable: productsUnavailable },
    { label: 'Total Units', value: metrics.totalUnits, detail: 'units on hand', tone: 'teal', icon: 'layers', unavailable: productsUnavailable },
  ];
  const salesStats = [
    { label: 'Total Orders', value: dashboardData.orders.length, detail: 'sales orders', tone: 'teal', icon: 'cart', unavailable: ordersUnavailable },
    { label: 'Pending Orders', value: metrics.pendingOrders, detail: 'awaiting action', tone: 'amber', icon: 'clock', unavailable: ordersUnavailable },
    { label: 'Confirmed Orders', value: metrics.confirmedOrders, detail: 'confirmed', tone: 'teal', icon: 'check', unavailable: ordersUnavailable },
    { label: 'Delivered Orders', value: metrics.deliveredOrders, detail: 'delivered', tone: 'teal', icon: 'truck', unavailable: ordersUnavailable },
  ];
  const procurementStats = [
    { label: 'Total Purchase Orders', value: dashboardData.purchaseOrders.length, detail: 'purchase orders', tone: 'teal', icon: 'clipboard', unavailable: purchaseOrdersUnavailable },
    { label: 'Pending Purchase Orders', value: metrics.pendingPurchaseOrders, detail: 'awaiting action', tone: 'amber', icon: 'clock', unavailable: purchaseOrdersUnavailable },
    { label: 'Received Purchase Orders', value: metrics.receivedPurchaseOrders, detail: 'received', tone: 'teal', icon: 'check', unavailable: purchaseOrdersUnavailable },
  ];

  const heroStats = [
    { label: 'Products', value: dashboardData.products.length, tone: 'text-teal-300', unavailable: productsUnavailable },
    { label: 'Units on hand', value: metrics.totalUnits, tone: 'text-white', unavailable: productsUnavailable },
    { label: 'Low stock', value: metrics.lowStockCount, tone: 'text-amber-300', unavailable: productsUnavailable },
    { label: 'Pending orders', value: metrics.pendingOrders, tone: 'text-rose-300', unavailable: ordersUnavailable },
  ];

  return (
    <div className="space-y-5">
      <section className="animate-rise relative overflow-hidden rounded-2xl border border-white/5 bg-[radial-gradient(130%_130%_at_0%_0%,#17322d_0%,#101a1c_48%,#0a1011_100%)] p-5 text-stone-100 shadow-[0_30px_70px_-52px_rgba(12,20,22,0.95)] sm:p-6">
        <div className="pointer-events-none absolute -right-28 -top-28 h-72 w-72 rounded-full bg-teal-400/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 left-1/3 h-56 w-56 rounded-full bg-emerald-400/[0.07] blur-3xl" />

        <div className="relative grid items-center gap-6 lg:grid-cols-[1.05fr_1fr]">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-teal-300/20 bg-teal-400/10 px-2.5 py-1 text-[9px] font-semibold uppercase tracking-[0.2em] text-teal-200">
                <Icon name="spark" size={11} />
                Live operations
              </span>
              <span className="inline-flex items-center gap-1.5 text-[9px] uppercase tracking-[0.22em] text-stone-400">
                <span className="relative flex h-1.5 w-1.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-70" />
                  <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-teal-400" />
                </span>
                Synced with ERP
              </span>
            </div>

            <h1 className="mt-3 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
              Inventory command center
            </h1>
            <p className="mt-2 max-w-xl text-sm leading-relaxed text-stone-400">
              A live 3D snapshot of stock health across your catalog, with demand
              forecasts feeding the reorder queue.
            </p>

            <div className="mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {heroStats.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-lg border border-white/[0.07] bg-white/[0.04] px-3 py-2 backdrop-blur-sm"
                >
                  <p className="text-[8px] font-semibold uppercase tracking-[0.18em] text-stone-400">
                    {stat.label}
                  </p>
                  <p className={`mt-1 text-lg font-semibold leading-none tabular-nums ${stat.tone}`}>
                    {showInitialPlaceholders || stat.unavailable
                      ? '—'
                      : numberFormatter.format(stat.value)}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => loadDashboard(true)}
                disabled={loading || refreshing}
                className="inline-flex items-center gap-2 rounded-lg bg-teal-300 px-3.5 py-2 text-sm font-semibold text-[#06201d] shadow-[0_10px_30px_-14px_rgba(45,212,191,0.9)] transition hover:bg-teal-200 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Icon
                  name="refresh"
                  size={15}
                  className={refreshing ? 'animate-spin' : ''}
                />
                {refreshing ? 'Refreshing…' : 'Refresh data'}
              </button>
              <Link
                to="/forecasting"
                className="inline-flex items-center gap-1.5 rounded-lg border border-white/15 px-3.5 py-2 text-sm font-medium text-stone-200 transition hover:border-teal-300/50 hover:bg-white/[0.06] hover:text-white"
              >
                Open forecast
                <Icon name="arrowRight" size={14} />
              </Link>
            </div>
          </div>

          <div className="relative h-56 sm:h-64 lg:h-72">
            <Warehouse3D items={warehouseItems} />
            <div className="pointer-events-none absolute inset-x-0 bottom-1 flex flex-wrap justify-center gap-3 text-[8px] uppercase tracking-[0.18em] text-stone-400">
              <span className="inline-flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-[2px] bg-teal-400" /> In stock
              </span>
              <span className="inline-flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-[2px] bg-amber-400" /> Low
              </span>
              <span className="inline-flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-[2px] bg-rose-500" /> Out
              </span>
            </div>
          </div>
        </div>
      </section>

      {loading && (
        <p className="text-sm text-stone-600" role="status">
          <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-stone-300 border-t-teal-700 align-[-3px]" />
          Loading dashboard data…
        </p>
      )}

      {failedEntries.length > 0 && (
        <div role="alert" className="flex flex-col gap-2 border-l-4 border-amber-500 bg-amber-50 px-3 py-2.5 text-sm text-amber-950 sm:flex-row sm:items-center sm:justify-between">
          <span>
            Some dashboard sections could not load:{' '}
            {failedEntries.map((endpoint) => endpoint.label).join(', ')}. Other
            sections show the latest available data.
          </span>
          <button
            type="button"
            onClick={() => loadDashboard(Boolean(data))}
            disabled={refreshing || loading}
            className="w-fit font-medium text-amber-950 underline decoration-amber-400 underline-offset-2 hover:decoration-amber-700 disabled:opacity-60"
          >
            Try again
          </button>
        </div>
      )}

      <section className="space-y-3">
        <SectionHeading icon="box" title="Inventory" />
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
          {inventoryStats.map((stat) => (
            <StatCard key={stat.label} {...stat} loading={showInitialPlaceholders} />
          ))}
        </div>
      </section>

      <section className="overflow-hidden rounded-xl border border-stone-200 bg-[#fffdf9] shadow-sm">
        <div className="flex items-center justify-between gap-3 border-b border-stone-200 p-4">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-amber-50 text-amber-700 ring-1 ring-amber-100">
              <Icon name="alert" size={16} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-stone-900">Low-stock alerts</h2>
              <p className="text-xs text-stone-500">
                Products at or below their reorder level
              </p>
            </div>
          </div>
          <span className="rounded-full border border-amber-200/70 bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-900 tabular-nums">
            {showInitialPlaceholders || productsUnavailable
              ? '—'
              : numberFormatter.format(lowStockProducts.length)}
          </span>
        </div>

        {productsUnavailable ? (
          <p className="p-4 text-sm text-stone-600">
            Stock alerts are unavailable right now. Use Try again above to reload
            them.
          </p>
        ) : !data ? (
          <p className="p-4 text-sm text-stone-600">
            {loading ? 'Loading stock alerts…' : 'Stock alerts are unavailable.'}
          </p>
        ) : lowStockProducts.length === 0 ? (
          <p className="p-4 text-sm text-stone-600">
            No products are at or below their reorder level.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-stone-50 text-[10px] uppercase tracking-[0.12em] text-stone-500">
                <tr>
                  <th className="px-4 py-3 font-semibold">Status</th>
                  <th className="px-4 py-3 font-semibold">Product</th>
                  <th className="px-4 py-3 font-semibold">SKU</th>
                  <th className="px-4 py-3 text-right font-semibold">Current quantity</th>
                  <th className="px-4 py-3 text-right font-semibold">Reorder level</th>
                </tr>
              </thead>
              <tbody>
                {lowStockProducts.map((product) => {
                  const quantity = getProductQuantity(product);
                  const outOfStock = quantity <= 0;
                  return (
                    <tr
                      key={product.id}
                      className="border-t border-stone-100 transition hover:bg-stone-50/70"
                    >
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium ring-1 ${
                            outOfStock
                              ? 'bg-red-50 text-red-800 ring-red-100'
                              : 'bg-amber-50 text-amber-900 ring-amber-100'
                          }`}
                        >
                          <span
                            className={`h-1.5 w-1.5 rounded-full ${
                              outOfStock ? 'bg-red-500' : 'bg-amber-500'
                            }`}
                          />
                          {outOfStock ? 'Out of stock' : 'Low stock'}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-medium text-stone-800">{product.name}</td>
                      <td className="px-4 py-3 font-mono text-xs text-stone-500">{product.sku || '—'}</td>
                      <td className="px-4 py-3 text-right font-medium tabular-nums">
                        {numberFormatter.format(quantity)}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums text-stone-500">
                        {numberFormatter.format(getProductReorderLevel(product))}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="space-y-3">
        <SectionHeading icon="cart" title="Sales" />
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {salesStats.map((stat) => (
            <StatCard key={stat.label} {...stat} loading={showInitialPlaceholders} />
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <SectionHeading icon="truck" title="Procurement & Suppliers" />
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {[
            ...procurementStats,
            {
              label: 'Total Suppliers',
              value: dashboardData.suppliers.length,
              detail: 'suppliers',
              tone: 'teal',
              icon: 'users',
              unavailable: suppliersUnavailable,
            },
          ].map((stat) => (
            <StatCard key={stat.label} {...stat} loading={showInitialPlaceholders} />
          ))}
        </div>
      </section>

      <div className="grid gap-4 xl:grid-cols-[1.5fr_1fr]">
        <section className="rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-50 text-teal-700 ring-1 ring-teal-100">
                <Icon name="layers" size={16} />
              </span>
              <div>
                <h2 className="text-base font-semibold text-stone-900">Inventory Health</h2>
                <p className="text-xs text-stone-500">Stock level by product count</p>
              </div>
            </div>
            <span className="rounded-full border border-teal-200/70 bg-teal-50 px-2 py-1 text-[9px] font-semibold uppercase tracking-[0.2em] text-teal-700">
              Live data
            </span>
          </div>

          <div className="mt-5 space-y-4">
            {inventoryHealth.map((item) => (
              <div key={item.label}>
                <div className="mb-1.5 flex items-center justify-between text-sm">
                  <span className="flex items-center gap-2 font-medium text-stone-700">
                    <span
                      className={`h-2 w-2 rounded-full ${
                        item.tone === 'teal'
                          ? 'bg-teal-500'
                          : item.tone === 'amber'
                            ? 'bg-amber-400'
                            : 'bg-red-500'
                      }`}
                    />
                    {item.label}
                  </span>
                  <span className="font-semibold tabular-nums text-stone-600">
                    {showInitialPlaceholders || productsUnavailable ? '—' : item.value}
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-stone-200/80">
                  <div
                    className={`h-full rounded-full transition-[width] duration-700 ease-out ${
                      item.tone === 'teal'
                        ? 'bg-gradient-to-r from-teal-400 to-emerald-500'
                        : item.tone === 'amber'
                          ? 'bg-gradient-to-r from-amber-300 to-orange-400'
                          : 'bg-gradient-to-r from-rose-400 to-red-500'
                    }`}
                    style={{
                      width:
                        showInitialPlaceholders || productsUnavailable
                          ? '0%'
                          : item.value,
                    }}
                  />
                </div>
                <p className="mt-1 text-xs text-stone-500">
                  {productsUnavailable
                    ? 'Product levels are unavailable right now.'
                    : loading
                      ? 'Loading product levels…'
                      : !data
                        ? 'Product levels are unavailable.'
                        : item.amount}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-rose-50 text-rose-600 ring-1 ring-rose-100">
              <Icon name="alert" size={16} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-stone-900">Attention Required</h2>
              <p className="text-xs text-stone-500">Items that need an operator decision</p>
            </div>
          </div>
          <div className="mt-4 space-y-2.5">
            {attentionSummaries.map((alert) => (
              <div
                key={alert.title}
                className={`rounded-lg border p-3 ${
                  alert.tone === 'amber'
                    ? 'border-amber-200/70 bg-amber-50/60'
                    : 'border-rose-200/70 bg-rose-50/60'
                }`}
              >
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-medium text-stone-800">{alert.title}</p>
                  <span
                    className={`rounded-full bg-white/70 px-2 py-0.5 text-xs font-semibold tabular-nums ring-1 ${
                      alert.tone === 'amber'
                        ? 'text-amber-800 ring-amber-200/70'
                        : 'text-rose-800 ring-rose-200/70'
                    }`}
                  >
                    {showInitialPlaceholders || alert.unavailable
                      ? '—'
                      : numberFormatter.format(alert.records.length)}
                  </span>
                </div>
                <p className="mt-1 line-clamp-2 text-xs leading-relaxed text-stone-600">
                  {alert.unavailable
                    ? alert.detail
                    : loading
                      ? 'Loading…'
                      : !data
                        ? 'Dashboard data is unavailable.'
                        : alert.detail}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-stone-100 text-stone-700 ring-1 ring-stone-200">
            <Icon name="spark" size={16} />
          </span>
          <div>
            <h2 className="text-base font-semibold text-stone-900">Quick Actions</h2>
            <p className="text-xs text-stone-500">Jump straight into the most common tasks</p>
          </div>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {quickActions.map((action) => (
            <Link
              key={action.label}
              to={action.path}
              className="group flex items-center gap-2 rounded-lg border border-stone-200 bg-stone-50 px-3 py-2.5 text-sm font-medium text-stone-700 transition hover:border-teal-300 hover:bg-teal-50 hover:text-teal-800"
            >
              <span className="text-stone-400 transition group-hover:text-teal-600">
                <Icon name={action.icon} size={15} />
              </span>
              <span className="flex-1 truncate">{action.label}</span>
              <span className="text-stone-300 transition group-hover:translate-x-0.5 group-hover:text-teal-600">
                <Icon name="arrowRight" size={13} />
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-sm">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-stone-100 text-stone-700 ring-1 ring-stone-200">
              <Icon name="clock" size={16} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-stone-900">Recent Activity</h2>
              <p className="text-xs text-stone-500">Latest sales and purchase orders by ID</p>
            </div>
          </div>
          <span className="text-[9px] font-semibold uppercase tracking-[0.2em] text-stone-400">
            Live data
          </span>
        </div>

        {!data ? (
          <p className="mt-4 text-sm text-stone-600" role="status">
            {loading ? 'Loading recent orders…' : 'Recent orders are unavailable.'}
          </p>
        ) : (
          <div className="mt-4 grid gap-5 sm:grid-cols-2">
            <div>
              <h3 className="mb-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-stone-500">Sales Orders</h3>
              {ordersUnavailable ? (
                <p className="text-sm text-stone-500">
                  Recent sales orders are unavailable right now.
                </p>
              ) : recentSalesOrders.length ? (
                <div className="space-y-3">
                  {recentSalesOrders.map((order) => (
                    <div
                      key={order.id}
                      className="flex items-start gap-3 rounded-lg px-1 py-1.5 transition hover:bg-stone-50"
                    >
                      <span className="mt-1 flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-teal-600 ring-1 ring-teal-100">
                        <Icon name="cart" size={12} />
                      </span>
                      <div className="flex-1 border-b border-stone-100 pb-2 last:border-b-0 last:pb-0">
                        <div className="flex items-center justify-between gap-2">
                          <p className="truncate text-sm font-medium text-stone-700">
                            Order #{order.id} · {order.customer_name}
                          </p>
                          <span className="shrink-0 rounded-full bg-stone-100 px-2 py-0.5 text-[10px] font-medium text-stone-600">
                            {order.status}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-stone-500">No sales orders available.</p>
              )}
            </div>

            <div>
              <h3 className="mb-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-stone-500">Purchase Orders</h3>
              {purchaseOrdersUnavailable ? (
                <p className="text-sm text-stone-500">
                  Recent purchase orders are unavailable right now.
                </p>
              ) : recentPurchaseOrders.length ? (
                <div className="space-y-3">
                  {recentPurchaseOrders.map((order) => (
                    <div
                      key={order.id}
                      className="flex items-start gap-3 rounded-lg px-1 py-1.5 transition hover:bg-stone-50"
                    >
                      <span className="mt-1 flex h-6 w-6 items-center justify-center rounded-md bg-amber-50 text-amber-600 ring-1 ring-amber-100">
                        <Icon name="clipboard" size={12} />
                      </span>
                      <div className="flex-1 border-b border-stone-100 pb-2 last:border-b-0 last:pb-0">
                        <div className="flex items-center justify-between gap-2">
                          <p className="truncate text-sm font-medium text-stone-700">
                            Purchase order #{order.id} · Supplier {order.supplier_id}
                          </p>
                          <span className="shrink-0 rounded-full bg-stone-100 px-2 py-0.5 text-[10px] font-medium text-stone-600">
                            {order.status}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-stone-500">No purchase orders available.</p>
              )}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

export default Dashboard;
