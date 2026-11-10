# NextGenERP Test Execution Report

Date: 2026-11-11

## Executive summary

- Catalog scenarios: **1000**
- Executed and passed: **14**
- Not yet executed: **947**
- Blocked: **39**
- Automated backend suite: **43 passed** (1 third-party deprecation warning).
- Frontend production build: **passed**; one chunk-size warning for the lazy Three.js bundle.
- Assistant browser flow: **passed** on desktop and mobile with no console errors.
- Dashboard partial-failure check: **passed**; an aborted sales-orders request did not blank the other sections.
- Inventory Operations browser check: **passed**; one main landmark, form, snapshot, and history rendered.

## Commands actually run

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest -q
# 43 passed, 1 warning

cd ..\frontend
npm run build
# built successfully; three.module chunk is 694.91 kB
```

Browser checks used Puppeteer with Microsoft Edge against `http://localhost:5173` and the live backend on `http://127.0.0.1:8000`.

## Executed scenarios

| ID | Scenario | Evidence |
| --- | --- | --- |
| TC-0071 | Login UI: valid credentials sign in | Puppeteer assistant-test.cjs, 2026-11-11: login and authenticated shell rendered. |
| TC-0072 | Login UI: signed-in identity shows the username | Puppeteer assistant-test.cjs, 2026-11-11: identity showed demo438765052 and no hardcoded Ops Admin. |
| TC-0109 | Partial loading: sales orders endpoint unavailable | Puppeteer stabilization-check.cjs, 2026-11-11: orders aborted; products, categories, low-stock table and counts still rendered; sales cards showed Unavailable right now. |
| TC-0456 | UI: page renders inside the app shell without nested main | Puppeteer stabilization-check.cjs, 2026-11-11: exactly one main landmark; form, snapshot and history rendered. |
| TC-0457 | UI: stock history table renders rows | Puppeteer stabilization-check.cjs, 2026-11-11: Stock History showed three seeded movements with product, type, quantity and stock values. |
| TC-0880 | UI: launcher is visible | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0881 | UI: panel opens | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0882 | UI: panel closes | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0883 | UI: low-stock suggestion returns live answer | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0884 | UI: help suggestion returns steps | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0885 | UI: off-topic question is refused | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0886 | UI: mobile panel fits viewport | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0887 | UI: Escape closes panel | Puppeteer assistant-test.cjs, 2026-11-11: desktop and mobile assistant flow passed with no console errors. |
| TC-0927 | 404 and error boundary: unknown route shows Page not found | Puppeteer assistant-test.cjs, 2026-11-11: /does-not-exist rendered Page not found. |

## Blocked scenarios

| Count | Area | Reason |
| ---: | --- | --- |
| 8 | Inventory Operations / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite treats with_for_update() as a no-op. |
| 8 | Sales Orders / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently. |
| 12 | Purchase Orders / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently. |
| 5 | NextGenERP Assistant / LLM external provider | No external provider key is configured in this environment; the local fallback path is tested instead. |
| 6 | Security and API / Rate limiting | Rate limiting is not implemented in this build; the scenario is blocked until the control exists. |

## Honest status notes

- The 1000 scenarios are distinct test intents, not 1000 automated tests. Only the rows marked `passed` were executed.
- The backend suite covers 43 tests; it is not mapped one-to-one to catalog IDs, so no bulk pass status was inferred.
- `blocked` means the capability or environment is missing, not that the test failed.
- No result in this report was fabricated or copied from an earlier run.

## Known gaps

- PostgreSQL-specific concurrency and locking paths are blocked in this SQLite-based test environment.
- External LLM provider success, timeout, 401, 429, and custom-base-URL paths are blocked without a provider key.
- Rate limiting is not implemented, so those security scenarios are blocked.
- Frontend unit tests and a permanent cross-browser E2E suite are not configured.
- The Three.js chunk remains above Vite's 500 kB warning threshold.
