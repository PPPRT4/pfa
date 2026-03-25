const STOP_WORDS = new Set([
  "the","a","an","is","in","it","to","of","and","or","i","my","me",
  "we","this","that","for","with","have","was","are","be","been",
  "but","not","on","at","by","as","do","so","if","up","no","our",
  "you","your","will","can","they","all","from","which","its",
]);

/**
 * Classifies a note and returns { type, summary, keywords }.
 * Runs locally — no API key needed.
 */
export function classifyNote(text) {
  const lower = text.toLowerCase();

  let type = "Idea";
  if (/bug|error|crash|broken|fix|issue|fail/i.test(lower))              type = "Bug";
  else if (/remind|don.t forget|must|todo|to-do|remember/i.test(lower))  type = "Reminder";
  else if (/task|complete|finish|implement|ship|deploy/i.test(lower))    type = "Task";
  else if (/research|study|learn|explore|investigate|look into/i.test(lower)) type = "Research";

  const words   = text.trim().split(/\s+/);
  const summary = words.length <= 12 ? text.trim() : words.slice(0, 12).join(" ") + "…";

  const keywords = [
    ...new Set(
      words
        .map((w) => w.replace(/[^a-zA-Z]/g, "").toLowerCase())
        .filter((w) => w.length > 3 && !STOP_WORDS.has(w))
    ),
  ].slice(0, 5);

  return { type, summary, keywords };
}

export const NOTE_TYPES = ["Idea", "Bug", "Reminder", "Task", "Research"];

export const TYPE_META = {
  Idea:     { badge: "badge-idea",     label: "Idea",     color: "#7f77dd", icon: "💡" },
  Bug:      { badge: "badge-bug",      label: "Bug",      color: "#e24b4a", icon: "🐛" },
  Reminder: { badge: "badge-reminder", label: "Reminder", color: "#ef9f27", icon: "⏰" },
  Task:     { badge: "badge-task",     label: "Task",     color: "#378add", icon: "✅" },
  Research: { badge: "badge-research", label: "Research", color: "#1d9e75", icon: "🔬" },
};
