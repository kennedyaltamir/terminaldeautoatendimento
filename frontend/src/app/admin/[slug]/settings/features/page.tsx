"use client";

import React from "react";
import { useFeatureFlags } from "@/context/FeatureFlagContext";
import { Zap, ShieldAlert, Loader2, Info, Lock } from "lucide-react";
import { Toaster } from "sonner";
import FeatureToggleCard from "@/components/admin/FeatureToggleCard";

/**
 * Mapeamento de metadados para exibição amigável das flags.
 */
const FLAG_METADATA: Record<string, { label: string; desc: string }> = {
  "fiscal_module_v2": {
    label: "Módulo Fiscal v2 (Homologação)",
    desc: "Habilita a emissão real de NFC-e com suporte a múltiplos certificados A1."
  },
  "ifood_sync_v2": {
    label: "Sincronização de Cardápio iFood",
    desc: "Sincroniza preços e disponibilidade com o portal do iFood em tempo real."
  },
  "ai_demand_prediction": {
    label: "IA: Previsão de Demanda",
    desc: "Algoritmo preditivo para sugestão de compras baseado em sazonalidade."
  }
};

export default function FeaturesBetaPage() {
  const { flags, isImpersonator, toggleFlag, loading } = useFeatureFlags();
  
  // FIX: Removido useState/useEffect desnecessário que causava loop de renderização.
  // O estado de loading já vem do contexto.

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-gray-500">
        <Loader2 className="animate-spin mb-4" size={32} />
        <p className="font-medium">Carregando configurações de rede...</p>
      </div>
    );
  }

  // GUARD DE SEGURANÇA: Bloqueio total se não for suporte
  if (!isImpersonator) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in">
        <div className="bg-red-900/20 p-6 rounded-full text-red-500 mb-6 border border-red-900/30">
          <Lock size={48} />
        </div>
        <h1 className="text-2xl font-bold text-white mb-2">Acesso Restrito</h1>
        <p className="text-gray-400 max-w-md">
          Esta área é destinada exclusivamente à equipe de suporte técnico do MesaFlow para ativação de recursos Beta.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <Toaster position="top-right" richColors />
      
      <div className="flex items-center gap-3">
        <div className="bg-orange-600 p-3 rounded-xl shadow-lg shadow-orange-900/20">
          <Zap size={24} className="text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Funcionalidades Beta</h1>
          <p className="text-gray-400 text-sm">Controle de Canary Releases e módulos experimentais.</p>
        </div>
      </div>

      <div className="bg-red-900/20 border border-red-800 p-4 rounded-xl flex gap-3 items-start">
        <ShieldAlert className="text-red-500 shrink-0 mt-0.5" size={20} />
        <div className="text-sm">
          <p className="text-red-200 font-bold uppercase tracking-wider">Modo Suporte Ativo</p>
          <p className="text-red-300/80">
            Alterações nestas chaves afetam a operação do cliente imediatamente. 
            Certifique-se de que o lojista está ciente dos riscos de recursos experimentais.
          </p>
        </div>
      </div>

      <div className="grid gap-4">
        {Object.keys(flags).length === 0 ? (
          <div className="text-center py-12 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700 text-gray-500">
            Nenhuma flag configurada para este tenant.
          </div>
        ) : (
          Object.entries(flags).map(([key, isEnabled]) => {
            const meta = FLAG_METADATA[key] || { label: key, desc: "Funcionalidade sem descrição técnica." };
            return (
              <FeatureToggleCard
                key={key}
                flagKey={key}
                label={meta.label}
                description={meta.desc}
                isEnabled={isEnabled}
                isImpersonator={isImpersonator}
                onToggle={toggleFlag}
              />
            );
          })
        )}
      </div>

      <div className="bg-blue-900/10 border border-blue-800/30 p-4 rounded-xl flex gap-3">
        <Info className="text-blue-400 shrink-0" size={18} />
        <p className="text-xs text-blue-300/70 leading-relaxed">
          As Feature Flags são persistidas no banco de dados e possuem cache de 5 minutos no servidor. 
          A invalidação do cache ocorre automaticamente após qualquer alteração nesta tela.
        </p>
      </div>
    </div>
  );
}

