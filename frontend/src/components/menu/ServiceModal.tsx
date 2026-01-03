"use client";
import { useState, useEffect } from "react";
import { X, HandPlatter, Receipt, Sparkles, MessageSquare } from "lucide-react";

export default function ServiceModal({ isOpen, onClose, onConfirm, primaryColor }: { isOpen: boolean, onClose: () => void, onConfirm: (type: string, notes: string) => void, primaryColor: string }) {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  
  useEffect(() => { 
    if (isOpen) { 
      setSelectedType(null); 
      setNotes(""); 
    } 
  }, [isOpen]);

  if (!isOpen) return null;
  
  const options = [
    { id: 'help', label: 'Ajuda com Pedido', icon: HandPlatter },
    { id: 'bill', label: 'Trazer a Conta', icon: Receipt },
    { id: 'cleaning', label: 'Limpeza / Guardanapo', icon: Sparkles },
    { id: 'other', label: 'Outros', icon: MessageSquare },
  ];

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-sm rounded-2xl p-6 shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-gray-900">Chamar Garçom</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600"><X size={24}/></button>
        </div>
        
        <div className="grid grid-cols-2 gap-3 mb-6">
          {options.map((opt) => (
            <button 
              key={opt.id} 
              onClick={() => setSelectedType(opt.id)} 
              className={`flex flex-col items-center justify-center gap-2 p-4 rounded-xl border transition-all ${selectedType === opt.id ? 'border-orange-500 bg-orange-50 text-orange-700 ring-1 ring-orange-500' : 'border-gray-200 text-gray-600 hover:bg-gray-50'}`}
            >
              <opt.icon size={24} />
              <span className="text-xs font-bold text-center">{opt.label}</span>
            </button>
          ))}
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Observação (Opcional)</label>
          <textarea 
            className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-orange-500 outline-none resize-none bg-gray-50" 
            placeholder="Ex: Trazer maquininha, mais gelo..." 
            rows={2} 
            value={notes} 
            onChange={e => setNotes(e.target.value)} 
          />
        </div>

        <button 
          disabled={!selectedType} 
          onClick={() => selectedType && onConfirm(selectedType, notes)} 
          className="w-full text-white py-3.5 rounded-xl font-bold shadow-md disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95" 
          style={{ backgroundColor: primaryColor }}
        >
          Chamar Agora
        </button>
      </div>
    </div>
  );
}