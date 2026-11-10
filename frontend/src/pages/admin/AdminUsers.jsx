import { useState } from 'react';
import { apiFetch } from '../../api';
import { Icon } from '../../components/Icons';
import {
  ErrorBlock,
  KpiCard,
  LoadingBlock,
  Modal,
  Pagination,
  Panel,
  SortHeader,
  formatCurrency,
  formatDate,
  formatDateTime,
  formatNumber,
  useAdminResource,
} from './AdminComponents';

const PAGE_SIZE = 20;

function StatusPill({ active }) {
  return (
    <span
      className={`inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] ${
        active
          ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
          : 'border-rose-200 bg-rose-50 text-rose-800'
      }`}
    >
      {active ? 'Active' : 'Inactive'}
    </span>
  );
}

export default function AdminUsers() {
  const [query, setQuery] = useState('');
  const [appliedQuery, setAppliedQuery] = useState('');
  const [sort, setSort] = useState('revenue');
  const [direction, setDirection] = useState('desc');
  const [page, setPage] = useState(1);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [statusTarget, setStatusTarget] = useState(null);
  const [statusBusy, setStatusBusy] = useState(false);
  const [statusError, setStatusError] = useState('');

  const params = new URLSearchParams();
  if (appliedQuery) params.set('q', appliedQuery);
  params.set('sort', sort);
  params.set('direction', direction);
  params.set('limit', String(PAGE_SIZE));
  params.set('offset', String((page - 1) * PAGE_SIZE));

  const users = useAdminResource(`/admin/users?${params.toString()}`);
  const profile = useAdminResource('/auth/me');
  const detail = useAdminResource(
    selectedUserId ? `/admin/users/${selectedUserId}` : null,
  );

  function applySearch(event) {
    event.preventDefault();
    setAppliedQuery(query.trim());
    setPage(1);
  }

  function handleSort(value) {
    if (value === sort) {
      setDirection((current) => (current === 'desc' ? 'asc' : 'desc'));
    } else {
      setSort(value);
      setDirection('desc');
    }
    setPage(1);
  }

  function openStatusDialog(user) {
    setStatusError('');
    setStatusTarget(user);
  }

  async function confirmStatusChange() {
    if (!statusTarget) return;
    setStatusBusy(true);
    setStatusError('');
    try {
      const response = await apiFetch(`/admin/users/${statusTarget.user_id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !statusTarget.is_active }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : `The account could not be updated (HTTP ${response.status}).`,
        );
      }
      setStatusTarget(null);
      users.reload();
      if (selectedUserId) detail.reload();
    } catch (error) {
      setStatusError(error.message || 'The account could not be updated.');
    } finally {
      setStatusBusy(false);
    }
  }

  const items = users.data?.items ?? [];
  const myId = profile.data?.id;

  return (
    <div className="space-y-4">
      <Panel
        title="User accounts"
        subtitle="Accounts, sales activity and safe activation controls. Password hashes and tokens are never shown."
        actions={
          <button
            type="button"
            onClick={users.reload}
            className="inline-flex items-center gap-1.5 rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs font-medium text-stone-700 transition hover:bg-stone-50"
          >
            <Icon name="refresh" size={12} />
            Refresh
          </button>
        }
      >
        <form onSubmit={applySearch} className="mb-3 flex flex-wrap items-center gap-2">
          <label className="relative min-w-[13rem] flex-1">
            <span className="sr-only">Search users</span>
            <span className="pointer-events-none absolute inset-y-0 left-2.5 flex items-center text-stone-400">
              <Icon name="search" size={14} />
            </span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search by username or email"
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
          <label className="inline-flex items-center gap-1.5 text-xs text-stone-600">
            Sort
            <select
              value={sort}
              onChange={(event) => handleSort(event.target.value)}
              className="rounded-lg border border-stone-300 bg-white px-2 py-1.5 text-xs text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
            >
              <option value="revenue">Revenue</option>
              <option value="orders">Orders</option>
              <option value="username">Username</option>
              <option value="created_at">Created date</option>
            </select>
          </label>
          <button
            type="button"
            onClick={() => {
              setDirection((current) => (current === 'desc' ? 'asc' : 'desc'));
              setPage(1);
            }}
            className="rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs font-medium text-stone-700 transition hover:bg-stone-50"
          >
            {direction === 'desc' ? 'Highest first' : 'Lowest first'}
          </button>
        </form>

        {users.loading && !users.data ? (
          <LoadingBlock label="Loading user accounts…" />
        ) : users.error ? (
          <ErrorBlock message={users.error} onRetry={users.reload} />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-stone-200 text-sm">
                <thead className="bg-stone-50/80">
                  <tr>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      ID
                    </th>
                    <SortHeader
                      label="User"
                      value="username"
                      sort={sort}
                      direction={direction}
                      onSort={handleSort}
                    />
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      Email
                    </th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      Role
                    </th>
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      Status
                    </th>
                    <SortHeader
                      label="Created"
                      value="created_at"
                      sort={sort}
                      direction={direction}
                      onSort={handleSort}
                    />
                    <th scope="col" className="px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      Last sign-in
                    </th>
                    <SortHeader
                      label="Orders"
                      value="orders"
                      sort={sort}
                      direction={direction}
                      onSort={handleSort}
                      align="right"
                    />
                    <SortHeader
                      label="Revenue"
                      value="revenue"
                      sort={sort}
                      direction={direction}
                      onSort={handleSort}
                      align="right"
                    />
                    <th scope="col" className="px-3 py-2 text-right text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((user) => {
                    const isSelf = myId != null && user.user_id === myId;
                    return (
                      <tr
                        key={user.user_id ?? 'unassigned'}
                        className="border-t border-stone-100 transition hover:bg-stone-50/70"
                      >
                        <td className="whitespace-nowrap px-3 py-2.5 tabular-nums text-stone-500">
                          {user.user_id ?? '—'}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5">
                          <span className="font-medium text-stone-900">{user.username}</span>
                          {isSelf && (
                            <span className="ml-1.5 rounded bg-indigo-50 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-[0.08em] text-indigo-700">
                              You
                            </span>
                          )}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-stone-600">
                          {user.email || '—'}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5">
                          <span className="rounded bg-stone-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] text-stone-600">
                            {user.role || '—'}
                          </span>
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5">
                          {user.is_active === null ? (
                            <span className="text-stone-400">—</span>
                          ) : (
                            <StatusPill active={user.is_active} />
                          )}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-stone-600">
                          {formatDate(user.created_at)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-stone-600">
                          {formatDateTime(user.last_login_at)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-right tabular-nums text-stone-700">
                          {formatNumber(user.orders)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-right tabular-nums text-stone-700">
                          {formatCurrency(user.revenue)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-2.5 text-right">
                          {user.user_id === null ? (
                            <span className="text-[11px] text-stone-400">Legacy</span>
                          ) : (
                            <div className="inline-flex items-center gap-1">
                              <button
                                type="button"
                                onClick={() => setSelectedUserId(user.user_id)}
                                className="rounded-md border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-700 transition hover:bg-stone-50"
                              >
                                View
                              </button>
                              <button
                                type="button"
                                onClick={() => openStatusDialog(user)}
                                disabled={isSelf}
                                title={
                                  isSelf
                                    ? 'You cannot deactivate your own administrator account'
                                    : user.is_active
                                      ? 'Deactivate this account'
                                      : 'Reactivate this account'
                                }
                                className={`rounded-md border px-2 py-1 text-[11px] font-semibold transition disabled:cursor-not-allowed disabled:opacity-40 ${
                                  user.is_active
                                    ? 'border-rose-200 bg-rose-50 text-rose-800 hover:bg-rose-100'
                                    : 'border-emerald-200 bg-emerald-50 text-emerald-800 hover:bg-emerald-100'
                                }`}
                              >
                                {user.is_active ? 'Deactivate' : 'Reactivate'}
                              </button>
                            </div>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                  {items.length === 0 && (
                    <tr>
                      <td colSpan={10} className="px-3 py-10 text-center text-sm text-stone-500">
                        No accounts match this search.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <Pagination
              page={page}
              pageSize={PAGE_SIZE}
              total={users.data.total}
              onChange={setPage}
            />
          </>
        )}
      </Panel>

      <Modal
        open={selectedUserId !== null}
        onClose={() => setSelectedUserId(null)}
        title="User details"
        subtitle="Safe account and sales information"
        footer={
          <>
            <button
              type="button"
              onClick={() => setSelectedUserId(null)}
              className="rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 transition hover:bg-stone-50"
            >
              Close
            </button>
            {detail.data?.user && detail.data.user.id !== myId && (
              <button
                type="button"
                onClick={() =>
                  openStatusDialog({
                    user_id: detail.data.user.id,
                    username: detail.data.user.username,
                    is_active: detail.data.user.is_active,
                  })
                }
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold text-white transition ${
                  detail.data.user.is_active
                    ? 'bg-rose-700 hover:bg-rose-800'
                    : 'bg-emerald-700 hover:bg-emerald-800'
                }`}
              >
                {detail.data.user.is_active ? 'Deactivate account' : 'Reactivate account'}
              </button>
            )}
          </>
        }
      >
        {detail.loading && !detail.data ? (
          <LoadingBlock label="Loading user details…" />
        ) : detail.error ? (
          <ErrorBlock message={detail.error} onRetry={detail.reload} />
        ) : detail.data ? (
          <div className="space-y-4">
            <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
              <div>
                <dt className="text-stone-500">User ID</dt>
                <dd className="font-medium text-stone-900">{detail.data.user.id}</dd>
              </div>
              <div>
                <dt className="text-stone-500">Username</dt>
                <dd className="font-medium text-stone-900">{detail.data.user.username}</dd>
              </div>
              <div>
                <dt className="text-stone-500">Email</dt>
                <dd className="text-stone-800">{detail.data.user.email || '—'}</dd>
              </div>
              <div>
                <dt className="text-stone-500">Role</dt>
                <dd className="text-stone-800">{detail.data.user.role}</dd>
              </div>
              <div>
                <dt className="text-stone-500">Status</dt>
                <dd className="mt-0.5">
                  <StatusPill active={detail.data.user.is_active} />
                </dd>
              </div>
              <div>
                <dt className="text-stone-500">Created</dt>
                <dd className="text-stone-800">{formatDate(detail.data.user.created_at)}</dd>
              </div>
              <div>
                <dt className="text-stone-500">Last sign-in</dt>
                <dd className="text-stone-800">{formatDateTime(detail.data.user.last_login_at)}</dd>
              </div>
            </dl>

            <div className="grid gap-2 sm:grid-cols-3">
              <KpiCard
                label="Realized revenue"
                value={detail.data.sales_summary.revenue}
                format="currency"
              />
              <KpiCard label="Orders" value={detail.data.sales_summary.orders} />
              <KpiCard
                label="Completed"
                value={detail.data.sales_summary.completed_orders}
                tone="teal"
              />
            </div>

            <div>
              <h3 className="text-[10px] font-semibold uppercase tracking-[0.2em] text-stone-500">
                Recent orders
              </h3>
              {detail.data.recent_orders.length === 0 ? (
                <p className="mt-2 text-xs text-stone-500">
                  This account has no sales orders.
                </p>
              ) : (
                <div className="mt-2 overflow-x-auto rounded-lg border border-stone-200">
                  <table className="min-w-full divide-y divide-stone-200 text-xs">
                    <thead className="bg-stone-50">
                      <tr>
                        <th scope="col" className="px-2.5 py-2 text-left text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Order</th>
                        <th scope="col" className="px-2.5 py-2 text-left text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Product</th>
                        <th scope="col" className="px-2.5 py-2 text-right text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Qty</th>
                        <th scope="col" className="px-2.5 py-2 text-right text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Amount</th>
                        <th scope="col" className="px-2.5 py-2 text-left text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Status</th>
                        <th scope="col" className="px-2.5 py-2 text-left text-[9px] font-semibold uppercase tracking-[0.12em] text-stone-500">Created</th>
                      </tr>
                    </thead>
                    <tbody>
                      {detail.data.recent_orders.map((order) => (
                        <tr key={order.id} className="border-t border-stone-100">
                          <td className="px-2.5 py-1.5 tabular-nums text-stone-600">#{order.id}</td>
                          <td className="px-2.5 py-1.5 text-stone-800">{order.product_name || '—'}</td>
                          <td className="px-2.5 py-1.5 text-right tabular-nums text-stone-700">{formatNumber(order.quantity)}</td>
                          <td className="px-2.5 py-1.5 text-right tabular-nums text-stone-700">{formatCurrency(order.total_amount)}</td>
                          <td className="px-2.5 py-1.5 text-stone-700">{order.status}</td>
                          <td className="px-2.5 py-1.5 text-stone-600">{formatDateTime(order.created_at)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        ) : null}
      </Modal>

      <Modal
        open={statusTarget !== null}
        onClose={() => {
          if (!statusBusy) {
            setStatusTarget(null);
            setStatusError('');
          }
        }}
        title={statusTarget?.is_active ? 'Deactivate account?' : 'Reactivate account?'}
        subtitle={statusTarget ? statusTarget.username : ''}
        footer={
          <>
            <button
              type="button"
              onClick={() => {
                setStatusTarget(null);
                setStatusError('');
              }}
              disabled={statusBusy}
              className="rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 transition hover:bg-stone-50 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={confirmStatusChange}
              disabled={statusBusy}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold text-white transition disabled:opacity-60 ${
                statusTarget?.is_active
                  ? 'bg-rose-700 hover:bg-rose-800'
                  : 'bg-emerald-700 hover:bg-emerald-800'
              }`}
            >
              {statusBusy
                ? 'Updating…'
                : statusTarget?.is_active
                  ? 'Deactivate account'
                  : 'Reactivate account'}
            </button>
          </>
        }
      >
        <p className="text-sm leading-relaxed text-stone-700">
          {statusTarget?.is_active
            ? 'The account will no longer be able to sign in or use the application. Existing sales orders, purchase orders and inventory records are kept unchanged.'
            : 'The account will be allowed to sign in again. Its existing business records are unchanged.'}
        </p>
        {statusError && (
          <p role="alert" className="mt-3 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-800">
            {statusError}
          </p>
        )}
      </Modal>
    </div>
  );
}
