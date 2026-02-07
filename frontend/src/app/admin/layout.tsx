// DOMAIN: FRONTEND
// FILE: src/app/admin/layout.tsx
// COMPAT: Next.js 16 App Router
// LAST_MODIFIED: 2026-01-25

import React from "react";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { headers } from "next/headers";

import Providers from "@/components/Providers";
import NetworkStatus from "@/components/ui/NetworkStatus";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

/**
 * 📌 METADATA — Admin
 * (sem themeColor, sem manifest)
 */
export const metadata: Metadata = {
  title: "MesaFlow OS | Administração",
  description: "Centro de comando soberano da operação.",
};

/**
 * 🧠 ADMIN ROOT LAYOUT
 */
export default function AdminRootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-black text-white">
      {children}
    </div>
  );
}
