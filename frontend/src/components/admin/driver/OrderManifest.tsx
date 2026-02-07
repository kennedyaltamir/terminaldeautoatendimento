/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.0.0 (Tactical Overlay Edition)
 * DNA_ID: MF-COMP-ORDER-MANIFEST-V2
 * OBJETIVO: Prover um checklist tático para o motorista verificar o conteúdo da bag sem sair do contexto de navegação.
 * Comportamento esperado: 
 *  1. Renderiza um painel animado (bottom-sheet style) via Framer Motion.
 *  2. Lista itens, quantidades e nomes dos produtos de forma legível.
 *  3. Exibe notas de coleta (pickup_note) com destaque visual de alerta.
 *  4. Utiliza glassmorphism para integração visual com o cockpit.
 */
"use client";

import React from "react";
import { Order } from "@/types";
import { Package, X, Info } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface OrderManifestProps {
  order: Order;
  isOpen: boolean;
  onClose: () => void;
}

export default function OrderManifest({ order, isOpen, onClose }: OrderManifestProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.95 }}
          className="absolute bottom-24 left-4 right-4 bg-slate-900/95 backdrop-blur-xl border border-slate-700 p-5 rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.5)] z-50"
        >
          <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
            <div className="flex items-center gap-3">
              <div className="bg-orange-500/20 p-2 rounded-xl text-orange-500">
                <Package size={20} />
              </div>
              <div>
                <span className="text-xs font-black uppercase tracking-[0.2em] text-white">Conteúdo da Bag</span>
                <p className="text-[10px] text-slate-500 font-bold uppercase">Verificação Obrigatória</p>
              </div>
            </div>
            <button 
              onClick={onClose} 
              className="p-2 bg-slate-800 hover:bg-slate-700 rounded-full text-slate-400 hover:text-white transition-all active:scale-90"
            >
              <X size={20} />
            </button>
          </div>

          <div className="space-y-3 max-h-48 overflow-y-auto custom-scrollbar pr-2">
            {order.items.map((item, i) => (
              <div key={i} className="flex justify-between items-center bg-black/20 p-3 rounded-xl border border-white/5">
                <div className="flex items-center gap-3">
                  <span className="bg-slate-800 text-orange-500 w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm border border-slate-700">
                    {item.quantity}
                  </span>
                  <span className="text-sm font-bold text-slate-200 uppercase tracking-tight">
                    {item.product.name}
                  </span>
                </div>
              </div>
            ))}

            {order.pickup_note && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-4 p-4 bg-orange-500/10 border border-orange-500/20 rounded-2xl flex gap-3 items-start"
              >
                <Info size={18} className="text-orange-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-[10px] font-black text-orange-500 uppercase tracking-widest mb-1">Nota de Coleta</p>
                  <p className="text-xs text-orange-200 font-medium leading-relaxed">
                    {order.pickup_note}
                  </p>
                </div>
              </motion.div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800">
            <button 
              onClick={onClose}
              className="w-full py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-black uppercase text-[10px] tracking-[0.2em] rounded-xl transition-all"
            >
              Fechar Manifesto
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}