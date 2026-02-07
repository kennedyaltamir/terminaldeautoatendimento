/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 12.8.0 (Concurrent-Safe Edition)
 * DNA_ID: MF-CLIENT-TOASTER-V12-8
 * Objective: Resolve "Cannot update a component while rendering" by isolating the Toaster instance.
 */
"use client";

import { Toaster } from "sonner";
import { useTheme } from "next-themes";
import { useEffect, useState, useMemo } from "react";

export function ClientToaster() {
  const { theme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // 🛡️ RITO DE MONTAGEM SOBERANO
  // O useEffect garante que o componente só "exista" para o React 
  // após a hidratação completa, movendo qualquer efeito colateral 
  // para fora da fase de renderização inicial.
  useEffect(() => {
    setMounted(true);
  }, []);

  // 🎨 RESOLUÇÃO DE TEMA ESTÁVEL
  // Calculamos o tema fora do retorno para garantir que o valor 
  // passado ao Toaster seja estável durante o ciclo de render.
  const activeTheme = useMemo(() => {
    return (theme === "system" ? resolvedTheme : theme) as "light" | "dark" | "system";
  }, [theme, resolvedTheme]);

  if (!mounted) {
    return null;
  }

  return (
    <Toaster 
      position="top-right" 
      richColors 
      closeButton 
      theme={activeTheme}
      // 🛡️ HARDENING: Configurações de performance para evitar re-renders excessivos
      pauseWhenPageIsHidden
      visibleToasts={5}
      toastOptions={{
        style: {
          borderRadius: '1.25rem',
          background: activeTheme === 'dark' ? '#0f172a' : '#ffffff',
          color: activeTheme === 'dark' ? '#f8fafc' : '#0f172a',
          border: '1px solid rgba(148, 163, 184, 0.1)',
        }
      }}
    />
  );
}
