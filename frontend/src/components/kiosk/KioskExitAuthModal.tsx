/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Modal de Desbloqueio Administrativo.
 * FEATURES: Teclado virtual, feedback de erro, estado de violação (Vermelho).
 */
"use client";
import { useState, useEffect, useCallback } from "react";
import { Lock, ShieldAlert, Delete, Loader2 } from "lucide-react";
import { useKiosk } from "@/context/KioskContext";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

export default function KioskExitAuthModal() {
  const { state, validateAndUnlock, toggleLock, lockoutEndTime } = useKiosk();
  const [password, setPassword] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorType, setErrorType] = useState<"INVALID_PASSWORD" | "LOCKED_OUT" | "NETWORK_ERROR" | null>(null);
  const [timeLeft, setTimeLeft] = useState<number>(0);

  const isOpen = state === "UNLOCKING" || state === "BREACHED";
  const isBreach = state === "BREACHED";

  // Gerenciador de Cooldown (Lockout)
  useEffect(() => {
    if (!lockoutEndTime) return;
    const update = () => {
      const remaining = Math.ceil((lockoutEndTime - Date.now()) / 1000);
      if (remaining <= 0) {
        setTimeLeft(0);
        setErrorType(null);
      } else {
        setTimeLeft(remaining);
      }
    };
    update();
    const timer = setInterval(update, 1000);
    return () => clearInterval(timer);
  }, [lockoutEndTime]);

  const handleConfirm = async () => {
    if (password.length === 0 || isProcessing || timeLeft > 0) return;
    setIsProcessing(true);
    try {
      const result = await validateAndUnlock(password);
      if (result.ok) {
        setPassword("");
        setErrorType(null);
      } else {
        setErrorType(result.reason);
        setPassword("");
        if (typeof navigator !== "undefined" && navigator.vibrate) navigator.vibrate([50, 50, 50]);
      }
    } catch (e) {
      setErrorType("NETWORK_ERROR");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeypad = useCallback((key: string) => {
    if (isProcessing || timeLeft > 0) return;
    if (key === "DEL") setPassword((p) => p.slice(0, -1));
    else if (key === "ENTER") handleConfirm();
    else if (password.length < 6) setPassword((p) => p + key);
  }, [isProcessing, timeLeft, password]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[10000] flex items-center justify-center bg-slate-950/98 backdrop-blur-xl p-4 select-none">
      <AnimatePresence>
        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1, x: errorType === "INVALID_PASSWORD" ? [0, -10, 10, -10, 10, 0] : 0 }}
          className={cn(
            "w-full max-w-md rounded-[3rem] shadow-2xl overflow-hidden border-4 flex flex-col",
            isBreach ? "bg-red-950/30 border-red-600" : "bg-slate-900 border-slate-800"
          )}
        >
          {/* Header do Modal */}
          <div className="p-8 text-center">
            <div className={cn(
              "w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 border-4",
              isBreach ? "bg-red-900/50 border-red-500 text-red-500 animate-pulse" : "bg-slate-800 border-slate-700 text-orange-500"
            )}>
              {isBreach ? <ShieldAlert size={40} /> : <Lock size={36} />}
            </div>
            <h2 className="text-2xl font-black text-white uppercase tracking-tight">
              {isBreach ? "SISTEMA VIOLADO" : "Manutenção"}
            </h2>
            <p className="text-sm font-bold text-slate-500 mt-2">
              {timeLeft > 0 ? `Bloqueado por ${timeLeft}s` : "Digite a senha mestra para continuar."}
            </p>
          </div>

          {/* Senha Visual */}
          <div className="px-8 mb-6">
            <div className={cn(
              "h-16 rounded-2xl border-2 flex items-center justify-center gap-4 transition-all bg-slate-950/50",
              errorType === "INVALID_PASSWORD" ? "border-red-500" : "border-slate-700"
            )}>
              {[...Array(6)].map((_, i) => (
                <div key={i} className={cn("w-3 h-3 rounded-full", i < password.length ? "bg-orange-500 scale-125" : "bg-slate-800")} />
              ))}
            </div>
          </div>

          {/* Teclado */}
          <div className="px-6 pb-6 grid grid-cols-3 gap-3">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
              <button key={num} onClick={() => handleKeypad(String(num))} className="h-16 bg-slate-800 hover:bg-slate-700 rounded-2xl text-2xl font-bold text-white transition-colors">
                {num}
              </button>
            ))}
            <button onClick={() => !isBreach && toggleLock()} className="h-16 text-slate-500 font-black uppercase text-xs hover:text-white transition-colors">
              {isBreach ? "" : "Cancelar"}
            </button>
            <button onClick={() => handleKeypad("0")} className="h-16 bg-slate-800 hover:bg-slate-700 rounded-2xl text-2xl font-bold text-white">0</button>
            <button onClick={() => handleKeypad("DEL")} className="h-16 flex items-center justify-center text-slate-400 hover:text-white transition-colors"><Delete /></button>
          </div>

          <div className="p-6 pt-0">
            <button 
              onClick={handleConfirm}
              disabled={isProcessing || timeLeft > 0}
              className={cn(
                "w-full py-5 rounded-2xl font-black uppercase tracking-widest text-white shadow-xl transition-all active:scale-95",
                isBreach ? "bg-red-600 hover:bg-red-500" : "bg-orange-600 hover:bg-orange-500"
              )}
            >
              {isProcessing ? <Loader2 className="animate-spin mx-auto" /> : "DESBLOQUEAR"}
            </button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
