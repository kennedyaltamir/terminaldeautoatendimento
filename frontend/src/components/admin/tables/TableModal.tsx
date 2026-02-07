/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 15.0.0 (Platinum Master)
 * DNA_ID: MF-TABLE-MODAL-V15-GOLD
 * Objective: Unified, elegant, and high-performance table management modal.
 */
"use client";

import React, { useState, useEffect, useCallback } from "react";
import { 
  X, Users, Clock, DollarSign, 
  ArrowRightLeft, Trash2, UserPlus,
  CheckCircle2, Loader2, Printer, 
  Plus, Copy, Hash, Receipt, ExternalLink
} from "lucide-react";
import Modal from "@/components/ui/Modal";
import { TableDashboard, TableSession } from "@/types";
import { formatCurrency, cn } from "@/lib/utils";
import TransferModal from "@/components/waiter/TransferModal";
import { deleteTable, openTable, closeTable, getTableActiveSession } from "@/lib/api";
import { toast } from "sonner";

interface TableModalProps {
  isOpen: boolean;
  onClose: () => void;
  table: TableDashboard | null;
  slug: string;
  onRefresh: () => void;
}

export default function TableModal({ 
  isOpen, 
  onClose, 
  table, 
  slug, 
  onRefresh 
}: TableModalProps) {
  // 🛡️ GUARD: Se não houver mesa, não renderiza nada.
  if (!table) return null;

  const isOccupied = table.status === 'occupied' || table.status === 'payment' || table.status === 'alert';

  // --- ESTADOS ---
  const [customerName, setCustomerName] = useState("");
  const [loading, setLoading] = useState(false);
  const [session, setSession] = useState<TableSession | null>(null);
  const [duration, setDuration] = useState("0min");
  const [isTransferOpen, setIsTransferOpen] = useState(false);

  // --- EFEITOS ---

  // 1. Reset e Fetch Inicial
  useEffect(() => {
    if (isOpen) {
      if (isOccupied) {
        // Estado inicial otimista baseado nos dados da dashboard
        if (table.active_session) {
          setSession({
            ...table.active_session,
            orders: [], // Será preenchido pelo fetch detalhado
            is_active: true,
            created_at: table.active_session.start_time,
            session_token: "",
            access_pin: table.active_session.access_pin
          } as any);
        }
        fetchSessionDetails();
      } else {
        setSession(null);
        setCustomerName("");
      }
    }
  }, [isOpen, table.id, isOccupied]);

  // 2. Timer de Duração (Apenas se ocupada)
  useEffect(() => {
    if (isOccupied && (session?.created_at || table.active_session?.start_time)) {
      const startTime = new Date(session?.created_at || table.active_session!.start_time).getTime();
      
      const updateTimer = () => {
        const now = Date.now();
        const diff = Math.floor((now - startTime) / 60000);
        const hours = Math.floor(diff / 60);
        const mins = diff % 60;
        setDuration(hours > 0 ? `${hours}h ${mins}min` : `${mins}min`);
      };

      updateTimer(); // Executa imediatamente
      const interval = setInterval(updateTimer, 60000); // Atualiza a cada minuto
      return () => clearInterval(interval);
    }
  }, [isOccupied, session, table]);

  // --- API CALLS ---

  const fetchSessionDetails = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getTableActiveSession(table.id);
      setSession(data);
    } catch (e) {
      console.error("Erro ao buscar detalhes da sessão:", e);
    } finally {
      setLoading(false);
    }
  }, [table.id]);

  const handleOpenSession = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customerName.trim()) return toast.warning("Informe o nome do cliente.");
    
    setLoading(true);
    try {
      await openTable(table.id, customerName);
      toast.success(`Mesa ${table.table_number} aberta para ${customerName}!`);
      onRefresh();
      onClose();
    } catch (e: any) {
      toast.error(e.message || "Falha ao abrir mesa.");
    } finally {
      setLoading(false);
    }
  };

  const handleCloseTable = async (method: string) => {
    if (!confirm("Tem certeza que deseja fechar esta mesa?")) return;
    setLoading(true);
    try {
      await closeTable(table.id, method);
      toast.success("Mesa finalizada!");
      onRefresh();
      onClose();
    } catch (e: any) {
      toast.error(e.message || "Erro ao fechar mesa");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm(`Deseja realmente excluir a Mesa ${table.table_number}?`)) return;
    setLoading(true);
    try {
      await deleteTable(table.id);
      toast.success("Mesa removida com sucesso.");
      onRefresh();
      onClose();
    } catch (e: any) {
      toast.error(e.message || "Erro ao excluir mesa.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopyPin = () => {
    const pin = session?.access_pin || table.active_session?.access_pin;
    if (pin) {
      navigator.clipboard.writeText(pin);
      toast.success("PIN copiado!");
    }
  };

  const tableUrl = `${typeof window !== 'undefined' ? window.location.origin : ''}/${slug}/menu?table=${table.table_number}&token=${table.qr_token}`;

  return (
    <>
      <Modal 
        isOpen={isOpen} 
        onClose={onClose} 
        title={isOccupied ? `Mesa ${table.table_number}` : `Mesa ${table.table_number} (Livre)`}
      >
        <div className="space-y-6">
          {!isOccupied ? (
            // ============================================================
            // 🟢 BRANCH A: MESA LIVRE (MODO ABERTURA)
            // ============================================================
            <form onSubmit={handleOpenSession} className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
               <div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl text-center">
                  <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/20 rounded-full flex items-center justify-center mx-auto mb-4 text-emerald-600">
                    <UserPlus size={32} />
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">Iniciar Atendimento</h3>
                  <p className="text-xs text-slate-500">Informe o cliente para liberar o cardápio.</p>
               </div>

               <div className="space-y-2">
                 <label className="text-[10px] font-black uppercase tracking-widest text-slate-500 ml-1">Nome do Cliente</label>
                 <div className="relative">
                    <Users className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                    <input 
                        autoFocus
                        value={customerName}
                        onChange={(e) => setCustomerName(e.target.value)}
                        className="w-full bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl pl-12 pr-4 py-4 text-lg font-bold outline-none focus:ring-2 focus:ring-orange-500 transition-all placeholder:text-slate-400"
                        placeholder="Ex: João Silva"
                    />
                 </div>
               </div>

               <div className="grid grid-cols-1 gap-3 pt-2">
                 <button 
                   type="submit"
                   disabled={loading || !customerName.trim()}
                   className="w-full py-4 bg-orange-600 hover:bg-orange-700 text-white rounded-xl font-black uppercase text-xs tracking-widest shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                 >
                   {loading ? <Loader2 className="animate-spin" /> : <CheckCircle2 size={18} />}
                   ABRIR MESA AGORA
                 </button>
                 
                 <button 
                   type="button"
                   onClick={handleDelete}
                   disabled={loading}
                   className="w-full py-3 bg-transparent border-2 border-red-100 dark:border-red-900/30 text-red-500 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-red-50 dark:hover:bg-red-900/10 transition-all flex items-center justify-center gap-2"
                 >
                   <Trash2 size={16} /> Excluir Mesa Física
                 </button>
               </div>
            </form>
          ) : (
            // ============================================================
            // 🔵 BRANCH B: MESA OCUPADA (TACTICAL DASHBOARD)
            // ============================================================
            <div className="space-y-5 animate-in fade-in slide-in-from-bottom-4">
              {/* Hero Card: Cliente & Total */}
              <div className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 p-6 rounded-[1.5rem] shadow-xl relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none group-hover:bg-emerald-500/20 transition-colors duration-700" />
                
                <div className="flex justify-between items-start relative z-10">
                  <div>
                    <p className="text-[10px] text-slate-400 font-black uppercase tracking-[0.2em] mb-1">Cliente</p>
                    <h3 className="text-2xl font-black text-white truncate max-w-[180px] tracking-tight">
                      {session?.customer_name || table.active_session?.customer_name}
                    </h3>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] text-emerald-500 font-black uppercase tracking-[0.2em] mb-1">Consumo</p>
                    <p className="text-3xl font-mono font-black text-emerald-400 tracking-tighter">
                      {formatCurrency(session?.total_spent || table.active_session?.total_spent || 0)}
                    </p>
                  </div>
                </div>

                {/* Vitals Grid */}
                <div className="grid grid-cols-2 gap-3 mt-6">
                  <div className="bg-slate-800/50 rounded-xl p-3 flex items-center gap-3 border border-white/5">
                    <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
                      <Clock size={16} />
                    </div>
                    <div>
                      <p className="text-[9px] text-slate-500 font-bold uppercase">Tempo</p>
                      <p className="text-sm font-mono font-bold text-slate-200">{duration}</p>
                    </div>
                  </div>
                  
                  <div 
                    onClick={handleCopyPin}
                    className="bg-slate-800/50 rounded-xl p-3 flex items-center gap-3 border border-white/5 cursor-pointer hover:bg-slate-800 transition-colors group/pin"
                  >
                    <div className="p-2 bg-orange-500/10 text-orange-400 rounded-lg">
                      <Hash size={16} />
                    </div>
                    <div>
                      <p className="text-[9px] text-slate-500 font-bold uppercase flex items-center gap-1">
                        PIN <Copy size={8} className="opacity-0 group-hover/pin:opacity-100 transition-opacity" />
                      </p>
                      <p className="text-sm font-mono font-bold text-slate-200 tracking-wider">
                        {session?.access_pin || table.active_session?.access_pin}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Grid */}
              <div className="grid grid-cols-2 gap-3">
                <button 
                  onClick={() => window.location.href = `/admin/${slug}/waiter/pos/${table.id}`}
                  className="col-span-2 py-4 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-black uppercase text-xs tracking-widest flex items-center justify-center gap-2 shadow-lg shadow-orange-900/20 active:scale-95 transition-all"
                >
                  <Plus size={18} /> Novo Pedido (POS)
                </button>

                <button 
                  onClick={() => setIsTransferOpen(true)}
                  className="flex flex-col items-center justify-center p-4 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-xl border border-slate-200 dark:border-slate-700 transition-all gap-1 active:scale-95"
                >
                  <ArrowRightLeft size={20} className="text-blue-500" />
                  <span className="text-[9px] font-black uppercase text-slate-600 dark:text-slate-300">Transferir</span>
                </button>
                
                <button 
                  onClick={() => window.open(tableUrl, '_blank')}
                  className="flex flex-col items-center justify-center p-4 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-xl border border-slate-200 dark:border-slate-700 transition-all gap-1 active:scale-95"
                >
                  <Receipt size={20} className="text-slate-500" />
                  <span className="text-[9px] font-black uppercase text-slate-600 dark:text-slate-300">Cardápio</span>
                </button>
              </div>

              <div className="pt-2 border-t border-slate-200 dark:border-slate-800">
                <button 
                  onClick={() => handleCloseTable('cash')}
                  disabled={loading}
                  className="w-full py-4 bg-emerald-600/10 hover:bg-emerald-600/20 text-emerald-600 border border-emerald-600/20 rounded-xl font-black uppercase text-xs tracking-widest flex items-center justify-center gap-2 transition-all active:scale-95"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <DollarSign size={18} />}
                  FECHAR CONTA
                </button>
              </div>
            </div>
          )}
        </div>
      </Modal>

      {/* Sub-Modal de Transferência */}
      <TransferModal 
        isOpen={isTransferOpen}
        onClose={() => setIsTransferOpen(false)}
        fromTableId={table.id}
        fromTableName={`Mesa ${table.table_number}`}
        slug={slug} 
        onSuccess={() => {
          onRefresh();
          onClose();
        }}
      />
    </>
  );
}
