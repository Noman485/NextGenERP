# NextGenERP Bug Tracker

Date: 2026-11-11
Branch: `main`

Status values: `fixed`, `open`, `blocked`, `accepted`.
Severity values: `critical`, `high`, `medium`, `low`.

## Fixed

| ID | Severity | Area | Symptom | Root cause | Fix | Regression evidence |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-001 | High | Auth | Signed-in shell displayed a hardcoded identity instead of the real account | The shell rendered a static user label and never called `/auth/me` | Fetch the current user after login and render the returned username; clear it on sign-out or 401 | `Login UI: signed-in identity shows the username`; browser check confirmed `demo438765052` |
| BUG-002 | High | Routing | Unknown URLs rendered a blank content area | No catch-all route existed | Added a `NotFound` route and a link back to the dashboard | `404 and error boundary: unknown route shows Page not found` |
| BUG-003 | Medium | Shell | A render error in one page could blank the whole app | No error boundary around routed content | Added `ErrorBoundary` keyed by pathname with a reset action | Backend suite and browser navigation checks |
| BUG-004 | Medium | Dashboard | One failed endpoint blanked every dashboard section | `Promise.allSettled` results were collapsed into a single thrown error | Keep fulfilled collections, track failures per section, render a banner and per-section unavailable states | `Partial loading: sales orders endpoint unavailable`; aborted `/orders/` kept products, counts and low-stock table live |
| BUG-005 | Medium | Inventory | Inventory page nested a second `<main>` landmark | Page component rendered its own `<main>` inside the shell `<main>` | Replaced it with a page-level container and section headings | `UI: page renders inside the app shell without nested main`; exactly one `main` measured |
| BUG-006 | High | Suppliers | Database commit failures returned an unhandled 500 | Create/update/delete paths did not catch `SQLAlchemyError` | Catch commit failures, roll back, return 503 with a safe message | `test_supplier_commit_failures_return_service_unavailable` (POST/PUT/DELETE) |
| BUG-007 | Medium | Sales orders | Updating a customer accepted whitespace-only names and stored untrimmed values | Update route did not normalize or validate the name | Trim name and email; reject blank names with 400; clear email when blank | `test_order_update_trims_customer_fields_and_rejects_blank_name` |
| BUG-008 | Medium | Forecasting | `/ml/insights` generated the forecast twice per request | The route called `generate_forecast()` and the service called it again when no frame was passed | Generate once and pass the frame into the service | `test_ml_insights_generates_forecast_once_and_matches_erp_case_insensitively`; call counter equals 1 |
| BUG-009 | Medium | Forecasting | ERP stock overlay missed products whose catalog name differed only by case | Matching used exact string equality | Match on normalized lowercase names while preserving fallback behavior | Same regression test: `Amul Butter` matched forecast `amul butter` |
| BUG-010 | Low | Search | Header module search gave no feedback when nothing matched | The submit handler silently returned | Added a visible no-match message with a clear action | Browser check of the search field |
| BUG-011 | Medium | Assistant | Chat returned HTTP 404 through the Vite dev server | The proxy allowlist did not include `/assistant` | Added `assistant` to the proxy path regex | Assistant E2E: low-stock and help answers returned live replies |
| BUG-012 | High | Assistant | Launcher and panel did not appear in the browser even though the source contained them | Vite served a stale transform because native file events are unreliable in the OneDrive folder | Enabled `server.watch.usePolling` and restarted the dev server | Assistant E2E: launcher visible, panel opened, desktop and mobile flows passed |
| BUG-013 | Low | Copy | Dashboard described the product as "ML-driven demand signals" | Legacy AI-centric wording | Replaced with "demand forecasts feeding the reorder queue" | Source grep; production build |
| BUG-014 | Low | Assistant | Off-topic questions could reach the optional provider | Scope check was not guaranteed before the LLM bridge | Engine refuses out-of-scope messages before calling the provider; tests assert the refusal path | `test_assistant.py` scope-refusal cases |
| BUG-024 | Medium | Assistant | Hindi/Bengali greetings such as `नमस्ते` and `নমস্কার` were treated as off-topic | The greeting normalizer stripped Devanagari/Bengali combining marks, so the words no longer matched the greeting list | Preserve `U+0900-U+097F` and `U+0980-U+09FF` in `_is_greeting` and add localized greeting tests | `test_assistant_localizes_greeting_and_suggestions`; Hindi/Bengali greetings return the localized intro instead of a refusal |
| BUG-025 | High | Administrator | `/admin/*` API calls returned 404 through the Vite development server | The proxy allowlist regex omitted `admin` | Added `admin` to `apiPaths` in `frontend/vite.config.js` | Administrator E2E: overview, all analytics tabs and user APIs returned 200 |
| BUG-026 | High | Voice | A rapid double-click on the microphone created two recognition sessions | The `starting` React state had not committed before the second click handler ran | Added a synchronous `startingRef` guard and reset it on start failure, stop, error, end and unmount | Mocked voice E2E: rapid double-click created at most one session |
| BUG-027 | Medium | Voice | On an insecure HTTP origin the microphone looked available and could attempt recognition | The UI checked API presence but not `window.isSecureContext` | Detect secure context, disable the microphone with guidance, and refuse to start recognition even if the control is forced | Secure-context E2E: 8/8 checks passed on `http://192.168.1.7:5174` |
| BUG-028 | Medium | Voice | Voices that arrived after mount were missed, and playback could pick an unrelated voice | The voice list was read once and matching used the first available voice | Listen for `voiceschanged`, then select exact locale, same-language, then a safe default | Mocked voice E2E: exact `English India`, `Hindi India` and `Bengali India` voices selected |
| BUG-029 | Medium | Voice | Late recognition results after stop or panel close could still submit a message | Result handlers did not check whether the session was still current | Abort on stop/close and ignore results whose recognition object is no longer current | Mocked voice E2E: late result after stop and after close were both ignored |
| BUG-030 | Medium | Administrator | Legacy demo orders had no timestamps, so daily/monthly analytics were empty | The analytics columns were added after the demo data was created | Added an idempotent backfill that only touches `@example.test` demo rows | Live database: 100 orders spread over the last year; real rows untouched |
| BUG-031 | Medium | Administrator | Existing databases lacked the role, active-status and timestamp columns | The original schema used `create_all` with no migration step | Added additive, idempotent migrations for SQLite and PostgreSQL and called `ensure_schema()` at startup | Live database migrated after a backup; backend suite passes |
| BUG-015 | High | Security | No rate limiting on login, registration or assistant chat | Credential stuffing, spam accounts and LLM cost abuse were possible | Added `security_controls.py` with per-IP, per-account and per-user fixed windows; 429 responses include `Retry-After`; forwarded headers are not trusted | Security suite `SEC-0741`–`SEC-0800` (60/60) |
| BUG-016 | Medium | Security | No Content-Security-Policy or baseline security headers | Stored XSS impact was larger than necessary and framing/MIME sniffing were unrestricted | Added FastAPI header middleware, TLS-only HSTS, and matching nginx headers/CSP for the SPA | Security suite `SEC-0801`–`SEC-0840` (40/40) |

