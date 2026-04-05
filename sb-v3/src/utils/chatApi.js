const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export function buildSystemPrompt(notes) {
  return "";
}

export function findRelevantNote(query, notes) {
  return null;
}

export async function callChatAPI(messages, notes) {
  const lastUserMsg = messages.filter((m) => m.role === "user").slice(-1)[0];
  if (!lastUserMsg) return { text: "No message found.", noteRef: null };

  const res = await fetch(`${API_BASE}/agent/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: lastUserMsg.content }),
  });

  if (!res.ok) throw new Error(`API error ${res.status}`);

  const data = await res.json();
  const text = data.final_answer || data.full_response || "No response.";

  return { text, noteRef: null };
}