/**
 * Author: MESAFLOW_AI
 * Version: 1.0.0
 * Objective: Exibir ingredientes e modo de preparo para o cozinheiro.
 */
"use client";

import React from "react";
import Modal from "@/components/ui/Modal";
import { OrderItemResponse } from "@/types";
import { Utensils, Info, AlertTriangle } from "lucide-react";

interface RecipeViewModalProps {
  item: OrderItemResponse | null;
  onClose: () => void;
}

export default function RecipeViewModal({ item, onClose }: RecipeViewModalProps) {
  if (!item) return null;

  return (
    <Modal isOpen={!!item} onClose={onClose} title={`Ficha Técnica: ${item.product.name}`}>
      <div className="space-y-6">
        <div className="flex items-center gap-4 p-4 bg-slate-900 rounded-2xl border border-slate-800">
          <div className="bg-orange-600 p-3 rounded-xl text-white">
            <Utensils size={24} />
          </div>
          <div>
            <h3 className="font-black text-white uppercase">{item.product.name}</h3>
            <p className="text-xs text-slate-500">Estação: {item.product.station.toUpperCase()}</p>
          </div>
        </div>

        <div className="space-y-3">
          <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Composição / Ingredientes</h4>
          <div className="grid gap-2">
            {/* Aqui simulamos a exibição de ingredientes que viriam da Ficha Técnica do produto */}
            <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700 text-sm text-slate-300 flex justify-between">
              <span>Base do Produto</span>
              <span className="font-bold text-white">Padrão</span>
            </div>
            {item.selected_options.map((opt, i) => (
              <div key={i} className="p-3 bg-orange-500/5 rounded-xl border border-orange-500/20 text-sm text-orange-200 flex justify-between">
                <span>{opt.name}</span>
                <span className="font-bold">ADICIONAL</span>
              </div>
            ))}
          </div>
        </div>

        {item.notes && (
          <div className="p-4 bg-amber-900/20 border border-amber-500/30 rounded-2xl">
            <div className="flex items-center gap-2 text-amber-500 mb-2">
              <AlertTriangle size={16} />
              <span className="text-xs font-black uppercase">Observação do Cliente</span>
            </div>
            <p className="text-sm text-amber-200 font-medium italic">"{item.notes}"</p>
          </div>
        )}

        <button 
          onClick={onClose}
          className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold uppercase text-xs tracking-widest transition-all"
        >
          Voltar para a Fila
        </button>
      </div>
    </Modal>
  );
}

