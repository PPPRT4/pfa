const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const TIMEOUT  = 3000; // ms

const TYPE_MAP = {
  task: "Task",
  reminder: "Reminder",
  idea: "Idea",
  resource: "Research",
  bug: "Bug",
  other: "Idea",
};

function normalizeType(type) {
  if (!type) return null;
  const key = String(type).toLowerCase();
  return TYPE_MAP[key] || type;
}

function mapBackendNote(note) {
  if (!note || typeof note !== "object") return null;

  if (note.aiResult) {
    return {
      ...note,
      aiLoading: false,
      apiStatus: note.apiStatus || "success",
      aiResult: {
        ...note.aiResult,
        type: normalizeType(note.aiResult.type),
      },
    };
  }

  const type = normalizeType(note.topic);
  return {
    id: note.id,
    content: note.content || "",
    createdAt: note.createdAt || note.created_at || new Date().toISOString(),
    apiStatus: "success",
    aiLoading: false,
    aiResult: type
      ? { type, summary: note.content || "", keywords: [] }
      : null,
  };
}

async function fetchJson(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT);

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      signal: controller.signal,
    });

    const data = await res.json().catch(() => null);
    return { ok: res.ok, status: res.status, data };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * GET /notes
 * Returns an array of notes (or null on failure)
 */
export async function getNotes() {
  try {
    const { ok, data } = await fetchJson("/notes", { method: "GET" });
    return ok && Array.isArray(data)
      ? data.map(mapBackendNote).filter(Boolean)
      : null;
  } catch {
    return null;
  }
}

/**
 * POST /add-note
 * Returns "success" | "error"
 */
export async function postNote(content) {
  try {
    const { ok, data } = await fetchJson("/add-note", {
      method: "POST",
      body: JSON.stringify({ content }),
    });
    const note = ok ? mapBackendNote(data?.data) : null;
    return ok ? { status: "success", note } : { status: "error" };
  } catch {
    return { status: "error" };
  }
}
