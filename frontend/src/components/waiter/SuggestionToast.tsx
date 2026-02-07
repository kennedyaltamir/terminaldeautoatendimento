"use client";
/**
 * DOMAIN: FRONTEND
 * FILE: src/components/waiter/SuggestionToast.tsx
 * OBJECTIVE: Notificação flutuante para sugestões de Upsell (IA).
 */
import { useEffect } from "react";
import { Product } from "@/types";
import { Sparkles, Plus, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { formatCurrency } from "@/lib/utils";

interface SuggestionToastProps {
  suggestion: Product | null;
  onAdd: (product: Product) => void;
  onClose: () => void;
}

export default function SuggestionToast({ suggestion, onAdd, onClose }: SuggestionToastProps) {
  // Auto-dismiss após 10 segundos para não atrapalhar a operação
  useEffect(() => {
    if (suggestion) {
      const timer = setTimeout(onClose, 10000);
      return () => clearTimeout(timer);
    }
  }, [suggestion, onClose]);

  return (
    <AnimatePresence>
      {suggestion && (
        <motion.div
          initial={{ y: 100, opacity: 0, scale: 0.9 }}
          animate={{ y: 0, opacity: 1, scale: 1 }}
          exit={{ y: 100, opacity: 0, scale: 0.9 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className="fixed bottom-24 left-4 right-4 z-50 md:left-auto md:right-4 md:w-96"
        >
          <div className="bg-slate-900 text-white p-4 rounded-2xl shadow-2xl border border-purple-500/50 flex items-center gap-4 relative overflow-hidden">
            {/* Efeito de Fundo */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/20 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>
            
            <div className="bg-purple-600/20 p-3 rounded-xl text-purple-400 shrink-0 border border-purple-500/30">
              <Sparkles size={24} className="animate-pulse" />
            </div>
            
            <div className="flex-1 min-w-0 z-10">
              <p className="text-[10px] text-purple-300 font-black uppercase tracking-widest mb-0.5">Sugestão Inteligente</p>
              <p className="font-bold text-sm truncate text-white">Ofereça {suggestion.name}</p>
              <p className="text-xs text-gray-400 font-mono mt-0.5">+ {formatCurrency(suggestion.price)}</p>
            </div>

            <div className="flex items-center gap-2 z-10">
              <button 
                onClick={() => onAdd(suggestion)}
                className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2.5 rounded-xl font-bold text-xs flex items-center gap-1.5 transition-all shadow-lg active:scale-95"
              >
                <Plus size={16} /> Adicionar
              </button>
              <button 
                onClick={onClose}
                className="p-2 text-gray-500 hover:text-white hover:bg-white/10 rounded-full transition-colors"
              >
                <X size={18} />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
