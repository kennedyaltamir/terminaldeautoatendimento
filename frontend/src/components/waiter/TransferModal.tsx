/**
 * MODULE: WAITER_TRANSFER
 * VERSION: 3.0 (Visual Map)
 * DNA_ID: MF-TRANSFER-MODAL-V3
 * PURPOSE: Move or merge tables with visual confirmation.
 */
"use client";

import React, { useState, useEffect, useCallback } from "react";
import { 
  X, 
  ArrowRightLeft, 
  Users, 
  AlertTriangle, 
  Loader2, 
  CheckCircle2 ,
  ArrowRight
} from "lucide-react";
import Modal from "@/components/ui/Modal";
import { getTablesDashboard, transferTable } from "@/lib/api";
import { toast } from "sonner";
import { TableDashboard } from "@/types";
import { cn } from "@/lib/utils";

interface TransferModalProps {
  isOpen: boolean;
  onClose: () => void;
  fromTableId: number;
  fromTableName: string;
  slug: string;
  onSuccess: () => void;
}

export default function TransferModal({ 
  isOpen, 
  onClose, 
  fromTableId, 
  fromTableName, 
  slug,
  onSuccess 
}: TransferModalProps) {
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTarget, setSelectedTarget] = useState<number | null>(null);
  const [processing, setProcessing] = useState(false);
  const [mergeConfirm, setMergeConfirm] = useState(false);

  const loadTables = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getTablesDashboard();
      // Filtra a própria mesa da lista de destinos
      setTables(data.filter(t => t.id !== fromTableId));
    } catch (e) {
      toast.error("Falha ao carregar mapa de mesas.");
    } finally {
      setLoading(false);
    }
  }, [fromTableId]);

  useEffect(() => {
    if (isOpen) {
      loadTables();
      setMergeConfirm(false);
      setSelectedTarget(null);
    }
  }, [isOpen, loadTables]);

  const handleTransfer = async (forceMerge = false) => {
    if (!selectedTarget) return;
    setProcessing(true);
    try {
      await transferTable({
        from_table_id: fromTableId,
        to_table_id: selectedTarget,
        merge: forceMerge
      });
      toast.success(forceMerge ? "Mesas unificadas com sucesso!" : "Mesa transferida!");
      onSuccess();
      onClose();
    } catch (err: any) {
      // O Backend retorna 409 se a mesa de destino estiver ocupada
      if (err.status === 409 || (err.detail && err.detail.includes("ocupada"))) {
        setMergeConfirm(true);
      } else {
        toast.error(err.message || "Erro na operação de transferência.");
      }
    } finally {
      setProcessing(false);
    }
  };

  const targetTable = tables.find(t => t.id === selectedTarget);

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Transferir ${fromTableName}`}>
      <div className="space-y-6">
        {mergeConfirm ? (
          <div className="bg-orange-500/10 border border-orange-500/20 p-6 rounded-[2rem] animate-in zoom-in duration-300">
            <div className="flex items-center gap-3 mb-4 text-orange-500">
              <AlertTriangle size={28} />
              <h4 className="font-black uppercase text-sm tracking-widest">Mesa Ocupada</h4>
            </div>
            <p className="text-sm text-slate-300 mb-6 leading-relaxed">
              A <span className="text-white font-bold">Mesa {targetTable?.table_number}</span> já possui uma sessão ativa para <span className="text-orange-400 font-bold">{targetTable?.active_session?.customer_name}</span>. 
              Deseja <span className="text-white font-black underline">JUNTAR</span> os pedidos de ambas as mesas?
            </p>
            <div className="flex gap-3">
              <button 
                onClick={() => setMergeConfirm(false)}
                className="flex-1 bg-slate-800 text-slate-300 py-4 rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-slate-700 transition-all"
              >
                Voltar
              </button>
              <button 
                onClick={() => handleTransfer(true)}
                disabled={processing}
                className="flex-[2] bg-orange-600 text-white py-4 rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-orange-900/20 flex items-center justify-center gap-2 active:scale-95 transition-all"
              >
                {processing ? <Loader2 className="animate-spin" size={18} /> : <Users size={18} />}
                Confirmar União
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between px-2">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Selecione o Destino</p>
              {loading && <Loader2 size={14} className="animate-spin text-orange-500" />}
            </div>
            
            <div className="grid grid-cols-3 gap-3 max-h-[45vh] overflow-y-auto p-1 custom-scrollbar">
              {tables.map(table => (
                <button
                  key={table.id}
                  onClick={() => setSelectedTarget(table.id)}
                  className={cn(
                    "p-4 rounded-[1.5rem] border-2 flex flex-col items-center justify-center transition-all active:scale-95 h-24",
                    selectedTarget === table.id 
                      ? 'border-orange-500 bg-orange-500/10 shadow-md ring-1 ring-orange-500/50' 
                      : table.status === 'occupied' 
                        ? 'border-slate-800 bg-slate-900/50 text-slate-500' 
                        : 'border-slate-800 bg-slate-900 text-slate-400 hover:border-slate-700'
                  )}
                >
                  <span className="text-2xl font-black tracking-tighter">{table.table_number}</span>
                  <span className="text-[8px] font-black uppercase tracking-widest mt-1">
                    {table.status === 'occupied' ? 'Ocupada' : 'Livre'}
                  </span>
                </button>
              ))}
            </div>

            <div className="pt-4 space-y-3">
              <button
                disabled={!selectedTarget || processing}
                onClick={() => handleTransfer(false)}
                className="w-full bg-white text-slate-950 py-5 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-xl transition-all active:scale-[0.98] disabled:opacity-20 flex items-center justify-center gap-3"
              >
                {processing ? <Loader2 className="animate-spin" /> : <ArrowRightLeft size={20} />}
                Mover Pedidos
              </button>
              <button 
                onClick={onClose}
                className="w-full py-2 text-slate-500 font-bold text-[10px] uppercase tracking-widest hover:text-slate-300 transition-colors"
              >
                Cancelar Operação
              </button>
            </div>
          </>
        )}
      </div>
    </Modal>
  );
}
