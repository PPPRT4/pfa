const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const TIMEOUT  = 3000;

export async function postNote(content) {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT);

    const res = await fetch(`${API_BASE}/add-note`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ content }),
      signal:  controller.signal,
    });

    clearTimeout(timer);
    if (res.ok) {
      const data = await res.json();
      return data;
    }
    return null;
  } catch {
    return null;
  }
}