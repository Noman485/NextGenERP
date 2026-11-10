"""Small, dependency-free retrieval over the project's own documentation."""

import math
import re
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DOCUMENTS = {"deployment.md", "blender-mcp.md"}
SENSITIVE_MARKERS = ("jwt_secret", "postgres_password", "secret_key", "password=")
STOP_WORDS = {
    "the", "and", "for", "with", "this", "that", "from", "are", "was", "were",
    "has", "have", "had", "not", "but", "you", "your", "our", "can", "will",
    "into", "when", "what", "how", "why", "where", "which", "who", "all", "any",
    "use", "using", "used", "its", "their", "they", "them", "then", "than",
    "also", "such", "only", "more", "most", "some", "each", "other", "about",
}


def _tokenize(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]{3,}", value.lower())
        if token not in STOP_WORDS
    }


def _read_chunks() -> list[dict]:
    candidates = [REPO_ROOT / "README.md"]
    docs_dir = REPO_ROOT / "docs"
    if docs_dir.exists():
        candidates.extend(sorted(docs_dir.glob("*.md")))

    chunks = []
    for path in candidates:
        if not path.exists() or path.name in SKIP_DOCUMENTS:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        current_title = path.stem.replace("-", " ").title()
        current_lines = []

        def flush():
            text = "\n".join(current_lines).strip()
            lowered = text.lower()
            if (
                len(text) >= 80
                and not any(marker in lowered for marker in SENSITIVE_MARKERS)
            ):
                chunks.append(
                    {
                        "source": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                        "title": current_title,
                        "text": text[:1400],
                        "tokens": _tokenize(text),
                    }
                )

        for line in content.splitlines():
            if line.startswith("## "):
                flush()
                current_title = line[3:].strip()
                current_lines = [line]
            elif line.startswith("# "):
                current_title = line[2:].strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        flush()

    return chunks


@lru_cache(maxsize=1)
def _chunk_cache() -> tuple[dict, ...]:
    return tuple(_read_chunks())


def search_docs(message: str):
    """Return the best matching documentation chunk, or None."""
    query_tokens = _tokenize(message)
    if not query_tokens:
        return None

    best = None
    best_score = 0.0

    for chunk in _chunk_cache():
        overlap = query_tokens & chunk["tokens"]
        if not overlap:
            continue
        score = len(overlap) / math.sqrt(len(chunk["tokens"]) + 1)
        if score > best_score:
            best_score = score
            best = chunk

    if best is None or best_score < 0.09:
        return None
    return best
