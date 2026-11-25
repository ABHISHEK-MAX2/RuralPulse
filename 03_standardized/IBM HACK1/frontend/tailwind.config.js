/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#060B1E",         // Deep dark navy page background
          sidebar: "#080E21",    // Dark sidebar background
          card: "#0F1A34",       // Dark card background
          cardBorder: "#1E2D50", // Card border
          inset: "#091024",      // Dark inset metric box background
          insetBorder: "#162347" // Inset box border
        },
        brand: {
          emerald: "#10B981",    // Primary active green
          emeraldBg: "#064E3B",  // Green badge fill
          emeraldBorder: "#047857",
          gold: "#F59E0B",       // Gold warning / demo badge text
          goldBg: "#451A03",     // Gold badge fill
          goldBorder: "#B45309",
          rose: "#EF4444",       // Red alert
          cyan: "#06B6D4"        // Cyan accents
        }
      }
    },
  },
  plugins: [],
}
