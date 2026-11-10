import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../config';
import { apiFetch } from '../api';
import { Icon } from '../components/Icons';

async function fetchInventory(path, options) {
  try {
    return await apiFetch(path, options);
  } catch (error) {
    if (error instanceof TypeError) {
      const target = API_BASE_URL || 'the frontend API proxy';
      throw new Error(
        `Cannot connect to ${target}. Verify that the backend is running and the frontend API proxy is configured.`,
      );
    }
    throw error;
  }
}

function getResponseError(data, fallback) {
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail
      .map((issue) => issue.msg)
      .filter(Boolean)
      .join(' ');
  }
  return fallback;
}

async function requestInventoryData() {
  const [productResponse, transactionResponse] = await Promise.all([
    fetchInventory('/products/'),
    fetchInventory('/inventory-transactions/'),
  ]);

  if (!productResponse.ok || !transactionResponse.ok) {
    const failedResponse = !productResponse.ok ? productResponse : transactionResponse;
    const data = await failedResponse.json().catch(() => ({}));
    throw new Error(
      getResponseError(data, `Could not load inventory data (HTTP ${failedResponse.status}).`),
    );
  }

  const productData = await productResponse.json();
  const transactionData = await transactionResponse.json();

  return {
    products: productData,
    transactions: Array.isArray(transactionData)
      ? transactionData
      : transactionData.items || [],
  };
}

function getQuantity(product) {
  const value = Number(product.stock_quantity);
  return Number.isFinite(value) ? value : 0;
}

function getReorderLevel(product) {
  const value = Number(product.reorder_level);
  return Number.isFinite(value) ? value : 0;
}

const numberFormatter = new Intl.NumberFormat('en-IN');

const inputClassName =
  'w-full rounded-lg border border-stone-300 bg-white px-3 py-2.5 text-sm text-stone-800 outline-none transition placeholder:text-stone-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-100';

