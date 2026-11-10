import { useState } from 'react';
import { apiFetch } from '../api';
import { Icon } from '../components/Icons';
import Warehouse3D from '../components/Warehouse3D';

const FEATURES = [
  { icon: 'forecast', title: '7-day demand forecast', detail: 'XGBoost model · 8.42% WAPE' },
  { icon: 'cart', title: 'Smart reorder queue', detail: 'Safety stock + lead time aware' },
  { icon: 'inventory', title: 'Live inventory ops', detail: 'Stock in / out with full audit trail' },
];

export default function Auth({ onAuthenticated }) {
  const [mode, setMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const isRegistration = mode === 'register';

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      const response = await apiFetch(`/auth/${mode}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail = Array.isArray(data.detail)
          ? data.detail.map((issue) => issue.msg).filter(Boolean).join(' ')
          : data.detail;
        throw new Error(detail || `Authentication failed (HTTP ${response.status}).`);
      }

      if (!data.access_token) {
        throw new Error('The authentication service did not return an access token.');
      }
      onAuthenticated(data.access_token);
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? 'Unable to connect to the authentication service. Check that the backend is running.'
          : requestError instanceof Error
            ? requestError.message
            : 'Authentication failed.',
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-screen bg-[#f4f0e9] lg:grid-cols-[1.05fr_1fr]">
      <section className="relative hidden overflow-hidden bg-[radial-gradient(120%_120%_at_0%_0%,#17322d_0%,#101a1c_48%,#0a1011_100%)] p-10 text-stone-100 lg:flex lg:flex-col lg:justify-between">
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-teal-400/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 -left-16 h-64 w-64 rounded-full bg-emerald-400/[0.07] blur-3xl" />

        <div className="relative">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-teal-200 via-teal-300 to-emerald-400 text-base font-bold text-[#06201d] shadow-[0_0_26px_-6px_rgba(45,212,191,0.9)]">
              N
            </div>
            <div>
              <p className="text-base font-semibold tracking-tight text-white">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-teal-300/70">Ops Center</p>
            </div>
          </div>

          <h1 className="mt-12 max-w-md text-3xl font-semibold leading-tight tracking-tight text-white">
            Inventory decisions, backed by live data and demand forecasts.
          </h1>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-stone-400">
            One workspace for catalog, stock movement, orders and ML-driven reorder
            recommendations.
          </p>

          <ul className="mt-8 space-y-3">
            {FEATURES.map((feature) => (
              <li key={feature.title} className="flex items-start gap-3">
                <span className="mt-0.5 flex h-8 w-8 items-center justify-center rounded-lg border border-teal-300/20 bg-teal-400/10 text-teal-300">
                  <Icon name={feature.icon} size={15} />
                </span>
                <div>
                  <p className="text-sm font-medium text-stone-100">{feature.title}</p>
                  <p className="text-[11px] text-stone-500">{feature.detail}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="relative mt-10 h-56">
          <Warehouse3D items={[]} />
          <p className="pointer-events-none absolute inset-x-0 bottom-0 text-center text-[9px] uppercase tracking-[0.24em] text-stone-500">
            Live 3D stock snapshot
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center p-5 sm:p-10">
        <div className="w-full max-w-md">
          <div className="mb-6 flex items-center gap-3 lg:hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-teal-300 to-emerald-500 text-base font-bold text-[#06201d]">
              N
            </div>
            <div>
              <p className="text-base font-semibold tracking-tight text-stone-900">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-teal-700">Ops Center</p>
            </div>
          </div>

          <div className="rounded-2xl border border-stone-200 bg-[#fffdf9] p-6 shadow-[0_30px_60px_-45px_rgba(28,25,23,0.6)] sm:p-7">
            <div className="mb-6">
              <p className="text-[9px] font-semibold uppercase tracking-[0.26em] text-teal-700">
                {isRegistration ? 'New workspace access' : 'Welcome back'}
              </p>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight text-stone-900">
                {isRegistration ? 'Create your account' : 'Sign in'}
              </h2>
              <p className="mt-1 text-sm text-stone-600">
                {isRegistration
                  ? 'Register to access the ERP workspace.'
                  : 'Sign in to access your ERP workspace.'}
              </p>
            </div>

            {error && (
              <p
                role="alert"
                className="mb-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-900"
              >
                <Icon name="alert" size={15} className="mt-0.5 shrink-0" />
                {error}
              </p>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
                Username
                <input
                  autoComplete="username"
                  required
                  minLength={isRegistration ? 3 : 1}
                  maxLength={80}
                  pattern="[A-Za-z0-9_.\-]+"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  className="rounded-lg border border-stone-300 bg-white px-3 py-2.5 text-sm font-normal normal-case tracking-normal text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
                />
              </label>

              <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
                Password
                <span className="relative block">
                  <input
                    autoComplete={isRegistration ? 'new-password' : 'current-password'}
                    required
                    minLength={isRegistration ? 12 : 1}
                    maxLength={128}
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="w-full rounded-lg border border-stone-300 bg-white px-3 py-2.5 pr-11 text-sm font-normal normal-case tracking-normal text-stone-800 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((value) => !value)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    className="absolute inset-y-0 right-0 flex w-10 items-center justify-center rounded-r-lg text-stone-400 hover:text-teal-700"
                  >
                    <Icon name={showPassword ? 'eyeOff' : 'eye'} size={16} />
                  </button>
                </span>
                {isRegistration && (
                  <span className="text-[11px] font-normal normal-case tracking-normal text-stone-500">
                    Use at least 12 characters.
                  </span>
                )}
              </label>

              <button
                type="submit"
                disabled={submitting}
                className="flex w-full items-center justify-center gap-2 rounded-lg bg-stone-900 px-4 py-2.5 text-sm font-semibold text-white shadow-[0_14px_30px_-18px_rgba(28,25,23,0.9)] transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {submitting ? 'Please wait…' : isRegistration ? 'Create account' : 'Sign in'}
                {!submitting && <Icon name="arrowRight" size={15} />}
              </button>
            </form>

            <p className="mt-5 text-center text-sm text-stone-600">
              {isRegistration ? 'Already registered?' : 'New to NextGenERP?'}{' '}
              <button
                type="button"
                onClick={() => {
                  setMode(isRegistration ? 'login' : 'register');
                  setError('');
                }}
                className="font-medium text-teal-800 underline decoration-teal-300 underline-offset-2 hover:decoration-teal-600"
              >
                {isRegistration ? 'Sign in' : 'Create an account'}
              </button>
            </p>
          </div>

          <p className="mt-4 text-center text-[10px] uppercase tracking-[0.18em] text-stone-400">
            Secured with JWT · Session stored per tab
          </p>
        </div>
      </section>
    </main>
  );
}
