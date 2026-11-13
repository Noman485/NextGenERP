import { useEffect, useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { apiFetch, clearSessionTokens, logoutSession } from '../../api';
import { Icon } from '../../components/Icons';
import AdminOverview from './AdminOverview';
import AdminAnalytics from './AdminAnalytics';
import AdminUsers from './AdminUsers';

const NAVIGATION = [
  { name: 'Overview', path: '/admin', icon: 'dashboard' },
  { name: 'Sales Analytics', path: '/admin/analytics', icon: 'chart' },
  { name: 'Users', path: '/admin/users', icon: 'users' },
];

const PAGE_META = {
  '/admin': { title: 'Administrator overview', eyebrow: 'Business health' },
  '/admin/analytics': { title: 'Sales analytics', eyebrow: 'Revenue and orders' },
  '/admin/users': { title: 'User management', eyebrow: 'Accounts and sales' },
};

function AccessDenied({ message }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f4f0e9] p-5">
      <div className="w-full max-w-lg rounded-2xl border border-stone-200 bg-[#fffdf9] p-7 text-center shadow-sm">
        <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-700">
          <Icon name="shield" size={22} />
        </span>
        <h1 className="mt-4 text-xl font-semibold tracking-tight text-stone-900">
          Administrator access required
        </h1>
        <p className="mt-2 text-sm leading-relaxed text-stone-600">{message}</p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <Link
            to="/admin/login"
            className="rounded-lg bg-indigo-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-800"
          >
            Administrator sign-in
          </Link>
          <Link
            to="/"
            className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-semibold text-stone-700 transition hover:bg-stone-50"
          >
            Return to workspace
          </Link>
        </div>
      </div>
    </main>
  );
}

