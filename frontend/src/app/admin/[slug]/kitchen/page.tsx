/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 22.3.0 (Audio Unlock & Production Sealed)
 * DNA_ID: MF-KDS-CORE-V22-3
 * OBJETIVO: Monitor de Produção (KDS) de alta performance.
 * Comportamento esperado: 
 *  1. Rito de Ativação: Exige interação inicial para habilitar áudio (Autoplay Policy).
 *  2. FSM Integration: Sincronia determinística de estados via useKdsController.
 *  3. BI Tático: Pace Indicator e Vazão em tempo real.
 *  4. Filtros de Estação: Separação lógica entre Cozinha, Bar e Doces.
 */

"use client";

import React, { use, useState, useCallback, useMemo, useEffect } from "react";
import { 
  Loader2, WifiOff, RefreshCw, 
  Volume2, VolumeX, History, Maximize2, Minimize2,
  ListChecks, Box, ChefHat, Gauge, Zap, Utensils,
  Wine, IceCream, Play, Printer, Info
} from "lucide-react";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { toast } from "sonner";

// --- INTERNAL LIBS & HOOKS ---
import { useKdsController } from "@/hooks/kds/useKdsController";
import { audioManager } from "@/lib/kds/audio-engine";
import { printOrder } from "@/lib/printer/driver";
import { Order, OrderItemResponse } from "@/types";

// --- COMPONENTS ---
import OrderCard from "@/components/admin/KDS/OrderCard";
import RecallModal from "@/components/admin/KDS/RecallModal";
import StockModal from "@/components/admin/StockModal";
import ItemAggregator from "@/components/admin/KDS/ItemAggregator";
import RecipeViewModal from "@/components/admin/KDS/RecipeViewModal";

// --- TYPES ---
type StationFilter = 'all' | 'kitchen' | 'bar' | 'dessert';

interface KdsHeaderProps {
  uiMode: 'NORMAL' | 'SATURATION';
  connectionStatus: string;
  actions: {
    refresh: () => void;
    toggleMute: () => void;
    getMuteState: () => boolean;
    openRecall: () => void;
  };
  isMuted: boolean;
  activeTab: StationFilter;
  setActiveTab: (tab: StationFilter) => void;
  toggleFullscreen: () => void;
  isFullscreen: boolean;
  onOpenStock: () => void;
  onOpenAggregator: () => void;
  pace: {
    avgTime: number;
    ordersPerHour: number;
  };
}

// --- SUB-COMPONENT: PACE INDICATOR (BI Tático) ---
const PaceIndicator = ({ pace }: { pace: { avgTime: number; ordersPerHour: number } }) => (
  <div className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 px-5 py-2.5 rounded-2xl shadow-2xl backdrop-blur-md">
    <div className="flex flex-col">
      <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1">
        <Gauge size={10} className="text-orange-500" /> Ritmo (30m)
      </span>
      <div className="flex items-baseline gap-1">
        <span className="text-xl font-black text-white">{pace.avgTime}</span>
        <span className="text-[9px] font-bold text-slate-500 uppercase">min</span>
      </div>
    </div>
    <div className="w-px h-8 bg-slate-800" />
    <div className="flex flex-col">
      <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1">
        <Zap size={10} className="text-yellow-500" /> Vazão
      </span>
      <div className="flex items-baseline gap-1">
        <span className="text-xl font-black text-white">{pace.ordersPerHour}</span>
        <span className="text-[9px] font-bold text-slate-500 uppercase">ped/h</span>
      </div>
    </div>
  </div>
);

