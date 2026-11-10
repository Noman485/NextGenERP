# NextGenERP Test Execution Report

Date: 2026-11-11

## Executive summary

- Catalog scenarios: **1000**
- Executed and passed: **27**
- Not yet executed: **932**
- Blocked: **41**
- Automated backend suite: **48 passed** (1 third-party deprecation warning).
- Frontend production build: **passed**; one chunk-size warning for the lazy Three.js bundle.
- Assistant browser flow: **passed** on desktop and mobile with no console errors.
- Assistant voice/language flow: **passed** in headless Edge for the three language options, mic control, auto-speak, localized Hindi/Bengali answers, Bengali refusal, speaker state and mobile layout; real microphone capture remains blocked.
- Dashboard partial-failure check: **passed**; an aborted sales-orders request did not blank the other sections.
- Inventory Operations browser check: **passed**; one main landmark, form, snapshot, and history rendered.

## Commands actually run

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest -q
# 48 passed, 1 warning

cd ..\frontend
npm run build
# built successfully; three.module chunk is 694.91 kB
```

Browser checks used Puppeteer with Microsoft Edge against `http://localhost:5173` and the live backend on `http://127.0.0.1:8000`.
The assistant voice/language script also checked the three language options, mic control state, auto-speak, localized live answers, refusal, speaker state and mobile layout.

## Executed scenarios

| ID | Scenario | Evidence |
| --- | --- | --- |
| TC-0071 | Login UI: valid credentials sign in | Puppeteer assistant-test.cjs, 2026-11-11: login and authenticated shell rendered. |
| TC-0072 | Login UI: signed-in identity shows the username | Puppeteer assistant-test.cjs, 2026-11-11: identity showed demo438765052 and no hardcoded Ops Admin. |
| TC-0109 | Partial loading: sales orders endpoint unavailable | Puppeteer stabilization-check.cjs, 2026-11-11: orders aborted; products, categories, low-stock table and counts still rendered; sales cards showed Unavailable right now. |
| TC-0456 | UI: page renders inside the app shell without nested main | Puppeteer stabilization-check.cjs, 2026-11-11: exactly one main landmark; form, snapshot and history rendered. |
| TC-0457 | UI: stock history table renders rows | Puppeteer stabilization-check.cjs, 2026-11-11: Stock History showed three seeded movements with product, type, quantity and stock values. |
| TC-0870 | UI: launcher is visible | Puppeteer assistant-test.cjs, 2026-11-11: launcher visible on desktop and mobile. |
| TC-0871 | UI: panel opens | Puppeteer assistant-test.cjs, 2026-11-11: panel opened from the launcher. |
| TC-0872 | UI: panel closes | Puppeteer assistant-test.cjs, 2026-11-11: close button removed the panel. |
| TC-0873 | UI: low-stock suggestion returns live answer | Puppeteer assistant-test.cjs, 2026-11-11: low-stock reply contained live DEMO- products. |
| TC-0874 | UI: help suggestion returns steps | Puppeteer assistant-test.cjs, 2026-11-11: add-product help returned step-by-step instructions. |
| TC-0875 | UI: off-topic question is refused | Puppeteer assistant-test.cjs, 2026-11-11: off-topic request returned the scope refusal. |
| TC-0876 | UI: mobile panel fits viewport | Puppeteer assistant-test.cjs, 2026-11-11: 390 px viewport, panel inside the viewport, zero horizontal overflow. |
| TC-0877 | UI: Escape closes panel | Puppeteer assistant-test.cjs, 2026-11-11: Escape removed the panel. |
| TC-0878 | Localization: Hindi greeting returns a localized intro and suggestions | pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_greeting_and_suggestions returned language=hi with a Devanagari intro and suggestions. |
| TC-0879 | Localization: Bengali greeting returns a localized intro and suggestions | pytest backend/tests/test_assistant.py, 2026-11-11: same test returned language=bn with a Bengali intro and suggestions. |
| TC-0880 | Localization: Devanagari combining-mark greeting is recognized | pytest backend/tests/test_assistant.py, 2026-11-11: 'नमस्ते' returned the intro after _is_greeting preserved U+0900-U+097F combining marks. |
| TC-0881 | Localization: Hindi live low-stock answer is localized | pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_live_low_stock_answers returned a Devanagari reply containing the live Hindi Widget record. |
| TC-0882 | Localization: Bengali live low-stock answer is localized | pytest backend/tests/test_assistant.py, 2026-11-11: same test returned a Bengali reply containing the live Hindi Widget record. |
| TC-0883 | Localization: localized help topic answer | pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_help_and_scope_refusal returned Hindi and Bengali add-product steps with SKU guidance. |
| TC-0884 | Localization: localized scope refusal in Hindi and Bengali | pytest backend/tests/test_assistant.py, 2026-11-11: Hindi refusal contained 'केवल NextGenERP'; Bengali refusal contained 'শুধু NextGenERP'. |
| TC-0885 | Localization: unsupported language code is rejected | pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_rejects_unsupported_language returned 422 for language=fr. |
| TC-0886 | Localization: LLM receives an explicit language instruction | pytest backend/tests/test_assistant.py, 2026-11-11: mocked provider payload contained 'Hindi using Devanagari script'; response mode=llm, language=hi. |
| TC-0887 | Voice UI: language selector lists English, Hindi and Bengali | Puppeteer assistant-voice-test.cjs, 2026-11-11: options were en/English, hi/हिन्दी and bn/বাংলা. |
| TC-0888 | Voice UI: language switch updates welcome and suggestions | Puppeteer assistant-voice-test.cjs, 2026-11-11: Hindi and Bengali welcome text and suggestion chips appeared after switching; the launcher kept the Bengali label after close. |
| TC-0889 | Voice UI: microphone control is enabled when supported | Puppeteer assistant-voice-test.cjs, 2026-11-11: headless Edge reported recognition=true and the mic button was enabled; actual audio capture was not exercised. |
| TC-0890 | Voice UI: speaker play/stop and auto-speak toggle | Puppeteer assistant-voice-test.cjs, 2026-11-11: auto-speak toggled on/off and the speaker button changed to the stop state; no console errors. |
| TC-0927 | 404 and error boundary: unknown route shows Page not found | Puppeteer assistant-test.cjs, 2026-11-11: /does-not-exist rendered Page not found. |

