import { useEffect, useRef, useState } from 'react';
import { apiFetch } from '../../api';
import { Icon } from '../../components/Icons';

const currencyFormatter = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  maximumFractionDigits: 2,
});

const compactCurrencyFormatter = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  notation: 'compact',
  maximumFractionDigits: 1,
});

const numberFormatter = new Intl.NumberFormat('en-IN');

export function formatCurrency(value) {
  const number = Number(value);
  return Number.isFinite(number) ? currencyFormatter.format(number) : '—';
}

export function compactCurrency(value) {
  const number = Number(value);
  return Number.isFinite(number) ? compactCurrencyFormatter.format(number) : '—';
}

export function formatNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? numberFormatter.format(number) : '—';
}

export function formatPercent(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '—';
  const sign = number > 0 ? '+' : '';
  return `${sign}${number.toFixed(2)}%`;
}

export function formatDate(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

export function formatDateTime(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatDay(value) {
  if (!value) return '—';
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' });
}

export function errorMessage(data, status) {
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) {
    const joined = data.detail.map((issue) => issue.msg).filter(Boolean).join(' ');
    if (joined) return joined;
  }
  if (status === 403) {
    return 'You do not have administrator permission for this resource.';
  }
  if (status === 401) return 'Your session has expired. Sign in again.';
  return `The request failed (HTTP ${status}).`;
}

export function useAdminResource(path) {
  const [state, setState] = useState({ data: null, error: '', loading: true });
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    if (!path) {
      setState({ data: null, error: '', loading: false });
      return undefined;
    }
    let active = true;
    setState((current) => ({ data: current.data, error: '', loading: true }));
    apiFetch(path)
      .then(async (response) => {
        const body = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(errorMessage(body, response.status));
        return body;
      })
      .then((data) => {
        if (active) setState({ data, error: '', loading: false });
      })
      .catch((error) => {
        if (active) {
          setState({
            data: null,
            error: error.message || 'Unable to load this data.',
            loading: false,
          });
        }
      });
    return () => {
      active = false;
    };
  }, [path, reloadKey]);

  return {
    ...state,
    reload: () => setReloadKey((value) => value + 1),
  };
}

