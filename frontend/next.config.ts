import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "standalone",
  
  // Habilita rotas tipadas (Nativo no Next.js 16)
  typedRoutes: true,

  // 🔓 LISTA BRANCA DE IPs (Crucial para acesso via Wi-Fi)
  // Adicionamos variações para garantir que o Next.js aceite a conexão
  allowedDevOrigins: [
    "localhost:3000", 
    "localhost:3001",
    "127.0.0.1:3000",
    "192.168.0.150:3000", // Seu IP com porta
    "192.168.0.150:3001", // Porta alternativa
    "192.168.0.150",      // IP puro (fallback)
  ],

  // Fallback de CORS para garantir carregamento de assets
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "Access-Control-Allow-Methods", value: "GET,OPTIONS,PATCH,DELETE,POST,PUT" },
        ],
      },
    ];
  },

  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
};

export default nextConfig;