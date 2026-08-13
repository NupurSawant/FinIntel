import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
const target = process.env.VITE_API_TARGET || (process.env.PORT ? `http://localhost:${process.env.PORT}` : 'http://localhost:8000');

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      '/auth': target,
      '/query': target,
      '/rag': target,
      '/sql': target,
      '/conversations': target,
      '/slo': target,
      '/health': target,
    },
  },
})
