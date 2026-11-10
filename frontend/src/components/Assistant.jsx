import { useEffect, useRef, useState } from 'react';
import { apiFetch } from '../api';
import { Icon } from './Icons';

const INITIAL_SUGGESTIONS = [
  'Show low-stock products',
  'What are the pending sales orders?',
  'How do I add a product?',
  'What should I reorder?',
];

const WELCOME_MESSAGE = {
  role: 'assistant',
  content:
    "Hi! I'm the NextGenERP Assistant. I can answer questions about this workspace using live inventory, order and supplier data. I only cover NextGenERP topics.",
};

function getErrorMessage(data, fallback) {
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail.map((issue) => issue.msg).filter(Boolean).join(' ');
  }
  return fallback;
}

export default function Assistant() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [suggestions, setSuggestions] = useState(INITIAL_SUGGESTIONS);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const [lastAttempt, setLastAttempt] = useState(null);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  useEffect(() => {
    if (open) endRef.current?.scrollIntoView({ block: 'nearest' });
  }, [messages, sending, open]);

  useEffect(() => {
    if (!open) return undefined;

    function handleKeyDown(event) {
      if (event.key === 'Escape') setOpen(false);
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  async function requestReply(content, history) {
    setSending(true);
    setError('');
    setLastAttempt({ content, history });

    try {
      const response = await apiFetch('/assistant/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, history }),
      });
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          getErrorMessage(
            data,
            `The assistant could not answer right now (HTTP ${response.status}).`,
          ),
        );
      }

      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: data.reply || 'I could not generate an answer for that.',
        },
      ]);
      if (Array.isArray(data.suggestions) && data.suggestions.length) {
        setSuggestions(data.suggestions);
      }
      setLastAttempt(null);
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? 'Cannot reach the assistant. Check that the backend is running.'
          : requestError.message,
      );
    } finally {
      setSending(false);
    }
  }

  function submitContent(rawContent) {
    const content = rawContent.trim();
    if (!content || sending) return;

    const history = messages.slice(-8).map(({ role, content: text }) => ({
      role,
      content: text,
    }));

    setMessages((current) => [...current, { role: 'user', content }]);
    setInput('');
    requestReply(content, history);
  }

  function handleSubmit(event) {
    event.preventDefault();
    submitContent(input);
  }

  function retry() {
    if (lastAttempt && !sending) {
      requestReply(lastAttempt.content, lastAttempt.history);
    }
  }

  function clearChat() {
    setMessages([WELCOME_MESSAGE]);
    setSuggestions(INITIAL_SUGGESTIONS);
    setInput('');
    setError('');
    setLastAttempt(null);
  }

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-expanded="false"
        aria-controls="assistant-panel"
        className="fixed bottom-4 right-4 z-40 inline-flex items-center gap-2 rounded-full bg-stone-900 py-2.5 pl-2.5 pr-4 text-sm font-semibold text-white shadow-[0_18px_40px_-18px_rgba(28,25,23,0.9)] transition hover:bg-stone-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-teal-300 to-emerald-400 text-[#06201d]">
          <Icon name="spark" size={16} />
        </span>
        <span className="hidden sm:inline">Ask assistant</span>
        <span className="sr-only sm:hidden">Open NextGenERP Assistant</span>
      </button>
    );
  }

  return (
    <section
      id="assistant-panel"
      aria-label="NextGenERP Assistant"
      className="fixed inset-x-3 bottom-3 z-50 flex h-[min(34rem,calc(100vh-1.5rem))] flex-col overflow-hidden rounded-2xl border border-stone-200 bg-[#fffdf9] shadow-[0_30px_80px_-30px_rgba(28,25,23,0.7)] sm:inset-x-auto sm:bottom-5 sm:right-5 sm:w-[24rem]"
    >
      <header className="flex items-center gap-3 border-b border-stone-200 bg-gradient-to-r from-[#12181a] via-[#0f1517] to-[#0b1112] px-4 py-3 text-stone-100">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-400/15 text-teal-200">
          <Icon name="spark" size={17} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold tracking-tight">NextGenERP Assistant</p>
          <p className="truncate text-[10px] text-stone-400">Project help and live workspace data</p>
        </div>
        <button
          type="button"
          onClick={clearChat}
          className="rounded-md px-2 py-1 text-[10px] font-medium text-stone-400 transition hover:bg-white/10 hover:text-white"
        >
          Clear
        </button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          aria-label="Close assistant"
          className="rounded-md p-1.5 text-stone-400 transition hover:bg-white/10 hover:text-white"
        >
          <Icon name="close" size={16} />
        </button>
      </header>

      <div
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        className="flex-1 space-y-3 overflow-y-auto px-4 py-4"
      >
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
                message.role === 'user'
                  ? 'rounded-br-md bg-teal-700 text-white'
                  : 'rounded-bl-md border border-stone-200 bg-white text-stone-700'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex justify-start">
            <div className="flex items-center gap-1.5 rounded-2xl rounded-bl-md border border-stone-200 bg-white px-3.5 py-3 text-stone-500">
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.2s]" />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.1s]" />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400" />
              <span className="sr-only">Assistant is thinking</span>
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {error && (
        <div
          role="alert"
          className="mx-3 mb-2 flex items-start justify-between gap-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-800"
        >
          <span>{error}</span>
          {lastAttempt && (
            <button
              type="button"
              onClick={retry}
              className="shrink-0 font-semibold underline decoration-rose-300 underline-offset-2 hover:decoration-rose-600"
            >
              Retry
            </button>
          )}
        </div>
      )}

      {!sending && suggestions.length > 0 && (
        <div className="flex flex-wrap gap-1.5 border-t border-stone-100 px-3 pt-2.5">
          {suggestions.slice(0, 4).map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => submitContent(suggestion)}
              className="rounded-full border border-stone-200 bg-stone-50 px-2.5 py-1 text-[11px] font-medium text-stone-600 transition hover:border-teal-300 hover:bg-teal-50 hover:text-teal-800"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit} className="border-t border-stone-200 p-3">
        <div className="flex items-end gap-2">
          <input
            ref={inputRef}
            value={input}
            onChange={(event) => setInput(event.target.value)}
            maxLength={1000}
            placeholder="Ask about stock, orders, suppliers..."
            aria-label="Message the NextGenERP Assistant"
            className="min-w-0 flex-1 rounded-lg border border-stone-300 bg-white px-3 py-2.5 text-sm text-stone-800 outline-none placeholder:text-stone-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            aria-label="Send message"
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-stone-900 text-white transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Icon name="send" size={16} />
          </button>
        </div>
        <p className="mt-2 text-[10px] leading-snug text-stone-400">
          Only NextGenERP topics. Answers use live workspace data and can be wrong; verify before acting.
        </p>
      </form>
    </section>
  );
}
