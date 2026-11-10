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
  |-- documentation retrieval (assistant/docs.py)
  |-- optional LLM bridge (assistant/llm.py)
```

1. The message is normalized and checked against the NextGenERP domain.
2. The engine builds a read-only snapshot of the current workspace.
3. It looks for a matching help topic and relevant project documentation.
4. If no LLM is configured, a deterministic local answer is returned.
5. If an LLM is configured, the engine sends the scope rules, the snapshot and
   the retrieved context to an OpenAI-compatible endpoint. If that call fails,
   the local answer is used instead.

The local mode needs no API key, no network access and no additional Python
packages beyond the existing `requests` dependency.

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
  ]
}
```

- `message` is required, trimmed, 1-1000 characters.
- `history` is optional, at most 10 turns, each content 1-2000 characters.
- Roles are limited to `user` and `assistant`.

Response:

```json
{
  "reply": "Products at or below their reorder level:\n- amul butter (5): 5 units left, reorder level 5",
  "suggestions": ["Show low-stock products", "..."],
  "mode": "local"
}
```

`mode` is `local` for the built-in engine and `llm` when a provider answered.

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

- Floating **Ask assistant** launcher in the authenticated app shell.
- Panel closes with Escape, the close button, or by navigating (the launcher
  remains available on every page).
- Suggestion chips provide project-specific starting points.
- Errors show a retry action without losing the conversation.
- Mobile layout uses a full-width panel above the bottom edge; desktop uses a
  fixed 24rem panel.
- The message log uses `role="log"` and `aria-live="polite"`.

## Testing

Backend tests: `backend/tests/test_assistant.py`

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest tests\test_assistant.py -q
```

Covered behavior:

- Authentication is required.
- Blank, oversized and over-long history payloads are rejected.
- Greeting stays project-scoped.
- Off-topic questions are refused.
- Low-stock answers use live data.
- Product stock lookup uses live data.
- Pending sales orders are listed from live data.
- Help topics explain how to add a product.
- Catalog counts come from the database.
- A failing LLM provider falls back to local mode.
- A configured LLM receives the strict scope prompt and the key is not leaked.

The browser flow was verified with a Puppeteer smoke test: login, open panel,
low-stock answer, help answer, off-topic refusal, close, 404 route, mobile
layout, mobile chat and Escape close. The test finished with no console errors.

## Limitations

- Live answers cover the most recent 20 sales orders and 20 purchase orders in
  the snapshot; counts are complete.
- Product and supplier lists are capped for prompt size. The UI remains the
  source of truth for full lists.
- Documentation retrieval is keyword-based and intentionally small.
- The assistant does not stream responses.
- The assistant does not know about data changed after the snapshot is built.

## Troubleshooting

- **"Cannot reach the assistant"** — confirm the backend is running and `/health`
  returns `{"status":"ok"}`.
- **HTTP 404 on `/assistant/chat`** — the backend process is running old code.
  Restart it from the `backend` directory.
- **HTTP 401** — the session expired; sign in again.
- **Always local mode** — no provider key is configured, or the provider call
  failed. Check the backend log for the fallback warning.
- **Vite serves an old UI** — the project lives in a OneDrive folder, so
  `vite.config.js` enables polling. If a change still does not appear, restart
  the dev server.
