/**
 * Sends a chat message to the backend /chat endpoint.
 *
 * @param {Array} messages - Chat history [{ role: "user"|"assistant", content: string }]
 * @param {Array} notes    - The user's notes array (with aiResult)
 * @returns {Promise<{ text: string, noteRef: string|null }>}
 */

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const STOP_WORDS = new Set([
  "the","a","an","is","in","it","to","of","and","or","i","my","me",
  "we","this","that","for","with","have","was","are","be","been",
]);

/**
 * Find the most relevant note reference for a given user query.
 */
export function findRelevantNote(query, notes) {
  const q = query.toLowerCase();
  const analyzed = notes.filter((n) => n.aiResult);

  const scored = analyzed.map((n) => {
    let score = 0;
    if (n.aiResult.type && q.includes(n.aiResult.type.toLowerCase())) score += 3;
    n.aiResult.keywords.forEach((kw) => {
      if (q.includes(kw.toLowerCase())) score += 2;
    });
    const words = q.split(/\s+/).filter((w) => w.length > 3 && !STOP_WORDS.has(w));
    words.forEach((w) => {
      if (n.content.toLowerCase().includes(w)) score += 1;
    });
    return { note: n, score };
  });

  const best = scored.sort((a, b) => b.score - a.score)[0];
  if (!best || best.score === 0) return null;

  const content = best.note.content;
  return content.length > 90 ? content.slice(0, 90) + "…" : content;
}

/**
 * Call the Anthropic API.
 */
export async function callChatAPI(messages, notes) {
  const lastUserMsg = messages.filter((m) => m.role === "user").slice(-1)[0];
  const prompt = lastUserMsg?.content?.trim();

  if (!prompt) {
    return { text: "Please enter a message.", noteRef: null };
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || `API error ${res.status}`);
  }

  const data = await res.json();
  const text = data.answer ?? data.text ?? "No response received.";

  // Find the most relevant note to cite
  const noteRef = lastUserMsg ? findRelevantNote(lastUserMsg.content, notes) : null;

  return { text, noteRef };
}
