"use client";
import { useState, useEffect } from "react";
import { X, HandPlatter, Receipt, Sparkles, MessageSquare, Phone, LogOut, Shield, HelpCircle, Utensils, User } from "lucide-react";
import { getSegmentLabels } from "@/lib/segment-utils";

// Mapa de ícones para renderização dinâmica
const ICON_MAP: any = {
  HandPlatter, Receipt, Sparkles, MessageSquare, Phone, LogOut, Shield, HelpCircle, Utensils, User
};

export default function ServiceModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  primaryColor,
  segment 
}: { 
  isOpen: boolean, 
  onClose: () => void, 
  onConfirm: (type: string, notes: string) => void, 
  primaryColor: string,
  segment?: string
}) {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  
  const labels = getSegmentLabels(segment);
  
  useEffect(() => { 
    if (isOpen) { 
      setSelectedType(null); 
      setNotes(""); 
    } 
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-sm rounded-2xl p-6 shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-gray-900">Solicitar Serviço</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600"><X size={24}/></button>
        </div>
        
        <div className="grid grid-cols-2 gap-3 mb-6">
          {labels.service_options.map((opt) => {
            const Icon = ICON_MAP[opt.icon] || MessageSquare;
            return (
              <button 
                key={opt.id} 
                onClick={() => setSelectedType(opt.id)} 
                className={`flex flex-col items-center justify-center gap-2 p-4 rounded-xl border transition-all ${selectedType === opt.id ? 'border-orange-500 bg-orange-50 text-orange-700 ring-1 ring-orange-500' : 'border-gray-200 text-gray-600 hover:bg-gray-50'}`}
              >
                <Icon size={24} />
                <span className="text-xs font-bold text-center">{opt.label}</span>
              </button>
            );
          })}
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Observação (Opcional)</label>
          <textarea 
            className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-orange-500 outline-none resize-none bg-gray-50" 
            placeholder="Detalhes do pedido..." 
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