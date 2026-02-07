"use client";

import { useState } from "react";
import { Lock, Key, ArrowRight, Loader2, ChevronLeft } from "lucide-react";
import { joinTable } from "@/lib/api";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

interface BlockedTableScreenProps {
  customerName: string;
  tableId: string;
  slug: string;
  qrToken: string;
  onSuccess: (token: string) => void;
}

/**
 * BlockedTableScreen - Interface de bloqueio de mesa ocupada.
 * Permite a recuperação de sessão via Token de Acesso (PIN).
 */
export default function BlockedTableScreen({ 
  customerName, 
  tableId, 
  slug, 
  qrToken,
  onSuccess 
}: BlockedTableScreenProps) {
  const [pin, setPin] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPinInput, setShowPinInput] = useState(false);

  const handleRecover = async () => {
    if (pin.length < 10) {
      toast.error("O Token deve conter exatamente 10 dígitos.");
      return;
    }

    setLoading(true);
    try {
      // CORREÇÃO DO ERRO TS2554: Passando os argumentos como objeto conforme definido em lib/api.ts
      const session = await joinTable(slug, {
        table_id: parseInt(tableId),
        qr_token: qrToken,
        customer_name: customerName,
        pin: pin
      });

      toast.success("Acesso restaurado com sucesso!");
      onSuccess(session.session_token);
    } catch (e: any) {
      toast.error(e.message || "Token inválido ou expirado. Verifique com o garçom.");
      setPin(""); // Limpa o input em caso de erro
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center text-white font-sans">
      <motion.div 
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="w-24 h-24 bg-red-500/10 rounded-full flex items-center justify-center mb-8 border border-red-500/20 shadow-[0_0_30px_rgba(239,68,68,0.1)]"
      >
        <Lock size={48} className="text-red-500 animate-pulse" />
      </motion.div>

      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        <h1 className="text-4xl font-black mb-3 tracking-tight">Mesa Ocupada</h1>
        <p className="text-slate-400 text-lg mb-10 max-w-sm mx-auto leading-relaxed">
          Esta mesa está sendo utilizada por <span className="text-white font-bold underline decoration-orange-500/50">{customerName}</span>.
        </p>
      </motion.div>

      <AnimatePresence mode="wait">
        {!showPinInput ? (
          <motion.div 
            key="options"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6 w-full max-w-xs"
          >
            <button 
              onClick={() => setShowPinInput(true)}
              className="w-full bg-white text-slate-950 py-4 rounded-2xl font-black flex items-center justify-center gap-3 transition-all hover:bg-orange-500 hover:text-white active:scale-95 shadow-xl"
            >
              <Key size={20} /> TENHO O TOKEN
            </button>
            
            <div className="pt-6 border-t border-slate-800">
              <p className="text-xs text-slate-500 font-medium leading-relaxed">
                Se você é <span className="text-slate-300">{customerName}</span> e sua sessão expirou, 
                solicite o Token de 10 dígitos ao garçom para continuar seu pedido.
              </p>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            key="input"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="w-full max-w-xs"
          >
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-[2.5rem] shadow-2xl">
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-4">
                Token de Acesso
              </label>
              
              <div className="flex flex-col gap-4">
                <input 
                  type="tel" 
                  maxLength={10}
                  className="w-full bg-slate-950 border-2 border-slate-800 rounded-2xl p-4 text-center text-white text-2xl font-mono tracking-[0.3em] focus:border-orange-500 outline-none transition-all"
                  placeholder="0000000000"
                  value={pin}
                  onChange={e => setPin(e.target.value.replace(/\D/g, ""))}
                  autoFocus
                />
                
                <button 
                  onClick={handleRecover}
                  disabled={loading || pin.length < 10}
                  className="w-full bg-orange-600 text-white py-4 rounded-2xl font-black uppercase tracking-widest text-sm hover:bg-orange-500 disabled:opacity-30 disabled:grayscale transition-all flex items-center justify-center gap-2 shadow-lg shadow-orange-900/20"
                >
                  {loading ? <Loader2 className="animate-spin" /> : (
                    <>VALIDAR ACESSO <ArrowRight size={18} /></>
                  )}
                </button>
              </div>
            </div>

            <button 
              onClick={() => setShowPinInput(false)}
              className="mt-8 text-slate-500 hover:text-white text-xs font-black uppercase tracking-widest flex items-center justify-center gap-2 mx-auto transition-colors"
            >
              <ChevronLeft size={14} /> Voltar
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <footer className="fixed bottom-8 text-[10px] text-slate-600 font-mono uppercase tracking-[0.3em]">
        MesaFlow Security Protocol v2.4
      </footer>
    </div>
  );
}