"use client";

/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 13.7 (Unified Gold Master - Consolidated)
 * DNA_ID: MF-DASHBOARD-V13-7-GOLD
 * Objective: Sovereign Command Center with Type-Safe BI, Scenario Simulation, and L7 Governance.
 * Fixes: TS2339 (total_revenue), Next.js 16 Async Params, and FSM State Sync.
 */

import React, { use, useState, useEffect, useCallback, useMemo } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { 
  TrendingUp, ShieldCheck, Settings2, Sparkles, 
  Database, Zap, Lightbulb, Activity, DollarSign
} from "lucide-react";

// --- INTERNAL LIB & HOOKS ---
import { useDashboardFSM } from "@/hooks/useDashboardFSM";
import { useDecisionAuthority } from "@/hooks/useDecisionAuthority";
import { useDashboardStats } from "@/hooks/useDashboardStats";
import { useBIEngine } from "@/hooks/useBIEngine";
import { cn, formatCurrency } from "@/lib/utils";
import { Metrics, DashboardMode } from "@/types";

// --- COMPONENTS ---
import DashboardSkeleton from "@/components/admin/DashboardSkeleton";
import KPICard from "@/components/admin/BI/KPICard";
import AdaptiveChart from "@/components/admin/BI/AdaptiveChart";
import ScenarioSimulator from "@/components/admin/BI/ScenarioSimulator";
import AlertPanel from "@/components/admin/BI/AlertPanel";
import DrillDownModal from "@/components/admin/BI/DrillDownModal";

