/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 21.0.1 (Reference Fix)
 * DNA_ID: MF-KDS-CARD-V21-FIX
 * Objective: Corrigir ReferenceError do ícone Info e garantir estabilidade visual.
 */

"use client";

import React, { useEffect, useState } from 'react';
import { Order, OrderItemResponse } from '@/types';
import { cn } from '@/lib/utils';
import { 
  MapPin, Smartphone, Monitor, Layout, 
  Play, CheckCircle2, Clock, AlertCircle, 
  Printer, List, User, Bike, Ban, Zap,
  Info // 🛡️ FIX: Import adicionado para resolver ReferenceError
} from 'lucide-react';
import { motion } from "framer-motion";
import OrderTimer from '../OrderTimer';

interface OrderCardProps {
  order: Order & { isOptimistic?: boolean };
  complexity: number;
  onAction: () => void;
  onPrint: (order: Order) => void;
  onShowRecipe: (item: OrderItemResponse) => void;
  onExhaustProduct: (id: number, name: string) => void;
  activeStation?: string;
}

export default function OrderCard({ 
  order, 
  complexity, 
  onAction, 
  onPrint,
  onShowRecipe,
  onExhaustProduct,
  activeStation = 'all' 
}: OrderCardProps) {
  const [elapsedMinutes, setElapsedMinutes] = useState(0);
  const SLA_TARGET = 20;

  useEffect(() => {
    const start = new Date(order.created_at).getTime();
    const tick = () => setElapsedMinutes(Math.floor((Date.now() - start) / 60000));
    tick();
    const timer = setInterval(tick, 30000);
    return () => clearInterval(timer);
  }, [order.created_at]);

  const progress = Math.min((elapsedMinutes / SLA_TARGET) * 100, 100);
  const isOverdue = elapsedMinutes >= SLA_TARGET;
  const urgencyColor = isOverdue 
    ? "bg-red-600 shadow-[0_0_20px_rgba(220,38,38,0.5)]" 
    : progress >= 75 ? "bg-orange-500" : "bg-emerald-500";

  const getOriginMeta = (origin: string) => {
    const map: any = {
      kiosk: { label: "TOTEM", icon: Layout, theme: "text-purple-400 bg-purple-400/10 border-purple-400/20" },
      admin: { label: "BALCÃO", icon: Monitor, theme: "text-blue-400 bg-blue-400/10 border-blue-400/20" },
      mobile: { label: "MESA", icon: Smartphone, theme: "text-orange-400 bg-orange-400/10 border-orange-400/20" },
      delivery: { label: "DELIVERY", icon: Bike, theme: "text-red-400 bg-red-400/10 border-red-400/20" },
      waiter: { label: "GARÇOM", icon: Zap, theme: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20" }
    };
    return map[origin] || { label: "WEB", icon: User, theme: "text-slate-400 bg-slate-400/10" };
  };

  const meta = getOriginMeta(order.origin || 'mobile');

  return (
    <motion.div 
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        "flex flex-col bg-slate-900 rounded-[2.5rem] overflow-hidden shadow-2xl transition-all relative border border-slate-800 h-full",
        order.status === 'preparing' ? "ring-2 ring-orange-500/40" : "hover:border-slate-700",
        order.isOptimistic && "opacity-50 scale-95 grayscale pointer-events-none",
        isOverdue && "border-red-900/50"
      )}
    >
      {/* 🛡️ BARRA DE SLA SOBERANA */}
      <div className="h-2 w-full bg-slate-800 relative overflow-hidden">
        <motion.div 
          className={cn("h-full rounded-r-full transition-colors duration-500", urgencyColor)}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
        />
      </div>

      {/* HEADER: ORIGEM, IMPRESSÃO E TEMPO */}
      <div className="p-5 flex justify-between items-center bg-slate-800/30 border-b border-slate-800/50">
        <div className={cn("flex items-center gap-2 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border", meta.theme)}>
          <meta.icon size={12} /> {meta.label}
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={(e) => { e.stopPropagation(); onPrint(order); }}
            className="p-2 bg-slate-700 hover:bg-slate-600 text-white rounded-xl transition-all active:scale-90"
            title="Imprimir Ticket"
          >
            <Printer size={16} />
          </button>
          <div className={cn(
            "flex items-center gap-1.5 text-sm font-mono font-black",
            isOverdue ? "text-red-500 animate-pulse" : "text-slate-400"
          )}>
            <Clock size={14} /> {elapsedMinutes}m
          </div>
        </div>
      </div>

      {/* IDENTIFICAÇÃO E LOGÍSTICA */}
      <div className="p-5 space-y-4">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-black text-white tracking-tighter leading-none">
              {order.table?.table_number ? `MESA ${order.table.table_number}` : "RETIRADA"}
            </h2>
            <p className="text-[11px] text-slate-500 font-bold mt-1.5 uppercase tracking-widest truncate max-w-[160px]">
              {order.customer_name || "Consumidor"}
            </p>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-[10px] font-mono text-slate-600 font-bold">#{order.id.slice(0,4).toUpperCase()}</span>
            <div className="flex items-center gap-1 mt-1">
               <div className={cn("w-1.5 h-1.5 rounded-full", order.payment_status === 'paid' ? "bg-emerald-500" : "bg-red-500")} />
               <span className="text-[8px] font-black text-slate-500 uppercase">{order.payment_status === 'paid' ? 'Pago' : 'Pendente'}</span>
            </div>
          </div>
        </div>

        {/* LOCALIZAÇÃO / PICKUP NOTE */}
        {(order.delivery_address || order.pickup_note) && (
          <div className="p-3 bg-black/20 rounded-2xl border border-white/5 space-y-2">
            {order.delivery_address && (
              <div className="flex items-start gap-2 text-slate-300">
                <MapPin size={14} className="text-red-500 shrink-0 mt-0.5" />
                <p className="text-[10px] font-medium leading-tight">{order.delivery_address}</p>
              </div>
            )}
            {order.pickup_note && (
              <div className="flex items-center gap-2 text-orange-400">
                <Info size={14} className="shrink-0" />
                <p className="text-[10px] font-black uppercase tracking-tight">{order.pickup_note}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* LISTA DE PRODUÇÃO (RITO 86 & RECEITA) */}
      <div className="p-5 flex-1 space-y-3 overflow-y-auto custom-scrollbar min-h-[200px] bg-black/10">
        {order.items.map((item, idx) => {
          const isDimmed = activeStation !== 'all' && item.product.station !== activeStation;
          return (
            <div 
              key={idx} 
              className={cn(
                "group/item relative flex gap-4 items-start p-2 rounded-xl transition-all cursor-pointer",
                isDimmed ? "opacity-15 grayscale" : "hover:bg-white/5"
              )}
              onClick={() => onShowRecipe(item)}
              onContextMenu={(e) => {
                e.preventDefault();
                onExhaustProduct(item.product.id, item.product.name);
              }}
            >
              <div className="bg-slate-800 text-orange-500 w-9 h-9 rounded-xl flex items-center justify-center font-black text-lg shrink-0 border border-slate-700 shadow-lg">
                {item.quantity}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-black text-slate-100 text-sm leading-tight uppercase tracking-tight group-hover/item:text-orange-400 transition-colors">
                  {item.product.name}
                </p>
                {item.selected_options?.map((opt, i) => (
                  <p key={i} className="text-[10px] text-slate-500 font-bold">+ {opt.name.toUpperCase()}</p>
                ))}
                {item.notes && (
                  <p className="text-[10px] text-amber-400 italic mt-1 bg-amber-400/5 p-1.5 rounded border border-amber-400/10">
                    "{item.notes}"
                  </p>
                )}
                <div className="mt-2 flex items-center gap-1 text-[8px] text-slate-600 font-black uppercase opacity-0 group-hover/item:opacity-100 transition-opacity">
                  <List size={10} /> Ver Ingredientes
                </div>
              </div>

              {/* INDICADOR DE AÇÃO 86 (DESKTOP HOVER) */}
              <div className="absolute right-0 top-1/2 -translate-y-1/2 opacity-0 group-hover/item:opacity-100 transition-all translate-x-2 group-hover/item:translate-x-0">
                <div className="bg-red-600 text-white p-1.5 rounded-lg shadow-xl" title="Esgotar Item">
                  <Ban size={14} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* BOTÃO DE COMANDO SOBERANO */}
      <div className="p-5 bg-slate-950/50 border-t border-slate-800">
        <button
          onClick={onAction}
          className={cn(
            "w-full py-5 rounded-2xl font-black uppercase tracking-[0.2em] text-xs transition-all active:scale-[0.97] flex items-center justify-center gap-3 shadow-2xl",
            order.status === 'pending' 
              ? "bg-white text-slate-950 hover:bg-slate-200" 
              : "bg-emerald-600 text-white hover:bg-emerald-500 shadow-emerald-900/20"
          )}
        >
          {order.status === 'pending' ? (
            <><Play size={18} fill="currentColor" /> ACEITAR PEDIDO</>
          ) : (
            <><CheckCircle2 size={18} /> MARCAR COMO PRONTO</>
          )}
        </button>
      </div>

      {/* COMPLEXITY OVERLAY (PASSIVO) */}
      <div className="absolute bottom-20 right-5 opacity-10 pointer-events-none">
        <span className="text-[40px] font-black text-white italic">CS:{complexity}</span>
      </div>
    </motion.div>
  );
}
