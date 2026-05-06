// Note classification is handled by the backend.

export const NOTE_TYPES = ["Idea", "Bug", "Reminder", "Task", "Research"];

export const TYPE_META = {
  Idea:     { badge: "badge-idea",     label: "Idea",     color: "#7f77dd", icon: "💡" },
  Bug:      { badge: "badge-bug",      label: "Bug",      color: "#e24b4a", icon: "🐛" },
  Reminder: { badge: "badge-reminder", label: "Reminder", color: "#ef9f27", icon: "⏰" },
  Task:     { badge: "badge-task",     label: "Task",     color: "#378add", icon: "✅" },
  Research: { badge: "badge-research", label: "Research", color: "#1d9e75", icon: "🔬" },
};
