# NextGenERP Test Execution Report

Date: 2026-11-11

## Executive summary

- Catalog scenarios: **2000**
- Executed and passed: **80**
- Not yet executed: **1879**
- Blocked: **41**
- Automated backend suite: **62 passed** (1 third-party deprecation warning).
- Frontend production build: **passed**; one chunk-size warning for the lazy Three.js bundle.
- Voice-focused catalog module: **1000 additional scenarios** covering support detection, permission and recognition errors, locale coverage, lifecycle, transcripts, request payloads, speech synthesis, auto-speak, accessibility, privacy, responsive layout and reliability.
- Assistant browser flow: **passed** on desktop and mobile with no console errors.
- Mocked voice E2E: **41/41 passed**; secure-context E2E: **8/8 passed**; support-detection E2E: **4/4 passed**.
- Native assistant language/layout flow: **passed** on rerun for Hindi/Bengali welcome, suggestions, live answers, Bengali refusal, Escape close and 390 px layout; real microphone capture remains blocked.
- Administrator browser E2E: **50/50 passed**, including normal-user 403, all seven analytics tabs, user deactivation/reactivation, 390 px layout and no unexpected console errors.
- Dashboard partial-failure check: **passed**; an aborted sales-orders request did not blank the other sections.
- Inventory Operations browser check: **passed**; one main landmark, form, snapshot, and history rendered.

## Commands actually run

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest -q
# 62 passed, 1 warning

