"use client";

import { useState, useEffect } from "react";
import { X, ArrowRight, ArrowRightLeft, Users, AlertTriangle, Loader2 } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { getTablesDashboard, transferTable } from "@/lib/api";
import { toast } from "sonner";

interface TransferModalProps {
  isOpen: boolean;
  onClose: () => void;
  fromTableId: number;
  fromTableName: string;
  slug: string;
  onSuccess: () => void;
}

export default function TransferModal({ isOpen, onClose, fromTableId, fromTableName, slug, onSuccess }: TransferModalProps) {
  const [tables, setTables] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTarget, setSelectedTarget] = useState<number | null>(null);
  const [processing, setProcessing] = useState(false);
  const [mergeConfirm, setMergeConfirm] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      setMergeConfirm(false);
      setSelectedTarget(null);
      getTablesDashboard(slug)
        .then(data => {
          // Filtra a própria mesa da lista
          setTables(data.filter((t: any) => t.id !== fromTableId));
        })
        .catch(() => toast.error("Erro ao carregar mesas"))
        .finally(() => setLoading(false));
    }
  }, [isOpen, slug, fromTableId]);

  const handleTransfer = async (forceMerge = false) => {
    if (!selectedTarget) return;
    
    setProcessing(true);
    try {
      await transferTable({
        from_table_id: fromTableId,
        to_table_id: selectedTarget,
        merge: forceMerge
      });
      
      toast.success("Mesa transferida com sucesso!");
      onSuccess();
      onClose();
    } catch (err: any) {
      if (err.detail && err.detail.includes("Deseja juntar")) {
        setMergeConfirm(true);
      } else {
        toast.error(err.detail || "Erro na transferência");
      }
    } finally {
      setProcessing(false);
    }
  };

  const targetTable = tables.find(t => t.id === selectedTarget);

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Transferir ${fromTableName}`}>
      <div className="space-y-4">
        
        {mergeConfirm ? (
          <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-xl animate-in fade-in">
            <div className="flex items-center gap-3 mb-3 text-yellow-800">
              <AlertTriangle size={24} />
              <h4 className="font-bold">Mesa Ocupada!</h4>
            </div>
            <p className="text-sm text-gray-700 mb-4">
              A Mesa {targetTable?.table_number} já tem uma conta aberta ({targetTable?.active_session?.customer_name}). 
              Deseja <b>JUNTAR</b> as duas mesas em uma só conta?
            </p>
            <div className="flex gap-2">
              <button 
                onClick={() => setMergeConfirm(false)}
                className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-lg font-bold"
              >
                Cancelar
              </button>
              <button 
                onClick={() => handleTransfer(true)}
                disabled={processing}
                className="flex-1 bg-yellow-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2"
              >
                {processing ? <Loader2 className="animate-spin" /> : <Users size={18} />}
                Juntar Mesas
              </button>
            </div>
          </div>
        ) : (
          <>
            <p className="text-sm text-gray-500">Selecione a mesa de destino:</p>
            
            <div className="grid grid-cols-3 gap-2 max-h-[50vh] overflow-y-auto p-1">
              {loading ? (
                <p className="col-span-3 text-center py-4 text-gray-400">Carregando...</p>
              ) : (
                tables.map(table => (
                  <button
                    key={table.id}
                    onClick={() => setSelectedTarget(table.id)}
                    className={`p-3 rounded-xl border-2 flex flex-col items-center justify-center transition-all ${
                      selectedTarget === table.id 
                        ? 'border-orange-500 bg-orange-50 text-orange-700' 
                        : table.status === 'occupied' 
                          ? 'border-red-200 bg-red-50 text-red-400 opacity-80' 
                          : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                    }`}
                  >
                    <span className="text-xl font-bold">{table.table_number}</span>
                    <span className="text-[10px] font-bold uppercase">
                      {table.status === 'occupied' ? 'Ocupada' : 'Livre'}
                    </span>
                  </button>
                ))
              )}
            </div>

            <button
              disabled={!selectedTarget || processing}
              onClick={() => handleTransfer(false)}
              className="w-full bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg"
            >
              {processing ? <Loader2 className="animate-spin" /> : <ArrowRightLeft size={20} />}
              Confirmar Transferência
            </button>
          </>
        )}
      </div>
    </Modal>
  );
}