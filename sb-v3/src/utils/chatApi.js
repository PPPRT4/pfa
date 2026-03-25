/**
 * Sends a chat message to the Anthropic API using the user's notes as context.
 * The API key is read from the .env file (REACT_APP_ANTHROPIC_KEY).
 *
 * @param {Array} messages - Chat history [{ role: "user"|"assistant", content: string }]
 * @param {Array} notes    - The user's notes array (with aiResult)
 * @returns {Promise<{ text: string, noteRef: string|null }>}
 */

const STOP_WORDS = new Set([
  "the","a","an","is","in","it","to","of","and","or","i","my","me",
  "we","this","that","for","with","have","was","are","be","been",
]);

export function buildSystemPrompt(notes) {
  if (notes.length === 0) {
    return (
      "You are a helpful AI assistant called 'Brain Assistant'. " +
      "The user has not added any notes yet. Encourage them to add notes " +
      "in the 'Add note' section so you can help them better. Be concise and friendly."
    );
  }

  const analyzed = notes.filter((n) => n.aiResult);
  const unanalyzed = notes.filter((n) => !n.aiResult);

  const ctx = analyzed
    .map(
      (n, i) =>
        `[Note ${i + 1}] Type: ${n.aiResult.type}\n` +
        `Content: ${n.content}\n` +
        `Summary: ${n.aiResult.summary}\n` +
        `Keywords: ${n.aiResult.keywords.join(", ")}`
    )
    .join("\n\n");

  const extra =
    unanalyzed.length > 0
      ? `\n\nAdditional notes (not yet classified):\n` +
        unanalyzed.map((n, i) => `[U${i + 1}] ${n.content}`).join("\n")
      : "";

  return (
    "You are 'Brain Assistant', a personal AI with access to the user's Second Brain notes. " +
    "Use these notes as your primary context when answering questions. " +
    "Be concise, insightful, and reference relevant notes when helpful. " +
    "If the question is unrelated to the notes, still answer helpfully as a general assistant.\n\n" +
    "USER'S NOTES:\n" +
    ctx +
    extra
  );
}

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
  const apiKey = process.env.REACT_APP_ANTHROPIC_KEY;

  if (!apiKey) {
    return {
      text:
        "No API key found. Add REACT_APP_ANTHROPIC_KEY to your .env file to enable AI chat.",
      noteRef: null,
    };
  }

  const system = buildSystemPrompt(notes);

  // Keep only last 20 messages to stay within context limits
  const trimmed = messages.slice(-20).map(({ role, content }) => ({ role, content }));

  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      system,
      messages: trimmed,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || `API error ${res.status}`);
  }

  const data = await res.json();
  const text = data.content?.[0]?.text ?? "No response received.";

  // Find the most relevant note to cite
  const lastUserMsg = messages.filter((m) => m.role === "user").slice(-1)[0];
  const noteRef = lastUserMsg
    ? findRelevantNote(lastUserMsg.content, notes)
    : null;

  return { text, noteRef };
}
