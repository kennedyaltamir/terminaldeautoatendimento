/**
 * Author: MESAFLOW_AI
 * Version: 1.6.0 (Station-Aware Aggregator)
 * DNA_ID: kds-aggregator-v1-6
 * Objective: Agregação de itens respeitando o filtro de estação ativo.
 */
"use client";

import { Order } from "@/types";
import { X, ChefHat, ArrowRight, ListChecks } from "lucide-react";
import { useMemo } from "react";
import { cn } from "@/lib/utils";

interface ItemAggregatorProps {
  isOpen: boolean;
  onClose: () => void;
  orders: Order[];
  activeStation?: string; // 🛡️ NOVO: Respeita o filtro da tela principal
}

interface AggregatedItem {
  id: number;
  name: string;
  quantity: number;
  station: string;
  notes: string[];
}

export default function ItemAggregator({ isOpen, onClose, orders, activeStation = 'all' }: ItemAggregatorProps) {
  const aggregatedItems = useMemo(() => {
    const map = new Map<string, AggregatedItem>();
    
    // Filtra apenas pedidos em produção
    const activeOrders = orders.filter(o => o.status === 'pending' || o.status === 'preparing');

    activeOrders.forEach(order => {
      if (!order.items) return;
      
      order.items.forEach(item => {
        // 🛡️ FILTRO DE ESTAÇÃO: Se o agregador for station-aware, ignora itens de outras praças
        if (activeStation !== 'all' && item.product.station !== activeStation) return;

        const productId = item.product.id;
        const key = productId.toString();

        if (!map.has(key)) {
          map.set(key, {
            id: productId,
            name: item.product.name,
            quantity: 0,
            station: item.product.station,
            notes: []
          });
        }

        const entry = map.get(key)!;
        entry.quantity += item.quantity;
        if (item.notes) entry.notes.push(item.notes);
      });
    });

    return Array.from(map.values()).sort((a, b) => b.quantity - a.quantity);
  }, [orders, activeStation]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-[100] w-full max-w-md bg-slate-950 border-l border-slate-800 shadow-2xl flex flex-col animate-in slide-in-from-right duration-300">
      <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50 backdrop-blur-md">
        <div>
          <h2 className="text-xl font-black text-white flex items-center gap-3 uppercase tracking-tighter">
            <ListChecks className="text-emerald-500" /> Resumo {activeStation !== 'all' ? activeStation : 'Geral'}
          </h2>
          <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mt-1">Total acumulado na fila</p>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-slate-800 rounded-full text-slate-500 hover:text-white transition-colors">
          <X size={24} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
        {aggregatedItems.length === 0 ? (
          <div className="text-center py-20 text-slate-700">
            <ChefHat size={48} className="mx-auto mb-4 opacity-20" />
            <p className="font-bold uppercase text-xs tracking-widest">Nenhum item pendente nesta praça.</p>
          </div>
        ) : (
          aggregatedItems.map((item) => (
            <div key={item.id} className="bg-slate-900 rounded-2xl p-5 border border-slate-800 flex items-start gap-5 group hover:border-slate-700 transition-all">
              <div className="bg-emerald-500/10 text-emerald-500 w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-black border border-emerald-500/20 shrink-0 shadow-inner">
                {item.quantity}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-white font-black text-lg leading-tight uppercase truncate">{item.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                   <span className="text-[9px] font-black text-slate-500 bg-slate-800 px-2 py-0.5 rounded uppercase tracking-tighter">
                    {item.station}
                  </span>
                </div>
                
                {item.notes.length > 0 && (
                  <div className="mt-3 space-y-1">
                    {Array.from(new Set(item.notes)).slice(0, 3).map((note, i) => (
                      <p key={i} className="text-[10px] text-orange-400 italic font-medium leading-tight">
                        • "{note}"
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="p-6 border-t border-slate-800 bg-slate-900/30">
        <button 
          onClick={onClose}
          className="w-full bg-white text-slate-950 py-4 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-xl hover:bg-slate-200 transition-all active:scale-95"
        >
          VOLTAR AO MONITOR
        </button>
      </div>
    </div>
  );
}
