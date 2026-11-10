# NextGenERP Project Audit

Date: 2026-11-11
Scope: repository state on branch `main`, including the in-app assistant, the
administrator system, sales analytics and the stabilization work that is not yet
pushed.

## 1. Purpose

This audit records what the application contains, how its parts interact, what
was verified, and where the remaining risk sits. It is based on direct
inspection of the repository and on commands that were actually run; it does not
repeat marketing claims.

## 2. System overview

NextGenERP is a single-page React application backed by a FastAPI service and a
relational database.

```
Browser (React 19 + Vite)
  |  fetch /auth, /products, /categories, /suppliers, /orders,
  |        /purchase-orders, /inventory-transactions, /ml, /assistant, /admin
  v
FastAPI (backend/main.py)
  |-- JWT authentication (backend/auth)
  |-- CRUD and workflow routes (backend/routes)
  |-- administrator and analytics routes (backend/routes/admin.py)
  |-- forecasting service (backend/ml)
  |-- project-scoped assistant (backend/assistant)
  v
SQLAlchemy 2 -> SQLite (development/tests) or PostgreSQL (Docker Compose)
```

### Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | React 19, React Router 7, Vite 8, Tailwind CSS 3, Three.js 0.180 |
| Backend | FastAPI, SQLAlchemy 2, Pydantic 2, PyJWT, pwdlib/Argon2 |
| Forecasting | XGBoost, scikit-learn, pandas, numpy (frozen trained artifacts) |
| Database | SQLite for local development and tests; PostgreSQL for Compose |
| Tests | pytest + FastAPI TestClient; Puppeteer/Edge for browser checks |

## 3. Repository layout

| Path | Responsibility |
| --- | --- |
| `backend/main.py` | App creation, CORS, validation handler, table creation, router wiring |
| `backend/routes/` | `auth`, `products`, `categories`, `suppliers`, `orders`, `purchase_orders`, `inventory_transactions`, `ml`, `assistant`, `admin` |
| `backend/models/` | SQLAlchemy models for users, catalog, suppliers, orders, purchase orders, inventory history |
| `backend/schemas/` | Pydantic request/response contracts, including safe administrator responses |
| `backend/auth/` | Password hashing, JWT creation/validation, active-user and role dependencies |
| `backend/services/analytics.py` | Revenue, user, product, inventory and supplier aggregation |
| `backend/database/migrations.py` | Additive, idempotent schema migration for SQLite and PostgreSQL |
| `backend/ml/` | Frozen model loading, prediction, reorder calculation, service facade |
| `backend/assistant/` | Scope check, knowledge base, documentation retrieval, live snapshot, local engine, optional LLM bridge |
| `backend/tests/` | 62 pytest tests, including assistant, administrator and regression suites |
| `frontend/src/` | App shell, pages, API helper, icons, 3D components, error boundary, assistant panel, administrator shell |
| `tests/` | 2000-scenario catalog generator and generated artifacts |
| `docs/` | Deployment, ML integration, UI redesign, assistant, audit, tracker, UX, test plan, progress |

## 4. Domain model

| Entity | Key fields | Relationships and rules |
| --- | --- | --- |
| `User` | `id`, `username`, `email`, password hash, `role`, `is_active`, `last_login_at`, `created_at` | Username normalized to lowercase; unique. Role is `ADMIN` or `USER`; registration always creates `USER`; inactive accounts cannot authenticate |
| `Category` | `id`, `name`, `description` | Cannot be deleted while a product references it |
| `Product` | `id`, `name`, `sku`, `price`, `stock_quantity`, `reorder_level`, `category_id` | Unique SKU; stock changes create inventory history |
| `Supplier` | `id`, `name`, contact fields, `lead_time_days`, `performance_rating` | Cannot be deleted while a purchase order references it |
| `Order` | `id`, customer fields, `product_id`, `quantity`, `total_amount`, `status`, `user_id`, `created_at` | Creating an order deducts stock; cancellation restores it once; history is not deletable; analytics use UTC timestamps |
| `PurchaseOrder` | `id`, `supplier_id`, `product_id`, `quantity`, `unit_price`, `total_amount`, `status`, `created_at` | Receiving adds stock once; received orders are protected |
| `InventoryTransaction` | `id`, `product_id`, `transaction_type`, `quantity`, previous/new stock, reason, timestamp | Append-only audit trail for stock movements |

