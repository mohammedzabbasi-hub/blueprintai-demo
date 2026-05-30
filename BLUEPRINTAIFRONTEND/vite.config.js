import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/demo/shops": {
  	target: "http://127.0.0.1:8000",
  	changeOrigin: true,
      },	
      "/analytics": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/creatives": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/briefs": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/blueprint": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/video-analysis": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/auth": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/onboarding": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/import": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom", "react-router-dom"],
          charts: ["recharts"],
          motion: ["framer-motion"],
          query: ["@tanstack/react-query"],
          icons: ["lucide-react"],
        },
      },
    },
  },
  plugins: [react()],
});
