// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 21:45:00
"use client";
import { useState, useEffect } from "react";
import { X, Plus, Minus, ShoppingBag, Info } from "lucide-react";
import { Product, Option } from "@/types";
import { formatCurrency } from "@/lib/utils";

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product | null;
  onConfirm: (quantity: number, notes: string, selectedOptions: Option[]) => void;
  primaryColor: string;
  initialValues?: any;
}

export default function ProductModal({ isOpen, onClose, product, onConfirm, primaryColor, initialValues }: ProductModalProps) {
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState("");
  const [selectedOptions, setSelectedOptions] = useState<Option[]>([]);

  useEffect(() => {
    if (isOpen) {
      if (initialValues) {
        setQuantity(initialValues.quantity);
        setNotes(initialValues.notes || "");
        setSelectedOptions(initialValues.selectedOptions || []);
      } else {
        setQuantity(1);
        setNotes("");
        setSelectedOptions([]);
      }
    }
  }, [isOpen, initialValues]);

  if (!isOpen || !product) return null;

  const handleToggleOption = (option: Option) => {
    setSelectedOptions(prev => {
      const isSelected = prev.find(o => o.id === option.id);
      if (isSelected) return prev.filter(o => o.id !== option.id);
      return [...prev, option];
    });
  };

  if (!product) return null;
  const basePrice = Number(product.price);
  const optionsPrice = selectedOptions.reduce((acc, opt) => acc + Number(opt.price), 0);
  const totalPrice = (basePrice + optionsPrice) * quantity;

  return (
    <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="bg-white dark:bg-gray-900 w-full sm:max-w-lg sm:rounded-3xl rounded-t-[2.5rem] max-h-[95vh] flex flex-col overflow-hidden shadow-2xl border-t-4" style={{ borderTopColor: primaryColor }}>
        <div className="relative h-48 sm:h-64 shrink-0">
          {product.image_url ? (
            <img src={product.image_url} className="w-full h-full object-cover" alt={product.name} />
          ) : (
            <div className="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-300">
              <ShoppingBag size={64} />
            </div>
          )}
          <button onClick={onClose} className="absolute top-4 right-4 bg-black/50 text-white p-2 rounded-full backdrop-blur-md hover:bg-black/70 transition-colors">
            <X size={24} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
          <div>
            <h2 className="text-2xl font-black text-gray-900 dark:text-white tracking-tight">{product.name}</h2>
            <p className="text-gray-500 dark:text-gray-400 text-sm mt-2 leading-relaxed">{product.description}</p>
          </div>

          {product.option_groups?.map(group => (
            <div key={group.id} className="space-y-3">
              <div className="flex justify-between items-center bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl">
                <h3 className="font-bold text-gray-900 dark:text-white text-sm uppercase tracking-wider">{group.name}</h3>
                <span className="text-[10px] font-black bg-gray-200 dark:bg-gray-700 px-2 py-0.5 rounded-full text-gray-500">
                  MÁX {group.max_selection}
                </span>
              </div>
              <div className="space-y-2">
                {group.options.map(opt => (
                  <label key={opt.id} className="flex items-center justify-between p-4 rounded-2xl border border-gray-100 dark:border-gray-800 hover:border-orange-200 cursor-pointer transition-all active:scale-[0.98]">
                    <div className="flex items-center gap-3">
                      <input 
                        type="checkbox" 
                        className="w-5 h-5 rounded-full border-gray-300 text-orange-600 focus:ring-orange-500"
                        checked={!!selectedOptions.find(o => o.id === opt.id)}
                        onChange={() => handleToggleOption(opt)}
                      />
                      <span className="font-bold text-gray-700 dark:text-gray-300">{opt.name}</span>
                    </div>
                    {Number(opt.price) > 0 && (
                      <span className="text-xs font-black text-orange-600">+ {formatCurrency(Number(opt.price))}</span>
                    )}
                  </label>
                ))}
              </div>
            </div>
          ))}

          <div className="space-y-2">
            <label className="text-xs font-black text-gray-400 uppercase tracking-widest flex items-center gap-2">
              <Info size={14} /> Observações
            </label>
            <textarea 
              className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl p-4 text-sm outline-none focus:ring-2 focus:ring-orange-500/20 transition-all"
              placeholder="Ex: Sem cebola, ponto da carne, etc..."
              rows={3}
              value={notes}
              onChange={e => setNotes(e.target.value)}
            />
          </div>
        </div>

        <div className="p-6 bg-white dark:bg-gray-900 border-t border-gray-100 dark:border-gray-800 safe-area-bottom">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4 bg-gray-100 dark:bg-gray-800 p-1 rounded-2xl">
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-orange-600 transition-colors"
              >
                <Minus size={20} />
              </button>
              <span className="text-xl font-black text-gray-900 dark:text-white w-8 text-center">{quantity}</span>
              <button 
                onClick={() => setQuantity(quantity + 1)}
                className="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-orange-600 transition-colors"
              >
                <Plus size={20} />
              </button>
            </div>
            <div className="text-right">
              <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Subtotal</p>
              <p className="text-2xl font-black text-gray-900 dark:text-white">{formatCurrency(totalPrice)}</p>
            </div>
          </div>

          <button 
            onClick={() => onConfirm(quantity, notes, selectedOptions)}
            className="w-full py-5 rounded-2xl text-white font-black text-lg shadow-xl shadow-orange-900/20 flex items-center justify-center gap-3 active:scale-95 transition-all"
            style={{ backgroundColor: primaryColor }}
          >
            <Plus size={24} /> {initialValues ? "Atualizar Item" : "Adicionar ao Pedido"}
          </button>
        </div>
      </div>
    </div>
  );
}
