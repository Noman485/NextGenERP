# NextGenERP Assistant

The NextGenERP Assistant is an in-app assistant that is deliberately limited to
this application. It answers questions about the workspace and explains how to
use the app. It is **read-only**: it can read live data, but it cannot create,
edit, cancel, receive or delete records.

## What it covers

- Live inventory: stock levels, low-stock items, out-of-stock items, reorder levels.
- Catalog: products, SKUs, prices, categories.
- Suppliers: lead times, ratings, contact details, linked purchase orders.
- Sales orders: counts by status, pending orders, order lookup.
- Purchase orders: open orders, receiving workflow, order lookup.
- Demand forecasting and suggested reorders (explanation only; the model is unchanged).
- Navigation, accounts, common errors and troubleshooting.

The panel and answers are available in **English**, **Hindi** and **Bengali**,
including voice input and spoken replies in browsers that support the Web Speech
API.

Anything outside NextGenERP is refused before any model call is made.

## How it works

```
Browser (Assistant.jsx)
        |
        | POST /assistant/chat  (JWT required)
        v
FastAPI route (routes/assistant.py)
        |
        v
Answer engine (assistant/engine.py)
  |-- project scope check
  |-- live snapshot (assistant/snapshot.py)
  |-- curated help topics (assistant/knowledge.py)
  |-- localization (assistant/localization.py)
  |-- documentation retrieval (assistant/docs.py)
  |-- optional LLM bridge (assistant/llm.py)
```

1. The message is normalized and checked against the NextGenERP domain.
2. The engine builds a read-only snapshot of the current workspace.
3. It looks for a matching help topic and relevant project documentation in the
   selected language.
4. If no LLM is configured, a deterministic localized answer is returned.
5. If an LLM is configured, the engine sends the scope rules, the language
   instruction, the snapshot and the retrieved context to an
   OpenAI-compatible endpoint. If that call fails, the local answer is used
   instead.

The local mode needs no API key, no network access and no additional Python
packages beyond the existing `requests` dependency.

## Languages and voice

| Language | Code | Speech locale | Coverage |
| --- | --- | --- | --- |
| English | `en` | `en-IN` | Panel copy, suggestions, help topics, live answers, refusals |
| Hindi | `hi` | `hi-IN` | Same, with Devanagari script |
| Bengali | `bn` | `bn-IN` | Same, with Bengali script |

- Language-specific copy, keywords, status labels and reply templates live in
  `backend/assistant/localization.py`. Product names, SKUs, order numbers and
  stored status values are not translated.
- The selected language is sent with every request. Changing the language
  clears the current conversation so answers do not mix scripts or context.
- Voice input uses the browser-native `SpeechRecognition` /
  `webkitSpeechRecognition` API. The interim transcript is shown while listening
  and only the final transcript is submitted.
- Microphone input requires a secure context (HTTPS or localhost). On an insecure
  origin the control is disabled with guidance, and typing remains available.
- A 15-second silence timeout stops listening and explains what happened.
- Permission, service, no-speech, audio-capture, network,
  language-not-supported, busy and unknown errors each map to specific localized
  guidance.
- Stop, Escape, close, language change and unmount abort recognition safely.
  Late results after stop or close are ignored, and a synchronous guard prevents
  a rapid double-click from starting two sessions.
- Spoken replies use `speechSynthesis`. Auto-speak is **off by default**; each
  assistant message also has its own play/stop button.
- Voices are loaded again when the browser fires `voiceschanged`. Playback uses
  the exact locale voice when available, then a same-language voice, then a safe
  default.
- No audio is stored or sent to NextGenERP. Browser speech recognition may use
  the browser vendor's speech service, so availability and privacy behavior
  depend on the browser.
- Voice controls are disabled with an explanatory tooltip when the browser does
  not support the API. Typing always remains available.

## Configuration

The assistant works out of the box. To enable an LLM-backed mode, set these
environment variables for the backend process:

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `ASSISTANT_LLM_API_KEY` | No | unset | API key for an OpenAI-compatible provider. `OPENAI_API_KEY` is also accepted. |
| `ASSISTANT_LLM_BASE_URL` | No | `https://api.openai.com/v1` | Base URL of the chat-completions API. |
| `ASSISTANT_LLM_MODEL` | No | `gpt-4o-mini` | Model name sent to the provider. |

Example:

```env
ASSISTANT_LLM_API_KEY=replace-with-your-provider-key
ASSISTANT_LLM_BASE_URL=https://api.openai.com/v1
ASSISTANT_LLM_MODEL=gpt-4o-mini
```

Restart the backend after changing these values. Keys are read from the
environment only; they are never stored in the database, logged or returned to
the browser.

## API

`POST /assistant/chat`

Authentication: `Authorization: Bearer <JWT>` (same session token as the app).

Request:

```json
{
  "message": "Show low-stock products",
  "history": [
    { "role": "user", "content": "hello" },
    { "role": "assistant", "content": "Hi!" }
  ],
  "language": "en"
}
```

- `message` is required, trimmed, 1-1000 characters.
- `history` is optional, at most 10 turns, each content 1-2000 characters.
- Roles are limited to `user` and `assistant`.
- `language` is optional and defaults to `en`; allowed values are `en`, `hi`
  and `bn`. Any other value is rejected with HTTP 422.

Response:

