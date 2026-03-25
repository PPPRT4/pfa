import React, { useState, useEffect } from "react";
import Sidebar    from "../components/Sidebar";
import AddNote    from "../components/AddNote";
import NoteCard   from "../components/NoteCard";
import StatsPanel from "../components/StatsPanel";
import ChatView   from "../components/ChatView";
import { classifyNote, NOTE_TYPES } from "../utils/classifier";
import { postNote } from "../utils/api";

/* ── Icons ── */
const IconMenu = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
    <path d="M3 4.5h12M3 9h12M3 13.5h12"
      stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
  </svg>
);
const IconSearch = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="6" cy="6" r="4.5" stroke="currentColor" strokeWidth="1.25" />
    <path d="M11 11L9 9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
  </svg>
);

const greet = () => {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 18) return "Good afternoon";
  return "Good evening";
};

const PAGE_TITLES = { add: "New note", notes: "All notes", chat: "AI Chat" };

/* ════════════════════════════════════════
   NOTES PAGE (main shell)
════════════════════════════════════════ */
export default function Notes() {
  const [notes,     setNotes]     = useState([]);
  const [view,      setView]      = useState("add");
  const [filter,    setFilter]    = useState("all");
  const [search,    setSearch]    = useState("");
  const [mobileNav, setMobileNav] = useState(false);
  const [chatCount, setChatCount] = useState(0);

  const username = sessionStorage.getItem("sb_user") || "User";

  /* Restore from sessionStorage */
  useEffect(() => {
    try {
      const saved = JSON.parse(sessionStorage.getItem("sb_notes") || "[]");
      if (Array.isArray(saved)) setNotes(saved);
    } catch {}
  }, []);

  /* Persist on every change */
  useEffect(() => {
    sessionStorage.setItem("sb_notes", JSON.stringify(notes));
  }, [notes]);

  /* ── Add note handler ── */
  const handleAdd = async (content) => {
    const id        = Date.now();
    const apiStatus = await postNote(content);
    const newNote   = {
      id, content,
      createdAt:  new Date().toISOString(),
      aiLoading:  true,
      aiResult:   null,
      apiStatus,
    };

    setNotes((prev) => [newNote, ...prev]);
    setView("notes");

    /* Simulate AI classification delay */
    await new Promise((r) => setTimeout(r, 1000));
    const ai = classifyNote(content);
    setNotes((prev) =>
      prev.map((n) => n.id === id ? { ...n, aiResult: ai, aiLoading: false } : n)
    );

    return apiStatus;
  };

  /* ── Filtered + searched notes ── */
  const visible = notes.filter((n) => {
    const matchFilter = filter === "all" || n.aiResult?.type === filter;
    const matchSearch = !search || n.content.toLowerCase().includes(search.toLowerCase());
    return matchFilter && matchSearch;
  });

  return (
    <div className="flex min-h-screen bg-ink-900">

      {/* Sidebar */}
      <Sidebar
        active={view}
        onNav={(v) => { setView(v); if (v === "chat") setSearch(""); }}
        notes={notes}
        chatCount={chatCount}
        mobileOpen={mobileNav}
        onClose={() => setMobileNav(false)}
      />

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden min-h-screen">

        {/* ── Top bar ── */}
        <header className="sticky top-0 z-10 h-12 flex items-center gap-3 px-5
                           bg-ink-900 border-b border-ink-700 flex-shrink-0">
          <button
            onClick={() => setMobileNav(true)}
            className="lg:hidden text-ink-500 hover:text-white transition-colors"
          >
            <IconMenu />
          </button>

          <div className="flex items-center gap-2 text-sm">
            <span className="text-ink-600">Second Brain</span>
            <span className="text-ink-700">/</span>
            <span className="font-medium text-white">{PAGE_TITLES[view]}</span>
          </div>

          <div className="ml-auto flex items-center gap-3">
            {view === "notes" && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-ink-800
                              border border-ink-700 rounded-lg">
                <IconSearch />
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search notes…"
                  className="bg-transparent text-sm text-white placeholder-ink-600
                             outline-none w-32 sm:w-44"
                />
                {search && (
                  <button onClick={() => setSearch("")}
                    className="text-ink-600 hover:text-white text-xs transition-colors">
                    ✕
                  </button>
                )}
              </div>
            )}

            {/* Chat context pill — shows in chat view */}
            {view === "chat" && (
              <div className="flex items-center gap-2 text-xs text-gold-400
                              bg-gold-400/10 border border-gold-400/20 rounded-full px-3 py-1">
                <span className="w-1.5 h-1.5 rounded-full bg-gold-400 animate-pulse" />
                {notes.length} notes as context
              </div>
            )}

            {notes.length > 0 && view !== "chat" && (
              <div className="hidden sm:flex items-center gap-2 text-xs text-ink-500
                              bg-ink-800 border border-ink-700 rounded-full px-3 py-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                {notes.length} notes
              </div>
            )}

            <span className="hidden md:block text-xs text-ink-600">
              {greet()}, <span className="text-ink-400 font-medium">{username}</span>
            </span>
          </div>
        </header>

        {/* ── Page content ── */}
        <main className={`flex-1 px-5 py-6 ${view === "chat" ? "overflow-hidden flex flex-col" : "overflow-y-auto"}`}>

          {/* ADD VIEW */}
          {view === "add" && (
            <div className="grid grid-cols-1 lg:grid-cols-[1fr_260px] gap-6 max-w-5xl mx-auto">
              <AddNote onAdd={handleAdd} />
              <div className="hidden lg:block">
                <StatsPanel notes={notes} />
              </div>
            </div>
          )}

          {/* NOTES VIEW */}
          {view === "notes" && (
            <div className="max-w-2xl mx-auto">
              <div className="flex items-start justify-between mb-5">
                <div>
                  <h2 className="text-xl font-semibold text-white">All notes</h2>
                  <p className="text-sm text-ink-400 mt-1">
                    {notes.length === 0
                      ? "Nothing yet — add your first thought!"
                      : `${visible.length} of ${notes.length} note${notes.length !== 1 ? "s" : ""}`}
                  </p>
                </div>
                <button onClick={() => setView("add")} className="btn-primary">
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <circle cx="6.5" cy="6.5" r="6" stroke="currentColor" strokeWidth="1.25" />
                    <path d="M6.5 4v5M4 6.5h5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
                  </svg>
                  New note
                </button>
              </div>

              {/* Filter chips */}
              <div className="flex gap-2 flex-wrap mb-5">
                {["all", ...NOTE_TYPES].map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`text-xs px-3 py-1.5 rounded-full border transition-all ${
                      filter === f
                        ? "bg-gold-400 text-ink-900 border-gold-400 font-semibold"
                        : "border-ink-700 text-ink-500 hover:border-ink-600 hover:text-white"
                    }`}
                  >
                    {f === "all" ? "All" : f}
                  </button>
                ))}
              </div>

              {/* Empty state */}
              {notes.length === 0 && (
                <div className="text-center py-20 card">
                  <span className="text-5xl">📭</span>
                  <h3 className="text-lg font-semibold text-white mt-4 mb-2">
                    Your second brain is empty
                  </h3>
                  <p className="text-sm text-ink-400 mb-6 max-w-xs mx-auto">
                    Capture your first thought and let AI organize it.
                  </p>
                  <button onClick={() => setView("add")} className="btn-primary">
                    Add your first note
                  </button>
                </div>
              )}

              {/* No results */}
              {notes.length > 0 && visible.length === 0 && (
                <div className="text-center py-16 card">
                  <span className="text-4xl">🔍</span>
                  <p className="text-white font-medium mt-4">No results found</p>
                  <p className="text-sm text-ink-400 mt-1">Try a different search or filter.</p>
                </div>
              )}

              <div className="space-y-3">
                {visible.map((note, i) => (
                  <NoteCard key={note.id} note={note} index={i} />
                ))}
              </div>
            </div>
          )}

          {/* CHAT VIEW */}
          {view === "chat" && (
            <div className="flex-1 max-w-3xl mx-auto w-full flex flex-col min-h-0"
                 style={{ height: "calc(100vh - 6rem)" }}>
              <ChatView
                notes={notes}
                username={username}
                onMessageCountChange={setChatCount}
              />
            </div>
          )}
        </main>

        {/* ── Footer ── */}
        <footer className="flex items-center justify-between px-5 py-2
                           border-t border-ink-700 text-xs text-ink-700 flex-shrink-0">
          <span>Second Brain · AI Notes + Chat</span>
          <span>{notes.length} note{notes.length !== 1 ? "s" : ""} this session</span>
        </footer>
      </div>
    </div>
  );
}
