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

## Open

| ID | Severity | Area | Issue | Impact | Suggested action |
| --- | --- | --- | --- | --- | --- |
| BUG-015 | High | Security | No rate limiting on login, registration or assistant chat | Credential stuffing, spam accounts and LLM cost abuse are possible | Add per-IP and per-account limits with 429 responses and tests |
| BUG-016 | Medium | Security | No Content-Security-Policy header | Stored XSS impact is larger than necessary | Add CSP and baseline security headers in FastAPI middleware |
| BUG-017 | Medium | Forecasting | Three.js chunk is 694.91 kB and triggers Vite's 500 kB warning | Slower first load on weak networks | Split the chart/warehouse code further or ship a 2D fallback |
| BUG-018 | Medium | Testing | No frontend unit/component test runner | UI regressions depend on ad-hoc browser scripts | Add Vitest + Testing Library and commit the E2E scripts |
| BUG-019 | Medium | Data | Large product and inventory-history lists are not paginated | Rendering cost grows with data volume | Add server-side pagination or virtualization |
| BUG-020 | Low | Auth | Access tokens last 30 minutes with no refresh rotation | Users are signed out abruptly; stolen tokens live up to 30 minutes | Add refresh tokens or a sliding session |
| BUG-021 | Low | Observability | No structured audit log for stock and order mutations | Harder to investigate disputes | Log actor, action, entity and before/after values without secrets |
| BUG-022 | Low | Assistant | Snapshot caps products, suppliers and recent orders | Very large workspaces get partial answers | State the caps in the reply or add targeted lookup tools |
| BUG-023 | Low | Assistant | Documentation retrieval is keyword-based | Some paraphrased questions miss the best doc | Add embeddings or a larger curated topic map |

## Blocked verification

| ID | Area | Why blocked | What is needed |
| --- | --- | --- | --- |
| BLK-001 | Inventory/Sales/Purchase concurrency | Tests run on SQLite, where `with_for_update()` is a no-op | PostgreSQL service and concurrent test harness |
| BLK-002 | External LLM provider | No provider key is configured | A test key and a mock/live OpenAI-compatible endpoint |
| BLK-003 | Rate limiting | The control does not exist yet | Implement BUG-015 first |
| BLK-004 | Cross-browser E2E | Only headless Edge is installed | Firefox/WebKit runners or Playwright browsers |
| BLK-005 | Voice microphone capture | Headless Edge cannot grant a real microphone permission or supply audio input | Manual or device-farm check with a real microphone |
| BLK-006 | Cross-browser voice | Web Speech support and voice availability differ by browser | Test Firefox/Safari or document supported browsers |

## Triage rules

1. Any path that can make stock negative or double-add stock is `critical`.
2. Any secret leak or authentication bypass is `critical`.
3. Any unhandled 500 on a normal user action is `high`.
4. Any misleading zero, blank screen or inaccessible control is `medium`.
5. Copy, spacing and non-blocking polish are `low`.

Every fix must add or update a regression test, or record why a test is not
feasible. A bug is not marked fixed until the relevant suite and a browser check
have been rerun.
