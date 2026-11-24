/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./core/**/*.py",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#FAFAFA",
        surface: "#FFFFFF",
        line: "#E5E5E5",
        ink: { DEFAULT: "#0A0A0A", soft: "#404040", muted: "#595959" },
        accent: { DEFAULT: "#2563EB", hover: "#1D4ED8", soft: "#EFF6FF" },
      },
      fontFamily: {
        display: ['"Space Grotesk"', "ui-sans-serif", "system-ui", "sans-serif"],
        body: ['"Inter"', "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(10,10,10,.04), 0 12px 28px -14px rgba(10,10,10,.12)",
      },
    },
  },
  plugins: [],
}
