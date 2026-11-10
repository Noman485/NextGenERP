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
| Backend test suite | 62 passed, 1 third-party deprecation warning |
| Frontend production build | Passed; lazy Three.js chunk 694.91 kB (warning only) |
| In-app assistant | Implemented, tested and browser-verified on desktop and mobile |
| Assistant languages and voice | English/Hindi/Bengali localization plus browser voice input/output; reliability fixes verified in headless Edge |
| Administrator system | Separate `/admin/login` and `/admin` area, database-backed `ADMIN` role, 403 for normal users |
| Sales analytics | Daily, monthly, yearly, user, product, inventory and supplier views implemented |
| Dashboard partial loading | Implemented and verified by aborting a request |
| Inventory Operations redesign | Implemented and browser-verified |
| Required documentation | Complete for this cycle |
| Test catalog | 2000 scenarios generated: 80 passed, 41 blocked, 1879 not_run |
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
- Multilingual by design. English, Hindi and Bengali share one engine; localized
  copy, keywords, status labels and templates live in one module.
- Voice uses browser-native APIs only: `SpeechRecognition` for input and
  `speechSynthesis` for output. No new dependency, no stored audio and no
  server-side speech service.
- Language changes reset the conversation so scripts and context do not mix;
  auto-speak is off by default and every answer has its own speaker control.

Files:

- `backend/assistant/knowledge.py` — curated topics and suggestion chips.
- `backend/assistant/localization.py` — language metadata, localized copy,
  keywords, status labels, reply templates and the LLM language instruction.
- `backend/assistant/docs.py` — keyword retrieval over project docs.
- `backend/assistant/snapshot.py` — read-only workspace snapshot.
- `backend/assistant/engine.py` — scope check, intent routing, live answers,
  localization, LLM orchestration and fallback.
- `backend/assistant/llm.py` — OpenAI-compatible bridge with a strict system
  prompt and explicit language instruction.
- `backend/routes/assistant.py` — authenticated `POST /assistant/chat`.
- `backend/schemas/assistant.py` — request/response validation, including the
  `language` field.
- `frontend/src/components/Assistant.jsx` — floating panel, language selector,
  microphone input, spoken replies, auto-speak, suggestions, retry, Escape close
  and mobile layout.
- `frontend/src/App.jsx` — shell integration.
- `frontend/src/components/Icons.jsx` — `send`, `mic`, `volume`, `volumeOff` and
  `globe` icons.
- `docs/ai-assistant.md` — architecture, config, API, privacy, languages, voice
  and testing.
- `.env.example` — commented provider variables.

Verification:

- `backend/tests/test_assistant.py`: 16 tests covering authentication, limits,
  greeting, refusal, live low stock, stock lookup, pending sales, help topics,
  catalog counts, provider fallback, prompt/key handling, Hindi/Bengali
  greetings, localized live answers, localized help/refusal, unsupported
  language rejection and the LLM language instruction.
- Browser E2E on desktop and mobile: launcher, open, live low-stock answer, help
  answer, scope refusal, close, 404 route, mobile chat, Escape close, zero
  horizontal overflow, no console errors.
- Voice/language E2E: three language options, mic control enabled in Edge,
  auto-speak toggle, Hindi and Bengali welcome/suggestions, localized live
  low-stock answers, Bengali scope refusal, localized launcher, speaker
  play/stop state, 366 × 544 px mobile panel and zero horizontal overflow.
  Real microphone capture and permission prompts remain a manual check.

### 2. Administrator system and sales analytics

User request: a separate administrator area with sales analytics, without giving
normal users elevated access.

Decisions:

- Two roles only: `ADMIN` and `USER`. Existing accounts remain `USER`.
- The role is stored on the user row and checked from the database on every
  request. It is deliberately not trusted from a JWT claim, so a modified token
  cannot grant administrator access.
- `require_authenticated_user()`, `require_role()` and `require_admin()` enforce
  active accounts and administrator access. Deactivated tokens receive HTTP 403.
- Registration never creates administrators. Provisioning uses
  `backend/create_admin.py` or the optional `ADMIN_BOOTSTRAP_USERNAME` /
  `ADMIN_BOOTSTRAP_PASSWORD` environment bootstrap. No password is hardcoded.
- The administrator UI is a separate shell at `/admin/login` and `/admin`.
  Normal users are rejected at sign-in and receive an access-denied screen; the
  admin APIs return 403.
- Administrator responses expose safe account fields only. Password hashes,
  JWTs, refresh tokens and other authentication secrets are never returned.
- An administrator cannot deactivate their own account, and the last active
  administrator is protected. Deactivation preserves all business records.
- Analytics are computed in Python so SQLite and PostgreSQL behave the same.
  Money is rounded with `Decimal` and `ROUND_HALF_UP` to two decimals.
- Revenue rules: realized revenue includes only `Confirmed`, `Shipped` and
  `Delivered`; `Pending` is reported separately as pipeline; `Cancelled` is
  excluded. Dates are handled in UTC and each order is counted once.
- Inventory value is labelled "at selling price" because product cost is not
  stored in the current schema.
