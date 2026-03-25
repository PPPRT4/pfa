import React, { useState, useEffect, useRef } from "react";
import { callChatAPI } from "../utils/chatApi";

/* ── Icons ── */
const IconBrain = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 28 28" fill="none">
    <path
      d="M7 10c0-3.87 3.13-7 7-7s7 3.13 7 7c0 .4-.03.8-.1 1.17C22.38 11.9 23.5 13.35 23.5 15c0 2.17-1.49 3.98-3.5 4.52V23H8v-3.48C5.99 18.98 4.5 17.17 4.5 15c0-.4.03-.8.1-1.17A6.97 6.97 0 017 10z"
      stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"
    />
    <line x1="14" y1="9" x2="14" y2="18" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    <line x1="18" y1="12" x2="18" y2="18" stroke="currentColor" strokeWidth="1.8"
      strokeDasharray="2.5 2" strokeLinecap="round" />
  </svg>
);

const IconSend = () => (
  <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
    <path d="M13 7.5L2 2l2 5.5L2 13l11-5.5z" fill="currentColor" />
  </svg>
);

const IconClear = () => (
  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
    <path d="M2 2l9 9M11 2L2 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
  </svg>
);

/* ── Typing indicator ── */
function TypingIndicator() {
  return (
    <div className="flex gap-2.5 max-w-[85%]">
      <div className="w-7 h-7 rounded-xl bg-ink-700 border border-ink-600
                      flex items-center justify-center text-ink-500 flex-shrink-0 mt-1">
        <IconBrain size={14} />
      </div>
      <div className="px-4 py-3 bg-ink-800 border border-ink-700 rounded-2xl
                      rounded-bl-sm flex items-center gap-1.5">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-ink-500"
            style={{ animation: `typing 1.2s ease-in-out ${i * 0.2}s infinite` }}
          />
        ))}
      </div>
    </div>
  );
}

