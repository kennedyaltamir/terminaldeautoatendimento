"use client";
import { useState } from "react";
import { Loader2, Layers, Check } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { createBulkTables } from "@/lib/api";
import { toast } from "sonner";

// FIX: Interface definida explicitamente para resolver o erro TS2322
interface TableBulkModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function TableBulkModal({ isOpen, onClose, onSuccess }: TableBulkModalProps) {
  const [start, setStart] = useState(1);
  const [end, setEnd] = useState(10);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (start > end) {
      toast.error("O início deve ser menor que o fim.");
      return;
    }
    if (end - start > 50) {
      toast.error("Máximo de 50 mesas por vez.");
      return;
    }
    
    setLoading(true);
    try {
      await createBulkTables({ start, end });
      toast.success(`${end - start + 1} mesas geradas!`);
      onSuccess();
      onClose();
    } catch (e: any) {
      toast.error(e.message || "Erro ao gerar mesas.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Gerar Mesas em Lote">
      <div className="space-y-6">
        <div className="bg-blue-900/20 border border-blue-800 p-4 rounded-xl flex gap-3">
          <Layers className="text-blue-400 shrink-0" size={20} />
          <p className="text-xs text-blue-200 leading-relaxed">
            Crie múltiplas mesas de uma vez. Mesas já existentes no intervalo serão ignoradas para evitar duplicidade.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Do Número</label>
            <input 
              type="number" 
              min="1"
              className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white font-mono text-center focus:border-orange-500 outline-none"
              value={start}
              onChange={(e) => setStart(parseInt(e.target.value) || 1)}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Ao Número</label>
            <input 
              type="number" 
              min="1"
              className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white font-mono text-center focus:border-orange-500 outline-none"
              value={end}
              onChange={(e) => setEnd(parseInt(e.target.value) || 1)}
            />
          </div>
        </div>

        <button 
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-white text-slate-900 py-4 rounded-xl font-black uppercase text-xs tracking-widest hover:bg-gray-200 transition-all flex items-center justify-center gap-2 shadow-lg active:scale-95 disabled:opacity-50"
        >
          {loading ? <Loader2 className="animate-spin" size={18} /> : <Check size={18} />}
          Confirmar Geração
        </button>
      </div>
    </Modal>
  );
}