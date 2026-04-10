import React, { useState, useRef } from "react";

const CHIPS = ["Idea", "Bug", "Reminder", "Task", "Research"];
const CHAR_LIMIT = 800;

export default function AddNote({ onAdd }) {
  const [text,     setText]    = useState("");
  const [active,   setActive]  = useState(null);
  const [loading,  setLoading] = useState(false);
  const [toast,    setToast]   = useState(null); // { type, msg }
  const [error,    setError]   = useState("");
  const taRef = useRef(null);

  const charOver = text.length > CHAR_LIMIT;

  const selectChip = (chip) => {
    setActive(chip);
    setText(chip + ": ");
    taRef.current?.focus();
    setError("");
  };

  const handleSubmit = async (ev) => {
    ev?.preventDefault();
    if (!text.trim()) { setError("Please write something before adding a note."); return; }
    if (charOver)     { setError(`Maximum ${CHAR_LIMIT} characters.`); return; }
    setError("");
    setLoading(true);
    const apiStatus = await onAdd(text.trim());
    setText(""); setActive(null);
    setLoading(false);
    showToast(
      apiStatus === "success" ? "success" : "warning",
      apiStatus === "success" ? "Note added and synced to server!" : "Note saved locally — server unreachable.",
    );
  };

  const showToast = (type, msg) => {
    setToast({ type, msg });
    setTimeout(() => setToast(null), 5000);
  };

  const charsLeft = CHAR_LIMIT - text.length;

  return (
    <div className="max-w-2xl mx-auto">

      {/* Section header */}
      <div className="mb-6">
       <h2 className="text-lg sm:text-xl font-semibold text-white">Capture a          thought</h2>
        <p className="text-sm text-ink-400 mt-1">
          Write anything — AI will classify and summarize it instantly.
        </p>
      </div>

      {/* Toast */}
      {toast && (
        <div className={`toast mb-5 animate-fade-up ${
          toast.type === "success" ? "toast-success" : "toast-warning"
        }`}>
          {toast.type === "success" ? (
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.25" />
              <path d="M4.5 7l2 2 3-3" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          ) : (
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M7 1.5L1 12.5h12z" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M7 6v3M7 10.5v.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
            </svg>
          )}
          {toast.msg}
        </div>
      )}

      {/* Main input card */}
      <div className="card p-5 mb-5">

        {/* Quick-type chips */}
        <div className="flex gap-2 flex-wrap mb-4">
          {CHIPS.map((chip) => (
            <button
              key={chip}
              type="button"
              onClick={() => selectChip(chip)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-all duration-150 ${
                active === chip
                  ? "bg-gold-400 text-ink-900 border-gold-400 font-semibold"
                  : "border-ink-600 text-ink-400 hover:border-ink-500 hover:text-white"
              }`}
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Textarea */}
        <textarea
          ref={taRef}
          value={text}
          rows={6}
          onChange={(e) => { setText(e.target.value); if (error) setError(""); }}
          onKeyDown={(e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") handleSubmit(); }}
          placeholder="What's on your mind? An idea, a bug, a task, a reminder…"
          className={`field-area ${charOver ? "error" : ""}`}
        />

        {/* Footer */}
        <div className="flex items-center justify-between mt-2.5">
          <div>
            {error && (
              <p className="text-xs text-red-400 flex items-center gap-1 animate-fade-up">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="1.25" />
                  <path d="M6 4v2.5M6 8v.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
                </svg>
                {error}
              </p>
            )}
          </div>
          <span className={`text-xs ${
            charsLeft < 0 ? "text-red-400 font-semibold" :
            charsLeft < 80 ? "text-amber-400" : "text-ink-600"
          }`}>
            {charsLeft} left
          </span>
        </div>

        {/* Submit */}
        <div className="flex items-center gap-3 mt-4">
          <button
            onClick={handleSubmit}
            disabled={loading || !text.trim() || charOver}
            className="btn-primary flex-1 py-2.5 text-xs sm:text-sm"
          >
            {loading ? (
              <>
                <svg className="w-4 h-4 animate-spin-slow" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2"
                    strokeDasharray="20" strokeDashoffset="8" />
                </svg>
                Adding…
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.25" />
                  <path d="M7 4.5v5M4.5 7h5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
                </svg>
                Add to Second Brain
              </>
            )}
          </button>
          <span className="text-xs text-ink-600">⌘↵</span>
        </div>
      </div>

      {/* Info tiles */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { icon: "🧠", title: "Any format",    body: "Ideas, bugs, tasks — anything goes." },
          { icon: "⚡", title: "Auto-classified", body: "AI detects type & keywords." },
          { icon: "🔒", title: "Session storage", body: "Notes persist this session." },
        ].map(({ icon, title, body }) => (
          <div key={title} className="card-sm p-4">
            <span className="text-xl">{icon}</span>
            <p className="text-sm font-medium text-white mt-2">{title}</p>
            <p className="text-xs text-ink-500 mt-1 leading-relaxed">{body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
