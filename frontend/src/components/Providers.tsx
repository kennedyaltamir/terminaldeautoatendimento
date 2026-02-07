/**
 * Author: MESAFLOW_AI
 * Version: 11.10 (Sovereign Context Hierarchy)
 * Objective: Unified provider tree to eliminate "useCart" scope errors.
 */
"use client";

import React from "react";
import { ThemeProvider } from "next-themes";
import { LanguageProvider } from "@/context/LanguageContext";
import { CartProvider } from "@/context/CartContext";
import { KioskProvider } from "@/context/KioskContext";
import { FeatureFlagProvider } from "@/context/FeatureFlagContext";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <LanguageProvider>
        <FeatureFlagProvider>
          <CartProvider>
            <KioskProvider>
              {children}
            </KioskProvider>
          </CartProvider>
        </FeatureFlagProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}
