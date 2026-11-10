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
| Backend test suite | 48 passed, 1 third-party deprecation warning |
| Frontend production build | Passed; lazy Three.js chunk 694.91 kB (warning only) |
| In-app assistant | Implemented, tested and browser-verified on desktop and mobile |
| Assistant languages and voice | English/Hindi/Bengali localization plus browser voice input/output; verified in headless Edge |
| Dashboard partial loading | Implemented and verified by aborting a request |
| Inventory Operations redesign | Implemented and browser-verified |
| Required documentation | Complete |
| 1000-scenario catalog | Generated: 27 passed, 41 blocked, 932 not_run |
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

### 4. Demo data

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

### 5. Test catalog

- `tests/generate_test_cases.py` deterministically builds 1000 distinct
  scenarios across twelve modules and writes:
  - `tests/test_cases.json`
  - `tests/TEST_CASE_CATALOG.md`
  - `tests/TEST_EXECUTION_REPORT.md`
- Counts are asserted by the generator: Authentication 80, Dashboard 60,
  Products 100, Categories 60, Suppliers 90, Inventory 110, Sales 120, Purchases
  120, Forecasting 80, Assistant 80, Navigation 50, Security 50.
- Statuses are honest: 27 passed with evidence, 41 blocked with reasons, 932
  not_run.
- Assistant coverage includes 9 localization scenarios and 6 voice UI scenarios;
  the two voice environment checks are blocked rather than claimed as passed.
- The generator rejects duplicate titles and enforces module counts.

### 6. Documentation

- `docs/PROJECT_AUDIT.md` — architecture, data model, API surface, security
  posture, verification, risks and recommendations.
- `docs/BUG_TRACKER.md` — 15 fixed defects, 9 open issues, blocked verification
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
| Backend suite | 48 passed, 1 Starlette deprecation warning |
| Production build | Built successfully; `three.module` 694.91 kB |
| Assistant E2E | Desktop and mobile flow passed; console errors none |
| Assistant voice/language E2E | Three language options, mic control, auto-speak, Hindi/Bengali live answers, Bengali refusal, speaker state, mobile layout; console errors none |
| Dashboard partial failure | Banner shown; products and low-stock data stayed live; sales section unavailable |
| Inventory page | One `main`; form, snapshot and history present |
| Catalog | 1000 unique IDs, 1000 unique titles, no missing steps or expected results |

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

## Constraints to preserve

- Do not retrain or replace the forecasting model.
- Do not remove existing business features or discard user changes.
- Do not hardcode demo credentials in production code.
- Do not expose secrets, tokens, passwords or provider keys in logs or responses.
- Keep the assistant strictly scoped to NextGenERP.
- Keep SQLite and PostgreSQL compatibility.
- Mark tests honestly; never fabricate results.