```json
{
  "reply": "Products at or below their reorder level:\n- Butter - Classic (DEMO-0006): 3 units left, reorder level 5",
  "suggestions": ["Show low-stock products", "..."],
  "mode": "local",
  "language": "en"
}
```

`mode` is `local` for the built-in engine and `llm` when a provider answered.
`language` echoes the language used for the reply.

## Privacy and safety

- The assistant only reads data that the signed-in user can already see in the app.
- The LLM prompt contains a trimmed workspace snapshot (up to 40 products, 20
  suppliers and 10 recent sales/purchase orders). Do not enable an external LLM
  provider if workspace data must not leave your network.
- The prompt forbids revealing keys, tokens, passwords, file paths, SQL or model
  weights.
- The assistant cannot mutate data; every write action must be performed by the
  user on the relevant page.
- Answers can be wrong. The panel includes a reminder to verify before acting.

## UI behavior

- Floating **Ask assistant** launcher in the authenticated app shell; the
  launcher text follows the selected language.
- Panel closes with Escape, the close button, or by navigating (the launcher
  remains available on every page).
- Language selector (English / हिन्दी / বাংলা) in the panel header area.
- Microphone button for voice input; the input placeholder shows a listening
  state while recognition is active.
- Auto-speak toggle and a per-message speaker button. Playback stops on close,
  language change, clear, Escape, or when another message starts playing.
- Suggestion chips provide project-specific starting points in the selected
  language.
- Errors show a retry action without losing the conversation; microphone
  permission and recognition errors are reported separately from API errors.
- Mobile layout uses a full-width panel above the bottom edge; desktop uses a
  fixed 24rem panel.
- The message log uses `role="log"`, `aria-live="polite"` and scrolls to the
  latest message.

## Testing

Backend tests: `backend/tests/test_assistant.py`

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest tests\test_assistant.py -q
```

Covered behavior:

- Authentication is required.
- Blank, oversized and over-long history payloads are rejected.
- Greeting stays project-scoped, including Devanagari and Bengali greetings.
- Off-topic questions are refused.
- Low-stock answers use live data.
- Product stock lookup uses live data.
- Pending sales orders are listed from live data.
- Help topics explain how to add a product.
- Catalog counts come from the database.
- A failing LLM provider falls back to local mode.
- A configured LLM receives the strict scope prompt and the key is not leaked.
- Hindi and Bengali greetings return localized intros and suggestions.
- Localized low-stock answers use live data and localized status text.
- Localized help topics and scope refusals work without a provider.
- Unsupported language codes return HTTP 422.
- A configured LLM receives an explicit Hindi/Devanagari language instruction.

The browser flow was verified with Puppeteer scripts on desktop and mobile:

- Existing assistant regression: login, open panel, live low-stock answer, help
  answer, off-topic refusal, close, 404 route, mobile layout, mobile chat and
  Escape close.
- Mocked voice flow: 41/41 checks covering no auto-start, locales, interim
  transcript, single final submission, exact voice selection, stop playback,
  auto-speak, eight error codes, timeout, late results, language switch
  mid-listen, XSS escaping and rapid double-click.
- Secure-context flow: 8/8 checks on a genuinely insecure non-localhost origin.
- Support-detection flow: 4/4 checks for missing recognition and missing
  synthesis.
- Native language/layout flow: Hindi/Bengali welcome, suggestions, live answers,
  Bengali scope refusal, Escape close, 366 × 544 px mobile panel, zero horizontal
  overflow and no console errors.

Real microphone capture and permission prompts cannot be automated in headless
Edge; they remain a manual check.

## Limitations

- Live answers cover the most recent 20 sales orders and 20 purchase orders in
  the snapshot; counts are complete.
- Product and supplier lists are capped for prompt size. The UI remains the
  source of truth for full lists.
- Documentation retrieval is keyword-based and intentionally small.
- The assistant does not stream responses.
- The assistant does not know about data changed after the snapshot is built.
- Voice input and spoken replies depend on browser support. In the test
  environment (headless Edge) the APIs exist, but actual microphone permission
  and audio capture were not automated.
- Recognition accuracy depends on the browser, microphone and selected locale;
  the transcript is sent as-is and can be edited before sending by typing.
- Only `en`, `hi` and `bn` are supported. Mixed-language requests still work in
  local mode for domain terms, but the reply uses the selected language.

## Troubleshooting

- **"Cannot reach the assistant"** — confirm the backend is running and `/health`
  returns `{"status":"ok"}`.
- **HTTP 404 on `/assistant/chat`** — the backend process is running old code.
  Restart it from the `backend` directory.
- **HTTP 401** — the session expired; sign in again.
- **Always local mode** — no provider key is configured, or the provider call
  failed. Check the backend log for the fallback warning.
- **Mic button disabled** — the browser does not expose the Web Speech
  recognition API. Use the text input or a supported browser.
- **"Microphone permission was denied"** — allow microphone access for the site
  in the browser's site settings, then try again.
- **No spoken audio** — the browser may lack a voice for the selected locale.
  Install a system/browser voice for Hindi or Bengali, or use the text answer.
- **Old English replies after switching language** — the backend is running old
  code or the panel was not reloaded. Restart the backend and refresh the page.
- **Vite serves an old UI** — the project lives in a OneDrive folder, so
  `vite.config.js` enables polling. If a change still does not appear, restart
  the dev server.
