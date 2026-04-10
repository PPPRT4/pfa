import React, { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function EvalView() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const runEval = async () => {
    setLoading(true);
    setData(null);
    setError(null);
    try {
      const res = await fetch(`${API}/evaluation`);
      const json = await res.json();
      if (json.error) { setError(json.error); return; }
      setData(json);
    } catch (e) {
      setError("Backend unreachable.");
    } finally {
      setLoading(false);
    }
  };

  const score = data?.summary?.overall;
  const scoreColor = !score ? "" : score >= 80
    ? "text-emerald-400" : score >= 60
    ? "text-amber-400" : "text-red-400";

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">System Evaluation</h2>
          <p className="text-sm text-ink-400 mt-1">
            Mesure la qualité de la classification et du RAG
          </p>
        </div>
        <button onClick={runEval} disabled={loading} className="btn-primary flex items-center gap-2">
          {loading ? (
            <>
              <svg className="w-3.5 h-3.5 animate-spin" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2"
                  strokeDasharray="20" strokeDashoffset="8" />
              </svg>
              Running…
            </>
          ) : (
            <>
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                <path d="M2 10L5 7l2.5 2.5L11 4" stroke="currentColor" strokeWidth="1.25"
                  strokeLinecap="round" strokeLinejoin="round" />
                <rect x="1" y="1" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="1.25" />
              </svg>
              Run Evaluation
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="card border-red-500/30 text-red-400 text-sm p-4">{error}</div>
      )}

      {!data && !loading && !error && (
        <div className="card text-center py-16">
          <span className="text-5xl">🧪</span>
          <h3 className="text-lg font-semibold text-white mt-4 mb-2">Ready to evaluate</h3>
          <p className="text-sm text-ink-400">
            Clique sur "Run Evaluation" pour mesurer les performances du système.
          </p>
        </div>
      )}

      {loading && (
        <div className="card text-center py-16">
          <div className="flex justify-center mb-4">
            <svg className="w-10 h-10 text-emerald-400 animate-spin" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2"
                strokeDasharray="20" strokeDashoffset="8" />
            </svg>
          </div>
          <p className="text-sm text-ink-400">Évaluation en cours… (~20 secondes)</p>
        </div>
      )}

      {data && (
        <div className="space-y-4">
          {/* Score global */}
          <div className="card p-5 flex items-center justify-between">
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500 mb-1">
                Score Global
              </p>
              <p className={`text-4xl font-bold ${scoreColor}`}>
                {data.summary.overall?.toFixed(0)}%
              </p>
            </div>
            <div className="text-right space-y-1">
              <p className="text-xs text-ink-500">
                Classification: <span className="text-white font-medium">
                  {data.summary.classification_accuracy?.toFixed(0)}%
                </span>
              </p>
              <p className="text-xs text-ink-500">
                RAG Recall@3: <span className="text-white font-medium">
                  {data.summary.rag_recall?.toFixed(0)}%
                </span>
              </p>
            </div>
          </div>

          {/* Classification */}
          <div className="card p-5">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500 mb-3">
              Classification des notes
            </p>
            <div className="space-y-2">
              {data.classification.map((item, i) => (
                <div key={i} className="flex items-center gap-3 text-xs bg-ink-700 rounded-lg px-3 py-2">
                  <span>{item.ok ? "✅" : "❌"}</span>
                  <span className="text-ink-500 w-20 flex-shrink-0">
                    {item.expected}
                  </span>
                  <span className={`w-20 flex-shrink-0 font-medium ${item.ok ? "text-emerald-400" : "text-red-400"}`}>
                    {item.predicted}
                  </span>
                  <span className="text-ink-400 truncate">{item.content}</span>
                </div>
              ))}
            </div>
          </div>

          {/* RAG */}
          <div className="card p-5">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-ink-500 mb-3">
              RAG — Recherche sémantique
            </p>
            <div className="space-y-2">
              {data.rag.map((item, i) => (
                <div key={i} className="flex items-center gap-3 text-xs bg-ink-700 rounded-lg px-3 py-2">
                  <span>{item.ok ? "✅" : "❌"}</span>
                  <span className="text-ink-400 w-36 flex-shrink-0">{item.query}</span>
                  <span className="text-ink-500 truncate">{item.top_result}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}