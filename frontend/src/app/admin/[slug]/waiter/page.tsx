/**
 * MODULE: WAITER_DASHBOARD
 * VERSION: 4.0 (Unified Gold Master)
 * DNA_ID: MF-WAITER-GRID-V4
 * PURPOSE: Tactical floor view for high-velocity operations.
 * NATURE: UI / Presentation (Dumb Component driven by Smart Hooks)
 */
"use client";

import React, { use, useState } from "react";
import { useRouter } from "next/navigation";
import { 
  Grid, List, Filter, BellRing, Clock, 
  User, DollarSign, Plus, Search, RefreshCw 
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

// --- INTERNAL LIBS ---
import { useWaiterController } from "@/hooks/waiter/useWaiterController";
import { cn, formatCurrency } from "@/lib/utils";
import WaiterBottomNav from "@/components/waiter/WaiterBottomNav";

// --- ATOMIC COMPONENTS (LOCAL) ---

const TableCard = ({ table, onClick }: { table: any, onClick: () => void }) => {
  const isAlert = table.status === 'alert';
  const isPayment = table.status === 'payment';
  const isOccupied = table.status === 'occupied';
  
  // SLA Visual Logic
  const getSLAColor = () => {
    if (!table.active_session?.start_time) return "";
    const minutes = (Date.now() - new Date(table.active_session.start_time).getTime()) / 60000;
    if (minutes > 90) return "border-red-500/50 bg-red-50"; // Crítico (>1h30)
    if (minutes > 60) return "border-orange-500/50 bg-orange-50"; // Atenção (>1h)
    return "border-blue-200 bg-white"; // Normal
  };

  return (
    <motion.button
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      onClick={onClick}
      className={cn(
        "relative flex flex-col justify-between p-4 rounded-3xl border-2 transition-all active:scale-95 h-32 shadow-sm overflow-hidden",
        isAlert ? "bg-red-600 border-red-500 text-white animate-pulse" :
        isPayment ? "bg-purple-600 border-purple-500 text-white" :
        isOccupied ? getSLAColor() :
        "bg-slate-50 border-slate-200 text-slate-400"
      )}
    >
      <div className="flex justify-between items-start w-full relative z-10">
        <span className={cn("text-2xl font-black tracking-tighter", isOccupied ? "text-slate-900" : "text-inherit")}>
          #{table.table_number}
        </span>
        {isAlert && <BellRing size={20} className="fill-current animate-bounce" />}
        {isPayment && <DollarSign size={20} className="fill-current" />}
        {isOccupied && !isAlert && !isPayment && (
          <span className="text-[10px] font-bold bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
            {formatCurrency(table.active_session?.total_spent || 0)}
          </span>
        )}
      </div>
      
      <div className="w-full text-left relative z-10">
        {isOccupied ? (
          <>
            <p className={cn("text-xs font-bold truncate", (isAlert || isPayment) ? "text-white/90" : "text-slate-600")}>
              {table.active_session?.customer_name || "Cliente"}
            </p>
            <div className={cn("flex items-center gap-1 text-[10px] font-mono mt-0.5", (isAlert || isPayment) ? "text-white/70" : "text-slate-400")}>
              <Clock size={10} />
              {new Date(table.active_session?.start_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
            </div>
          </>
        ) : (
          <span className="text-xs font-bold uppercase tracking-widest opacity-50">Livre</span>
        )}
      </div>

      {/* Background Pattern for Occupied */}
      {isOccupied && !isAlert && !isPayment && (
        <div className="absolute bottom-0 right-0 opacity-5 pointer-events-none">
          <User size={64} />
        </div>
      )}
    </motion.button>
  );
};

export default function WaiterPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  const router = useRouter();
  
  // 1. Lógica de Negócio (Controller)
  const { tables, stats, loading, filter, setFilter, actions } = useWaiterController(slug);
  
  // 2. Estado de UI Local
  const [searchTerm, setSearchTerm] = useState("");
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // --- HAPTICS ---
  const handleTableClick = (tableId: number) => {
    if (navigator.vibrate) navigator.vibrate(50);
    router.push(`/admin/${slug}/waiter/pos/${tableId}`);
  };

  // --- FILTERING ---
  const filteredTables = tables.filter(t => {
    const matchesSearch = t.table_number.toString().includes(searchTerm) || 
                          t.active_session?.customer_name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  return (
    <div className="min-h-screen bg-slate-100 pb-32 font-sans selection:bg-orange-500 selection:text-white">
      <Toaster position="top-center" />
      
      {/* HEADER FIXO (Sticky) */}
      <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 p-4 shadow-sm transition-all">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-xl font-black uppercase tracking-tight text-slate-900">Salão</h1>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
              {stats.occupied} Ocupadas • {stats.alerts} Chamados
            </p>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={actions.refresh} 
              className="p-2 bg-slate-100 rounded-xl text-slate-600 hover:bg-slate-200 active:rotate-180 transition-all"
            >
              <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
            </button>
            <button 
              onClick={() => setViewMode(v => v === 'grid' ? 'list' : 'grid')} 
              className="p-2 bg-slate-100 rounded-xl text-slate-600 hover:bg-slate-200 active:scale-95 transition-transform"
            >
              {viewMode === 'grid' ? <List size={20} /> : <Grid size={20} />}
            </button>
          </div>
        </div>

        {/* BARRA DE FILTROS & BUSCA */}
        <div className="flex gap-2 overflow-x-auto no-scrollbar pb-1 items-center">
          <div className="relative flex-1 min-w-[140px]">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Buscar mesa..." 
              className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-9 pr-3 py-2.5 text-xs font-bold focus:border-orange-500 outline-none transition-colors text-slate-900 placeholder:text-slate-400"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
          <button 
            onClick={() => setFilter('ALL')}
            className={cn(
              "px-4 py-2.5 rounded-xl text-xs font-black uppercase transition-all whitespace-nowrap shadow-sm",
              filter === 'ALL' ? "bg-slate-900 text-white" : "bg-white border border-slate-200 text-slate-500"
            )}
          >
            Todas
          </button>
          <button 
            onClick={() => setFilter('ALERTS')}
            className={cn(
              "px-4 py-2.5 rounded-xl text-xs font-black uppercase transition-all whitespace-nowrap flex items-center gap-1 shadow-sm",
              filter === 'ALERTS' ? "bg-red-600 text-white animate-pulse" : "bg-white border border-slate-200 text-slate-500"
            )}
          >
            <BellRing size={12} /> Atenção
          </button>
        </div>
      </header>

      {/* GRID DE MESAS */}
      <main className="p-4">
        {loading && tables.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <RefreshCw className="animate-spin text-orange-500" size={32} />
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Sincronizando...</p>
          </div>
        ) : (
          <div className={cn("grid gap-3", viewMode === 'grid' ? "grid-cols-2 md:grid-cols-3 lg:grid-cols-4" : "grid-cols-1")}>
            <AnimatePresence mode="popLayout">
              {filteredTables.map(table => (
                <TableCard 
                  key={table.id} 
                  table={table} 
                  onClick={() => handleTableClick(table.id)}
                />
              ))}
            </AnimatePresence>
            
            {/* BOTÃO DE VENDA RÁPIDA (BALCÃO) */}
            <button
              onClick={() => router.push(`/admin/${slug}/waiter/pos/quick`)}
              className="flex flex-col justify-center items-center p-4 rounded-3xl border-2 border-dashed border-slate-300 text-slate-400 hover:bg-slate-50 active:scale-95 transition-all h-32 group"
            >
              <div className="bg-slate-200 p-3 rounded-full mb-2 group-hover:bg-orange-100 group-hover:text-orange-600 transition-colors">
                <Plus size={24} />
              </div>
              <span className="text-xs font-black uppercase tracking-widest group-hover:text-orange-600 transition-colors">Venda Rápida</span>
            </button>
          </div>
        )}
        
        {filteredTables.length === 0 && !loading && (
          <div className="text-center py-20 text-slate-400">
            <p className="font-medium">Nenhuma mesa encontrada.</p>
          </div>
        )}
      </main>

      <WaiterBottomNav slug={slug} />
    </div>
  );
}
