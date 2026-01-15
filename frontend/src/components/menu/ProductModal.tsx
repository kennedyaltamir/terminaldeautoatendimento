"use client";
import { useState, useEffect } from "react";
import { X, Minus, Plus, ShoppingBag } from "lucide-react";
import { Product, Option, CartItem } from "@/types";
import { formatCurrency } from "@/lib/utils";

interface ProductModalProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (qty: number, notes: string, opts: Option[]) => void;
  primaryColor: string;
  initialValues?: CartItem | null; // Adicionado para suportar edição
}

export default function ProductModal({ product, isOpen, onClose, onConfirm, primaryColor, initialValues }: ProductModalProps) {
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

  const handleOptionToggle = (option: Option, groupMin: number, groupMax: number) => {
    const isSelected = selectedOptions.some(o => o.id === option.id);
    const groupOptions = selectedOptions.filter(o => 
      product.option_groups.find(g => g.options.some(opt => opt.id === o.id))?.id === 
      product.option_groups.find(g => g.options.some(opt => opt.id === option.id))?.id
    );

    if (isSelected) {
      setSelectedOptions(prev => prev.filter(o => o.id !== option.id));
    } else {
      if (groupMax === 1) {
        // Radio behavior: remove others from same group
        const otherOptionsIds = product.option_groups
          .find(g => g.options.some(opt => opt.id === option.id))
          ?.options.map(o => o.id) || [];
        
        setSelectedOptions(prev => [
          ...prev.filter(o => !otherOptionsIds.includes(o.id)),
          option
        ]);
      } else {
        if (groupOptions.length < groupMax) {
          setSelectedOptions(prev => [...prev, option]);
        }
      }
    }
  };

  const calculateTotal = () => {
    const optionsTotal = selectedOptions.reduce((acc, opt) => acc + Number(opt.price), 0);
    return (Number(product.price) + optionsTotal) * quantity;
  };

  const isValid = () => {
    return product.option_groups.every(group => {
      const selectedCount = selectedOptions.filter(o => group.options.some(opt => opt.id === o.id)).length;
      return selectedCount >= group.min_selection;
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full sm:max-w-md sm:rounded-xl rounded-t-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        
        {/* Header Image */}
        <div className="relative h-48 bg-gray-100">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gray-200 text-gray-400">
              <ShoppingBag size={48} />
            </div>
          )}
          <button 
            onClick={onClose}
            className="absolute top-4 right-4 bg-white/90 p-2 rounded-full shadow-lg hover:bg-white transition-colors"
          >
            <X size={20} className="text-gray-900" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div>
            <h2 className="text-2xl font-black text-gray-900 leading-tight">{product.name}</h2>
            <p className="text-gray-500 mt-2 text-sm leading-relaxed">{product.description}</p>
            <p className="text-xl font-bold text-orange-600 mt-2">{formatCurrency(product.price)}</p>
          </div>

          {/* Options */}
          {product.option_groups.map(group => (
            <div key={group.id} className="space-y-3">
              <div className="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
                <h3 className="font-bold text-gray-800">{group.name}</h3>
                <span className="text-xs font-medium text-gray-500 bg-white px-2 py-1 rounded border border-gray-200">
                  {group.min_selection > 0 ? `Obrigatório (Min ${group.min_selection})` : 'Opcional'}
                  {group.max_selection > 1 && ` - Max ${group.max_selection}`}
                </span>
              </div>
              <div className="space-y-2">
                {group.options.map(option => {
                  const isSelected = selectedOptions.some(o => o.id === option.id);
                  return (
                    <div 
                      key={option.id}
                      onClick={() => handleOptionToggle(option, group.min_selection, group.max_selection)}
                      className={`flex justify-between items-center p-3 rounded-xl border cursor-pointer transition-all ${
                        isSelected 
                          ? 'border-orange-500 bg-orange-50 ring-1 ring-orange-500' 
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${
                          isSelected ? 'bg-orange-500 border-orange-500' : 'border-gray-300'
                        }`}>
                          {isSelected && <div className="w-2 h-2 bg-white rounded-full" />}
                        </div>
                        <span className={`text-sm font-medium ${isSelected ? 'text-gray-900' : 'text-gray-600'}`}>
                          {option.name}
                        </span>
                      </div>
                      {Number(option.price) > 0 && (
                        <span className="text-sm font-bold text-gray-900">+ {formatCurrency(option.price)}</span>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}

          {/* Notes */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Observações</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Ex: Sem cebola, ponto da carne..."
              className="w-full p-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-orange-500 outline-none resize-none bg-gray-50"
              rows={3}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-white border-t border-gray-100 safe-area-bottom">
          <div className="flex items-center justify-between gap-4 mb-4">
            <div className="flex items-center gap-3 bg-gray-100 rounded-xl p-1">
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-10 flex items-center justify-center bg-white rounded-lg shadow-sm text-gray-600 hover:text-orange-600 disabled:opacity-50"
                disabled={quantity <= 1}
              >
                <Minus size={18} />
              </button>
              <span className="text-lg font-black w-8 text-center">{quantity}</span>
              <button 
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 flex items-center justify-center bg-white rounded-lg shadow-sm text-gray-600 hover:text-orange-600"
              >
                <Plus size={18} />
              </button>
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-500 font-bold uppercase">Total</p>
              <p className="text-2xl font-black text-gray-900">{formatCurrency(calculateTotal())}</p>
            </div>
          </div>
          <button
            onClick={() => onConfirm(quantity, notes, selectedOptions)}
            disabled={!isValid()}
            className="w-full py-4 rounded-xl font-bold text-white shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ backgroundColor: isValid() ? primaryColor : '#9ca3af' }}
          >
            {initialValues ? 'Atualizar Pedido' : 'Adicionar ao Carrinho'}
          </button>
        </div>
      </div>
    </div>
  );
}

 