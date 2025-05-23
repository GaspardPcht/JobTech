import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    devSourcemap: true,
  },
  server: {
    hmr: {
      overlay: false, // Désactiver l'overlay d'erreur pour le développement
    },
  },
})
