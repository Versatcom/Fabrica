import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.svg"],
      manifest: {
        name: "Fabrica Perobell",
        short_name: "Fabrica",
        description: "Gestión de fabricación y stock para Perobell",
        theme_color: "#0f172a",
        background_color: "#f8fafc",
        display: "standalone",
        scope: "/",
        start_url: "/",
        icons: [
          {
            src: "favicon.svg",
            sizes: "any",
            type: "image/svg+xml"
          }
        ]
      }
    })
  ],
  server: {
    port: 5173
  }
});