/* ── Message bubble ── */
function MessageBubble({ msg, username }) {
  const isUser = msg.role === "user";
  const timeStr = msg.time
    ? new Date(msg.time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    : "";

  return (
    <div
      className={`flex gap-2.5 max-w-[85%] animate-fade-up ${
        isUser ? "self-end flex-row-reverse" : "self-start"
      }`}
    >
      {/* Avatar */}
      <div
        className={`w-7 h-7 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 text-xs font-semibold ${
          isUser
            ? "bg-gold-400 text-ink-900"
            : "bg-ink-700 border border-ink-600 text-ink-500"
        }`}
      >
        {isUser ? (username?.[0]?.toUpperCase() || "U") : <IconBrain size={14} />}
      </div>

      {/* Content */}
      <div>
        <div
          className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
            isUser
              ? "bg-gold-400 text-ink-900 rounded-br-sm"
              : "bg-ink-800 border border-ink-700 text-ink-300 rounded-bl-sm"
          }`}
        >
          {msg.content}
        </div>

        {/* Referenced note */}
        {msg.noteRef && (
          <div className="mt-1.5 pl-3 border-l-2 border-gold-400 text-xs text-ink-500
                          leading-relaxed max-w-xs animate-fade-up">
            <span className="text-gold-400 font-medium block mb-0.5">
              Referenced from your notes
            </span>
            {msg.noteRef}
          </div>
        )}

        {/* Timestamp */}
        <p className={`text-[10px] text-ink-700 mt-1 ${isUser ? "text-right" : "text-left"}`}>
          {timeStr}
        </p>
      </div>
    </div>
  );
}

/* ── Suggested questions ── */
function Suggestions({ notes, onSelect }) {
  const hasBugs     = notes.some((n) => n.aiResult?.type === "Bug");
  const hasIdeas    = notes.some((n) => n.aiResult?.type === "Idea");
  const hasTasks    = notes.some((n) => n.aiResult?.type === "Task");
  const hasReminder = notes.some((n) => n.aiResult?.type === "Reminder");

  const suggestions = [
    notes.length === 0 && "What can I capture in my Second Brain?",
    hasBugs         && "Summarize my bug notes",
    hasIdeas        && "What are my best ideas?",
    hasTasks        && "What tasks do I have pending?",
    hasReminder     && "What should I remember today?",
    notes.length > 0 && "Give me a full summary of all my notes",
  ].filter(Boolean);

  if (suggestions.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 px-4 pb-2">
      {suggestions.slice(0, 4).map((s) => (
        <button
          key={s}
          onClick={() => onSelect(s)}
          className="text-xs px-3 py-1.5 bg-ink-800 border border-ink-700
                     text-ink-400 rounded-full hover:border-gold-400/50 hover:text-gold-400
                     transition-all duration-150"
        >
          {s}
        </button>
      ))}
    </div>
  );
}

/* ════════════════════════════════════════
   CHATVIEW — main export
════════════════════════════════════════ */
export default function ChatView({ notes, username }) {
  const [messages, setMessages] = useState([]);
  const [input,    setInput]    = useState("");
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState("");
  const bottomRef = useRef(null);
  const taRef     = useRef(null);

  /* Welcome message */
  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        content:
          notes.length > 0
            ? `Hi ${username}! I have access to your ${notes.length} note${notes.length !== 1 ? "s" : ""}. Ask me anything — I'll use them to give you personalized answers.`
            : `Hi ${username}! I'm your Brain Assistant. Add some notes in the "Add note" section and I'll use them to answer your questions intelligently.`,
        time: new Date(),
      },
    ]);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* Scroll to bottom on new messages */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { role: "user", content: text, time: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setError("");
    setLoading(true);

    if (taRef.current) {
      taRef.current.style.height = "auto";
    }

    try {
      const history = [...messages, userMsg].filter((m) => m.role);
      const { text: reply, noteRef } = await callChatAPI(history, notes);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: reply, time: new Date(), noteRef },
      ]);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I couldn't reach the AI. Check your API key in .env and try again.",
          time: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const autoResize = (e) => {
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Chat cleared. What would you like to know?",
        time: new Date(),
      },
    ]);
    setError("");
  };

  const analyzedCount = notes.filter((n) => n.aiResult).length;

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto">

      {/* ── Header ── */}
      <div className="flex items-center gap-3 pb-4 mb-4 border-b border-ink-700 flex-shrink-0">
        <div className="w-10 h-10 bg-gold-400 rounded-xl flex items-center justify-center flex-shrink-0">
          <IconBrain size={20} />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-base font-semibold text-white">Brain Assistant</h2>
          <p className="text-xs text-ink-500 mt-0.5">
            {notes.length > 0
              ? `Answering from your ${analyzedCount} analyzed note${analyzedCount !== 1 ? "s" : ""}`
              : "Add notes to give me context"}
          </p>
        </div>

        {/* Context badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-gold-400/10 border
                        border-gold-400/20 rounded-full text-xs text-gold-400 flex-shrink-0">
          <span className="w-1.5 h-1.5 rounded-full bg-gold-400 animate-pulse" />
          {notes.length} note{notes.length !== 1 ? "s" : ""} loaded
        </div>

        {/* Clear button */}
        <button
          onClick={clearChat}
          className="btn-ghost p-2 text-ink-600 hover:text-red-400"
          title="Clear chat"
        >
          <IconClear />
        </button>
      </div>

      {/* ── Messages ── */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-4 pb-4 min-h-0">
        {messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} username={username} />
        ))}
        {loading && <TypingIndicator />}
        {error && (
          <p className="text-xs text-red-400 text-center py-2 animate-fade-up">{error}</p>
        )}
        <div ref={bottomRef} />
      </div>

      {/* ── Suggestions (shown only when last message is from assistant) ── */}
      {!loading && messages[messages.length - 1]?.role === "assistant" && (
        <Suggestions notes={notes} onSelect={(s) => { setInput(s); taRef.current?.focus(); }} />
      )}

      {/* ── Input area ── */}
      <div className="flex-shrink-0 pt-3 border-t border-ink-700">
        <div className="flex items-end gap-2.5">
          <textarea
            ref={taRef}
            value={input}
            rows={1}
            onChange={(e) => { setInput(e.target.value); autoResize(e); }}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about your notes…"
            disabled={loading}
            className="flex-1 field-area min-h-[44px] max-h-[120px] py-3 leading-relaxed
                       disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ resize: "none" }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="btn-primary w-11 h-11 p-0 rounded-xl flex-shrink-0 disabled:opacity-40"
          >
            <IconSend />
          </button>
        </div>

        <div className="flex items-center justify-between mt-2">
          <p className="text-[11px] text-ink-700">
            Context: your <span className="text-gold-400 font-medium">{notes.length}</span> notes
            · Press <kbd className="text-[10px] bg-ink-800 border border-ink-700
                                    text-ink-500 rounded px-1 font-mono">Enter</kbd> to send,{" "}
            <kbd className="text-[10px] bg-ink-800 border border-ink-700
                            text-ink-500 rounded px-1 font-mono">Shift+Enter</kbd> for new line
          </p>
          <span className="text-[11px] text-ink-700">{messages.length} messages</span>
        </div>
      </div>

      {/* Typing animation keyframe */}
      <style>{`
        @keyframes typing {
          0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
