/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        garden: {
          ink: "#08111f",
          panel: "#101b2c",
          panelSoft: "#15243a",
          line: "#263650",
          cyan: "#38d5e8",
          blue: "#4d8dff",
          mint: "#5ee0a5",
          warning: "#f2b84b",
          danger: "#f87171",
        },
      },
      boxShadow: {
        glow: "0 18px 70px rgba(56, 213, 232, 0.12)",
      },
    },
  },
  plugins: [],
};

