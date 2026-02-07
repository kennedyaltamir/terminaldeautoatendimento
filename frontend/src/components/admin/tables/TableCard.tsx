/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Card de mesa (Visual Layer).
 * FIX: Adicionado import faltante de 'Clock'.
 */
"use client";
import { TableDashboard } from "@/types";
import { QRCodeSVG } from "qrcode.react";
import { 
  BellRing, Lock, Hash, 
  DollarSign, Users, Hourglass, Clock // FIX: Import adicionado
} from "lucide-react";
import { cn, formatCurrency } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

interface TableCardProps {
  table: TableDashboard;
  slug: string;
  onClick: () => void;
  onResolveAlert?: (id: number) => void;
  isIncidentMode?: boolean;
}

export default function TableCard({ 
  table, 
  slug, 
  onClick, 
  onResolveAlert, 
  isIncidentMode = false 
}: TableCardProps) {
  // Derivação de Estados
  const isOccupied = table.status === 'occupied';
  const isAlert = table.status === 'alert';
  const isPreparing = table.status === 'preparing';
  const isPayment = table.status === 'payment';
  
  const tableUrl = `${window.location.origin}/${slug}/menu?table=${table.table_number}&token=${table.qr_token}`;

  // Lógica de Cor de Fundo
  const getBgColor = () => {
    if (isAlert) return "bg-red-950/20 border-red-500 ring-4 ring-red-500/20";
    if (isPayment) return "bg-purple-900/20 border-purple-500 shadow-lg shadow-purple-900/20";
    if (isPreparing) return "bg-yellow-900/10 border-yellow-500/50 border-dashed";
    if (isOccupied) return "bg-slate-900 border-orange-500/50 shadow-2xl shadow-orange-900/20";
    return "bg-white dark:bg-slate-900 border-slate-100 dark:border-slate-800 hover:border-orange-500/30 shadow-xl";
  };

  const isDimmed = isIncidentMode && !isAlert && !isPayment;

  return (
    <div 
      onClick={onClick}
      className={cn(
        "group cursor-pointer rounded-[2.5rem] border-2 relative overflow-hidden flex flex-col h-full transition-all duration-300",
        "hover:-translate-y-1 hover:shadow-2xl", // Efeito Hover via CSS
        getBgColor(),
        isDimmed && "opacity-40 grayscale"
      )}
    >
      {/* Overlay de Alerta (Mantido Motion apenas para o pulso interno) */}
      <AnimatePresence>
        {isAlert && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="absolute inset-0 bg-red-500/10 pointer-events-none animate-pulse z-0"
          />
        )}
      </AnimatePresence>

      <div className="p-6 flex flex-col h-full relative z-10">
        {/* HEADER DO CARD */}
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center gap-2">
            <span className={cn(
              "text-3xl font-black tracking-tighter", 
              isOccupied || isPayment || isAlert ? "text-white" : "text-slate-900 dark:text-white"
            )}>
              #{table.table_number}
            </span>
            
            {/* Badge de Capacidade */}
            <div className={cn(
              "flex items-center gap-1 px-2 py-0.5 rounded-full border",
              isOccupied ? "bg-slate-800/50 border-slate-700/50" : "bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700"
            )}>
                <Users size={10} className="text-slate-400" />
                <span className="text-[10px] font-bold text-slate-500 dark:text-slate-300">
                    {table.active_session?.people_count || 0}/{table.capacity || 4}
                </span>
            </div>
          </div>

          {/* Ícone de Status */}
          {isAlert ? (
            <button 
              onClick={(e) => { e.stopPropagation(); onResolveAlert?.(table.id); }}
              className="bg-red-600 text-white p-2 rounded-full shadow-lg hover:bg-red-500 transition-all active:scale-90 z-20"
              title="Atender Chamado"
            >
              <BellRing size={20} className="animate-bounce" />
            </button>
          ) : isPayment ? (
            <div className="bg-purple-500 p-2 rounded-full text-white animate-pulse shadow-lg shadow-purple-500/40">
                <DollarSign size={18} />
            </div>
          ) : isPreparing ? (
            <div className="bg-yellow-500/20 p-2 rounded-full text-yellow-500 border border-yellow-500/30">
                <Hourglass size={18} />
            </div>
          ) : (
            <div className={cn("w-2.5 h-2.5 rounded-full", isOccupied ? "bg-orange-500 animate-pulse" : "bg-emerald-500")} />
          )}
        </div>

        {/* QR CODE */}
        {!isIncidentMode && !isOccupied && !isPayment && (
            <div className="bg-white p-3 rounded-3xl shadow-inner mb-auto self-center border border-slate-100 group-hover:scale-105 transition-transform duration-300">
              <QRCodeSVG value={tableUrl} size={100} level="M" />
            </div>
        )}

        {/* CORPO DO CARD */}
        <div className="flex-1 flex flex-col justify-end space-y-3 mt-4">
          {table.active_session ? (
            <div className={cn(
                "rounded-2xl p-4 space-y-2 transition-colors",
                isPayment ? "bg-purple-600/10 border border-purple-500/20" : 
                isPreparing ? "bg-yellow-600/10 border border-yellow-500/20" :
                "bg-orange-600/10 border border-orange-500/20"
            )}>
              <div className="flex items-center justify-between">
                <span className={cn(
                  "text-[10px] font-black uppercase truncate max-w-[100px]", 
                  isPayment ? "text-purple-400" : 
                  isPreparing ? "text-yellow-400" : "text-orange-500"
                )}>
                  {table.active_session.customer_name}
                </span>
                <span className="text-lg font-black text-white">
                  {formatCurrency(table.active_session.total_spent)}
                </span>
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t border-white/5">
                 <div className="flex items-center gap-1 text-slate-400 text-[9px] font-bold">
                   <Lock size={10} className={isPayment ? "text-purple-500" : "text-orange-500"} /> 
                   PIN: {table.active_session.access_pin}
                 </div>
                 <div className="flex items-center gap-1 text-slate-400 text-[9px] font-bold">
                   <Clock size={10} /> 
                   {new Date(table.active_session.start_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
                 </div>
              </div>
            </div>
          ) : (
            <div className="h-20 flex flex-col items-center justify-center text-slate-500 opacity-30 border-2 border-dashed border-slate-800 rounded-2xl">
              <Hash size={20} className="mb-1" />
              <span className="text-[9px] font-black uppercase tracking-widest">
                {isPreparing ? "Aguardando..." : "Mesa Livre"}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}