export default function AdminApp() {
  const [admin, setAdmin] = useState(null);
  const [loading, setLoading] = useState(true);
  const [accessError, setAccessError] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const token = sessionStorage.getItem('access_token');

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return undefined;
    }
    let active = true;
    setLoading(true);
    apiFetch('/auth/me')
      .then(async (response) => {
        if (response.status === 401) return { unauthorized: true };
        if (response.status === 403) return { inactive: true };
        if (!response.ok) throw new Error(`Profile request failed (HTTP ${response.status}).`);
        return response.json();
      })
      .then((profile) => {
        if (!active) return;
        if (profile?.unauthorized) {
          clearSessionTokens();
          setAccessError('Your session has expired. Sign in again.');
        } else if (profile?.inactive) {
          setAccessError('This account has been deactivated.');
        } else if (profile?.role !== 'ADMIN') {
          setAccessError(
            'The signed-in account is a normal user account. Use a provisioned administrator account to continue.',
          );
        } else {
          setAdmin(profile);
        }
      })
      .catch((error) => {
        if (active) setAccessError(error.message || 'Could not verify the administrator session.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [token]);

  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  function handleLogout() {
    logoutSession();
    setAdmin(null);
    navigate('/admin/login', { replace: true });
  }

  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f4f0e9]">
        <p className="text-sm text-stone-500">Verifying administrator access…</p>
      </main>
    );
  }

  if (accessError || !admin) {
    return <AccessDenied message={accessError || 'Administrator access is required.'} />;
  }

  const meta = PAGE_META[location.pathname] ?? {
    title: 'Administration',
    eyebrow: 'Administrator workspace',
  };

  let page = <AdminOverview />;
  if (location.pathname === '/admin/analytics') page = <AdminAnalytics />;
  else if (location.pathname === '/admin/users') page = <AdminUsers />;
  else if (location.pathname !== '/admin') {
    page = (
      <div className="rounded-xl border border-stone-200 bg-white p-6">
        <h2 className="text-lg font-semibold text-stone-900">Administrator page not found</h2>
        <p className="mt-2 text-sm text-stone-600">
          The requested administrator page does not exist.
        </p>
        <Link
          to="/admin"
          className="mt-4 inline-flex rounded-lg bg-stone-900 px-4 py-2 text-sm font-semibold text-white"
        >
          Back to overview
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f4f0e9] text-stone-800">
      <a
        href="#admin-main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-stone-900 focus:shadow-lg"
      >
        Skip to administrator content
      </a>
      <div className="flex min-h-screen">
        {sidebarOpen && (
          <button
            type="button"
            aria-label="Close administrator navigation"
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 z-30 cursor-default bg-stone-950/50 backdrop-blur-sm lg:hidden"
          />
        )}

        <aside
          className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-white/5 bg-gradient-to-b from-[#151b2b] via-[#101624] to-[#0a0f18] text-stone-200 transition-transform duration-300 lg:sticky lg:top-0 lg:h-screen lg:translate-x-0 ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <div className="flex items-center gap-3 border-b border-white/5 px-5 py-5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-200 via-indigo-300 to-sky-400 text-[#0b1220]">
              <Icon name="shield" size={19} />
            </div>
            <div className="min-w-0">
              <p className="truncate text-base font-semibold tracking-tight text-white">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-indigo-300/70">
                Administration
              </p>
            </div>
            <button
              type="button"
              onClick={() => setSidebarOpen(false)}
              className="ml-auto rounded-md p-1.5 text-stone-400 hover:bg-white/10 hover:text-white lg:hidden"
              aria-label="Close administrator navigation"
            >
              <Icon name="close" size={16} />
            </button>
          </div>

          <nav className="mt-5 flex-1 space-y-1 overflow-y-auto px-3 pb-4">
            <p className="px-3 pb-2 text-[9px] font-semibold uppercase tracking-[0.28em] text-stone-500">
              Administrator
            </p>
            {NAVIGATION.map((item) => {
              const active =
                item.path === '/admin'
                  ? location.pathname === '/admin'
                  : location.pathname.startsWith(item.path);
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                    active
                      ? 'bg-white/[0.07] text-white'
                      : 'text-stone-400 hover:bg-white/[0.04] hover:text-stone-100'
                  }`}
                >
                  <span className={active ? 'text-indigo-300' : 'text-stone-500 group-hover:text-indigo-300'}>
                    <Icon name={item.icon} size={17} />
                  </span>
                  <span className="flex-1 truncate">{item.name}</span>
                  {active && <span className="h-1.5 w-1.5 rounded-full bg-indigo-300" />}
                </Link>
              );
            })}
          </nav>

          <div className="space-y-3 border-t border-white/5 p-3">
            <Link
              to="/"
              className="flex items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-xs font-medium text-stone-300 transition hover:bg-white/5 hover:text-white"
            >
              <Icon name="arrowLeft" size={14} />
              Return to workspace
            </Link>
            <div className="flex items-center gap-3 rounded-xl bg-white/[0.03] px-3 py-2.5">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-400/15 text-[11px] font-semibold uppercase text-indigo-200">
                {admin.username.slice(0, 2).toUpperCase()}
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-xs font-medium text-stone-200">{admin.username}</p>
                <p className="truncate text-[10px] text-indigo-300/70">Administrator</p>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                title="Sign out of administration"
                aria-label="Sign out of administration"
                className="rounded-md p-1.5 text-stone-400 transition hover:bg-white/10 hover:text-white"
              >
                <Icon name="logout" size={15} />
              </button>
            </div>
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-20 border-b border-stone-200/80 bg-[#f4f0e9]/85 backdrop-blur">
            <div className="flex items-center gap-3 px-4 py-3 sm:px-6">
              <button
                type="button"
                onClick={() => setSidebarOpen(true)}
                className="rounded-lg border border-stone-200 bg-[#fffdf9] p-2 text-stone-600 lg:hidden"
                aria-label="Open administrator navigation"
              >
                <Icon name="menu" size={17} />
              </button>
              <div className="min-w-0">
                <p className="text-[9px] font-semibold uppercase tracking-[0.28em] text-indigo-700/80">
                  {meta.eyebrow}
                </p>
                <h1 className="truncate text-sm font-semibold tracking-tight text-stone-800">
                  {meta.title}
                </h1>
              </div>
              <span className="ml-auto inline-flex items-center gap-1.5 rounded-full border border-indigo-200 bg-indigo-50 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-indigo-700">
                <Icon name="shield" size={12} />
                Admin
              </span>
            </div>
          </header>

          <main id="admin-main" className="flex-1 px-4 py-5 sm:px-6 sm:py-6">
            {page}
          </main>
        </div>
      </div>
    </div>
  );
}
