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
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
