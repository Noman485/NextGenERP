# Agent Progress Log

Project: NextGenERP
Branch: `main`
Last updated: 2026-11-11

This log records what was changed, why, how it was verified, and what remains. It
is written for the next person who picks up the work, not as a changelog of
every command.

## Current status

| Area | Status |
| --- | --- |
| Backend test suite | 43 passed, 1 third-party deprecation warning |
| Frontend production build | Passed; lazy Three.js chunk 694.91 kB (warning only) |
| In-app assistant | Implemented, tested and browser-verified on desktop and mobile |
| Dashboard partial loading | Implemented and verified by aborting a request |
| Inventory Operations redesign | Implemented and browser-verified |
| Required documentation | Complete |
| 1000-scenario catalog | Generated: 14 passed, 39 blocked, 947 not_run |
| Git | Work is uncommitted at the time of writing; push pending |

## Work completed

### 1. In-app project assistant

User request: an assistant that revolves only around NextGenERP.

Decisions:

- Provider-agnostic design. A built-in local engine works with no API key; an
  optional OpenAI-compatible provider can be enabled by environment variable.
- Strict project scope. Off-topic requests are refused before any provider call.
- Read-only. The assistant can query and explain but cannot mutate records.
- Grounded in live data. A snapshot of products, suppliers, sales orders and
  purchase orders is built per request.
- Mounted once in the authenticated shell so it is available on every page.

Files:

- `backend/assistant/knowledge.py` — curated topics and suggestion chips.
- `backend/assistant/docs.py` — keyword retrieval over project docs.
- `backend/assistant/snapshot.py` — read-only workspace snapshot.
- `backend/assistant/engine.py` — scope check, intent routing, live answers,
  LLM orchestration and fallback.
- `backend/assistant/llm.py` — OpenAI-compatible bridge with a strict system
  prompt.
- `backend/routes/assistant.py` — authenticated `POST /assistant/chat`.
- `backend/schemas/assistant.py` — request/response validation.
- `frontend/src/components/Assistant.jsx` — floating panel, suggestions, retry,
  Escape close, mobile layout.
- `frontend/src/App.jsx` — shell integration.
- `frontend/src/components/Icons.jsx` — `send` icon.
- `docs/ai-assistant.md` — architecture, config, API, privacy, testing.
- `.env.example` — commented provider variables.

Verification:

- `backend/tests/test_assistant.py`: 11 tests covering authentication, limits,
  greeting, refusal, live low stock, stock lookup, pending sales, help topics,
  catalog counts, provider fallback and prompt/key handling.
- Browser E2E on desktop and mobile: launcher, open, live low-stock answer, help
  answer, scope refusal, close, 404 route, mobile chat, Escape close, zero
  horizontal overflow, no console errors.

### 2. Stabilization fixes

| Fix | Root cause | Verification |
| --- | --- | --- |
| Real signed-in identity | Hardcoded shell label | `/auth/me` and browser check |
| 404 route | No catch-all route | Browser check |
| Error boundary | Unhandled render errors blanked the app | Implementation review |
| Dashboard partial loading | All-or-nothing `Promise.allSettled` handling | Aborted `/orders/` check |
| Inventory nested `<main>` | Page rendered its own landmark | Exactly one `main` measured |
| Supplier commit failures | Uncaught `SQLAlchemyError` | 503 regression test for POST/PUT/DELETE |
| Order update normalization | No trim or blank-name check | Regression test |
| Single forecast generation | Service generated a second frame | Regression test with call counter |
| Case-insensitive ERP overlay | Exact name matching | Regression test with `Amul Butter` |
| Search no-match feedback | Silent return | Browser check |
| Assistant 404 | Vite proxy allowlist missed `/assistant` | Assistant E2E |
| Assistant not rendering | Stale Vite transform in OneDrive folder | Polling enabled; dev server restarted |
| AI-centric dashboard copy | Legacy wording | Source grep and build |

### 3. UX work

- Dashboard: per-section unavailable states, failure banner with retry, honest
  loading placeholders, neutral copy.
- Inventory Operations: rebuilt layout, selected-product context, separated load
  and form errors, snapshot metrics, history table, empty state, mobile support.
- Shell: skip link, 404, error boundary, search feedback, real identity.
- Assistant: floating launcher, suggestion chips, retry, scope note, responsive
  panel.

