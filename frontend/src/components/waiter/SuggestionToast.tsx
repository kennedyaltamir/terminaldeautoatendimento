"use client";

import { useState, useEffect } from "react";
import { Product } from "@/types";
import { Sparkles, Plus, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface SuggestionToastProps {
  suggestion: Product | null;
  onAdd: (product: Product) => void;
  onClose: () => void;
}

export default function SuggestionToast({ suggestion, onAdd, onClose }: SuggestionToastProps) {
  useEffect(() => {
    if (suggestion) {
      const timer = setTimeout(onClose, 10000); // Auto-dismiss em 10s
      return () => clearTimeout(timer);
    }
  }, [suggestion, onClose]);

  return (
    <AnimatePresence>
      {suggestion && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          className="fixed bottom-24 left-4 right-4 z-50"
        >
          <div className="bg-gray-900 text-white p-4 rounded-2xl shadow-2xl border border-purple-500/50 flex items-center gap-4 relative overflow-hidden">
            {/* Background Effect */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/20 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>

            <div className="bg-purple-600/20 p-2 rounded-xl text-purple-400 shrink-0">
              <Sparkles size={24} className="animate-pulse" />
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-xs text-purple-300 font-bold uppercase tracking-wider mb-0.5">Sugestão da IA</p>
              <p className="font-bold text-sm truncate">Ofereça {suggestion.name}</p>
              <p className="text-xs text-gray-400">+ R$ {Number(suggestion.price).toFixed(2)}</p>
            </div>

            <div className="flex items-center gap-2 z-10">
              <button 
                onClick={() => onAdd(suggestion)}
                className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg font-bold text-xs flex items-center gap-1 transition-colors shadow-lg"
              >
                <Plus size={14} /> Adicionar
              </button>
              <button 
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-white transition-colors"
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
