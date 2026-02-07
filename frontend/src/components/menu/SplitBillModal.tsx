
"use client";
import { useState } from "react";
import { X, CheckCircle2, Calculator, DollarSign } from "lucide-react";
import { Order } from "@/types";

interface SplitBillModalProps {
  isOpen: boolean;
  onClose: () => void;
  orders: Order[];
  totalAmount: number;
  primaryColor: string;
  onPayPartial?: (amount: number) => void;
  // Props opcionais para compatibilidade com chamadas legadas ou futuras
  slug?: string;
  tableId?: number;
}

export default function SplitBillModal({ 
  isOpen, 
  onClose, 
  orders, 
  totalAmount, 
  primaryColor, 
  onPayPartial 
}: SplitBillModalProps) {
  const [mode, setMode] = useState<"equal" | "items">("equal");
  const [peopleCount, setPeopleCount] = useState(2);
  const [selectedItems, setSelectedItems] = useState<string[]>([]);

  const allItems = orders.flatMap(order => 
    order.items.map((item, idx) => ({
      ...item,
      orderId: order.id,
      uniqueId: `${order.id}-${idx}`,
      totalPrice: (Number(item.product.price) + item.selected_options.reduce((a, b) => a + Number(b.price), 0)) * item.quantity
    }))
  );

  const handleToggleItem = (uniqueId: string) => {
    if (selectedItems.includes(uniqueId)) {
      setSelectedItems(prev => prev.filter(id => id !== uniqueId));
    } else {
      setSelectedItems(prev => [...prev, uniqueId]);
    }
  };

  const calculateMyShare = () => {
    if (mode === "equal") {
      return totalAmount / peopleCount;
    } else {
      return allItems
        .filter(item => selectedItems.includes(item.uniqueId))
        .reduce((acc, item) => acc + item.totalPrice, 0);
    }
  };

  const myShare = calculateMyShare();

  const handleConfirm = () => {
    if (onPayPartial) {
      onPayPartial(myShare);
    } else {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[90] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full sm:max-w-md sm:rounded-xl rounded-t-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h3 className="font-bold text-lg text-gray-900 flex items-center gap-2">
            <Calculator size={20} className="text-gray-500"/> Dividir Conta
          </h3>
          <button onClick={onClose} className="bg-gray-200 p-2 rounded-full hover:bg-gray-300 transition-colors"><X size={20}/></button>
        </div>
        
        <div className="p-4 flex gap-2 bg-white border-b border-gray-100">
          <button 
            onClick={() => setMode("equal")}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${mode === "equal" ? "bg-gray-900 text-white shadow-md" : "bg-gray-100 text-gray-500 hover:bg-gray-200"}`}
          >
            Dividir Igual
          </button>
          <button 
            onClick={() => setMode("items")}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${mode === "items" ? "bg-gray-900 text-white shadow-md" : "bg-gray-100 text-gray-500 hover:bg-gray-200"}`}
          >
            Pagar o que consumi
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
          {mode === "equal" ? (
            <div className="text-center space-y-6 py-8">
              <div className="flex items-center justify-center gap-6">
                <button 
                  onClick={() => setPeopleCount(Math.max(1, peopleCount - 1))}
                  className="w-12 h-12 rounded-full bg-white border border-gray-200 shadow-sm flex items-center justify-center text-2xl font-bold text-gray-600 hover:bg-gray-100 active:scale-95 transition-transform"
                >
                  -
                </button>
                <div className="text-center">
                  <span className="text-4xl font-black text-gray-900">{peopleCount}</span>
                  <p className="text-xs text-gray-500 font-bold uppercase mt-1">Pessoas</p>
                </div>
                <button 
                  onClick={() => setPeopleCount(peopleCount + 1)}
                  className="w-12 h-12 rounded-full bg-white border border-gray-200 shadow-sm flex items-center justify-center text-2xl font-bold text-gray-600 hover:bg-gray-100 active:scale-95 transition-transform"
                >
                  +
                </button>
              </div>
              <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                <p className="text-gray-500 text-sm mb-1">Cada um paga</p>
                <p className="text-4xl font-black text-green-600">R$ {myShare.toFixed(2)}</p>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-sm text-gray-500 mb-2">Selecione os itens que você vai pagar:</p>
              {allItems.map((item) => {
                const isSelected = selectedItems.includes(item.uniqueId);
                return (
                  <div 
                    key={item.uniqueId}
                    onClick={() => handleToggleItem(item.uniqueId)}
                    className={`flex justify-between items-center p-4 rounded-xl border cursor-pointer transition-all ${isSelected ? 'bg-white border-green-500 shadow-md ring-1 ring-green-500' : 'bg-white border-gray-200 hover:border-gray-300'}`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${isSelected ? 'bg-green-500 border-green-500' : 'border-gray-300'}`}>
                        {isSelected && <CheckCircle2 size={14} className="text-white" />}
                      </div>
                      <div>
                        <p className="font-bold text-gray-800 text-sm">{item.quantity}x {item.product.name}</p>
                        {item.selected_options.length > 0 && <p className="text-xs text-gray-400">+ {item.selected_options.length} opcionais</p>}
                      </div>
                    </div>
                    <span className="font-bold text-gray-900">R$ {item.totalPrice.toFixed(2)}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="p-4 bg-white border-t border-gray-100 safe-area-bottom">
          <div className="flex justify-between items-center mb-4">
            <span className="text-gray-500 font-medium">Sua Parte</span>
            <span className="text-2xl font-black text-gray-900">R$ {myShare.toFixed(2)}</span>
          </div>
          <button 
            onClick={handleConfirm}
            className="w-full py-3.5 rounded-xl font-bold text-white shadow-lg active:scale-95 transition-transform flex items-center justify-center gap-2"
            style={{ backgroundColor: primaryColor }}
          >
            {onPayPartial ? <><DollarSign size={18} /> Pagar Agora</> : "Confirmar Valor"}
          </button>
        </div>
      </div>
    </div>
  );
}

