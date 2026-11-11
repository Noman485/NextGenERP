# NextGenERP Pre-Deployment Checklist

Date: 2026-11-11
Release candidate: working tree on `main` (uncommitted)
Decision rule: **do not deploy while any mandatory item below is unchecked.** Items marked “accepted” need an explicit owner sign-off.

Legend: `[x]` verified, `[ ]` outstanding or blocked, `[!]` accepted risk / manual sign-off required.

## 1. Build and automated tests

- [x] Security suite executes all 906 automated catalog cases: `906 passed, 0 failed, 0 skipped` in 325.15 s.
  - Command: `Set-Location backend; .\venv\Scripts\python.exe -m pytest tests\test_security_suite.py -q --junitxml=security-results-run2.xml`
  - Evidence: `security-results-run2.xml` (`tests="906" failures="0" errors="0" skipped="0"`).
- [x] Full backend regression suite (`backend/tests`) is green: `972 passed, 0 failed, 0 skipped` in 424.68 s.
  - Command: `Set-Location backend; .\venv\Scripts\python.exe -m pytest -q --junitxml=backend-full.xml`
  - Evidence: `backend-full.xml` (`tests="972" failures="0" errors="0" skipped="0"`). The 972 includes the 906 security cases plus the existing backend tests.
- [x] Frontend production build succeeds.
  - Command: `Set-Location frontend; npm run build`
  - Evidence: Vite 8.3.4, 51 modules transformed, `dist/index.html` + hashed CSS/JS assets emitted.
  - Known warning: the Three.js chunk is 694.91 kB (>500 kB warning). Tracked as BUG-017; not a release blocker.
- [ ] Frontend browser smoke test against the production build on the target browser(s). No committed E2E framework exists (BUG-018).
- [ ] PostgreSQL verification suite (`SEC-0941`–`SEC-0968`) is blocked: no PostgreSQL service/Docker in this environment. Run connectivity, schema, migrations, type parity, concurrency and rollback checks on PostgreSQL before release.

## 2. Secrets and environment

- [x] `.env` and `backend/.env` are untracked; `.gitignore` ignores `.env` and `.env.*` while tracking `.env.example`.
- [x] `.env.example` contains placeholders only; no real JWT secret, database password or provider key.
- [x] Source and `frontend/dist` scans find no JWT secret, database URL, provider key (`sk-…`) or password hash.
- [x] `docker-compose.yml` requires `POSTGRES_PASSWORD` and `JWT_SECRET_KEY` with `${VAR:?}`.
- [ ] Set production `JWT_SECRET_KEY` to a fresh random value of at least 32 characters (64 hex characters recommended). Do not reuse the test or development value.
- [ ] Set a unique production `POSTGRES_PASSWORD`; do not reuse the example value.
- [ ] Rotate any development/default administrator credential before exposing the service. The live `admin` credential referenced in older notes must not be treated as a production secret.
- [ ] Confirm no provider key is configured unless assistant LLM mode is intended; if configured, restrict spend and keep the key server-side.

## 3. Application configuration

- [x] `ENVIRONMENT=production` disables `/docs`, `/redoc` and `/openapi.json` unless `ENABLE_API_DOCS` is explicitly enabled.
- [ ] Leave `ENABLE_API_DOCS` unset in production (or set it only for a controlled, authenticated window).
- [x] CORS rejects `*` at startup, lists explicit origins, sets `allow_credentials=False`, and allows only `GET/POST/PUT/DELETE/OPTIONS` with `Authorization`/`Content-Type`.
- [ ] Replace the example `CORS_ORIGINS` with the exact production frontend origin(s); remove localhost/example entries.
- [x] Security headers are applied to API responses; nginx applies CSP and baseline headers to the SPA/static assets.
- [x] HSTS is emitted only for HTTPS / trusted `X-Forwarded-Proto: https`.
- [x] Rate limiting is enabled by default (`SECURITY_RATE_LIMIT_ENABLED` unset/1) with login/register/assistant scopes.
- [ ] Decide the backend worker count. The limiter is in-process; multi-worker deployments require a shared counter store before they can enforce global limits (BLK-003).
- [ ] If a reverse proxy adds clients through `X-Forwarded-For`, keep direct-client limiting or configure a trusted-proxy allowlist. The current code deliberately ignores forwarded headers.

## 4. Database and migrations