Workflow states:

- Sales: `Pending -> Confirmed -> Shipped -> Delivered`; `Pending` and
  `Confirmed` can be cancelled.
- Purchases: `Pending -> Approved -> Ordered -> Received`; unreceived orders can
  be cancelled or deleted.

## 5. API surface

| Method and path | Purpose | Auth |
| --- | --- | --- |
| `POST /auth/register` | Create account and return a token | No |
| `POST /auth/login` | Exchange credentials for a token | No |
| `GET /auth/me` | Current user identity | Yes |
| `GET/POST /products/`, `GET/PUT/DELETE /products/{id}` | Product catalog | Yes |
| `GET/POST /categories/`, `PUT/DELETE /categories/{id}` | Categories | Yes |
| `GET/POST /suppliers/`, `PUT/DELETE /suppliers/{id}` | Suppliers | Yes |
| `GET/POST /orders/`, `PUT /orders/{id}`, `PUT /orders/{id}/status`, `DELETE /orders/{id}` | Sales workflow | Yes |
| `GET/POST /purchase-orders/`, `PUT /purchase-orders/{id}/status`, `DELETE /purchase-orders/{id}` | Purchase workflow | Yes |
| `GET/POST /inventory-transactions/` | Stock movements and history | Yes |
| `GET /ml/insights` | 7-day forecast and reorder recommendations | Yes |
| `POST /assistant/chat` | Project-scoped assistant reply | Yes |
| `GET /admin/overview` | Administrator KPI overview | Administrator |
| `GET /admin/analytics/daily` | Daily revenue/orders for the last N days | Administrator |
| `GET /admin/analytics/monthly` | Monthly revenue/orders for a selected year | Administrator |
| `GET /admin/analytics/yearly` | Year-over-year revenue/orders | Administrator |
| `GET /admin/analytics/users` | User-wise sales | Administrator |
| `GET /admin/analytics/products` | Product and inventory sales | Administrator |
| `GET /admin/analytics/inventory` | Stock movement and inventory value | Administrator |
| `GET /admin/analytics/suppliers` | Supplier and purchase analytics | Administrator |
| `GET /admin/users`, `GET /admin/users/{id}` | Safe account listing and detail | Administrator |
| `PUT /admin/users/{id}/status` | Activate or deactivate an account | Administrator |
| `GET /health` | Liveness and database check | No |

All protected routes use the same bearer-token dependency. The assistant
endpoint is read-only and cannot mutate business data. Administrator routes add
a database-backed role check on every request; a normal-user token receives HTTP
403.

## 6. Authentication and security posture

Implemented controls:

- Passwords hashed with pwdlib's recommended Argon2 configuration.
- Dummy hash verification keeps login timing closer to constant for unknown
  usernames.
- JWT HS256 tokens expire after 30 minutes; the secret is required at runtime.
- Protected routers depend on `require_authenticated_user`, which rejects
  inactive accounts as well as invalid tokens.
- Two roles only: `ADMIN` and `USER`. The role is read from the database on every
  request; it is not trusted from a JWT claim. `require_admin()` returns HTTP 403
  for normal users.
- Registration always creates `USER` accounts. Administrator provisioning uses
  `backend/create_admin.py` or an optional environment bootstrap; there is no
  default administrator and no hardcoded password.
- Administrator responses expose safe account fields only. Password hashes,
  access tokens and refresh tokens are never returned.
- Administrators cannot deactivate their own account, and the last active
  administrator is protected. Deactivation preserves business records.
