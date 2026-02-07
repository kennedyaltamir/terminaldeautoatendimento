/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 13.2.0 (Global Style Hardening)
 * DNA_ID: MF-LAYOUT-V13-2
 * Objective: Root Layout with global Leaflet CSS to prevent ChunkLoadErrors.
 */
import React from "react";
import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

// 🛡️ FIX: Importação Global do CSS do Leaflet. 
// Deve estar aqui para ser carregado de forma síncrona e evitar 404s no Turbopack.
import "leaflet/dist/leaflet.css";

import Providers from "@/components/Providers";
import NetworkStatus from "@/components/ui/NetworkStatus";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "MesaFlow OS | Autoatendimento Inteligente",
  description: "Sistema operacional completo para gastronomia e eventos.",
};

export const viewport: Viewport = {
  themeColor: "#ea580c",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // 🛡️ FIX: data-scroll-behavior="smooth" silencia o aviso do Next.js 16
    <html lang="pt-BR" data-scroll-behavior="smooth" suppressHydrationWarning>
      <body className={`${inter.className} antialiased bg-black text-white`}>
        <Providers>
          {children}
          <NetworkStatus />
          {/* 🛡️ Única instância do Toaster para toda a aplicação */}
          <Toaster position="top-center" theme="dark" richColors closeButton />
        </Providers>
      </body>
    </html>
  );
}