Details are in `docs/UX_IMPROVEMENTS.md`.

### 4. Test catalog

- `tests/generate_test_cases.py` deterministically builds 1000 distinct
  scenarios across twelve modules and writes:
  - `tests/test_cases.json`
  - `tests/TEST_CASE_CATALOG.md`
  - `tests/TEST_EXECUTION_REPORT.md`
- Counts are asserted by the generator: Authentication 80, Dashboard 60,
  Products 100, Categories 60, Suppliers 90, Inventory 110, Sales 120, Purchases
  120, Forecasting 80, Assistant 80, Navigation 50, Security 50.
- Statuses are honest: 14 passed with evidence, 39 blocked with reasons, 947
  not_run.
- The generator rejects duplicate titles and enforces module counts.

### 5. Documentation

- `docs/PROJECT_AUDIT.md` — architecture, data model, API surface, security
  posture, verification, risks and recommendations.
- `docs/BUG_TRACKER.md` — 14 fixed defects, 9 open issues, blocked verification
  and triage rules.
- `docs/UX_IMPROVEMENTS.md` — before/after UX changes and remaining
  opportunities.
- `docs/TEST_PLAN.md` — strategy, environments, data, entry/exit criteria,
  commands, coverage map and risk matrix.
- `docs/AGENT_PROGRESS.md` — this file.

## Important decisions

1. **Do not touch the frozen model.** The XGBoost artifacts, dataset and reported
   metrics remain as they were. All forecasting work is display, matching or
   call-count related.
2. **Local-first assistant.** No API key is required for the core experience.
   External providers are opt-in and fall back to local answers on failure.
3. **Read-only assistant.** It cannot create, edit, cancel, receive or delete.
   This keeps the blast radius small and avoids duplicating workflow validation.
4. **Honest test reporting.** The catalog does not claim coverage that was not
   executed. Blocked is distinct from failed and from not_run.
5. **Keep SQLite and PostgreSQL compatible.** No new database dependency was
   added. PostgreSQL-only concurrency checks are documented as blocked.
6. **OneDrive-aware dev setup.** Vite polling is enabled because native file
   events are unreliable in the project folder on Windows.
7. **Work on the current branch.** No reset, rebase or destructive cleanup was
   performed.

## Environment notes

- Frontend dev server: `http://localhost:5173`
- Backend: `http://127.0.0.1:8000` (`/health`, `/docs`)
- Backend tests: `cd backend; .\venv\Scripts\python.exe -m pytest -q`
- Frontend build: `cd frontend; npm run build`
- Browser checks: Puppeteer with Microsoft Edge, scripts kept outside the repo in
  the working environment.
- The backend must be restarted from `backend` after code changes; an old process
  will serve old routes.
- The Vite dev server must be restarted after `vite.config.js` changes.

## Verification evidence

| Check | Evidence |
| --- | --- |
| Backend suite | 43 passed in 25.95 s, 1 Starlette deprecation warning |
| Production build | Built in 2.37 s; `three.module` 694.91 kB |
| Assistant E2E | Desktop and mobile flow passed; console errors none |
| Dashboard partial failure | Banner shown; products and low-stock data stayed live; sales section unavailable |
| Inventory page | One `main`; form, snapshot and history present |
| Catalog | 1000 unique IDs, 1000 unique titles, no missing steps or expected results |

## Remaining work

1. Rerun the backend suite and production build after the final copy/doc edits.
2. Rerun the assistant and stabilization browser checks; confirm no React key
   warnings on Sales Orders and Purchase Orders.
3. Review the generated catalog and docs for consistency with the final code.
4. Commit all work and push to `origin main`.
5. After push, run the blocked PostgreSQL concurrency suite in an environment
   that has PostgreSQL.
6. Implement rate limiting and security headers (see `docs/BUG_TRACKER.md`).
7. Add a committed frontend test runner and E2E suite.

## Constraints to preserve

- Do not retrain or replace the forecasting model.
- Do not remove existing business features or discard user changes.
- Do not hardcode demo credentials in production code.
- Do not expose secrets, tokens, passwords or provider keys in logs or responses.
- Keep the assistant strictly scoped to NextGenERP.
- Keep SQLite and PostgreSQL compatibility.
- Mark tests honestly; never fabricate results.