## Open

| ID | Severity | Area | Issue | Impact | Suggested action |
| --- | --- | --- | --- | --- | --- |
| BUG-017 | Medium | Forecasting | Three.js chunk is 694.91 kB and triggers Vite's 500 kB warning | Slower first load on weak networks | Split the chart/warehouse code further or ship a 2D fallback |
| BUG-018 | Medium | Testing | No frontend unit/component test runner | UI regressions depend on ad-hoc browser scripts | Add Vitest + Testing Library and commit the E2E scripts |
| BUG-019 | Medium | Data | Large product and inventory-history lists are not paginated | Rendering cost grows with data volume | Add server-side pagination or virtualization |
| BUG-020 | Low | Auth | Access tokens last 30 minutes with no refresh rotation | Users are signed out abruptly; stolen tokens live up to 30 minutes | Add refresh tokens or a sliding session |
| BUG-021 | Low | Observability | No structured audit log for stock and order mutations | Harder to investigate disputes | Log actor, action, entity and before/after values without secrets |
| BUG-022 | Low | Assistant | Snapshot caps products, suppliers and recent orders | Very large workspaces get partial answers | State the caps in the reply or add targeted lookup tools |
| BUG-023 | Low | Assistant | Documentation retrieval is keyword-based | Some paraphrased questions miss the best doc | Add embeddings or a larger curated topic map |

| BUG-032 | Medium | Administrator | Analytics load and aggregate all orders in Python on each request | Large datasets will make dashboards slow and memory-heavy | Add indexed SQL aggregation or a cached daily rollup |
| BUG-033 | Medium | Administrator | Inventory value is reported at selling price only | The dashboard cannot show cost-based inventory value | Add product cost data and a cost-value view |
| BUG-034 | Low | Administrator | Account activation changes are not audit-logged | Harder to investigate who deactivated an account | Log actor, target, action and timestamp without secrets |

## Blocked verification

| ID | Area | Why blocked | What is needed |
| --- | --- | --- | --- |
| BLK-001 | Inventory/Sales/Purchase concurrency | Tests run on SQLite, where `with_for_update()` is a no-op | PostgreSQL service and concurrent test harness |
| BLK-002 | External LLM provider | No provider key is configured | A test key and a mock/live OpenAI-compatible endpoint |
| BLK-003 | Rate limiting across workers | The limiter is in-process; the single-process behavior is tested, but multiple backend workers would each keep an independent window | Shared counter store (Redis/PostgreSQL) plus a multi-worker load test |
| BLK-004 | Cross-browser E2E | Only headless Edge is installed | Firefox/WebKit runners or Playwright browsers |
| BLK-005 | Voice microphone capture | Headless Edge cannot grant a real microphone permission or supply audio input | Manual or device-farm check with a real microphone |
| BLK-006 | Cross-browser voice | Web Speech support and voice availability differ by browser | Test Firefox/Safari or document supported browsers |
| BLK-007 | Administrator analytics on PostgreSQL | The suite and live database use SQLite; PostgreSQL aggregation and index behavior are unverified | Run the analytics tests and a seeded dataset against PostgreSQL |
| BLK-008 | Concurrent administrator changes | Last-admin protection is tested sequentially, not under two simultaneous deactivation requests | Add a PostgreSQL concurrency test with two administrator sessions |

## Triage rules

1. Any path that can make stock negative or double-add stock is `critical`.
2. Any secret leak or authentication bypass is `critical`.
3. Any unhandled 500 on a normal user action is `high`.
4. Any misleading zero, blank screen or inaccessible control is `medium`.
5. Copy, spacing and non-blocking polish are `low`.

Every fix must add or update a regression test, or record why a test is not
feasible. A bug is not marked fixed until the relevant suite and a browser check
have been rerun.
