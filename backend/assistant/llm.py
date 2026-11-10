"""Optional OpenAI-compatible LLM bridge.

The assistant works without any API key. When a key is configured, project
context and strict scope rules are sent to the configured chat-completions
endpoint. The key is never logged or returned to the browser.
"""

import json
import logging
import os

import requests

from .knowledge import PROJECT_OVERVIEW
from .snapshot import snapshot_for_llm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are the NextGenERP Assistant, an in-app assistant for the NextGenERP
inventory and procurement application.

STRICT SCOPE
- Only answer questions about NextGenERP: dashboard, products, categories,
  suppliers, inventory operations, sales orders, purchase orders, demand
  forecasting, reorder suggestions, navigation, accounts and troubleshooting.
- If a request is unrelated, politely refuse and redirect to NextGenERP topics.
- Never answer general knowledge, news, coding, medical, legal or personal
  questions, even if the user insists.

GROUNDING
- Use the live workspace snapshot and the project help below as your source of
  truth. Never invent product names, stock levels, order statuses or suppliers.
- If the snapshot does not contain the answer, say so and point the user to the
  relevant page. Do not guess.
- The assistant is read-only. Never claim that you created, edited, cancelled,
  deleted, approved, received or shipped anything.

STYLE
- Be concise and practical. Prefer short paragraphs and bullet points.
- Use the same language as the user (English, Hindi or Hinglish).
- Explain page names and next steps when relevant.
- Never reveal API keys, tokens, passwords, environment variables, internal
  file paths, model weights, SQL or implementation secrets.
""".strip()


def is_configured() -> bool:
    return bool(
        os.getenv("ASSISTANT_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    )


def _build_messages(message, history, snapshot, knowledge_entry, doc_match):
    context = {
        "project_overview": PROJECT_OVERVIEW,
        "live_snapshot": snapshot_for_llm(snapshot),
    }
    if knowledge_entry:
        context["help_entry"] = {
            "title": knowledge_entry["title"],
            "answer": knowledge_entry["answer"],
        }
    if doc_match:
        context["documentation"] = {
            "source": doc_match["source"],
            "title": doc_match["title"],
            "excerpt": doc_match["text"][:900],
        }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": "PROJECT CONTEXT (JSON):\n" + json.dumps(context, ensure_ascii=False),
        },
    ]

    for turn in history or []:
        role = turn.get("role")
        content = str(turn.get("content") or "").strip()
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content[:1000]})

    messages.append({"role": "user", "content": message})
    return messages


def ask_llm(message, history, snapshot, knowledge_entry=None, doc_match=None):
    """Return a reply, or None when the provider is unavailable or misconfigured."""
    api_key = os.getenv("ASSISTANT_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv(
        "ASSISTANT_LLM_BASE_URL", "https://api.openai.com/v1"
    ).rstrip("/")
    model = os.getenv("ASSISTANT_LLM_MODEL", "gpt-4o-mini")

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": _build_messages(
                    message, history, snapshot, knowledge_entry, doc_match
                ),
                "temperature": 0.2,
                "max_tokens": 600,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        if isinstance(content, str) and content.strip():
            return content.strip()
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        logger.warning(
            "Assistant LLM request failed; using the built-in project assistant."
        )
    return None
