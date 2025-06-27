// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      // This proxies all requests starting with /api to your backend server,
      // resolving 404 errors during local development.
      '/api': {
        target: 'http://localhost:8000', // Your FastAPI backend
        changeOrigin: true, // Recommended for virtual-hosted sites
        secure: false,      // Can be set to true if backend uses HTTPS
      },
    },
  },
});