function InventoryTransactions() {
  const [products, setProducts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [type, setType] = useState('Stock In');
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [reason, setReason] = useState('');
  const [message, setMessage] = useState('');
  const [messageIsError, setMessageIsError] = useState(false);
  const [loadError, setLoadError] = useState('');
  const [dataLoading, setDataLoading] = useState(true);
  const [loading, setLoading] = useState(false);

  async function loadData() {
    setDataLoading(true);
    setLoadError('');
    try {
      const inventoryData = await requestInventoryData();
      setProducts(inventoryData.products);
      setTransactions(inventoryData.transactions);
    } catch (error) {
      setLoadError(error.message);
    } finally {
      setDataLoading(false);
    }
  }

  useEffect(() => {
    let active = true;
    requestInventoryData()
      .then((inventoryData) => {
        if (!active) return;
        setProducts(inventoryData.products);
        setTransactions(inventoryData.transactions);
      })
      .catch((error) => {
        if (active) setLoadError(error.message);
      })
      .finally(() => {
        if (active) setDataLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage('');
    setMessageIsError(false);

    if (
      !productId
      || !Number.isInteger(Number(quantity))
      || Number(quantity) <= 0
      || !reason.trim()
    ) {
      setMessage('Select a product, enter a positive quantity, and provide a reason.');
      setMessageIsError(true);
      return;
    }

    setLoading(true);

    try {
      const response = await fetchInventory('/inventory-transactions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: Number(productId),
          transaction_type: type,
          quantity: Number(quantity),
          reason: reason.trim(),
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          getResponseError(data, `Inventory transaction failed (HTTP ${response.status}).`),
        );
      }

      setMessage('Inventory updated successfully.');
      setMessageIsError(false);
      setQuantity('');
      setReason('');
      await loadData();
    } catch (error) {
      setMessage(error.message);
      setMessageIsError(true);
    } finally {
      setLoading(false);
    }
  }

  const totalUnits = products.reduce(
    (total, product) => total + getQuantity(product),
    0,
  );
  const lowStockCount = products.filter((product) => {
    const stock = getQuantity(product);
    return stock > 0 && stock <= getReorderLevel(product);
  }).length;

  const selectedProduct = products.find(
    (product) => String(product.id) === String(productId),
  );

  return (
    <div className="space-y-5">
      <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-stone-200 bg-[#fffdf9] p-5 shadow-[0_1px_2px_rgba(28,25,23,0.04)] sm:p-6"
        >
          <div className="flex items-start gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal-700 ring-1 ring-teal-100">
              <Icon name="inventory" size={18} />
            </span>
            <div>
              <h1 className="text-lg font-semibold tracking-tight text-stone-900">
                Inventory Operations
              </h1>
              <p className="mt-0.5 text-xs leading-relaxed text-stone-500">
                Record a stock movement. Every change is written to the history
                below.
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-2">
            <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
              Transaction Type
              <select
                value={type}
                onChange={(event) => setType(event.target.value)}
                className={inputClassName}
              >
                <option value="Stock In">Stock In</option>
                <option value="Stock Out">Stock Out</option>
              </select>
            </label>

            <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
              Product
              <select
                required
                value={productId}
                onChange={(event) => setProductId(event.target.value)}
                className={inputClassName}
              >
                <option value="">Select a product</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name} — Stock: {product.stock_quantity}
                  </option>
                ))}
              </select>
            </label>

            <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
              Quantity
              <input
                required
                type="number"
                min="1"
                step="1"
                value={quantity}
                onChange={(event) => setQuantity(event.target.value)}
                className={inputClassName}
                placeholder="0"
              />
            </label>

            <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
              Reason
              <input
                required
                value={reason}
                onChange={(event) => setReason(event.target.value)}
                placeholder="e.g. New shipment or damaged goods"
                className={inputClassName}
              />
            </label>
          </div>

          {selectedProduct && (
            <p className="mt-3 rounded-lg border border-stone-200 bg-stone-50 px-3 py-2 text-xs text-stone-600">
              Current stock for{' '}
              <span className="font-semibold text-stone-800">
                {selectedProduct.name}
              </span>
              : {numberFormatter.format(getQuantity(selectedProduct))} units ·
              reorder level {numberFormatter.format(getReorderLevel(selectedProduct))}
            </p>
          )}

          <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-stone-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Icon name="check" size={15} />
              {loading ? 'Saving…' : 'Record Stock Movement'}
            </button>
            <p className="text-[11px] leading-snug text-stone-400">
              Stock Out is rejected when the quantity exceeds available stock.
            </p>
          </div>

          {message && (
            <p
              role={messageIsError ? 'alert' : 'status'}
              className={`mt-3 rounded-lg border px-3 py-2 text-sm ${
                messageIsError
                  ? 'border-rose-200 bg-rose-50 text-rose-800'
                  : 'border-teal-200 bg-teal-50 text-teal-800'
              }`}
            >
              {message}
            </p>
          )}
        </form>

        <section className="rounded-2xl border border-stone-200 bg-[#fffdf9] p-5 shadow-[0_1px_2px_rgba(28,25,23,0.04)] sm:p-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-semibold text-stone-900">
                Stock snapshot
              </h2>
              <p className="mt-0.5 text-xs text-stone-500">
                Live totals from the product catalog
              </p>
            </div>
            <button
              type="button"
              onClick={loadData}
              disabled={dataLoading}
              aria-label="Refresh inventory data"
              className="rounded-lg border border-stone-200 bg-white p-2 text-stone-500 transition hover:border-teal-300 hover:text-teal-700 disabled:opacity-50"
            >
              <Icon
                name="refresh"
                size={15}
                className={dataLoading ? 'animate-spin' : ''}
              />
            </button>
          </div>

          <div className="mt-5 grid grid-cols-3 gap-2">
            {[
              {
                label: 'Products',
                value: products.length,
                tone: 'text-stone-900',
                icon: 'box',
                chip: 'bg-teal-50 text-teal-700',
              },
              {
                label: 'Units on hand',
                value: totalUnits,
                tone: 'text-stone-900',
                icon: 'layers',
                chip: 'bg-stone-100 text-stone-600',
              },
              {
                label: 'Low stock',
                value: lowStockCount,
                tone: 'text-amber-900',
                icon: 'alert',
                chip: 'bg-amber-50 text-amber-700',
              },
            ].map((stat) => (
              <div
                key={stat.label}
                className="rounded-xl border border-stone-200 bg-white p-3"
              >
                <span className={`inline-flex rounded-md p-1.5 ${stat.chip}`}>
                  <Icon name={stat.icon} size={13} />
                </span>
                <p className={`mt-2 text-xl font-semibold leading-none tabular-nums ${stat.tone}`}>
                  {dataLoading ? '—' : numberFormatter.format(stat.value)}
                </p>
                <p className="mt-1 text-[10px] leading-tight text-stone-500">
                  {stat.label}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-4 space-y-2 border-t border-stone-100 pt-4 text-xs leading-relaxed text-stone-500">
            <p className="flex items-start gap-2">
              <Icon name="check" size={13} className="mt-0.5 shrink-0 text-teal-600" />
              Stock In adds units; Stock Out removes them.
            </p>
            <p className="flex items-start gap-2">
              <Icon name="clock" size={13} className="mt-0.5 shrink-0 text-teal-600" />
              Every successful movement appears in Stock History.
            </p>
            <p className="flex items-start gap-2">
              <Icon name="alert" size={13} className="mt-0.5 shrink-0 text-amber-600" />
              Low stock means at or below the product reorder level.
            </p>
          </div>
        </section>
      </section>

      <section className="overflow-hidden rounded-xl border border-stone-200 bg-[#fffdf9] shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-200 p-4">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-stone-100 text-stone-700 ring-1 ring-stone-200">
              <Icon name="clipboard" size={16} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-stone-900">
                Stock History
              </h2>
              <p className="text-xs text-stone-500">
                Every recorded stock movement, newest first
              </p>
            </div>
          </div>
          <span className="rounded-full border border-stone-200 bg-stone-50 px-2.5 py-1 text-xs font-semibold tabular-nums text-stone-600">
            {dataLoading ? '—' : numberFormatter.format(transactions.length)}
          </span>
        </div>

        {loadError && (
          <div
            role="alert"
            className="m-4 flex flex-col gap-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2.5 text-sm text-rose-800 sm:flex-row sm:items-center sm:justify-between"
          >
            <span>{loadError}</span>
            <button
              type="button"
              onClick={loadData}
              className="w-fit font-semibold underline decoration-rose-300 underline-offset-2 hover:decoration-rose-600"
            >
              Try again
            </button>
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-stone-50 text-[10px] uppercase tracking-[0.12em] text-stone-500">
              <tr>
                {['Product', 'Type', 'Quantity', 'Previous Stock', 'New Stock', 'Reason', 'Date'].map((heading) => (
                  <th key={heading} className="whitespace-nowrap px-4 py-3 font-semibold">
                    {heading}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {transactions.map((item) => (
                <tr
                  key={item.id}
                  className="border-t border-stone-100 transition hover:bg-stone-50/70"
                >
                  <td className="px-4 py-3 font-medium text-stone-800">
                    {item.product_name || item.product?.name || item.product_id}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium ring-1 ${
                        item.transaction_type === 'Stock In'
                          ? 'bg-teal-50 text-teal-800 ring-teal-100'
                          : 'bg-amber-50 text-amber-900 ring-amber-100'
                      }`}
                    >
                      <span
                        className={`h-1.5 w-1.5 rounded-full ${
                          item.transaction_type === 'Stock In'
                            ? 'bg-teal-500'
                            : 'bg-amber-500'
                        }`}
                      />
                      {item.transaction_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-medium tabular-nums">
                    {numberFormatter.format(item.quantity)}
                  </td>
                  <td className="px-4 py-3 tabular-nums text-stone-500">
                    {numberFormatter.format(item.previous_stock)}
                  </td>
                  <td className="px-4 py-3 font-medium tabular-nums text-stone-800">
                    {numberFormatter.format(item.new_stock)}
                  </td>
                  <td className="max-w-xs px-4 py-3 text-stone-600">
                    {item.reason}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-xs text-stone-500">
                    {item.created_at
                      ? new Date(item.created_at).toLocaleString()
                      : '—'}
                  </td>
                </tr>
              ))}
              {!dataLoading && transactions.length === 0 && !loadError && (
                <tr>
                  <td colSpan="7" className="px-4 py-10 text-center">
                    <span className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-stone-100 text-stone-400">
                      <Icon name="clipboard" size={18} />
                    </span>
                    <p className="mt-3 text-sm font-medium text-stone-700">
                      No inventory transactions yet
                    </p>
                    <p className="mt-1 text-xs text-stone-500">
                      Record a stock movement above to start the history.
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default InventoryTransactions;
