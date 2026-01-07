"use client";

import { Order } from "@/types";
import { X, ChefHat, ArrowRight } from "lucide-react";
import { useMemo } from "react";

interface ItemAggregatorProps {
  isOpen: boolean;
  onClose: () => void;
  orders: Order[];
}

interface AggregatedItem {
  id: number;
  name: string;
  quantity: number;
  station: string;
  notes: string[];
}

export default function ItemAggregator({ isOpen, onClose, orders }: ItemAggregatorProps) {
  const aggregatedItems = useMemo(() => {
    const map = new Map<string, AggregatedItem>();

    // Filtra apenas pedidos em produção (Pendente ou Preparando)
    const activeOrders = orders.filter(o => o.status === 'pending' || o.status === 'preparing');

    activeOrders.forEach(order => {
      // Garante que items existe antes de iterar
      if (!order.items) return;

      order.items.forEach(item => {
        // FIX CRÍTICO: Proteção contra item.product ou id indefinidos
        const productId = item?.product?.id;
        if (!productId) {
          console.warn("Item sem ID de produto detectado no agregador:", item);
          return;
        }

        const key = productId.toString();

        if (!map.has(key)) {
          map.set(key, {
            id: productId,
            name: item.product.name || "Produto sem nome",
            quantity: 0,
            station: item.product.station || "other",
            notes: []
          });
        }

        const entry = map.get(key)!;
        entry.quantity += (item.quantity || 0);

        // Coleta observações relevantes com segurança
        if (item.notes) entry.notes.push(item.notes);
        if (item.selected_options) {
          item.selected_options.forEach(opt => {
            if (opt.name) entry.notes.push(opt.name);
          });
        }
      });
    });

    // Retorna ordenado por quantidade (maior para menor)
    return Array.from(map.values()).sort((a, b) => b.quantity - a.quantity);
  }, [orders]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-gray-900 border-l border-gray-800 shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col">
      <div className="p-6 border-b border-gray-800 flex justify-between items-center bg-gray-900">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ChefHat className="text-orange-500" /> Resumo de Produção
          </h2>
          <p className="text-gray-400 text-xs mt-1">Total acumulado na fila</p>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-gray-800 rounded-full text-gray-400 hover:text-white transition-colors">
          <X size={24} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {aggregatedItems.length === 0 ? (
          <div className="text-center py-20 text-gray-600">
            <p>Nenhum item na fila de produção.</p>
          </div>
        ) : (
          aggregatedItems.map((item) => (
            <div key={item.id} className="bg-gray-800 rounded-xl p-4 border border-gray-700 flex items-start gap-4">
              <div className="bg-orange-600/20 text-orange-500 w-12 h-12 rounded-lg flex items-center justify-center text-xl font-black border border-orange-500/30 shrink-0">
                {item.quantity}
              </div>

              <div className="flex-1">
                <h3 className="text-white font-bold text-lg leading-tight">{item.name}</h3>
                <span className="text-[10px] uppercase font-bold text-gray-500 bg-gray-900 px-2 py-0.5 rounded mt-1 inline-block">
                  {item.station === 'kitchen' ? 'Cozinha' : item.station === 'bar' ? 'Bar' : 'Outros'}
                </span>

                {item.notes.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-700/50">
                    <p className="text-xs text-gray-400 mb-1 font-bold">Detalhes:</p>
                    <div className="flex flex-wrap gap-1">
                      {item.notes.slice(0, 5).map((note, i) => (
                        <span key={i} className="text-[10px] bg-gray-700 text-gray-300 px-2 py-0.5 rounded">
                          {note}
                        </span>
                      ))}
                      {item.notes.length > 5 && (
                        <span className="text-[10px] text-gray-500 px-1">+{item.notes.length - 5} mais...</span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="p-6 border-t border-gray-800 bg-gray-900">
        <button 
          onClick={onClose}
          className="w-full bg-gray-800 hover:bg-gray-700 text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors"
        >
          Voltar para Pedidos <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
