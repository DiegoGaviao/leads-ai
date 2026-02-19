/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#00FF41", // Dhawk Electric Green
          foreground: "#050505",
        },
        secondary: {
          DEFAULT: "#004D1A", // Deep Emerald
          foreground: "#FFFFFF",
        },
        accent: {
          DEFAULT: "#00FF41",
          foreground: "#050505",
        },
        slate: {
          950: "#050505", // Dhawk Obsidian
          900: "#0D0D0D",
          800: "#1A1A1A",
        }
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
        "3xl": "2rem",
      },
      boxShadow: {
        'premium': '0 0 50px -12px rgba(0, 0, 0, 0.5)',
        'glow': '0 0 20px -5px rgba(79, 70, 229, 0.3)',
      }
    },
  },
  plugins: [],
}
