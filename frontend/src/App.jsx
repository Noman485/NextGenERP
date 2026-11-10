import { useEffect, useMemo, useState } from 'react';
import { Link, NavLink, Route, Routes, useLocation, useNavigate } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import Auth from './pages/Auth';
import Categories from './pages/Categories';
import Products from './pages/Products';
import Suppliers from './pages/Suppliers';
import SalesOrders from './pages/SalesOrders';
import PurchaseOrders from './pages/PurchaseOrders';
import InventoryTransactions from './pages/InventoryTransactions';
import Forecasting from './pages/Forecasting';
import { Icon } from './components/Icons';
import ErrorBoundary from './components/ErrorBoundary';
import Assistant from './components/Assistant';
import { apiFetch } from './api';

const navigation = [
  { name: 'Dashboard', path: '/', icon: 'dashboard', keywords: ['home', 'overview'] },
  {
    name: 'Demand Forecast',
    path: '/forecasting',
    icon: 'forecast',
    keywords: ['forecast', 'demand', 'reorder', 'planning'],
  },
  { name: 'Products', path: '/products', icon: 'box', keywords: ['catalog', 'items', 'sku'] },
  {
    name: 'Inventory Operations',
    path: '/inventory-operations',
    icon: 'inventory',
    keywords: ['stock', 'inventory', 'movement', 'adjustment'],
  },
  { name: 'Categories', path: '/categories', icon: 'tag', keywords: ['catalog', 'groups'] },
  { name: 'Suppliers', path: '/suppliers', icon: 'truck', keywords: ['vendors', 'procurement'] },
  { name: 'Sales Orders', path: '/sales-orders', icon: 'cart', keywords: ['orders', 'customers'] },
  {
    name: 'Purchase Orders',
    path: '/purchase-orders',
    icon: 'clipboard',
    keywords: ['procurement', 'suppliers', 'purchasing'],
  },
];

const PAGE_META = {
  '/': { title: 'Dashboard', eyebrow: 'Operations overview' },
  '/forecasting': { title: 'Demand Forecast', eyebrow: 'Planning' },
  '/products': { title: 'Products', eyebrow: 'Catalog' },
  '/inventory-operations': { title: 'Inventory Operations', eyebrow: 'Stock movement' },
  '/categories': { title: 'Categories', eyebrow: 'Catalog' },
  '/suppliers': { title: 'Suppliers', eyebrow: 'Procurement' },
  '/sales-orders': { title: 'Sales Orders', eyebrow: 'Fulfilment' },
  '/purchase-orders': { title: 'Purchase Orders', eyebrow: 'Procurement' },
};

const todayLabel = new Intl.DateTimeFormat('en-IN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
}).format(new Date());

function getInitials(name) {
  const cleaned = (name || '').trim();
  return cleaned ? cleaned.slice(0, 2).toUpperCase() : '?';
}

function NotFound() {
  return (
    <div className="mx-auto max-w-xl rounded-xl border border-stone-200 bg-[#fffdf9] p-6 text-center shadow-sm">
      <p className="text-[10px] font-semibold uppercase tracking-[0.24em] text-teal-700">
        404
      </p>
      <h2 className="mt-2 text-xl font-semibold tracking-tight text-stone-900">
        Page not found
      </h2>
      <p className="mt-2 text-sm leading-relaxed text-stone-600">
        The page you requested does not exist or has moved. Use the sidebar or
        return to the dashboard.
      </p>
      <Link
        to="/"
        className="mt-5 inline-flex items-center gap-1.5 rounded-lg bg-stone-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-stone-800"
      >
        Back to dashboard
        <Icon name="arrowRight" size={14} />
      </Link>
    </div>
  );
}

