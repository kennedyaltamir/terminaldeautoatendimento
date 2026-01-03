import { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "MesaFlow - Sistema Operacional",
    short_name: "MesaFlow",
    description: "Gestão de pedidos e KDS para restaurantes.",
    start_url: "/",
    display: "standalone",
    background_color: "#0f172a", // Dark mode bg
    theme_color: "#ea580c", // Primary Orange
    orientation: "portrait",
    icons: [
      {
        src: "/icon",
        sizes: "192x192",
        type: "image/png",
        purpose: "maskable"
      },
      {
        src: "/icon",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable"
      }
    ],
    shortcuts: [
      {
        name: "Abrir KDS",
        url: "/admin/login",
        description: "Acessar monitor de cozinha"
      }
    ]
  };
}