- [x] Additive schema bootstrap (`ensure_schema`) creates missing tables, adds missing columns and indexes, and is idempotent on SQLite.
- [x] Unique SKU, foreign keys and failed-order rollback are covered by automated deployment cases.
- [ ] Take a verified backup before running migrations on the production database.
- [ ] Rehearse restore of that backup on a separate database.
- [ ] Run `ensure_schema()` against PostgreSQL and confirm existing rows are preserved.
- [ ] Verify UTC timestamp round-trip and naive/aware datetime behavior on PostgreSQL (SQLite returns naive datetimes).
- [ ] Run two concurrent stock/order/cancellation/purchase-receipt transactions on PostgreSQL; SQLite makes `with_for_update()` a no-op (BLK-001).

## 5. Network and edge

- [x] `docker-compose.yml` binds PostgreSQL to `127.0.0.1` and does not use host networking.
- [x] PostgreSQL healthcheck, service restart policies and a named data volume are present.
- [x] nginx denies dotfiles (except `/.well-known/`) and database/backup/log/key artifacts; request body limit is 2 MB; `server_tokens off`; `X-Powered-By` hidden.
- [ ] Terminate TLS at the edge and verify HSTS, certificate chain, redirect from HTTP, and the production CSP in a real browser.
- [ ] Confirm the frontend can reach the API only through the intended origin/proxy; no wildcard CORS.
- [ ] Confirm `/health` is the only unauthenticated diagnostic endpoint exposed; `/database-test` is hidden from the schema but still routed, so restrict it at the edge if not needed.

## 6. UI and chart regression

- [x] “Orders by status” maps colors by the actual status value, not array index:
  - Pending `#f59e0b`, Confirmed `#0ea5e9`, Shipped `#6366f1`, Delivered `#0f766e`, Cancelled `#e11d48`.
- [x] The legend uses the same `STATUS_COLORS` map as the bars, so graph and legend cannot drift.
- [x] All five statuses remain in `statusSeries` even when the count is zero; zero bars render at zero height and the legend row still renders.
- [x] Responsive `viewBox`/`w-full` behavior is preserved; no animation behavior was removed.
- [x] No fake order data or demo historical sales were added for chart verification; the chart reads only `/admin/overview` business counts.
- [x] Built bundle contains all five status colors.
- [ ] Perform a visual check with a real admin account and the target browser at desktop and mobile widths.

## 7. Manual, blocked and accepted items

- [ ] Real microphone permission/capture, permission denial, no-device behavior, and Hindi/Bengali speech output (20 blocked voice cases). Only English voices are installed here and headless Edge cannot grant microphone access.
- [ ] Cross-browser E2E (Firefox/WebKit); only headless Edge is available (BLK-004/BLK-006).
- [ ] Dependency advisory scan: `pip-audit` is unavailable and npm audit is constrained by network/offline access (SEC-0985–SEC-0988). Run both in CI with advisory database access.
- [ ] Python/npm transitive dependency review against current advisories.
- [ ] [!] Shared-workspace access: any authenticated USER can read all business records. Accepted as a product decision; obtain owner sign-off before release.
- [ ] [!] No structured audit log for admin/stock/order mutations (24 not-implemented cases). Accepted only with an explicit risk decision and compensating monitoring.
- [ ] [!] Stateless JWT replay until 30-minute expiry; no refresh rotation or server-side revocation. Accepted by design unless the threat model requires otherwise.
- [ ] [!] Frontend component/E2E test framework absent (BUG-018). Accepted temporarily; add Vitest/RTL or Playwright.

## 8. Release actions

- [ ] Review the complete working-tree diff; no debug code, test database, generated JUnit/log file or local secret is staged.
- [ ] Commit the security audit, reports, tests and chart fix as a reviewed change set. **No commit has been made by this audit.**
- [ ] Confirm the release commit SHA and archive the JUnit result, backend log and frontend build log with it.
- [ ] Obtain explicit approval for push/deploy. **No push to `main`, deployment, or repository creation has been performed.**
- [ ] Prepare rollback: previous image/commit, database backup restore command, and a smoke test for login, products, orders, admin overview and assistant.
- [ ] After deploy, re-run `/health`, login, one authenticated read, one rate-limit probe (429), and the chart visual check.

## Release sign-off

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Engineering |  |  |  |
| Security |  |  |  |
| Product owner (shared-workspace/audit-log acceptance) |  |  |  |
| Operations (PostgreSQL/TLS/rollback) |  |  |  |
