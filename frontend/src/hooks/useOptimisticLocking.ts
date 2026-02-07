/**
 * Author: MESAFLOW_AI
 * Version: 1.0
 * DNA_ID: hook-optimistic-locking-v1
 * Objective: Manage data concurrency and handle 409 Conflict states.
 */
import { useState, useCallback } from 'react';
import { toast } from 'sonner';

interface VersionedEntity {
  updated_at?: string;
  version?: number;
  [key: string]: any;
}

export function useOptimisticLocking<T extends VersionedEntity>() {
  const [lastKnownVersion, setLastKnownVersion] = useState<string | number | undefined>(undefined);

  // Inicializa o rastreamento de versão ao carregar o dado
  const trackVersion = useCallback((data: T | null) => {
    if (data) {
      setLastKnownVersion(data.updated_at || data.version);
    }
  }, []);

  // Verifica se o erro retornado pela API é um conflito de concorrência
  const isConflictError = (error: any) => {
    return error?.status === 409 || error?.message?.includes("conflict") || error?.code === "VERSION_MISMATCH";
  };

  // Manipulador padrão para UI de conflito
  const handleConflict = (onReload: () => void) => {
    toast.error("Conflito de Edição Detectado", {
      description: "Outro administrador alterou este registro enquanto você editava.",
      action: {
        label: "Atualizar Dados",
        onClick: onReload,
      },
      duration: 10000, // Duração longa para garantir leitura
    });
  };

  return { 
    lastKnownVersion, 
    trackVersion, 
    isConflictError, 
    handleConflict 
  };
}

