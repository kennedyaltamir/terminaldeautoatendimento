"use client";
import { useState, useEffect } from "react";
import { X } from "lucide-react";
import { Product, Option } from "@/types";

interface ProductModalProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (qty: number, notes: string, options: Option[]) => void;
  primaryColor: string;
  initialValues?: {
    quantity: number;
    notes?: string; // --- CORREÇÃO: Tornado opcional ---
    selectedOptions: Option[];
  } | null;
}

export default function ProductModal({ product, isOpen, onClose, onConfirm, primaryColor, initialValues }: ProductModalProps) {
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState("");
  const [selectedOptions, setSelectedOptions] = useState<Option[]>([]);
  
  useEffect(() => { 
    if (isOpen) { 
      if (initialValues) {
        // Modo Edição
        setQuantity(initialValues.quantity);
        setNotes(initialValues.notes || ""); // --- CORREÇÃO: Fallback para string vazia ---
        setSelectedOptions(initialValues.selectedOptions);
      } else {
        // Modo Adição (Reset)
        setQuantity(1); 
        setNotes(""); 
        setSelectedOptions([]); 
      }
    } 
  }, [isOpen, product, initialValues]);

  if (!isOpen || !product) return null;

  const handleOptionToggle = (option: Option) => {
    const isSelected = selectedOptions.find(o => o.id === option.id);
    if (isSelected) { 
      setSelectedOptions(prev => prev.filter(o => o.id !== option.id)); 
    } else { 
      setSelectedOptions(prev => [...prev, option]); 
    }
  };

  const currentTotal = (Number(product.price) + selectedOptions.reduce((acc, opt) => acc + Number(opt.price), 0)) * quantity;
  const maxStock = product.track_stock ? product.stock_quantity : 999;
  const isOutOfStock = product.track_stock && product.stock_quantity <= 0;

  return (
    <div className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full sm:max-w-md sm:rounded-xl rounded-t-2xl max-h-[90vh] flex flex-col overflow-hidden">
        <div className="relative h-48 bg-gray-200 shrink-0">
          {product.image_url && <img src={product.image_url} className="w-full h-full object-cover" alt={product.name} />}
          <button onClick={onClose} className="absolute top-4 right-4 bg-white/80 p-2 rounded-full text-gray-800 hover:bg-white transition-colors"><X size={20} /></button>
        </div>
        <div className="p-6 overflow-y-auto flex-1 text-gray-900">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-bold leading-tight">{product.name}</h2>
            {product.track_stock && (
              <span className={`text-xs font-bold px-2 py-1 rounded whitespace-nowrap ml-2 ${product.stock_quantity > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {product.stock_quantity > 0 ? `Restam ${product.stock_quantity}` : 'ESGOTADO'}
              </span>
            )}
          </div>
          <p className="text-gray-500 mt-2 text-sm leading-relaxed">{product.description}</p>
          
          {!isOutOfStock && (
            <>
              <div className="mt-6 space-y-6">
                {product.option_groups.map(group => (
                  <div key={group.id}>
                    <h3 className="font-semibold text-gray-800 mb-3 flex justify-between text-sm uppercase tracking-wide">{group.name}</h3>
                    <div className="space-y-2">
                      {group.options.map(option => {
                        const isSelected = !!selectedOptions.find(o => o.id === option.id);
                        return (
                          <div key={option.id} onClick={() => handleOptionToggle(option)} className={`flex justify-between items-center p-3 rounded-lg border cursor-pointer transition-all ${isSelected ? 'border-orange-500 bg-orange-50' : 'border-gray-200 hover:border-gray-300'}`}>
                            <span className="text-gray-700 font-medium">{option.name}</span>
                            <div className="flex items-center gap-2">
                              {Number(option.price) > 0 && <span className="text-sm text-gray-500">+ R$ {Number(option.price).toFixed(2)}</span>}
                              <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${isSelected ? 'bg-orange-500 border-orange-500' : 'border-gray-300'}`}>
                                {isSelected && <div className="w-2 h-2 bg-white rounded-full" />}
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Observações</label>
                <textarea 
                  className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-orange-500 outline-none resize-none bg-gray-50" 
                  placeholder="Ex: Tirar a cebola, ponto da carne..." 
                  rows={3} 
                  value={notes} 
                  onChange={e => setNotes(e.target.value)} 
                />
              </div>
            </>
          )}
        </div>
        <div className="p-4 border-t border-gray-100 bg-white shrink-0 safe-area-bottom">
          {isOutOfStock ? (
            <button disabled className="w-full bg-gray-300 text-gray-500 py-3.5 rounded-xl font-bold cursor-not-allowed">Produto Esgotado</button>
          ) : (
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center border border-gray-200 rounded-xl bg-gray-50">
                <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="px-4 py-3 text-gray-600 hover:bg-gray-200 rounded-l-xl transition-colors font-bold text-lg">-</button>
                <span className="px-2 font-bold text-gray-900 min-w-[20px] text-center">{quantity}</span>
                <button onClick={() => setQuantity(Math.min(maxStock, quantity + 1))} className="px-4 py-3 text-gray-600 hover:bg-gray-200 rounded-r-xl transition-colors font-bold text-lg">+</button>
              </div>
              <button 
                onClick={() => onConfirm(quantity, notes, selectedOptions)} 
                className="flex-1 text-white py-3.5 rounded-xl font-bold shadow-lg flex justify-between px-6 active:scale-95 transition-transform" 
                style={{ backgroundColor: primaryColor }}
              >
                <span>{initialValues ? "Atualizar" : "Adicionar"}</span>
                <span>R$ {currentTotal.toFixed(2)}</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}