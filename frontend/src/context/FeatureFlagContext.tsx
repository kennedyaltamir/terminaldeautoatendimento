"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
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
}

const FeatureFlagContext = createContext<FeatureFlagContextType | undefined>(undefined);

export function FeatureFlagProvider({ children }: { children: React.ReactNode }) {
  const [flags, setFlags] = useState<FeatureFlags>({});
  const [loading, setLoading] = useState(true);
  const [isImpersonator, setIsImpersonator] = useState(false);

  const fetchFlags = useCallback(async () => {
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      // 1. Decodificação segura do JWT via utilitário dedicado
      const payload = decodeJwtPayload(token);
      setIsImpersonator(!!payload.impersonator);

      // 2. Busca as flags do backend
      const data = await getFeatureFlags();
      setFlags(data);
    } catch (e) {
      console.error("Erro ao carregar Feature Flags", e);
      setFlags({}); // Fail Secure
    } finally {
      setLoading(false);
    }
  }, []);

  const toggleFlag = async (key: string) => {
    // Segurança: Bloqueio preventivo no client
    if (!isImpersonator) {
      toast.error("Acesso restrito ao suporte técnico.");
      return;
    }

    const previousValue = !!flags[key];
    const newValue = !previousValue;

    // 1. Atualização Otimista (UX fluida)
    setFlags(prev => ({ ...prev, [key]: newValue }));

    try {
      await updateFeatureFlag(key, newValue);
      toast.success(`Funcionalidade ${newValue ? 'ativada' : 'desativada'}.`);
    } catch (e: any) {
      // 2. Rollback em caso de erro (Fail Secure)
      setFlags(prev => ({ ...prev, [key]: previousValue }));
      
      const status = e.status;
      if (status === 403) {
        toast.error("Sessão de suporte inválida ou expirada.");
      } else if (status === 422) {
        toast.error("Erro de validação no servidor.");
      } else {
        toast.error("Falha na comunicação com o servidor.");
      }
    }
  };

  useEffect(() => {
    fetchFlags();
  }, [fetchFlags]);

  return (
    <FeatureFlagContext.Provider value={{ 
      flags, 
      loading, 
      isImpersonator, 
      refreshFlags: fetchFlags,
      toggleFlag
    }}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

export const useFeatureFlags = () => {
  const context = useContext(FeatureFlagContext);
  if (!context) throw new Error("useFeatureFlags deve ser usado dentro de FeatureFlagProvider");
  return context;
};
