/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        ink: {
          900: "#0e1117",
          800: "#1c2233",
          700: "#2a3350",
          600: "#3b4a6b",
          500: "#4f6080",
          400: "#6b7fa0",
        },
        cream: {
          50:  "#fefcf8",
          100: "#fdf8f0",
          200: "#faf0dc",
          300: "#f5e4c0",
        },
        gold: {
          300: "#fac775",
          400: "#f0a93b",
          500: "#e07b1a",
          600: "#c45e0a",
        },
      },
      animation: {
        "fade-up":   "fadeUp .3s ease both",
        "spin-slow": "spin .85s linear infinite",
        "pulse-slow":"pulse 1.4s ease-in-out infinite",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: 0, transform: "translateY(8px)" },
          to:   { opacity: 1, transform: "translateY(0)" },
        },
      },
      boxShadow: {
        card:       "0 1px 8px rgba(14,17,23,.06), 0 0 0 0.5px rgba(14,17,23,.06)",
        "card-md":  "0 4px 20px rgba(14,17,23,.1),  0 0 0 0.5px rgba(14,17,23,.07)",
        "card-lg":  "0 8px 40px rgba(14,17,23,.14), 0 0 0 0.5px rgba(14,17,23,.08)",
        "glow-gold":"0 0 0 3px rgba(240,169,59,.18)",
        "login":    "0 24px 80px rgba(14,17,23,.45)",
      },
    },
  },
  plugins: [],
};