export function Panel({ title, subtitle, actions, children, className = '' }) {
  return (
    <section
      className={`rounded-xl border border-stone-200 bg-[#fffdf9] shadow-[0_1px_2px_rgba(28,25,23,0.04)] ${className}`}
    >
      {(title || actions) && (
        <header className="flex flex-wrap items-start justify-between gap-3 border-b border-stone-100 px-4 py-3">
          <div className="min-w-0">
            {title && (
              <h2 className="text-sm font-semibold tracking-tight text-stone-900">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="mt-0.5 text-xs leading-relaxed text-stone-500">
                {subtitle}
              </p>
            )}
          </div>
          {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
        </header>
      )}
      <div className="p-4">{children}</div>
    </section>
  );
}

export function KpiCard({ label, value, detail, format = 'number', tone = 'teal' }) {
  const tones = {
    teal: 'from-teal-300 via-teal-400 to-emerald-500 text-stone-900',
    indigo: 'from-indigo-300 via-indigo-400 to-sky-400 text-stone-900',
    amber: 'from-amber-200 via-amber-300 to-orange-400 text-amber-950',
    rose: 'from-rose-300 via-rose-400 to-red-500 text-rose-950',
    stone: 'from-stone-300 via-stone-400 to-stone-500 text-stone-900',
  };
  const style = tones[tone] ?? tones.teal;
  const formatted =
    format === 'currency'
      ? formatCurrency(value)
      : format === 'percent'
        ? formatPercent(value)
        : formatNumber(value);

  return (
    <div className="relative overflow-hidden rounded-xl border border-stone-200 bg-[#fffdf9] p-4 shadow-[0_1px_2px_rgba(28,25,23,0.04)]">
      <div className={`absolute inset-x-0 top-0 h-[3px] bg-gradient-to-r ${style.split(' ').slice(0, 3).join(' ')}`} />
      <p className="text-[9px] font-semibold uppercase leading-snug tracking-[0.18em] text-stone-500">
        {label}
      </p>
      <p className={`mt-2.5 text-xl font-semibold leading-none tracking-tight tabular-nums ${style.split(' ').slice(3).join(' ')}`}>
        {formatted}
      </p>
      {detail && (
        <p className="mt-1.5 text-[11px] leading-tight text-stone-500">{detail}</p>
      )}
    </div>
  );
}

export function LoadingBlock({ label = 'Loading data…' }) {
  return (
    <div
      role="status"
      className="flex items-center justify-center gap-2 rounded-xl border border-stone-200 bg-[#fffdf9] px-4 py-12 text-sm text-stone-500"
    >
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-stone-300 border-t-teal-600" />
      {label}
    </div>
  );
}

export function ErrorBlock({ message, onRetry }) {
  return (
    <div
      role="alert"
      className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-900"
    >
      <span className="flex items-start gap-2">
        <Icon name="alert" size={16} className="mt-0.5 shrink-0" />
        {message}
      </span>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="rounded-md border border-rose-300 bg-white px-3 py-1.5 text-xs font-semibold text-rose-800 transition hover:bg-rose-100"
        >
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyState({ title, detail, icon = 'chart' }) {
  return (
    <div className="rounded-xl border border-dashed border-stone-300 bg-stone-50/60 px-4 py-10 text-center">
      <span className="mx-auto flex h-10 w-10 items-center justify-center rounded-lg border border-stone-200 bg-white text-stone-400">
        <Icon name={icon} size={18} />
      </span>
      <p className="mt-3 text-sm font-semibold text-stone-700">{title}</p>
      {detail && <p className="mt-1 text-xs text-stone-500">{detail}</p>}
    </div>
  );
}

export function Pagination({ page, pageSize, total, onChange }) {
  const pageCount = Math.max(1, Math.ceil((total || 0) / pageSize));
  const safePage = Math.min(Math.max(1, page), pageCount);
  const start = total === 0 ? 0 : (safePage - 1) * pageSize + 1;
  const end = Math.min(total || 0, safePage * pageSize);

  return (
    <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-xs text-stone-600">
      <p aria-live="polite">
        Showing {start}–{end} of {formatNumber(total || 0)}
      </p>
      <div className="flex items-center gap-1.5">
        <button
          type="button"
          onClick={() => onChange(safePage - 1)}
          disabled={safePage <= 1}
          className="rounded-md border border-stone-300 bg-white px-2.5 py-1.5 font-medium text-stone-700 transition hover:bg-stone-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Previous
        </button>
        <span className="px-1 tabular-nums">
          Page {safePage} of {pageCount}
        </span>
        <button
          type="button"
          onClick={() => onChange(safePage + 1)}
          disabled={safePage >= pageCount}
          className="rounded-md border border-stone-300 bg-white px-2.5 py-1.5 font-medium text-stone-700 transition hover:bg-stone-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export function SortHeader({ label, value, sort, direction, onSort, align = 'left' }) {
  const active = sort === value;
  return (
    <th
      scope="col"
      className={`whitespace-nowrap px-3 py-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-500 ${
        align === 'right' ? 'text-right' : 'text-left'
      }`}
    >
      <button
        type="button"
        onClick={() => onSort(value)}
        className={`inline-flex items-center gap-1 uppercase tracking-[0.14em] transition hover:text-stone-800 ${
          active ? 'text-stone-800' : ''
        }`}
        aria-label={`Sort by ${label}${active ? `, currently ${direction}` : ''}`}
      >
        {label}
        <span aria-hidden="true" className={active ? 'text-teal-700' : 'text-stone-300'}>
          {active && direction === 'asc' ? '↑' : '↓'}
        </span>
      </button>
    </th>
  );
}

export function Modal({ open, onClose, title, subtitle, children, footer }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else dialog.setAttribute('open', '');
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      onCancel={(event) => {
        event.preventDefault();
        onClose();
      }}
      onClose={onClose}
      aria-labelledby="admin-modal-title"
      className="w-[min(38rem,calc(100vw-2rem))] rounded-2xl border border-stone-200 bg-[#fffdf9] p-0 text-stone-800 shadow-[0_40px_90px_-30px_rgba(28,25,23,0.7)] backdrop:bg-stone-950/50"
    >
      <div className="flex items-start justify-between gap-3 border-b border-stone-100 px-5 py-4">
        <div>
          <h2 id="admin-modal-title" className="text-base font-semibold tracking-tight text-stone-900">
            {title}
          </h2>
          {subtitle && <p className="mt-0.5 text-xs text-stone-500">{subtitle}</p>}
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close dialog"
          className="rounded-md p-1.5 text-stone-400 transition hover:bg-stone-100 hover:text-stone-700"
        >
          <Icon name="close" size={16} />
        </button>
      </div>
      <div className="max-h-[70vh] overflow-y-auto px-5 py-4">{children}</div>
      {footer && (
        <div className="flex flex-wrap justify-end gap-2 border-t border-stone-100 px-5 py-3">
          {footer}
        </div>
      )}
    </dialog>
  );
}
