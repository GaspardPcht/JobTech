/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Couleurs personnalisées pour JobTech Radar
        primary: '#6366F1',    // Indigo
        accent: '#10B981',     // Emerald / Success
        background: '#F9FAFB', // Background clair
        textPrimary: '#111827', // Texte principal
        textSecondary: '#6B7280', // Texte secondaire
        danger: '#EF4444',     // Danger
      },
    },
  },
  plugins: [],
}
