import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiFetch } from '../../api';
import { Icon } from '../../components/Icons';

export default function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [checking, setChecking] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    let active = true;
    const token = sessionStorage.getItem('access_token');
    if (!token) {
      setChecking(false);
      return undefined;
    }
    apiFetch('/auth/me')
      .then(async (response) => {
        if (!response.ok) return null;
        return response.json();
      })
      .then((profile) => {
        if (active && profile?.role === 'ADMIN') {
          navigate('/admin', { replace: true });
        }
      })
      .catch(() => {})
      .finally(() => {
        if (active) setChecking(false);
      });
    return () => {
      active = false;
    };
  }, [navigate]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const response = await apiFetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const detail = Array.isArray(data.detail)
          ? data.detail.map((issue) => issue.msg).filter(Boolean).join(' ')
          : data.detail;
        throw new Error(detail || `Sign-in failed (HTTP ${response.status}).`);
      }
      if (data.user?.role !== 'ADMIN') {
        throw new Error(
          'This account is a normal user account. Administrator access is required.',
        );
      }
      sessionStorage.setItem('access_token', data.access_token);
      navigate('/admin', { replace: true });
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? 'Unable to connect to the authentication service. Check that the backend is running.'
          : requestError.message || 'Administrator sign-in failed.',
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (checking) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f4f0e9]">
        <p className="text-sm text-stone-500">Checking administrator session…</p>
      </main>
    );
  }

  return (
    <main className="grid min-h-screen bg-[#f4f0e9] lg:grid-cols-[1.05fr_1fr]">
      <section className="relative hidden overflow-hidden bg-[radial-gradient(120%_120%_at_0%_0%,#1f2a44_0%,#121826_48%,#0a0f18_100%)] p-10 text-stone-100 lg:flex lg:flex-col lg:justify-between">
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-indigo-400/10 blur-3xl" />
        <div className="relative">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-200 via-indigo-300 to-sky-400 text-[#0b1220]">
              <Icon name="shield" size={20} />
            </div>
            <div>
              <p className="text-base font-semibold tracking-tight text-white">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-indigo-300/70">
                Administration
              </p>
            </div>
          </div>
          <h1 className="mt-12 max-w-md text-3xl font-semibold leading-tight tracking-tight text-white">
            Business oversight, separate from day-to-day operations.
          </h1>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-stone-400">
            Administrators can review realized revenue, order trends, user sales,
            inventory health and supplier purchasing from one authorized workspace.
          </p>
          <ul className="mt-8 space-y-3 text-sm text-stone-300">
            <li className="flex items-center gap-2">
              <Icon name="check" size={15} className="text-indigo-300" />
              Daily, monthly and yearly sales analytics
            </li>
            <li className="flex items-center gap-2">
              <Icon name="check" size={15} className="text-indigo-300" />
              User, product and supplier breakdowns
            </li>
            <li className="flex items-center gap-2">
              <Icon name="check" size={15} className="text-indigo-300" />
              Administrator-only authorization on every API
            </li>
          </ul>
        </div>
        <p className="relative text-[10px] uppercase tracking-[0.18em] text-stone-500">
          Authorized personnel only
        </p>
      </section>

      <section className="flex items-center justify-center p-5 sm:p-10">
        <div className="w-full max-w-md">
          <div className="mb-6 flex items-center gap-3 lg:hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white">
              <Icon name="shield" size={19} />
            </div>
            <div>
              <p className="text-base font-semibold tracking-tight text-stone-900">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-indigo-700">
                Administration
              </p>
            </div>
          </div>

          <div className="rounded-2xl border border-stone-200 bg-[#fffdf9] p-6 shadow-[0_30px_60px_-45px_rgba(28,25,23,0.6)] sm:p-7">
            <div className="mb-6">
              <p className="text-[9px] font-semibold uppercase tracking-[0.26em] text-indigo-700">
                Administrator access
              </p>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight text-stone-900">
                Sign in to administration
              </h2>
              <p className="mt-1 text-sm text-stone-600">
                Use an administrator account provisioned by the operator.
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
                Administrator username
                <input
                  autoComplete="username"
                  required
                  minLength={1}
                  maxLength={80}
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  className="rounded-lg border border-stone-300 bg-white px-3 py-2.5 text-sm font-normal normal-case tracking-normal text-stone-800 outline-none focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100"
                />
              </label>

              <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
                Password
                <span className="relative block">
                  <input
                    autoComplete="current-password"
                    required
                    maxLength={128}
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="w-full rounded-lg border border-stone-300 bg-white px-3 py-2.5 pr-11 text-sm font-normal normal-case tracking-normal text-stone-800 outline-none focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((value) => !value)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    className="absolute inset-y-0 right-0 flex w-10 items-center justify-center rounded-r-lg text-stone-400 hover:text-indigo-700"
                  >
                    <Icon name={showPassword ? 'eyeOff' : 'eye'} size={16} />
                  </button>
                </span>
              </label>

              <button
                type="submit"
                disabled={submitting}
                className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {submitting ? 'Signing in…' : 'Sign in to administration'}
                {!submitting && <Icon name="arrowRight" size={15} />}
              </button>
            </form>

            <p className="mt-5 text-center text-sm text-stone-600">
              Not an administrator?{' '}
              <Link
                to="/"
                className="font-medium text-indigo-800 underline decoration-indigo-300 underline-offset-2 hover:decoration-indigo-600"
              >
                Return to the workspace
              </Link>
            </p>
          </div>

          <p className="mt-4 text-center text-[10px] uppercase tracking-[0.18em] text-stone-400">
            Separate administrator session · API authorization enforced
          </p>
        </div>
      </section>
    </main>
  );
}
