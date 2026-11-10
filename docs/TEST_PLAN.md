# NextGenERP Test Plan

Date: 2026-11-11
Version: 1.0
Owner: Engineering
Related artifacts: `tests/test_cases.json`,
`tests/TEST_CASE_CATALOG.md`, `tests/TEST_EXECUTION_REPORT.md`,
`docs/BUG_TRACKER.md`

## 1. Objective

Verify that NextGenERP's catalog, inventory, sales, purchasing, forecasting and
assistant workflows behave correctly, safely and accessibly, without changing
the frozen forecasting model or removing existing functionality.

## 2. Scope

In scope:

- Authentication and session handling.
- Products, categories, suppliers, sales orders, purchase orders and inventory
  transactions.
- Stock deduction, restoration and receiving invariants.
- Dashboard aggregation and partial-failure behavior.
- Demand forecast display, reorder suggestions and ERP overlay.
- Project-scoped assistant: allowed topics, refusals, live data, limits,
  fallbacks and UI.
- Navigation, 404 handling, responsive layout and keyboard access.
- API validation, authorization, CORS and secret handling.

Out of scope for this cycle:

- Model retraining, dataset changes or metric tuning.
- Payment, shipping-carrier and tax integrations (not present).
- Load testing at production scale.
- Native mobile applications (not present).

## 3. Test strategy

Risk-based, layered testing:

| Level | What it covers | Tooling |
| --- | --- | --- |
| Unit/service | Reorder math, assistant intent routing, snapshot shaping | pytest |
| API integration | Status codes, validation, persistence, auth, workflows | pytest + FastAPI TestClient |
| Component/UI | Rendering, dialogs, filters, empty/error states, accessibility | Browser automation (Puppeteer + Edge) |
| End-to-end | Login -> task -> persisted result across pages | Browser automation |
| Non-functional | Responsive widths, keyboard, console errors, secret exposure | Browser automation + inspection |
| Regression | Previously fixed defects | pytest regression suite + catalog IDs |

The 1000-scenario catalog is the traceability layer. It contains distinct test
intents across twelve modules. It is not 1000 automated tests. A scenario is
marked `passed` only when it was executed and evidence is recorded.

## 4. Environments

| Environment | Frontend | Backend | Database |
| --- | --- | --- | --- |
| Local development | Vite `http://localhost:5173` | FastAPI `http://127.0.0.1:8000` | SQLite file from `DATABASE_URL` |
| Automated backend tests | n/a | FastAPI TestClient | Temporary SQLite database with foreign keys enabled |
| Compose (documented) | Built frontend | FastAPI container | PostgreSQL |

Constraints:

- The test environment has no PostgreSQL service, so row-lock and true
  concurrency scenarios are blocked.
- Only headless Microsoft Edge is available; cross-browser coverage is blocked.
- No external LLM provider key is configured; provider success/timeout/401/429
  paths are blocked and local fallback is tested.

## 5. Test data

Backend tests create data per test through fixtures:

- A unique user per test and an authenticated client.
- Category, product and supplier factories with sensible defaults.
- Orders created through the API so stock and history stay consistent.
- The test database is dropped and recreated for every test.

Browser checks use the running development workspace:

- Products include `amul butter` (stock 5), `cheese` (stock 200) and `chips`
  (stock 500).
- `amul butter` is the low-stock product used for live assistant answers.
- Checks must not leave the workspace in a broken state; read-only checks are
  preferred, and any created record must be accounted for.

Rules:

- Never hardcode production credentials in source.
- Never log tokens, passwords or provider keys.
- Do not modify the frozen model, dataset or metrics.

## 6. Entry and exit criteria

Entry:

- Backend starts and `/health` returns `ok`.
- Frontend dev server or production build is reachable.
- Test database can be created.
- No unresolved blocker prevents the suite from running.

Exit for a release:

- All automated backend tests pass.
- Production build succeeds.
- No open `critical` or `high` defect that affects stock integrity, auth or
  secret handling.
- Executed catalog scenarios have evidence; blocked scenarios have a reason and
  an owner.
- No new console errors on the main flows.

Current status (2026-11-11):