## Blocked scenarios

| Count | Area | Reason |
| ---: | --- | --- |
| 8 | Inventory Operations / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite treats with_for_update() as a no-op. |
| 8 | Sales Orders / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently. |
| 12 | Purchase Orders / Concurrency | PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently. |
| 5 | NextGenERP Assistant / LLM external provider | No external provider key is configured in this environment; the local fallback path is tested instead. |
| 1 | NextGenERP Assistant / Voice UI | Headless Edge cannot grant a real microphone permission or provide audio input; only the controls and error paths were verified. |
| 1 | NextGenERP Assistant / Voice UI | Only headless Microsoft Edge is available; Firefox and Safari Web Speech behavior is not tested. |
| 6 | Security and API / Rate limiting | Rate limiting is not implemented in this build; the scenario is blocked until the control exists. |

## Honest status notes

- The 1000 scenarios are distinct test intents, not 1000 automated tests. Only the rows marked `passed` were executed.
- The backend suite covers 48 tests; it is not mapped one-to-one to catalog IDs, so no bulk pass status was inferred.
- `blocked` means the capability or environment is missing, not that the test failed.
- No result in this report was fabricated or copied from an earlier run.

## Known gaps

- PostgreSQL-specific concurrency and locking paths are blocked in this SQLite-based test environment.
- External LLM provider success, timeout, 401, 429, and custom-base-URL paths are blocked without a provider key.
- Rate limiting is not implemented, so those security scenarios are blocked.
- Real microphone capture and permission prompts cannot be exercised in headless Edge; only the controls and language payloads were verified.
- Cross-browser Web Speech behavior is not tested; only Microsoft Edge is available.
- Frontend unit tests and a permanent cross-browser E2E suite are not configured.
- The Three.js chunk remains above Vite's 500 kB warning threshold.
