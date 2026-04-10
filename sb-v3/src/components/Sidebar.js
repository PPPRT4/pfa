import React from "react";
import { useNavigate } from "react-router-dom";
import { TYPE_META } from "../utils/classifier";

const IconPlus = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.25" />
    <path d="M7 4.5v5M4.5 7h5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
  </svg>
);
const IconNotes = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <rect x="2" y="2" width="10" height="10" rx="1.5" stroke="currentColor" strokeWidth="1.25" />
    <path d="M4 5.5h6M4 8h4" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
  </svg>
);
const IconChat = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1.5 2.5h11a.5.5 0 01.5.5v6a.5.5 0 01-.5.5H4.5L2 12V3a.5.5 0 01-.5-.5z"
      stroke="currentColor" strokeWidth="1.25" strokeLinejoin="round" />
  </svg>
);
const IconLogout = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M5.5 2H3a1 1 0 00-1 1v8a1 1 0 001 1h2.5" stroke="currentColor"
      strokeWidth="1.25" strokeLinecap="round" />
    <path d="M9 9.5L12 7 9 4.5M12 7H6" stroke="currentColor" strokeWidth="1.25"
      strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
const IconEval = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M2 10L5 7l2.5 2.5L11 4" stroke="currentColor" strokeWidth="1.25"
      strokeLinecap="round" strokeLinejoin="round" />
    <rect x="1" y="1" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="1.25" />
  </svg>
);

const NAV = [
  { id: "add",   label: "Add note",   Icon: IconPlus  },
  { id: "notes", label: "All notes",  Icon: IconNotes },
  { id: "chat",  label: "AI Chat",    Icon: IconChat, highlight: true },
  { id: "eval",  label: "Evaluation", Icon: IconEval  },
];

export default function Sidebar({ active, onNav, notes, chatCount, mobileOpen, onClose }) {
  const navigate = useNavigate();
  const username = sessionStorage.getItem("sb_user") || "User";

  const handleLogout = () => {
    sessionStorage.removeItem("sb_user");
    navigate("/");
  };

  const counts = Object.keys(TYPE_META).reduce((acc, t) => {
    acc[t] = notes.filter((n) => n.aiResult?.type === t).length;
    return acc;
  }, {});

  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside className={`
        fixed inset-y-0 left-0 z-30 w-56 flex flex-col
        bg-ink-900 border-r border-ink-700
        transition-transform duration-300 ease-out
        lg:relative lg:translate-x-0 lg:z-auto
        ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
      `}>
        {/* Brand */}
        <div className="flex items-center gap-2.5 px-4 py-5 border-b border-ink-700">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-gold-400 to-gold-600
                          flex items-center justify-center flex-shrink-0">
            <svg width="16" height="16" viewBox="0 0 28 28" fill="none">
              <path d="M7 10c0-3.87 3.13-7 7-7s7 3.13 7 7c0 .4-.03.8-.1 1.17C22.38 11.9 23.5 13.35 23.5 15c0 2.17-1.49 3.98-3.5 4.52V23H8v-3.48C5.99 18.98 4.5 17.17 4.5 15c0-.4.03-.8.1-1.17A6.97 6.97 0 017 10z"
                stroke="#1c2233" strokeWidth="2" strokeLinecap="round" />
              <line x1="14" y1="9" x2="14" y2="18" stroke="#1c2233" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-semibold text-white leading-tight">Second Brain</p>
            <p className="text-xs text-ink-500 mt-0.5">AI Notes · v3.0</p>
          </div>
        </div>

        {/* Nav */}
        <nav className="px-2 py-3 space-y-0.5">
          <p className="px-2 mb-2 text-[10px] font-semibold uppercase tracking-widest text-ink-600">
            Workspace
          </p>
          {NAV.map(({ id, label, Icon, highlight }) => (
            <button
              key={id}
              onClick={() => { onNav(id); onClose?.(); }}
              className={`nav-link ${active === id ? "active" : ""} ${
                highlight && active !== id ? "text-gold-400/70 hover:text-gold-400" : ""
              } ${id === "eval" && active !== id ? "text-emerald-400/70 hover:text-emerald-400" : ""}`}
            >
              <Icon />
              {label}
              {id === "notes" && notes.length > 0 && (
                <span className="ml-auto text-xs bg-ink-700 text-ink-400 rounded-full px-2 py-0.5">
                  {notes.length}
                </span>
              )}
              {id === "chat" && chatCount > 0 && (
                <span className="ml-auto text-xs bg-gold-400/15 text-gold-400 rounded-full px-2 py-0.5">
                  {chatCount}
                </span>
              )}
            </button>
          ))}
        </nav>

        {/* Tag breakdown */}
        <div className="px-2 mt-1">
          <p className="px-2 mb-2 text-[10px] font-semibold uppercase tracking-widest text-ink-600">
            Tags
          </p>
          {Object.entries(TYPE_META).map(([type, meta]) => (
            <div key={type} className="flex items-center gap-2.5 px-2 py-1.5 rounded-lg">
              <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: meta.color }} />
              <span className="text-xs text-ink-500 flex-1">{meta.label}</span>
              <span className="text-xs text-ink-600 font-mono">{counts[type]}</span>
            </div>
          ))}
        </div>

        <div className="flex-1" />

        {/* User + Logout */}
        <div className="px-2 py-3 border-t border-ink-700 space-y-1">
          <div className="flex items-center gap-2.5 px-2 py-2 rounded-xl bg-ink-800">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-gold-400 to-gold-600
                            flex items-center justify-center text-ink-900 font-bold text-xs flex-shrink-0">
              {username[0].toUpperCase()}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-white truncate">{username}</p>
              <p className="text-xs text-ink-500">Active session</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 w-full px-2 py-2 rounded-xl text-xs
                       text-ink-500 hover:bg-red-500/10 hover:text-red-400 transition-all"
          >
            <IconLogout />
            Sign out
          </button>
        </div>
      </aside>
    </>
  );
}