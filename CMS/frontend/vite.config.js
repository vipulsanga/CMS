import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../backend/articles/static/articles/dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      output: {
        // Django serves these files directly, so keep their template references
        // stable across builds instead of requiring a manual hash update.
        entryFileNames: 'assets/index.js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name][extname]',
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
