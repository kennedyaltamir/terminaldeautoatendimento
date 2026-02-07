import { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "MesaFlow OS",
    short_name: "MesaFlow",
    description: "Sistema Operacional para Food Service",
    start_url: "/",
    display: "standalone",
    background_color: "#000000",
    theme_color: "#ea580c",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      }, 
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
