const API_BASE = "http://127.0.0.1:8000";

export function buildSystemPrompt(notes) {
  return "";
}

export function findRelevantNote(query, notes) {
  return null;
}

export async function callChatAPI(messages, notes) {
  const lastUserMsg = messages.filter((m) => m.role === "user").slice(-1)[0];
  if (!lastUserMsg) return { text: "No message found.", noteRef: null };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);

  try {
    const res = await fetch(`${API_BASE}/agent/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: lastUserMsg.content, reset: true }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!res.ok) throw new Error(`API error ${res.status}`);
    const data = await res.json();
    const text = data.final_answer || data.full_response || "No response.";
    return { text, noteRef: null };

  } catch (err) {
    clearTimeout(timeout);
    if (err.name === "AbortError") {
      throw new Error("Request timed out. Please try again.");
    }
    throw err;
  }
}