cd ..\frontend
npm run build
# built successfully; three.module chunk is 694.91 kB
```

Browser checks used Puppeteer with Microsoft Edge against `http://localhost:5173` and the live backend on `http://127.0.0.1:8000`.
The voice suites covered mocked speech APIs, a genuinely insecure origin, missing recognition/synthesis and the native language/layout flow. The administrator suite covered authorization, analytics and account activation.

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
| TC-0901 | Support detection: Microsoft Edge with standard SpeechRecognition present | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: SpeechRecognition and speechSynthesis mocks were installed in headless Edge and the microphone control was enabled. |
| TC-0903 | Support detection: Microsoft Edge with SpeechRecognition absent | Puppeteer support-detection E2E (voice-support-results.json), 2026-11-11, 4/4 checks passed: removing recognition disabled only the microphone; speaker and auto-speak controls stayed enabled. |
| TC-0904 | Support detection: Microsoft Edge with insecure HTTP origin | Puppeteer secure-context E2E (voice-secure-results.json), 2026-11-11, 8/8 checks passed: http://192.168.1.7:5174 was a genuinely insecure origin; the microphone was disabled with secure-connection guidance and no recognition session was created. |
| TC-0956 | Permission and errors: recognition error: not-allowed after switching to Hindi | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a Hindi permission denial showed the Hindi microphone-permission guidance. |
| TC-0997 | Permission and errors: recognition error: network after switching to Bengali | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a Bengali network error showed the Bengali connection guidance. |
| TC-1031 | Locale coverage: locale: en-IN recognition language assignment | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: recognition.lang was en-IN. |
| TC-1032 | Locale coverage: locale: en-IN speech synthesis language assignment | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.lang was en-IN. |
| TC-1033 | Locale coverage: locale: en-IN exact voice match | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.voice was 'English India' for en-IN. |
| TC-1036 | Locale coverage: locale: en-IN localized welcome text | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the English welcome rendered in the conversation log. |
| TC-1037 | Locale coverage: locale: en-IN localized suggestion chips | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the English suggestion chip 'What should I reorder?' was clickable and produced an answer. |
| TC-1039 | Locale coverage: locale: hi-IN recognition language assignment | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: recognition.lang was hi-IN after selecting Hindi. |
| TC-1040 | Locale coverage: locale: hi-IN speech synthesis language assignment | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.lang was hi-IN. |
| TC-1041 | Locale coverage: locale: hi-IN exact voice match | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.voice was 'Hindi India' for hi-IN. |
| TC-1044 | Locale coverage: locale: hi-IN localized welcome text | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the Hindi welcome (नमस्ते) rendered after switching language. |
| TC-1045 | Locale coverage: locale: hi-IN localized suggestion chips | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: the Hindi suggestion chip was present and clickable. |
| TC-1048 | Locale coverage: locale: bn-IN speech synthesis language assignment | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.lang was bn-IN. |
| TC-1049 | Locale coverage: locale: bn-IN exact voice match | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: utterance.voice was 'Bengali India' for bn-IN. |
| TC-1052 | Locale coverage: locale: bn-IN localized welcome text | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: the Bengali welcome rendered after switching language. |
| TC-1053 | Locale coverage: locale: bn-IN localized suggestion chips | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: the Bengali suggestion chip was present and clickable. |
| TC-1054 | Locale coverage: locale: bn-IN localized scope refusal | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: a Bengali out-of-scope question returned the localized scope refusal. |
| TC-1113 | Recognition lifecycle: click the microphone while actively listening | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a second microphone click stopped the active session. |
| TC-1123 | Recognition lifecycle: click stop listening while actively listening | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the active control was labelled Stop listening and clicking it aborted the session. |
| TC-1133 | Recognition lifecycle: press Escape while actively listening | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: Escape closed the panel and aborted the active recognition session. |
| TC-1153 | Recognition lifecycle: switch language while actively listening | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: selecting Hindi mid-listen aborted recognition. |
| TC-1171 | Recognition lifecycle: submit a typed message while idle | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a typed question submitted and rendered a reply while the assistant was idle. |
| TC-1181 | Recognition lifecycle: toggle auto-speak while idle | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: auto-speak toggled on and off while idle. |
| TC-1218 | Transcript handling: a single final result with an HTML tag | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a single final result containing a script tag was rendered as text; no script executed and no script element appeared. |
| TC-1312 | Voice request payload: message field — a voice question | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the POST /assistant/chat message equalled the final voice transcript. |
| TC-1342 | Voice request payload: language en — a voice question | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the POST /assistant/chat language field was 'en'. |
| TC-1411 | Speech synthesis: play a reply: voices already loaded | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the speaker button played the reply with loaded voices. |
| TC-1414 | Speech synthesis: play a reply: English selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: English playback used the en-IN utterance locale. |
| TC-1415 | Speech synthesis: play a reply: Hindi selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: Hindi playback used the hi-IN utterance locale. |
| TC-1416 | Speech synthesis: play a reply: Bengali selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: Bengali playback used the bn-IN utterance locale. |
| TC-1420 | Speech synthesis: play a reply: a language change mid-playback | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: switching language during Bengali playback cancelled speech. |
| TC-1421 | Speech synthesis: stop playback: voices already loaded | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: Stop playback cancelled speech and reset the speaker control. |
| TC-1471 | Speech synthesis: exact voice match: voices already loaded | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the exact 'English India' voice was selected with voices loaded. |
| TC-1474 | Speech synthesis: exact voice match: English selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the exact 'English India' voice was selected for en-IN. |
| TC-1475 | Speech synthesis: exact voice match: Hindi selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the exact 'Hindi India' voice was selected for hi-IN. |
| TC-1476 | Speech synthesis: exact voice match: Bengali selected | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the exact 'Bengali India' voice was selected for bn-IN. |
| TC-1528 | Auto-speak: auto-speak enabled on a suggestion click | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: auto-speak played the answer produced by a suggestion click. |
| TC-1531 | Auto-speak: auto-speak disabled again on a text reply | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: after disabling auto-speak, a typed question produced no playback. |
| TC-1643 | Accessibility: Escape close in keyboard-only use | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the Escape key closed the panel and aborted listening without a pointer. |
| TC-1686 | Voice privacy: XSS transcript is escaped on first load | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a script tag in a transcript did not execute and produced no script element. |
| TC-1714 | Voice privacy: microphone never auto-starts on first load | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: opening the panel created zero recognition sessions. |
| TC-1734 | Responsive layout: 390 px width — panel fits | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: the mobile panel box was 366x544 at left 12/top 288 inside a 390x844 viewport. |
| TC-1735 | Responsive layout: 390 px width — no horizontal overflow | Puppeteer native assistant test (assistant-voice-test.cjs), 2026-11-11, console run: mobile horizontal overflow measured 0 px. |
| TC-1781 | Reliability: rapid double-click on the microphone on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a rapid double-click created at most one recognition session after the synchronous startingRef guard was added. |
| TC-1791 | Reliability: start while already starting on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the second start was refused and only one recognition session existed. |
| TC-1811 | Reliability: a result arrives after stop on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a late final result after stop was ignored and sent no chat request. |
| TC-1821 | Reliability: a result arrives after close on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a late final result after Escape close was ignored. |
| TC-1831 | Reliability: the 15-second timeout fires on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: the timeout path fired and stopped recognition; the harness shortened the 15,000 ms constant to 350 ms to keep the run fast. |
| TC-1851 | Reliability: the network drops mid-listen on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a network error during listening cleared the listening state and showed localized guidance. |
| TC-1861 | Reliability: the language changes mid-listen on the first occurrence | Puppeteer mocked voice E2E (voice-e2e-results.json), 2026-11-11, 41/41 checks passed: a language switch during listening aborted recognition. |
| TC-1927 | 404 and error boundary: unknown route shows Page not found | Puppeteer assistant-test.cjs, 2026-11-11: /does-not-exist rendered Page not found. |

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

- The 2000 scenarios are distinct test intents, not 2000 automated tests. Only the rows marked `passed` were executed.
- The backend suite covers 62 tests; it is not mapped one-to-one to catalog IDs, so no bulk pass status was inferred.
- The 1000 new voice scenarios were not bulk-marked as passed; they remain `not_run` until the described browser state is exercised and evidence is recorded.
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
