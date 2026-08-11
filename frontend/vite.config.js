import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      '/auth': 'http://localhost:8000',
      '/query': 'http://localhost:8000',
      '/rag': 'http://localhost:8000',
      '/sql': 'http://localhost:8000',
      '/conversations': 'http://localhost:8000',
      '/slo': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
