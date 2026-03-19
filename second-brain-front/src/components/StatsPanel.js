import React, { useState } from "react";
import { TYPE_META } from "../utils/classifier";

const MOODS = ["😞", "😐", "🙂", "😄"];

export default function StatsPanel({ notes }) {
  const [mood, setMood] = useState(null);

  const total    = notes.length;
  const analyzed = notes.filter((n) => n.aiResult).length;
  const synced   = notes.filter((n) => n.apiStatus === "success").length;

  return (
    <div className="space-y-3">

      {/* Session stats */}
      <div className="card-sm p-4">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500
                      flex items-center gap-1.5 mb-3">
          <span className="w-3 h-0.5 rounded-full bg-gold-400" />
          Session stats
        </p>
        <div className="space-y-2">
          {[
            { label: "Total notes", value: total,    color: "text-white" },
            { label: "Analyzed",    value: analyzed, color: "text-gold-400" },
            { label: "Synced",      value: synced,   color: "text-emerald-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="flex items-center justify-between py-1.5
                                        border-b border-ink-700 last:border-0">
              <span className="text-xs text-ink-400">{label}</span>
              <span className={`text-sm font-semibold ${color}`}>{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Type breakdown */}
      {total > 0 && (
        <div className="card-sm p-4">
          <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500
                        flex items-center gap-1.5 mb-3">
            <span className="w-3 h-0.5 rounded-full bg-gold-400" />
            Breakdown
          </p>
          <div className="space-y-2">
            {Object.entries(TYPE_META).map(([type, meta]) => {
              const count = notes.filter((n) => n.aiResult?.type === type).length;
              const pct   = analyzed > 0 ? Math.round((count / analyzed) * 100) : 0;
              return (
                <div key={type}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-ink-400 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full" style={{ background: meta.color }} />
                      {meta.label}
                    </span>
                    <span className="text-xs font-mono text-ink-500">{count}</span>
                  </div>
                  {count > 0 && (
                    <div className="h-1 bg-ink-700 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{ width: `${pct}%`, background: meta.color }}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Mood tracker */}
      <div className="card-sm p-4">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500
                      flex items-center gap-1.5 mb-3">
          <span className="w-3 h-0.5 rounded-full bg-gold-400" />
          Mood tracker
        </p>
        <p className="text-xs text-ink-500 mb-2.5">How are you feeling now?</p>
        <div className="flex gap-2">
          {MOODS.map((m) => (
            <button
              key={m}
              onClick={() => setMood(m)}
              className={`flex-1 py-2 rounded-lg text-lg transition-all duration-150 border ${
                mood === m
                  ? "bg-ink-900 border-gold-400"
                  : "bg-ink-700 border-transparent hover:border-ink-600"
              }`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* Tips */}
      <div className="card-sm p-4">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500
                      flex items-center gap-1.5 mb-2">
          <span className="w-3 h-0.5 rounded-full bg-gold-400" />
          Tips
        </p>
        <p className="text-xs text-ink-400 leading-relaxed">
          Use the type chips to pre-fill the note prefix. Press{" "}
          <kbd className="text-[10px] bg-ink-700 border border-ink-600 rounded
                          px-1.5 py-0.5 font-mono text-ink-300">
            ⌘↵
          </kbd>{" "}
          to submit quickly.
        </p>
      </div>
    </div>
  );
}
