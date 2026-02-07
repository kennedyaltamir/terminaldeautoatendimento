/**
 * 🛡️ FEATURE FLAG CONTEXT - VERSION 12.4 (Network Resilient)
 * DOMAIN: FRONTEND / CORE
 * DESCRIPTION: Gerencia flags com proteção contra falhas de backend (Fail-Open).
 */
"use client";

import React, { createContext, useContext, useEffect, useState, useCallback, useRef } from "react";
import { getToken } from "@/lib/auth";
import { decodeJwtPayload } from "@/lib/jwt";
import { getFeatureFlags, updateFeatureFlag } from "@/lib/featureFlagsApi";
import { toast } from "sonner";

interface FeatureFlags {
  [key: string]: boolean;
}

interface FeatureFlagContextType {
  flags: FeatureFlags;
  loading: boolean;
  isImpersonator: boolean;
  refreshFlags: () => Promise<void>;
  toggleFlag: (key: string) => Promise<void>;
  isEnabled: (flag: string) => boolean;
}

const FeatureFlagContext = createContext<FeatureFlagContextType | undefined>(undefined);

export function FeatureFlagProvider({ children }: { children: React.ReactNode }) {
  const [flags, setFlags] = useState<FeatureFlags>({});
  const [loading, setLoading] = useState(true);
  const [isImpersonator, setIsImpersonator] = useState(false);
  
  // 🛡️ KERNEL GUARD: Impede disparos múltiplos
  const fetchLock = useRef(false);
  const lastToken = useRef<string | null>(null);

  const fetchFlags = useCallback(async () => {
    const token = getToken();

    // Se o token não mudou e já buscamos com sucesso, aborta
    if (token === lastToken.current && fetchLock.current) return;

    if (!token) {
      setFlags({});
      setLoading(false);
      return;
    }

    try {
      const payload = decodeJwtPayload(token);
      setIsImpersonator(!!payload?.impersonator);

      const data = await getFeatureFlags();
      setFlags(data || {}); // Garante objeto vazio se null
      
      // Sela o estado para este token
      fetchLock.current = true;
      lastToken.current = token;
    } catch (e: any) {
      // Silencia erros esperados de infraestrutura para não quebrar a UI
      if (e.message === "BACKEND_OFFLINE" || e.status === 0) {
        console.warn("⚠️ [FeatureFlags] Backend indisponível. Operando em modo degradado (Flags OFF).");
        setFlags({}); // Fallback seguro
      } else if (e.status !== 401 && e.status !== 403) {
        console.error("🚨 [FeatureFlags] Sync Error:", e);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const toggleFlag = async (key: string) => {
    if (!isImpersonator) {
      toast.error("Acesso restrito ao suporte técnico.");
      return;
    }

    const previousValue = !!flags[key];
    const newValue = !previousValue;

    // Optimistic Update
    setFlags(prev => ({ ...prev, [key]: newValue }));

    try {
      await updateFeatureFlag(key, newValue);
      toast.success(`Flag ${key} atualizada.`);
    } catch (e: any) {
      // Rollback em caso de erro
      setFlags(prev => ({ ...prev, [key]: previousValue }));
      toast.error("Falha ao sincronizar flag.");
    }
  };

  const isEnabled = (flag: string) => !!flags[flag];

  useEffect(() => {
    fetchFlags();
  }, [fetchFlags]);

  return (
    <FeatureFlagContext.Provider value={{ 
      flags, loading, isImpersonator, refreshFlags: fetchFlags, toggleFlag, isEnabled 
    }}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

export const useFeatureFlags = () => {
  const context = useContext(FeatureFlagContext);
  if (!context) throw new Error("useFeatureFlags must be used within FeatureFlagProvider");
  return context;
};