- CORS uses explicit configured origins; wildcard configuration is rejected.
- Inputs are validated by Pydantic; SQL access goes through SQLAlchemy.
- Secrets are read from environment variables and are not returned to clients.
- The assistant refuses out-of-scope topics before any provider call and its
  prompt forbids revealing secrets, SQL, paths or model internals.

Gaps and risks:

| Risk | Severity | Status |
| --- | --- | --- |
| No rate limiting on login, registration or assistant chat | High | Open |
| No Content-Security-Policy header | Medium | Open |
| Assistant LLM mode sends a trimmed workspace snapshot to a third party when enabled | Medium | Documented; opt-in only |
| SQLite tests cannot exercise PostgreSQL row locks (`with_for_update()`) | Medium | Blocked scenarios recorded |
| JWT is stored in `sessionStorage`; XSS would expose it | Medium | Accepted for this app; CSP would reduce impact |
| No refresh-token rotation | Low | Open |
| No account lockout after repeated failures | Medium | Open (depends on rate limiting) |

## 7. Forecasting

- The trained XGBoost artifacts and the Kaggle Store Item dataset are treated as
  frozen. The audit and stabilization work did not retrain, replace or tune the
  model.
- Reported held-out metrics remain WAPE 8.42% and R² 0.744.
- `GET /ml/insights` generates the forecast once per request and overlays live
  ERP stock using case-insensitive product matching.
- Reorder recommendations are derived from forecast demand, lead time, safety
  stock and current stock. The assistant only explains them; it does not change
  them.
- User-facing copy now says "demand forecast" rather than framing the whole
  product as an AI system.

## 8. In-app assistant

The assistant is deliberately narrow:

- Covers only NextGenERP: inventory, products, categories, suppliers, sales
  orders, purchase orders, forecasting, navigation, accounts and troubleshooting.
- Refuses unrelated topics before any LLM call.
- Reads a live snapshot of products, suppliers, orders and purchase orders.
- Answers from a curated knowledge base and project documentation in local mode.
- Optionally calls an OpenAI-compatible provider when a key is configured; a
  failure falls back to the local answer.
- Is read-only and cannot create, edit, cancel, receive or delete records.
- Is mounted once in the authenticated shell, so it is available on every page.
- Supports English, Hindi and Bengali for panel copy, suggestions, help topics,
  live answers and refusals.
- Offers browser-native voice input and spoken replies; no audio is stored and
  no new dependency is required.

Known limits: product and supplier lists are capped in the prompt, recent orders
are capped, retrieval is keyword-based, responses are not streamed, and answers
can be wrong. Voice support depends on the browser, and real microphone capture
was not automated in headless Edge. The panel tells the user to verify before
acting.

## 9. Administrator system and analytics

The administrator area is deliberately separate from the normal workspace.

- `/admin/login` accepts administrator credentials only. A normal user is
  rejected at sign-in with a clear message.
- `/admin` renders the administrator shell. A normal-user session sees an
  access-denied screen, and every `/admin/*` API returns HTTP 403.
- The role is database-backed and checked per request. The JWT contains identity,
  not an administrator claim.
- The administrator can search and inspect safe account fields, deactivate or
  reactivate users, and view sales analytics. Deactivation does not delete
  orders, purchase orders or inventory history.
- Self-deactivation is disabled in the API and UI, and the last active
  administrator cannot be deactivated.

Analytics views:

| View | What it reports |
| --- | --- |
| Overview | Realized revenue, pending pipeline, order counts, inventory value, purchase expenditure, recent activity |
| Daily | Last 30 days by UTC day, with revenue and order counts |
| Monthly | Selected calendar year by month |
| Yearly | Year-over-year revenue and orders |
| Users | Revenue and order counts per user |
| Products | Best-selling products and units sold |
| Inventory | Stock movement, low-stock counts and inventory value at selling price |
| Suppliers | Purchase spend and supplier activity |

