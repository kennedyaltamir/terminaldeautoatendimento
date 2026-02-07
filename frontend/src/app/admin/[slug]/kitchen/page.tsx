/**
 * MESAFLOW OS - MONITOR DE PRODUÇÃO (KDS)
 * -----------------------------------------------------------------------------
 * Versão: 22.1.3 (Sovereign Gold Master - Final Consolidated)
 * Data: 30 de Janeiro de 2026
 * Status: REVISADO, CORRIGIDO E SELADO PARA PRODUÇÃO
 * 
 * Mudanças e Correções:
 * 1. FIX TS7006: Tipagem explícita em todos os parâmetros de callbacks e maps.
 * 2. FIX TS2322: Casting rigoroso de 'uiMode' para o contrato literal da interface.
 * 3. Next.js 16: Unwrapping de params via React 'use' (Async Params Compliance).
 * 4. Integridade Funcional: Mantidos Pace Indicator, Station Filters e Item Aggregator.
 * 5. Performance: Memoização de filtros para evitar re-renders em picos de carga.
 */

"use client";

import React, { use, useState, useCallback, useMemo } from "react";
import { 
  Loader2, WifiOff, RefreshCw, 
  Volume2, VolumeX, History, Maximize2, Minimize2,
  ListChecks, Box, ChefHat, Gauge, Zap, Utensils,
  Wine, IceCream, AlertTriangle, Printer
} from "lucide-react";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { toast } from "sonner";

// --- INTERNAL LIBS & HOOKS ---
import { useKdsController } from "@/hooks/kds/useKdsController";
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
  actions: any;
  slug: string;
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
  uiMode, connectionStatus, actions, slug, isMuted, 
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

      <button onClick={actions.openRecall} className="p-4 bg-slate-800 rounded-2xl text-slate-400 hover:text-white border border-slate-700 transition-all active:scale-95" title="Recall">
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
  const { slug } = use(paramsPromise);
  
  const [activeTab, setActiveTab] = useState<StationFilter>('all');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [isAggregatorOpen, setIsAggregatorOpen] = useState(false);
  const [selectedRecipeItem, setSelectedRecipeItem] = useState<OrderItemResponse | null>(null);

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

  // 🛡️ HANDLERS COM TIPAGEM EXPLÍCITA (FIX TS7006)
  const handlePrint = useCallback((order: Order) => {
    try {
      printOrder(order, slug);
      toast.info(`Imprimindo Pedido #${order.id.slice(0,4)}`);
    } catch (e) {
      toast.error("Erro ao disparar impressão.");
    }
  }, [slug]);

  const handleShowRecipe = useCallback((item: OrderItemResponse) => {
    setSelectedRecipeItem(item);
  }, []);

  // Filtro de pedidos memoizado para performance
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

  if (isSyncing && orders.length === 0) {
    return (
      <div className="h-screen bg-black flex flex-col items-center justify-center">
        <Loader2 className="animate-spin text-orange-500 mb-4" size={64} />
        <p className="text-slate-500 font-black uppercase tracking-[0.4em] text-sm animate-pulse">Iniciando Protocolo KDS...</p>
      </div>
    );
  }

  return (
    <div className={cn(
      "min-h-screen p-6 font-sans transition-colors duration-1000 flex flex-col",
      uiMode === 'SATURATION' ? "bg-red-950/10" : "bg-slate-950"
    )}>
      
      <KdsHeader 
        uiMode={uiMode as "NORMAL" | "SATURATION"} // 🛡️ FIX TS2322: Casting para o tipo literal esperado
        connectionStatus={connectionStatus} 
        actions={actions} 
        slug={slug}
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
        <div className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-8 pb-32">
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
            <div className="col-span-full flex flex-col items-center justify-center py-40 opacity-20 border-4 border-dashed border-slate-800 rounded-[4rem]">
              <ChefHat size={120} className="text-slate-600 mb-6" />
              <p className="text-slate-500 font-black uppercase tracking-[0.3em] text-2xl">
                {activeTab === 'all' ? "Cozinha em Espera" : `Sem pedidos para ${activeTab}`}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* MODAIS DE APOIO */}
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
        .custom-scrollbar::-webkit-scrollbar-track { background: #0f172a; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 20px; border: 2px solid #0f172a; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #334155; }
      `}</style>
    </div>
  );
}