import { useEffect, useMemo, useState } from 'react';
import { NavLink, Route, Routes, useLocation, useNavigate } from 'react-router-dom';

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

const navigation = [
  { name: 'Dashboard', path: '/', icon: 'dashboard' },
  { name: 'Forecasting', path: '/forecasting', icon: 'forecast' },
  { name: 'Products', path: '/products', icon: 'box' },
  { name: 'Inventory Operations', path: '/inventory-operations', icon: 'inventory' },
  { name: 'Categories', path: '/categories', icon: 'tag' },
  { name: 'Suppliers', path: '/suppliers', icon: 'truck' },
  { name: 'Sales Orders', path: '/sales-orders', icon: 'cart' },
  { name: 'Purchase Orders', path: '/purchase-orders', icon: 'clipboard' },
];

const PAGE_META = {
  '/': { title: 'Dashboard', eyebrow: 'Operations overview' },
  '/forecasting': { title: 'Demand forecasting', eyebrow: 'ML module' },
  '/products': { title: 'Products', eyebrow: 'Catalog' },
  '/inventory-operations': { title: 'Inventory operations', eyebrow: 'Stock movement' },
  '/categories': { title: 'Categories', eyebrow: 'Catalog' },
  '/suppliers': { title: 'Suppliers', eyebrow: 'Procurement' },
  '/sales-orders': { title: 'Sales orders', eyebrow: 'Fulfilment' },
  '/purchase-orders': { title: 'Purchase orders', eyebrow: 'Procurement' },
};

const todayLabel = new Intl.DateTimeFormat('en-IN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
}).format(new Date());

function App() {
  const [token, setToken] = useState(() => sessionStorage.getItem('access_token'));
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [query, setQuery] = useState('');
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

  function handleAuthenticated(accessToken) {
    sessionStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  }

  function handleLogout() {
    sessionStorage.removeItem('access_token');
    setToken(null);
  }

  function handleSearch(event) {
    event.preventDefault();
    const term = query.trim().toLowerCase();
    if (!term) return;

    const match = navigation.find((item) => item.name.toLowerCase().includes(term));
    if (match) {
      navigate(match.path);
      setQuery('');
    }
  }

  const meta = useMemo(
    () => PAGE_META[location.pathname] ?? { title: 'NextGenERP', eyebrow: 'Workspace' },
    [location.pathname],
  );

  if (!token) {
    return <Auth onAuthenticated={handleAuthenticated} />;
  }

  return (
    <div className="min-h-screen bg-[#f4f0e9] text-stone-800">
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
            <div className="rounded-xl border border-teal-400/15 bg-teal-400/[0.06] p-3">
              <div className="flex items-center gap-2 text-[9px] font-semibold uppercase tracking-[0.2em] text-teal-300/80">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-60" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-teal-400" />
                </span>
                Forecast engine
              </div>
              <p className="mt-2 text-sm font-semibold text-white">XGBoost · WAPE 8.42%</p>
              <p className="text-[11px] leading-snug text-stone-400">7-day demand model online</p>
            </div>

            <div className="flex items-center gap-3 rounded-xl bg-white/[0.03] px-3 py-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-teal-400/15 text-[11px] font-semibold text-teal-200">
                AS
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-xs font-medium text-stone-200">Ops Admin</p>
                <p className="truncate text-[10px] text-stone-500">Inventory command center</p>
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

              <form
                onSubmit={handleSearch}
                className="ml-auto hidden items-center gap-2 rounded-lg border border-stone-200 bg-[#fffdf9] px-3 py-2 shadow-sm transition focus-within:border-teal-400 focus-within:ring-2 focus-within:ring-teal-500/15 sm:flex"
                role="search"
              >
                <Icon name="search" size={15} className="text-stone-400" />
                <input
                  type="text"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Jump to module…"
                  aria-label="Jump to module"
                  className="w-36 bg-transparent text-sm text-stone-700 outline-none placeholder:text-stone-400"
                />
                <kbd className="rounded border border-stone-200 bg-stone-50 px-1.5 py-0.5 text-[9px] font-medium text-stone-500">
                  Enter
                </kbd>
              </form>

              <div className="ml-auto flex items-center gap-2 sm:ml-0">
                <span className="hidden items-center gap-2 rounded-lg border border-stone-200 bg-[#fffdf9] px-3 py-2 text-xs text-stone-500 md:inline-flex">
                  <Icon name="clock" size={14} className="text-teal-600" />
                  {todayLabel}
                </span>
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-teal-200 to-emerald-300 text-[11px] font-bold text-teal-900 ring-2 ring-white">
                  AS
                </div>
              </div>
            </div>
          </header>

          <main className="flex-1 px-4 py-5 sm:px-6 sm:py-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/forecasting" element={<Forecasting />} />
              <Route path="/products" element={<Products />} />
              <Route path="/categories" element={<Categories />} />
              <Route path="/suppliers" element={<Suppliers />} />
              <Route path="/sales-orders" element={<SalesOrders />} />
              <Route path="/purchase-orders" element={<PurchaseOrders />} />
              <Route path="/inventory-operations" element={<InventoryTransactions />} />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