- Schema changes are additive and idempotent through
  `backend/database/migrations.py`; `main.py` calls `ensure_schema()`.
- Legacy demo orders without timestamps were backfilled only for
  `@example.test` demo rows. Real records were left untouched.

Endpoints:

- `GET /admin/overview`
- `GET /admin/analytics/daily?days=30`
- `GET /admin/analytics/monthly?year=...`
- `GET /admin/analytics/yearly?years=...`
- `GET /admin/analytics/users`
- `GET /admin/analytics/products`
- `GET /admin/analytics/inventory`
- `GET /admin/analytics/suppliers`
- `GET /admin/users`, `GET /admin/users/{id}`,
  `PUT /admin/users/{id}/status`

Frontend:

- `frontend/src/pages/admin/AdminLogin.jsx` and `AdminApp.jsx` provide the
  separate administrator shell.
- `AdminOverview.jsx`, `AdminAnalytics.jsx`, `AdminUsers.jsx` and
  `AdminComponents.jsx` provide KPIs, seven analytics tabs, accessible SVG
  charts, user search, pagination and activation controls.
- `frontend/src/Root.jsx` wires `/admin/login`, `/admin/*` and the normal app.
- `frontend/vite.config.js` now proxies `/admin/*` to the backend; the missing
  proxy entry was a real integration bug found during browser testing.

Verification:

- `backend/tests/test_admin.py`: 14 tests covering authorization, 403 for normal
  users, analytics totals and revenue rules, user listing, self-deactivation,
  last-admin protection, role escalation attempts and secret exclusion.
- Full backend suite: 62 passed, 1 third-party warning.
- Administrator browser E2E: 50/50 checks passed in headless Edge, including
  unauthenticated redirect, normal-user rejection, admin login, overview KPIs,
  all seven analytics tabs, monthly year selector, user detail, disabled
  self-deactivation, disposable user deactivate/reactivate, all admin APIs,
  390 px layout and no unexpected console errors.

Live provisioning:

- The local development database has an administrator account named `admin`.
  Its password was generated during provisioning and is not stored in the
  repository or documentation. Rotate it if the development database is shared.

### 3. Voice assistant reliability

The voice feature remains browser-native (`SpeechRecognition` /
`webkitSpeechRecognition` and `speechSynthesis`); no dependency or server-side
speech service was added.

Fixes made after the first voice implementation:

- Detect secure context explicitly. On an insecure non-localhost origin the
  microphone is disabled with guidance, and a forced click cannot create a
  recognition session. Typing remains available.
- Load voices asynchronously through `voiceschanged` as well as at mount, so a
  late voice list is not missed.
- Select an exact locale voice when available, then a same-language voice, then
  a safe default.
- Show the interim transcript without submitting it; submit only the final
  transcript.
- Add a 15-second recognition timeout with localized guidance.
- Map permission, service, no-speech, audio-capture, network,
  language-not-supported, busy and unknown errors to specific localized
  messages.
- Stop or abort recognition on stop, Escape, close, language change and unmount,
  and ignore late results after stop or close.
- Add a synchronous `startingRef` guard so a rapid double-click cannot create
  two recognition sessions. The mocked E2E found this race before the fix.

Verification:

- Mocked voice E2E: 41/41 checks passed, including locales, interim transcript,
  single final submission, voice selection, stop playback, auto-speak, eight
  error codes, timeout, late results, language switch mid-listen, XSS escaping
  and rapid double-click.
- Secure-context E2E: 8/8 checks passed on the genuinely insecure origin
  `http://192.168.1.7:5174` with a second Vite server.
- Support-detection E2E: 4/4 checks passed for missing recognition and missing
  synthesis.
- Native assistant test: passed on rerun, including Hindi/Bengali welcome,
  suggestions, live answers, Bengali scope refusal, Escape close and 390 px
  layout with zero horizontal overflow.

Remaining limit: headless Edge cannot grant a real microphone permission or
supply audio input. Real capture and permission prompts remain a manual check.

### 4. Stabilization fixes

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

### 5. UX work

- Dashboard: per-section unavailable states, failure banner with retry, honest
  loading placeholders, neutral copy.
- Inventory Operations: rebuilt layout, selected-product context, separated load
  and form errors, snapshot metrics, history table, empty state, mobile support.
- Shell: skip link, 404, error boundary, search feedback, real identity.
- Assistant: floating launcher, suggestion chips, retry, scope note, responsive
  panel.

Details are in `docs/UX_IMPROVEMENTS.md`.

### 6. Demo data

- Added `backend/seed_demo_data.py`, an idempotent seed script that preserves
  existing records and tops up short modules.
- Live workspace now has at least 100 rows in every business module: 100
  categories, 100 products, 100 suppliers, 100 sales orders, 100 purchase
  orders and 143 inventory-history rows.
- Stock movements go through `services/inventory.change_stock`, so sales
  deductions, cancellations and purchase receipts keep stock and history
  consistent.
- `DEMO-` SKUs are used for browser checks; 3 products are out of stock and 11
  are low stock, with no negative stock.