- Backend: 43 passed, 1 third-party deprecation warning.
- Build: passed, one chunk-size warning.
- Catalog: 1000 total, 14 passed, 39 blocked, 947 not_run.
- Release is **not** fully verified because most catalog scenarios are not yet
  executed and rate limiting is missing.

## 7. How to run

Backend suite:

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest -q
```

Single regression file:

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest tests\test_regressions.py -q
```

Frontend build:

```powershell
cd frontend
npm run build
```

Regenerate the catalog:

```powershell
python tests\generate_test_cases.py
```

Browser checks (examples live outside the repo in the working environment):

```powershell
node assistant-test.cjs
node stabilization-check.cjs
```

## 8. Coverage map

| Module | Scenarios | Focus |
| --- | ---: | --- |
| Authentication | 80 | Registration, login, tokens, conflicts, UI states |
| Dashboard | 60 | KPI math, boundaries, partial loads, empty states, 3D fallback, accessibility |
| Products | 100 | CRUD, validation, stock adjustments, relationships, search, dialogs, security |
| Categories | 60 | CRUD, duplicates, delete restrictions, UI, security |
| Suppliers | 90 | CRUD, boundaries, delete restrictions, UI, large lists, security |
| Inventory Operations | 110 | Stock in/out, validation, history, concurrency, UI, snapshot metrics |
| Sales Orders | 120 | Create, validation, deduction, transitions, cancellation, UI, security, concurrency |
| Purchase Orders | 120 | Create, validation, transitions, receiving, cancellation, UI, security, concurrency |
| Demand Forecast | 80 | Display, reorder logic, filters, refresh, model integrity, ERP overlay, accessibility |
| NextGenERP Assistant | 80 | Allowed/refused scope, live data, help, LLM paths, UI, privacy |
| Navigation and UI | 50 | Routes, shell, search, 404, accessibility, responsive |
| Security and API | 50 | Auth requirements, injection, CORS, secrets, XSS, rate limiting |

## 9. Risk matrix

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Stock goes negative under concurrent writes | Medium | Critical | PostgreSQL lock tests before production; keep current single-writer assumptions |
| Double receiving adds stock twice | Medium | Critical | Receiving status guard; blocked concurrency scenarios must run on PostgreSQL |
| Auth brute force | High | High | Rate limiting and lockout (open) |
| Assistant leaks workspace data to a provider | Low | High | Opt-in provider, trimmed snapshot, strict prompt, documented privacy note |
| Assistant answers outside scope | Medium | Medium | Pre-LLM scope refusal and tests |
| Partial dashboard hides failures | Low | Medium | Per-section unavailable states and banner |
| Large lists degrade performance | Medium | Medium | Pagination/virtualization (open) |
| Three.js chunk slows first load | High | Low | Lazy import already; further splitting recommended |
| SQLite/PostgreSQL behavior drift | Medium | High | Run the blocked suite against PostgreSQL |

## 10. Defect workflow

1. Reproduce and record the smallest reliable steps.
2. Classify severity using `docs/BUG_TRACKER.md`.
3. Write or identify a failing test.
4. Fix the root cause, not the symptom.
5. Add a regression test or record why automation is not feasible.
6. Rerun the focused test, the full backend suite and the production build.
7. Update the catalog status and evidence honestly.
8. Commit the fix with the test.

## 11. Reporting

- `tests/TEST_EXECUTION_REPORT.md` is regenerated with the catalog and lists only
  executed scenarios with evidence.
- Blocked rows include the reason and the missing capability.
- `not_run` is not a failure; it is unverified work.
- Do not bulk-mark scenarios as passed from an unrelated automated suite.

## 12. Current blocked items

| Area | Count | Reason | Unblock action |
| --- | ---: | --- | --- |
| Inventory concurrency | 8 | SQLite no-op row locks | Run against PostgreSQL with parallel clients |
| Sales concurrency | 8 | SQLite write serialization differs | Run against PostgreSQL |
| Purchase concurrency | 12 | SQLite write serialization differs | Run against PostgreSQL |
| External LLM provider | 5 | No provider key | Configure a test key or mock endpoint |
| Rate limiting | 6 | Control not implemented | Implement and test limits |
| Cross-browser E2E | n/a | Only Edge installed | Add Playwright browsers or another runner |
