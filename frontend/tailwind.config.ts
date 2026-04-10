import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#6B5CE7",
          light: "#F5F3FF",
        },
        accent: "#FF6B6B",
        success: "#10B981",
        warning: "#F59E0B",
        background: "#FAFAFA",
        surface: "#FFFFFF",
        "text-primary": "#1A1A2E",
        "text-secondary": "#6B7280",
      },
      borderRadius: {
        sm: "8px",
        md: "16px",
        lg: "24px",
      },
      boxShadow: {
        sm: "0 2px 4px rgba(107, 92, 231, 0.08)",
        md: "0 4px 12px rgba(107, 92, 231, 0.12)",
        lg: "0 8px 24px rgba(107, 92, 231, 0.16)",
      },
    },
  },
  plugins: [],
};
export default config;