export default function DashboardPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ PROTOCOLO NEXT 16: Unwrapping obrigatório da Promise de params
  const { slug } = use(paramsPromise);
  const router = useRouter();
  
  // 🛡️ SCOPE GUARD: Impede execução se o contexto for inválido
  const isValidContext = slug && slug !== "undefined";
  
  // Hooks de Estado e Dados
  const { state } = useDashboardFSM();
  const { metrics, loading, period, setPeriod, handleExport } = useDashboardStats(isValidContext ? slug : "");
  
  // Estados Locais
  const [mode, setMode] = useState<DashboardMode>('BUSINESS');
  const [selectedPoint, setSelectedPoint] = useState<any>(null);
  const [simulation, setSimulation] = useState({
    ticketMultiplier: 1,
    volumeMultiplier: 1,
    deliveryShare: 0.65
  });

  // Motor de BI e Autoridade de Decisão
  const bi = useBIEngine(metrics, simulation);
  const confidence = useMemo(() => 
    metrics?.margin_confidence_index ? metrics.margin_confidence_index * 100 : 100
  , [metrics]);
  const { authority } = useDecisionAuthority(state, confidence);

  // 🛡️ FIX: Acesso seguro à propriedade correta do objeto Metrics (TS2339 Resolved)
  const revenueForSimulation = metrics?.business_kpis?.revenue_today || 0;

  const getDailyStory = useCallback((trend: number) => {
    if (trend > 15) return "🚀 Hoje você está vendendo muito acima da média!";
    if (trend > 0) return "📈 Crescimento constante em relação a ontem.";
    if (trend > -10) return "🛡️ Dia de estabilidade. Foco em manter a margem.";
    return "⚠️ Atenção ao movimento. Hora de ativar promoções?";
  }, []);

  if (!isValidContext) return null;
  if (loading) return <DashboardSkeleton />;

  return (
    <div className="min-h-screen bg-black p-4 md:p-8 space-y-8 font-sans selection:bg-orange-500">
      {/* HEADER SOBERANO */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-900 pb-8 gap-4">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tighter uppercase">
            {mode === 'BUSINESS' ? 'Painel de ' : 'Governança '}
            <span className="text-orange-500">{mode === 'BUSINESS' ? 'Comando' : 'Técnica'}</span>
          </h1>
          <div className="flex items-center gap-3 mt-2">
            {mode === 'BUSINESS' ? (
              <div className="flex items-center gap-2 animate-in fade-in slide-in-from-left-2">
                <Sparkles size={12} className="text-orange-500" />
                <span className="text-xs font-bold text-slate-400">
                  {metrics?.business_kpis 
                    ? getDailyStory(metrics.business_kpis.revenue_change_pct || 0) 
                    : "Sincronizando inteligência..."}
                </span>
              </div>
            ) : (
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest flex items-center gap-2">
                <Database size={12} className="text-blue-500" />
                Kernel Snapshot: {metrics?.snapshot_id?.slice(0,8) || 'LOCAL'} | {metrics?.kernel_time || 'LIVE'}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800">
            {['today', '7d', '30d'].map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p as any)}
                className={cn(
                  "px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all",
                  period === p ? "bg-orange-600 text-white shadow-lg" : "text-slate-500 hover:text-slate-300"
                )}
              >
                {p}
              </button>
            ))}
          </div>

          <button 
            onClick={() => setMode(mode === 'BUSINESS' ? 'GOVERNANCE' : 'BUSINESS')}
            className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl text-[10px] font-black text-slate-400 hover:text-white transition-all hover:border-slate-700"
          >
            <Settings2 size={14} /> {mode === 'BUSINESS' ? 'MODO TÉCNICO' : 'MODO COMERCIAL'}
          </button>

          <div className={cn(
            "px-3 py-1 rounded-full border text-[9px] font-black uppercase tracking-widest", 
            confidence > 90 ? "text-emerald-500 border-emerald-500/20 bg-emerald-500/5" : "text-red-500 border-red-500/20 bg-red-500/5"
          )}>
            {authority.statusLabel}
          </div>
        </div>
      </header>

      <AlertPanel alerts={bi?.alerts || []} />

      <AnimatePresence mode="wait">
        {mode === 'BUSINESS' ? (
          <motion.div 
            key="biz" 
            initial={{ opacity: 0, y: 10 }} 
            animate={{ opacity: 1, y: 0 }} 
            exit={{ opacity: 0, y: -10 }} 
            className="space-y-8"
          >
            {/* L1: KPIs PRINCIPAIS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <KPICard 
                title="Receita Total" 
                value={formatCurrency(bi?.simulatedRevenue || 0)} 
                trend={metrics?.business_kpis?.revenue_change_pct || 0} 
                variant="hero"
                isSimulated={simulation.ticketMultiplier !== 1 || simulation.volumeMultiplier !== 1}
              />
              <KPICard 
                title="Pedidos" 
                value={bi?.simulatedOrders || 0} 
                trend={5.4} 
              />
              <KPICard 
                title="Ticket Médio" 
                value={formatCurrency(metrics?.business_kpis?.avg_ticket || 0)} 
                trend={-1.2} 
              />
            </div>

            {/* L2: ANALYTICS & SIMULATION */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8 bg-slate-900/50 border border-slate-800 p-8 rounded-[3rem] shadow-2xl relative overflow-hidden">
                <div className="flex justify-between items-center mb-10">
                  <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                    <TrendingUp size={16} className="text-orange-500" /> Performance de Vendas
                  </h3>
                  {authority.showWatermark && (
                    <span className="text-[9px] font-black text-orange-500 animate-pulse uppercase tracking-[0.3em]">
                      Modo Simulação Ativo
                    </span>
                  )}
                </div>
                <AdaptiveChart 
                  data={bi?.channelData || []} 
                  viewMode="total" 
                  onPointClick={setSelectedPoint}
                />
              </div>

              <div className="lg:col-span-4 space-y-6">
                <ScenarioSimulator 
                  simulation={simulation} 
                  setSimulation={setSimulation} 
                  baseRevenue={revenueForSimulation}
                />
                <div className="bg-orange-600 p-8 rounded-[2.5rem] text-white shadow-2xl shadow-orange-900/20 relative overflow-hidden group">
                  <Zap size={80} className="absolute -right-4 -bottom-4 opacity-20 group-hover:scale-110 transition-transform" />
                  <h4 className="font-black text-xl mb-2 uppercase tracking-tighter flex items-center gap-2">
                    <Lightbulb size={20} /> Insights de IA
                  </h4>
                  <p className="text-orange-100 text-sm font-medium leading-relaxed">
                    {metrics?.insights?.[0]?.message || "Analisando padrões de consumo para gerar recomendações táticas..."}
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            key="gov" 
            initial={{ opacity: 0, scale: 0.95 }} 
            animate={{ opacity: 1, scale: 1 }} 
            exit={{ opacity: 0, scale: 0.95 }} 
            className="space-y-8"
          >
            {/* L3: CAMADA DE GOVERNANÇA (Técnica) */}
            <div className="bg-slate-900 border border-slate-800 p-8 rounded-[3rem] shadow-2xl">
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-xl font-black text-white flex items-center gap-3">
                  <ShieldCheck className="text-blue-500" /> Auditoria de Integridade L7
                </h2>
                <button 
                  onClick={handleExport}
                  disabled={!authority.canExport}
                  className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
                >
                  Exportar Log Forense
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="p-6 rounded-3xl bg-black/40 border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Margem Líquida Auditada</p>
                  <h3 className="text-3xl font-mono text-emerald-500 tracking-tighter">
                    {formatCurrency(metrics?.net_margin_value || 0)}
                  </h3>
                  <p className="text-[10px] text-slate-600 mt-2">Baseado no Ledger Imutável</p>
                </div>
                <div className="p-6 rounded-3xl bg-black/40 border border-red-900/30">
                  <p className="text-[10px] font-black text-red-500 uppercase tracking-widest mb-2">SLA Debt (Técnico)</p>
                  <h3 className="text-3xl font-mono text-red-500 tracking-tighter">
                    {formatCurrency(metrics?.accumulated_sla_debt || 0)}
                  </h3>
                  <p className="text-[10px] text-slate-600 mt-2">Latência acumulada convertida</p>
                </div>
                <div className="p-6 rounded-3xl bg-black/40 border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Estado do FSM</p>
                  <h3 className="text-xl font-mono text-blue-400 uppercase">{state}</h3>
                  <p className="text-[10px] text-slate-600 mt-2">Máquina de Estados Ativa</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <DrillDownModal 
        isOpen={!!selectedPoint} 
        onClose={() => setSelectedPoint(null)} 
        data={selectedPoint} 
      />
    </div>
  );
}