Revenue rules:

- Realized revenue includes only `Confirmed`, `Shipped` and `Delivered`.
- `Pending` is reported separately as pipeline revenue.
- `Cancelled` is excluded.
- Each order is counted once.
- Dates are normalized to UTC.
- Money is rounded with `Decimal` and `ROUND_HALF_UP` to two decimals.

Data and schema notes:

- `backend/database/migrations.py` adds the new columns and indexes
  idempotently for SQLite and PostgreSQL. `main.py` calls `ensure_schema()`.
- Existing accounts default to `USER`.
- Legacy demo orders without timestamps were backfilled only for
  `@example.test` rows; real records were not modified.
- Inventory value is labelled "at selling price" because product cost is not
  stored.

Verification:

- `backend/tests/test_admin.py`: 14 tests covering authorization, 403 for normal
  users, analytics totals and revenue rules, safe user fields, self-deactivation,
  last-admin protection, role escalation attempts and inactive-account handling.
- Administrator browser E2E: 50/50 checks passed, including all seven analytics
  tabs, monthly year selector, user detail, disposable user
  deactivate/reactivate, 390 px layout and no unexpected console errors.
- The Vite proxy initially omitted `/admin`, which made the browser calls fail.
  Adding `admin` to the proxy path fixed a real integration bug.

## 10. Verification performed

| Check | Result |
| --- | --- |
| Backend pytest suite | 62 passed, 1 third-party deprecation warning |
| Frontend production build | Passed; lazy Three.js chunk 694.91 kB (warning only) |
| Administrator E2E | 50/50 checks passed in headless Edge; normal users receive 403; all analytics tabs render |
| Administrator API tests | 14 tests in `backend/tests/test_admin.py` |
| Assistant browser flow (desktop and mobile) | Passed; no console errors |
| Mocked voice E2E | 41/41 checks passed |
| Secure-context voice E2E | 8/8 checks passed on an insecure non-localhost origin |
| Support-detection voice E2E | 4/4 checks passed |
| Native assistant language/layout | Passed on rerun; Hindi/Bengali welcome, suggestions, live answers, Bengali refusal, Escape close, zero horizontal overflow |
| Dashboard partial failure | Passed; aborted sales-orders request left other sections live |
| Inventory Operations page | Passed; one `main` landmark, form, snapshot and history render |
| 404 route | Passed |
| Test catalog | 2000 distinct scenarios generated |

The catalog is honest about coverage: 80 scenarios have recorded evidence, 41 are
blocked by environment or missing controls, and 1879 are defined but not yet
executed. See `tests/TEST_EXECUTION_REPORT.md`.

## 11. Prioritized recommendations

1. Add rate limiting and account lockout for authentication and assistant chat.
2. Add a Content-Security-Policy and other baseline security headers.
3. Run the blocked concurrency scenarios against PostgreSQL before relying on
   stock guarantees under parallel load.
4. Add frontend unit/component tests and a committed E2E suite instead of
   ad-hoc Puppeteer scripts.
5. Reduce the Three.js chunk with deeper code splitting or a lighter fallback.
6. Add pagination or virtualized rendering for large product and history lists.
7. Add structured audit logging for stock and order mutations.
8. Consider refresh-token rotation and a shorter access-token lifetime.
9. Add product cost data so administrator inventory value can be reported at
   cost as well as at selling price.
10. Add administrator audit logging for account activation changes and exports.
11. Rotate the generated development administrator password if the database is
    shared beyond this machine.

## 12. Audit method

- Read the route, model, schema, auth, ML and assistant source files.
- Ran the backend suite and the production build.
- Exercised the running app with headless Edge, including failure injection for
  the dashboard and mobile viewport checks for the assistant.
- Generated the test catalog from the same source of truth and cross-checked
  counts, unique IDs, unique titles, evidence and blocked reasons.
- No result in this document was inferred from an unexecuted test.