### 7. Test catalog

- `tests/generate_test_cases.py` deterministically builds 2000 distinct
  scenarios across thirteen modules and writes:
  - `tests/test_cases.json`
  - `tests/TEST_CASE_CATALOG.md`
  - `tests/TEST_EXECUTION_REPORT.md`
- Counts are asserted by the generator: Authentication 80, Dashboard 60,
  Products 100, Categories 60, Suppliers 90, Inventory 110, Sales 120, Purchases
  120, Forecasting 80, Assistant 80, Voice Assistant 1000, Navigation 50,
  Security 50.
- Statuses are honest: 80 passed with evidence, 41 blocked with reasons, 1879
  not_run.
- The 1000 voice scenarios are a planning catalog, not 1000 automated tests.
  Fifty-three voice scenarios map exactly to executed browser checks; the rest
  remain not_run or blocked. Voice titles were cleaned so area prefixes are not
  duplicated, and evidence is attached only by exact title match.
- The generator rejects duplicate titles, enforces module counts, rejects
  passed scenarios without evidence and blocked scenarios without a reason.
- Browser evidence used for the catalog:
  - `voice-e2e-results.json`: 41/41 mocked voice checks.
  - `voice-secure-results.json`: 8/8 secure-context checks.
  - `voice-support-results.json`: 4/4 support-detection checks.
  - `assistant-voice-test.cjs`: native assistant language/layout run.
  - `admin-e2e-results.json`: 50/50 administrator checks.

### 8. Documentation

- `docs/PROJECT_AUDIT.md` — architecture, data model, API surface, security
  posture, verification, risks and recommendations.
- `docs/BUG_TRACKER.md` - 22 fixed defects, 12 open issues, blocked verification
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
8. **Role checks come from the database, not the token.** The JWT carries
   identity only. A modified token cannot claim `ADMIN`.
9. **Administrator provisioning is explicit.** No default administrator and no
   hardcoded password. Use `create_admin.py` or the optional environment
   bootstrap, then rotate the generated password if the database is shared.
10. **Voice stays browser-native.** No speech dependency, no stored audio and no
    server-side speech service. Unsupported or insecure browsers keep the typed
    path usable.

## Environment notes

- Frontend dev server: `http://localhost:5173`
- Administrator area: `http://localhost:5173/admin/login` (backend
  `/admin/*`)
- Backend: `http://127.0.0.1:8000` (`/health`, `/docs`)
- Backend tests: `cd backend; .\venv\Scripts\python.exe -m pytest -q`
- Frontend build: `cd frontend; npm run build`
- Administrator provisioning:
  `cd backend; .\venv\Scripts\python.exe create_admin.py --username <name>`
- Browser checks: Puppeteer with Microsoft Edge, scripts kept outside the repo in
  the working environment.
- The backend must be restarted from `backend` after code changes; an old process
  will serve old routes.
- The Vite dev server must be restarted after `vite.config.js` changes.

## Verification evidence

| Check | Evidence |
| --- | --- |
| Backend suite | 62 passed, 1 Starlette deprecation warning |
| Production build | Built successfully; `three.module` 694.91 kB |
| Administrator E2E | 50/50 checks passed in headless Edge; normal users receive 403; all analytics tabs render; no unexpected console errors |
| Administrator API tests | 14 tests in `backend/tests/test_admin.py` |
| Assistant E2E | Desktop and mobile flow passed; console errors none |
| Mocked voice E2E | 41/41 checks passed |
| Secure-context voice E2E | 8/8 checks passed on `http://192.168.1.7:5174` |
| Support-detection voice E2E | 4/4 checks passed |
| Native assistant language/layout | Passed on rerun; Hindi/Bengali welcome, suggestions, live answers, Bengali refusal, Escape close, zero horizontal overflow |
| Dashboard partial failure | Banner shown; products and low-stock data stayed live; sales section unavailable |
| Inventory page | One `main`; form, snapshot and history present |
| Catalog | 2000 unique IDs, 2000 unique titles, no missing steps or expected results |

## Remaining work

1. Commit all work and push to `origin main`.
2. Run a manual microphone-permission and audio-capture check in a real browser
   session; headless Edge cannot exercise the device.
3. After push, run the blocked PostgreSQL concurrency suite in an environment
   that has PostgreSQL.
4. Implement rate limiting and security headers (see `docs/BUG_TRACKER.md`).
5. Add a committed frontend test runner and E2E suite.
6. Recheck the assistant at 320 px, 768 px and 200% zoom; add a tablet pass for
   the purchase-order table.
7. Consider adding product cost data so inventory value can be reported at cost
   as well as at selling price.
8. Rotate the generated development administrator password if the database is
   shared beyond this machine.

## Constraints to preserve

- Do not retrain or replace the forecasting model.
- Do not remove existing business features or discard user changes.
- Do not hardcode demo credentials in production code.
- Do not expose secrets, tokens, passwords or provider keys in logs or responses.
- Keep the assistant strictly scoped to NextGenERP.
- Keep SQLite and PostgreSQL compatibility.
- Mark tests honestly; never fabricate results.
