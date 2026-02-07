"use client";

import { useState, useEffect } from "react";
import { X, Minus, Plus, ShoppingBag } from "lucide-react";
import { Product, Option } from "@/types";
import { formatCurrency } from "@/lib/utils";
import Modal from "@/components/ui/Modal";

export interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product | null;
  onAdd: (product: Product, quantity: number, notes: string, options: Option[]) => void;
  primaryColor: string;
}

export default function ProductModal({ 
  isOpen, 
  onClose, 
  product, 
  onAdd, 
  primaryColor 
}: ProductModalProps) {
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState("");
  const [selectedOptions, setSelectedOptions] = useState<Option[]>([]);

  useEffect(() => {
    if (isOpen) {
      setQuantity(1);
      setNotes("");
      setSelectedOptions([]);
    }
  }, [isOpen, product]);

  if (!isOpen || !product) return null;

  const basePrice = Number(product.price);
  const optionsTotal = selectedOptions.reduce((acc, opt) => acc + Number(opt.price), 0);
  const total = (basePrice + optionsTotal) * quantity;

  const handleOptionToggle = (option: Option, maxSelection: number) => {
    // Lógica simplificada de seleção
    const isSelected = selectedOptions.some(o => o.id === option.id);
    if (isSelected) {
      setSelectedOptions(prev => prev.filter(o => o.id !== option.id));
    } else {
      // TODO: Validar maxSelection por grupo
      setSelectedOptions(prev => [...prev, option]);
    }
  };

  const handleConfirm = () => {
    onAdd(product, quantity, notes, selectedOptions);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white dark:bg-slate-900 w-full sm:max-w-lg sm:rounded-2xl rounded-t-3xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        
        {/* Header com Imagem */}
        <div className="relative h-48 bg-gray-200 shrink-0">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-400">
              <ShoppingBag size={48} />
            </div>
          )}
          <button 
            onClick={onClose}
            className="absolute top-4 right-4 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors backdrop-blur-md"
          >
            <X size={20} />
          </button>
        </div>

        {/* Conteúdo Scrollável */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div>
            <h2 className="text-2xl font-black text-gray-900 dark:text-white leading-tight">{product.name}</h2>
            <p className="text-gray-500 dark:text-gray-400 mt-2 text-sm leading-relaxed">{product.description}</p>
          </div>

          {/* Grupos de Opções */}
          {product.option_groups?.map(group => (
            <div key={group.id} className="space-y-3">
              <div className="flex justify-between items-center">
                <h3 className="font-bold text-gray-900 dark:text-white">{group.name}</h3>
                <span className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded text-gray-500">
                  {group.max_selection > 1 ? `Até ${group.max_selection}` : 'Escolha 1'}
                </span>
              </div>
              <div className="space-y-2">
                {group.options.map(option => {
                  const isSelected = selectedOptions.some(o => o.id === option.id);
                  return (
                    <div 
                      key={option.id}
                      onClick={() => handleOptionToggle(option, group.max_selection)}
                      className={`flex justify-between items-center p-3 rounded-xl border cursor-pointer transition-all ${
                        isSelected 
                          ? 'border-orange-500 bg-orange-50 dark:bg-orange-900/20' 
                          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300'
                      }`}
                    >
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{option.name}</span>
                      <div className="flex items-center gap-3">
                        {Number(option.price) > 0 && (
                          <span className="text-xs text-gray-500">+ {formatCurrency(option.price)}</span>
                        )}
                        <div className={`w-5 h-5 rounded-full border flex items-center justify-center ${
                          isSelected ? 'bg-orange-500 border-orange-500' : 'border-gray-300'
                        }`}>
                          {isSelected && <div className="w-2 h-2 bg-white rounded-full" />}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}

          {/* Observações */}
          <div>
            <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Observações</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Ex: Tirar a cebola, ponto da carne..."
              className="w-full p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm outline-none focus:ring-2 focus:ring-orange-500/50 min-h-[80px]"
            />
          </div>
        </div>

        {/* Footer Fixo */}
        <div className="p-4 border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-slate-900 safe-area-bottom">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 bg-gray-100 dark:bg-gray-800 rounded-xl p-1">
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-10 flex items-center justify-center bg-white dark:bg-gray-700 rounded-lg shadow-sm text-gray-600 dark:text-white hover:scale-105 transition-transform"
              >
                <Minus size={16} />
              </button>
              <span className="font-black text-lg w-6 text-center text-gray-900 dark:text-white">{quantity}</span>
              <button 
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 flex items-center justify-center bg-white dark:bg-gray-700 rounded-lg shadow-sm text-gray-600 dark:text-white hover:scale-105 transition-transform"
              >
                <Plus size={16} />
              </button>
            </div>
            <button 
              onClick={handleConfirm}
              className="flex-1 py-3.5 rounded-xl font-black text-white shadow-lg active:scale-95 transition-all flex justify-between px-6 items-center"
              style={{ backgroundColor: primaryColor }}
            >
              <span>Adicionar</span>
              <span>{formatCurrency(total)}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}