import React, { useState, useEffect } from "react";
import { TYPE_META } from "../utils/classifier";

const API = "http://127.0.0.1:8000";

function AISkeleton() {
  return (
    <div className="mt-4 pt-4 border-t border-ink-700 animate-fade-up">
      <div className="flex items-center gap-2 mb-3">
        <span className="w-2 h-2 rounded-full bg-gold-400 animate-pulse-slow" />
        <span className="text-[10px] font-semibold uppercase tracking-widest text-ink-500">
          Analyzing…
        </span>
      </div>
      <div className="bg-ink-700 rounded-xl p-3 space-y-2">
        <div className="skeleton h-2.5 w-1/3" />
        <div className="skeleton h-2.5 w-2/3 mt-2" />
        <div className="skeleton h-2.5 w-1/2 mt-2" />
      </div>
    </div>
  );
}

function AIPanel({ result }) {
  const meta = TYPE_META[result.type] || TYPE_META.Idea;
  return (
    <div className="mt-4 pt-4 border-t border-ink-700 animate-fade-up">
      <div className="flex items-center gap-2 mb-3">
        <span className="w-2 h-2 rounded-full bg-gold-400" />
        <span className="text-[10px] font-semibold uppercase tracking-widest text-ink-500">
          AI Result
        </span>
      </div>
      <div className="bg-ink-700 rounded-xl p-3.5 space-y-2.5">
        <div className="flex items-center gap-2">
          <span className="text-xs text-ink-500 w-16 flex-shrink-0">Type</span>
          <span className={`badge ${meta.badge}`}>
            <span>{meta.icon}</span>
            {meta.label}
          </span>
        </div>
        <div className="flex items-start gap-2">
          <span className="text-xs text-ink-500 w-16 flex-shrink-0 pt-0.5">Summary</span>
          <span className="text-xs text-ink-300 leading-relaxed">{result.summary}</span>
        </div>
        {result.keywords?.length > 0 && (
          <div className="flex items-start gap-2">
            <span className="text-xs text-ink-500 w-16 flex-shrink-0 pt-0.5">Keywords</span>
            <div className="flex flex-wrap gap-1.5">
              {result.keywords.map((kw) => (
                <span key={kw}
                  className="text-[11px] bg-ink-800 border border-ink-600 text-ink-400 px-2 py-0.5 rounded-full">
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function RelatedNotes({ topic, currentNoteId }) {
  const [related, setRelated] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!topic) return;
    fetch(`${API}/related-notes/${topic}`)
      .then((r) => r.json())
      .then((data) => {
        const filtered = (data.related_notes || []).filter(
          (n) => n.id !== currentNoteId
        );
        setRelated(filtered);
      })
      .catch(() => setRelated([]))
      .finally(() => setLoading(false));
  }, [topic, currentNoteId]);

  if (loading) return (
    <div className="mt-4 pt-4 border-t border-ink-700">
      <div className="text-[10px] font-semibold uppercase tracking-widest text-ink-500 mb-2">
        Related notes…
      </div>
      <div className="skeleton h-2.5 w-1/2" />
    </div>
  );

  if (related.length === 0) return null;

  return (
    <div className="mt-4 pt-4 border-t border-ink-700 animate-fade-up">
      <div className="flex items-center gap-2 mb-3">
        <span className="w-2 h-2 rounded-full bg-emerald-500" />
        <span className="text-[10px] font-semibold uppercase tracking-widest text-ink-500">
          Related notes ({related.length})
        </span>
      </div>
      <div className="flex flex-col gap-2">
        {related.map((n) => (
          <div key={n.id}
            className="flex items-center gap-2 px-3 py-2 bg-ink-700 rounded-lg border border-ink-600">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 flex-shrink-0" />
            <span className="text-xs text-ink-300 truncate">{n.title}</span>
            <span className="ml-auto text-[10px] text-ink-600 flex-shrink-0">{n.topic}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function NoteCard({ note, index }) {
  const [open, setOpen] = useState(true);
  const meta = note.aiResult ? (TYPE_META[note.aiResult.type] || TYPE_META.Idea) : null;

  const timeStr = note.createdAt
    ? new Date(note.createdAt).toLocaleString([], {
        month: "short", day: "numeric",
        hour: "2-digit", minute: "2-digit",
      })
    : "";

  return (
    <article
      className="card hover:border-ink-600 hover:shadow-card-md transition-all duration-200 animate-fade-up overflow-hidden"
      style={{ animationDelay: `${Math.min(index * 50, 300)}ms` }}
    >
      <div
        className="flex items-center gap-2.5 px-4 py-3 cursor-pointer select-none"
        onClick={() => setOpen((v) => !v)}
      >
        <span className="font-mono text-xs text-ink-600 flex-shrink-0">
          #{String(index + 1).padStart(2, "0")}
        </span>

        {meta ? (
          <span className={`badge ${meta.badge} flex-shrink-0`}>
            <span>{meta.icon}</span>
            {meta.label}
          </span>
        ) : note.aiLoading ? (
          <span className="flex items-center gap-1.5 text-xs text-ink-500 flex-shrink-0">
            <svg className="w-3.5 h-3.5 animate-spin-slow" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2"
                strokeDasharray="20" strokeDashoffset="8" />
            </svg>
            Analyzing
          </span>
        ) : null}

        <span className="flex-1 text-sm text-ink-400 truncate min-w-0">
          {note.content}
        </span>

        <div className="flex items-center gap-2.5 flex-shrink-0">
          {timeStr && (
            <span className="text-xs text-ink-600 hidden sm:block">{timeStr}</span>
          )}
          <span
            title={note.apiStatus === "success" ? "Synced to server" : "Saved locally"}
            className={`w-2 h-2 rounded-full flex-shrink-0 ${
              note.apiStatus === "success" ? "bg-emerald-500" : "bg-amber-500"
            }`}
          />
          <svg
            className={`w-4 h-4 text-ink-600 transition-transform duration-200 ${open ? "rotate-0" : "-rotate-90"}`}
            viewBox="0 0 16 16" fill="none"
          >
            <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5"
              strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>

      <div className={`overflow-hidden transition-all duration-300 ${open ? "max-h-[800px] opacity-100" : "max-h-0 opacity-0"}`}>
        <div className="px-4 pb-4 border-t border-ink-700 pt-3">
          <p className="text-sm text-ink-300 leading-relaxed whitespace-pre-wrap">
            {note.content}
          </p>

          {note.apiStatus === "error" && (
            <p className="mt-2 text-xs text-amber-500 flex items-center gap-1.5">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M6 1.5L1 10.5h10z" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M6 5v2.5M6 9v.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
              </svg>
              Server unreachable — note saved locally only.
            </p>
          )}

          {note.aiLoading && <AISkeleton />}
          {!note.aiLoading && note.aiResult && <AIPanel result={note.aiResult} />}

          {note.apiStatus === "success" && note.aiResult?.type && (
            <RelatedNotes topic={note.aiResult.type} currentNoteId={note.id} />
          )}
        </div>
      </div>
    </article>
  );
}