// --- HEADER COMPONENT ---
const KdsHeader = ({ 
  uiMode, connectionStatus, actions, isMuted, 
  activeTab, setActiveTab, toggleFullscreen, isFullscreen,
  onOpenStock, onOpenAggregator, pace
}: KdsHeaderProps) => (
  <header className={cn(
    "flex flex-col xl:flex-row justify-between items-start xl:items-center mb-8 border-b pb-6 transition-all duration-500 gap-6",
    uiMode === 'SATURATION' ? "border-red-800 bg-red-950/20 p-6 rounded-[2.5rem]" : "border-slate-800"
  )}>
    <div className="flex items-center gap-5">
      <div className={cn(
        "p-3.5 rounded-2xl shadow-2xl transition-all",
        uiMode === 'SATURATION' ? "bg-red-600 animate-pulse" : "bg-orange-600"
      )}>
        <ChefHat size={32} className="text-white" />
      </div>
      <div className="space-y-2">
        <h1 className="text-3xl font-black tracking-tighter uppercase text-white flex items-center gap-3">
          Monitor de Produção
          {connectionStatus !== 'LIVE' && <WifiOff className="text-red-500 animate-bounce" size={20} />}
        </h1>
        <div className="flex items-center gap-3">
          <PaceIndicator pace={pace} />
          <span className={cn(
            "text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-widest border",
            connectionStatus === 'LIVE' ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : "bg-red-500/10 text-red-500 border-red-500/20"
          )}>
            {connectionStatus}
          </span>
        </div>
      </div>
    </div>

    <div className="flex bg-slate-900 p-1.5 rounded-2xl border border-slate-800 shadow-inner">
      {(['all', 'kitchen', 'bar', 'dessert'] as StationFilter[]).map((s) => (
        <button
          key={s}
          onClick={() => setActiveTab(s)}
          className={cn(
            "px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all",
            activeTab === s ? "bg-orange-600 text-white shadow-lg" : "text-slate-500 hover:text-slate-300"
          )}
        >
          {s === 'all' ? 'Todos' : s === 'kitchen' ? 'Cozinha' : s === 'bar' ? 'Bar' : 'Doces'}
        </button>
      ))}
    </div>

    <div className="flex gap-2 flex-wrap">
      <button onClick={onOpenAggregator} className="p-4 bg-slate-800 rounded-2xl text-emerald-500 hover:bg-emerald-500/10 border border-slate-700 transition-all active:scale-95" title="Resumo de Itens">
        <ListChecks size={22} />
      </button>
      
      <button onClick={onOpenStock} className="p-4 bg-slate-800 rounded-2xl text-orange-400 hover:bg-orange-500/10 border border-slate-700 transition-all active:scale-95" title="Gestão de Estoque">
        <Box size={22} />
      </button>

      <div className="w-px h-12 bg-slate-800 mx-2 hidden xl:block" />

      <button onClick={actions.openRecall} className="p-4 bg-slate-800 rounded-2xl text-slate-400 hover:text-white border border-slate-700 transition-all active:scale-95" title="Histórico Recente">
        <History size={22} />
      </button>
      
      <button onClick={actions.refresh} className="p-4 bg-slate-800 rounded-2xl text-blue-400 hover:text-white border border-slate-700 transition-all active:scale-95" title="Sincronizar">
        <RefreshCw size={22} />
      </button>
      
      <button onClick={actions.toggleMute} className={cn("p-4 rounded-2xl border transition-all active:scale-95", isMuted ? "bg-red-900/20 border-red-900/50 text-red-500" : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white")}>
        {isMuted ? <VolumeX size={22} /> : <Volume2 size={22} />}
      </button>

      <button onClick={toggleFullscreen} className="p-4 bg-slate-800 rounded-2xl text-slate-400 hover:text-white border border-slate-700 transition-all active:scale-95">
        {isFullscreen ? <Minimize2 size={22} /> : <Maximize2 size={22} />}
      </button>
    </div>
  </header>
);

export default function KitchenPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ Next.js 16 Async Params Unwrap
  const { slug } = use(paramsPromise);
  
  const [activeTab, setActiveTab] = useState<StationFilter>('all');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [isAggregatorOpen, setIsAggregatorOpen] = useState(false);
  const [selectedRecipeItem, setSelectedRecipeItem] = useState<OrderItemResponse | null>(null);
  
  // 🛡️ Audio Unlock State (Compliance with Autoplay Policies)
  const [isAudioUnlocked, setIsAudioUnlocked] = useState(false);

  const { 
    orders, 
    uiMode, 
    connectionStatus, 
    isSyncing, 
    isRecallOpen,
    productionPace,
    actions, 
    helpers 
  } = useKdsController(slug);

  // --- HANDLERS ---
  const handleUnlockAudio = () => {
    audioManager.play('bump'); // Prime o motor de áudio
    setIsAudioUnlocked(true);
    toast.success("Monitor de áudio ativado.", {
      description: "Alertas de novos pedidos habilitados."
    });
  };

  const handlePrint = useCallback((order: Order) => {
    try {
      printOrder(order, slug);
      toast.info(`Imprimindo Cupom: #${order.id.slice(0,4)}`);
    } catch (e) {
      toast.error("Erro ao disparar impressora nativa.");
    }
  }, [slug]);

  const handleShowRecipe = useCallback((item: OrderItemResponse) => {
    setSelectedRecipeItem(item);
  }, []);

  const filteredOrders = useMemo(() => {
    return orders.filter((order: Order) => {
      if (activeTab === 'all') return true;
      return order.items.some((item: OrderItemResponse) => item.product.station === activeTab);
    });
  }, [orders, activeTab]);

  const toggleFullscreen = useCallback(() => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  }, []);

  // --- RENDERING ---
  if (isSyncing && orders.length === 0) {
    return (
      <div className="h-screen bg-black flex flex-col items-center justify-center gap-6">
        <Loader2 className="animate-spin text-orange-500" size={64} />
        <div className="text-center">
            <p className="text-slate-500 font-black uppercase tracking-[0.4em] text-sm">MesaFlow OS</p>
            <p className="text-slate-600 font-bold text-xs mt-2 animate-pulse">Sincronizando protocolo KDS...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn(
      "min-h-screen p-6 font-sans transition-colors duration-1000 flex flex-col",
      uiMode === 'SATURATION' ? "bg-red-950/10" : "bg-slate-950"
    )}>
      
      {/* 🛡️ AUDIO ACTIVATION OVERLAY (Rito de Entrada) */}
      <AnimatePresence>
        {!isAudioUnlocked && (
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[1000] bg-slate-950/95 backdrop-blur-xl flex items-center justify-center p-6"
          >
            <div className="text-center space-y-10 max-w-sm">
              <div className="w-24 h-24 bg-orange-600 rounded-[2.5rem] flex items-center justify-center mx-auto shadow-2xl shadow-orange-900/40 relative">
                <div className="absolute inset-0 rounded-[2.5rem] bg-orange-600 animate-ping opacity-20" />
                <ChefHat size={48} className="text-white relative z-10" />
              </div>
              <div className="space-y-3">
                  <h2 className="text-3xl font-black text-white uppercase tracking-tighter">Preparar para o Turno</h2>
                  <p className="text-slate-400 text-sm font-medium leading-relaxed">
                    A política de segurança exige uma interação para ativar os alertas sonoros. Clique abaixo para assumir o monitor.
                  </p>
              </div>
              <button 
                onClick={handleUnlockAudio}
                className="w-full bg-white text-slate-950 py-5 rounded-3xl font-black uppercase tracking-widest text-sm flex items-center justify-center gap-3 shadow-xl hover:bg-slate-100 active:scale-95 transition-all"
              >
                <Play size={20} fill="currentColor" /> INICIAR MONITORAMENTO
              </button>
              <div className="flex items-center justify-center gap-2 text-slate-600">
                  <Info size={14} />
                  <span className="text-[10px] font-bold uppercase tracking-widest">Sovereign Edition v22.3</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <KdsHeader 
        uiMode={uiMode as "NORMAL" | "SATURATION"} 
        connectionStatus={connectionStatus} 
        actions={{
            refresh: actions.refresh,
            toggleMute: actions.toggleMute,
            getMuteState: actions.getMuteState,
            openRecall: actions.openRecall
        }} 
        isMuted={actions.getMuteState()}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        toggleFullscreen={toggleFullscreen}
        isFullscreen={isFullscreen}
        onOpenStock={() => setIsStockOpen(true)}
        onOpenAggregator={() => setIsAggregatorOpen(true)}
        pace={productionPace}
      />

      <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
        <div className="grid grid-cols-[repeat(auto-fill,minmax(340px,1fr))] gap-8 pb-32">
          <AnimatePresence mode="popLayout">
            {filteredOrders.map((order: Order) => (
              <motion.div 
                key={order.id} 
                layout 
                initial={{ opacity: 0, scale: 0.9 }} 
                animate={{ opacity: 1, scale: 1 }} 
                exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
              >
                <OrderCard 
                  order={order} 
                  complexity={helpers.calculateComplexity(order)} 
                  activeStation={activeTab}
                  onAction={() => {
                    if (order.status === 'pending') actions.acceptOrder(order);
                    else actions.completeOrder(order);
                  }} 
                  onPrint={handlePrint}
                  onShowRecipe={handleShowRecipe}
                  onExhaustProduct={actions.exhaustProduct}
                />
              </motion.div>
            ))}
          </AnimatePresence>
          
          {filteredOrders.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-40 opacity-10 border-4 border-dashed border-slate-800 rounded-[4rem]">
              <ChefHat size={120} className="text-slate-600 mb-6" />
              <p className="text-slate-500 font-black uppercase tracking-[0.3em] text-2xl">
                Aguardando Comandas
              </p>
            </div>
          )}
        </div>
      </div>

      {/* MODAL LAYER */}
      <RecallModal 
        isOpen={isRecallOpen} 
        onClose={actions.closeRecall} 
        slug={slug} 
        onRestore={actions.refresh} 
      />

      <StockModal 
        isOpen={isStockOpen} 
        onClose={() => setIsStockOpen(false)} 
      />

      <ItemAggregator 
        isOpen={isAggregatorOpen} 
        onClose={() => setIsAggregatorOpen(false)} 
        orders={orders} 
        activeStation={activeTab}
      />

      <RecipeViewModal 
        item={selectedRecipeItem} 
        onClose={() => setSelectedRecipeItem(null)} 
      />
      
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar { width: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 20px; border: 2px solid #020617; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #334155; }
      `}</style>
    </div>
  );
}