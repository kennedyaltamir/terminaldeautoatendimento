/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Gatekeeper de segurança para entrada em mesas ocupadas.
 * FEATURES: Teclado numérico, validação de 4 dígitos, feedback de erro.
 */
"use client";
import { useState } from "react";
import { Lock, ArrowRight, Loader2, XCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface PinEntryModalProps {
  isOpen: boolean;
  customerName: string;
  onConfirm: (pin: string) => Promise<void>;
  onCancel: () => void;
}

export default function PinEntryModal({ isOpen, customerName, onConfirm, onCancel }: PinEntryModalProps) {
  const [pin, setPin] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const handleKeypad = (num: string) => {
    setError(false);
    if (pin.length < 4) setPin(prev => prev + num);
  };

  const handleDelete = () => {
    setPin(prev => prev.slice(0, -1));
  };

  const handleSubmit = async () => {
    if (pin.length !== 4) return;
    setLoading(true);
    try {
      await onConfirm(pin);
    } catch (e) {
      setError(true);
      setPin("");
      if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-slate-950 p-4">
      <motion.div 
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-slate-900 border border-slate-800 w-full max-w-md rounded-[3rem] p-8 shadow-2xl text-center"
      >
        <div className="w-20 h-20 bg-orange-500/10 rounded-full flex items-center justify-center mx-auto mb-6 border border-orange-500/20">
          <Lock className="text-orange-500" size={32} />
        </div>

        <h2 className="text-2xl font-black text-white uppercase tracking-tight mb-2">Mesa Ocupada</h2>
        <p className="text-slate-400 text-sm mb-8">
          Esta mesa já está sendo usada por <span className="text-white font-bold">{customerName}</span>. 
          Insira o PIN de acesso para entrar na comanda.
        </p>

        {/* PIN Display */}
        <div className="flex justify-center gap-4 mb-10">
          {[...Array(4)].map((_, i) => (
            <div 
              key={i} 
              className={cn(
                "w-12 h-16 rounded-2xl border-2 flex items-center justify-center text-2xl font-black transition-all",
                error ? "border-red-500 text-red-500 animate-shake" : 
                pin[i] ? "border-orange-500 text-white bg-orange-500/10" : "border-slate-800 text-slate-700"
              )}
            >
              {pin[i] ? "•" : ""}
            </div>
          ))}
        </div>

        {/* Teclado Numérico */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
            <button 
              key={n} 
              onClick={() => handleKeypad(n.toString())}
              className="h-16 bg-slate-800 hover:bg-slate-700 rounded-2xl text-xl font-bold active:scale-90 transition-all"
            >
              {n}
            </button>
          ))}
          <button onClick={onCancel} className="text-slate-500 font-bold text-xs uppercase">Sair</button>
          <button onClick={() => handleKeypad("0")} className="h-16 bg-slate-800 hover:bg-slate-700 rounded-2xl text-xl font-bold">0</button>
          <button onClick={handleDelete} className="text-red-500 font-bold text-xs uppercase">Apagar</button>
        </div>

        <button
          disabled={pin.length !== 4 || loading}
          onClick={handleSubmit}
          className="w-full py-5 bg-orange-600 hover:bg-orange-500 disabled:bg-slate-800 disabled:text-slate-600 text-white rounded-2xl font-black uppercase tracking-widest shadow-xl transition-all flex items-center justify-center gap-2"
        >
          {loading ? <Loader2 className="animate-spin" /> : <ArrowRight size={20} />}
          Entrar na Mesa
        </button>

        {error && (
          <p className="text-red-500 text-xs font-bold mt-4 flex items-center justify-center gap-1">
            <XCircle size={14} /> PIN INCORRETO. TENTE NOVAMENTE.
          </p>
        )}
      </motion.div>
    </div>
  );
}