function App() {
  const [token, setToken] = useState(() => sessionStorage.getItem('access_token'));
  const [user, setUser] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [searchFeedback, setSearchFeedback] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    function handleExpiredToken() {
      setToken(null);
    }

    window.addEventListener('auth:expired', handleExpiredToken);
    return () => window.removeEventListener('auth:expired', handleExpiredToken);
  }, []);

  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return undefined;
    }

    let active = true;
    apiFetch('/auth/me')
      .then(async (response) => {
        if (!response.ok) return null;
        return response.json();
      })
      .then((profile) => {
        if (active && profile) setUser(profile);
      })
      .catch(() => {
        if (active) setUser(null);
      });

    return () => {
      active = false;
    };
  }, [token]);

  function handleAuthenticated(accessToken, authenticatedUser) {
    sessionStorage.setItem('access_token', accessToken);
    setUser(authenticatedUser ?? null);
    setToken(accessToken);
  }

  function handleLogout() {
    sessionStorage.removeItem('access_token');
    setUser(null);
    setToken(null);
  }

  function handleSearch(event) {
    event.preventDefault();
    const term = query.trim().toLowerCase();
    if (!term) return;

    const match = navigation.find(
      (item) =>
        item.name.toLowerCase().includes(term) ||
        item.keywords.some((keyword) => keyword.includes(term)),
    );

    if (match) {
      navigate(match.path);
      setQuery('');
      setSearchFeedback('');
      return;
    }

    setSearchFeedback(
      `No module matches "${query.trim()}". Try Products, Sales Orders or Suppliers.`,
    );
  }

  const meta = useMemo(
    () => PAGE_META[location.pathname] ?? { title: 'NextGenERP', eyebrow: 'Workspace' },
    [location.pathname],
  );
  const displayName = user?.username || 'Signed in';
  const initials = getInitials(user?.username);

  if (!token) {
    return <Auth onAuthenticated={handleAuthenticated} />;
  }

  return (
    <div className="min-h-screen bg-[#f4f0e9] text-stone-800">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-stone-900 focus:shadow-lg"
      >
        Skip to main content
      </a>

      <div className="flex min-h-screen">
        {sidebarOpen && (
          <button
            type="button"
            aria-label="Close navigation"
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 z-30 cursor-default bg-stone-950/50 backdrop-blur-sm lg:hidden"
          />
        )}

        <aside
          className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-white/5 bg-gradient-to-b from-[#12181a] via-[#0f1517] to-[#0b1112] text-stone-200 transition-transform duration-300 lg:sticky lg:top-0 lg:h-screen lg:translate-x-0 ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <div className="flex items-center gap-3 border-b border-white/5 px-5 py-5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-teal-200 via-teal-300 to-emerald-400 text-base font-bold text-[#06201d] shadow-[0_0_26px_-6px_rgba(45,212,191,0.9)]">
              N
            </div>
            <div className="min-w-0">
              <p className="truncate text-base font-semibold tracking-tight text-white">NextGenERP</p>
              <p className="text-[9px] uppercase tracking-[0.26em] text-teal-300/70">Ops Center</p>
            </div>
            <button
              type="button"
              onClick={() => setSidebarOpen(false)}
              className="ml-auto rounded-md p-1.5 text-stone-400 hover:bg-white/10 hover:text-white lg:hidden"
              aria-label="Close navigation"
            >
              <Icon name="close" size={16} />
            </button>
          </div>

          <nav className="mt-5 flex-1 space-y-1 overflow-y-auto px-3 pb-4">
            <p className="px-3 pb-2 text-[9px] font-semibold uppercase tracking-[0.28em] text-stone-500">
              Workspace
            </p>
            {navigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                    isActive
                      ? 'bg-white/[0.07] text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]'
                      : 'text-stone-400 hover:bg-white/[0.04] hover:text-stone-100'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <span
                      className={`transition ${
                        isActive ? 'text-teal-300' : 'text-stone-500 group-hover:text-teal-300'
                      }`}
                    >
                      <Icon name={item.icon} size={17} />
                    </span>
                    <span className="flex-1 truncate">{item.name}</span>
                    {isActive && (
                      <span className="h-1.5 w-1.5 rounded-full bg-teal-300 shadow-[0_0_10px_2px_rgba(45,212,191,0.55)]" />
                    )}
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          <div className="space-y-3 border-t border-white/5 p-3">
            <Link
              to="/forecasting"
              className="block rounded-xl border border-teal-400/15 bg-teal-400/[0.06] p-3 transition hover:border-teal-300/30 hover:bg-teal-400/[0.09]"
            >
              <div className="flex items-center gap-2 text-[9px] font-semibold uppercase tracking-[0.2em] text-teal-300/80">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-60" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-teal-400" />
                </span>
                Demand forecast
              </div>
              <p className="mt-2 text-sm font-semibold text-white">7-day outlook</p>
              <p className="text-[11px] leading-snug text-stone-400">
                Open planning and suggested reorders
              </p>
            </Link>

            <div className="flex items-center gap-3 rounded-xl bg-white/[0.03] px-3 py-2.5">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-teal-400/15 text-[11px] font-semibold uppercase text-teal-200">
                {initials}
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-xs font-medium text-stone-200" title={displayName}>
                  {displayName}
                </p>
                <p className="truncate text-[10px] text-stone-500">Inventory workspace</p>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                title="Sign out"
                aria-label="Sign out"
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
                aria-label="Open navigation"
              >
                <Icon name="menu" size={17} />
              </button>

              <div className="min-w-0">
                <p className="text-[9px] font-semibold uppercase tracking-[0.28em] text-teal-700/80">
                  {meta.eyebrow}
                </p>
                <h1 className="truncate text-sm font-semibold tracking-tight text-stone-800">
                  {meta.title}
                </h1>
              </div>

              <div className="relative ml-auto hidden sm:block">
                <form
                  onSubmit={handleSearch}
                  className="flex items-center gap-2 rounded-lg border border-stone-200 bg-[#fffdf9] px-3 py-2 shadow-sm transition focus-within:border-teal-400 focus-within:ring-2 focus-within:ring-teal-500/15"
                  role="search"
                >
                  <Icon name="search" size={15} className="text-stone-400" />
                  <input
                    type="text"
                    value={query}
                    onChange={(event) => {
                      setQuery(event.target.value);
                      setSearchFeedback('');
                    }}
                    placeholder="Jump to module..."
                    aria-label="Jump to module"
                    className="w-36 bg-transparent text-sm text-stone-700 outline-none placeholder:text-stone-400"
                  />
                  <kbd className="rounded border border-stone-200 bg-stone-50 px-1.5 py-0.5 text-[9px] font-medium text-stone-500">
                    Enter
                  </kbd>
                </form>
                {searchFeedback && (
                  <p
                    role="status"
                    className="absolute right-0 top-full z-30 mt-2 w-64 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-relaxed text-amber-900 shadow-lg"
                  >
                    {searchFeedback}
                  </p>
                )}
              </div>

              <div className="ml-auto flex items-center gap-2 sm:ml-0">
                <span className="hidden items-center gap-2 rounded-lg border border-stone-200 bg-[#fffdf9] px-3 py-2 text-xs text-stone-500 md:inline-flex">
                  <Icon name="clock" size={14} className="text-teal-600" />
                  {todayLabel}
                </span>
                <div
                  className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-teal-200 to-emerald-300 text-[11px] font-bold uppercase text-teal-900 ring-2 ring-white"
                  title={displayName}
                >
                  {initials}
                </div>
              </div>
            </div>
          </header>

          <main id="main-content" className="flex-1 px-4 py-5 sm:px-6 sm:py-6">
            <ErrorBoundary resetKey={location.pathname}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/forecasting" element={<Forecasting />} />
                <Route path="/products" element={<Products />} />
                <Route path="/categories" element={<Categories />} />
                <Route path="/suppliers" element={<Suppliers />} />
                <Route path="/sales-orders" element={<SalesOrders />} />
                <Route path="/purchase-orders" element={<PurchaseOrders />} />
                <Route path="/inventory-operations" element={<InventoryTransactions />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </ErrorBoundary>
          </main>
        </div>
      </div>

      <Assistant />
    </div>
  );
}

export default App;
