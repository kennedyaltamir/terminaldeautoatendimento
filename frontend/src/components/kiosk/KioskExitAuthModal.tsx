"use client";
import { useState, useEffect, useCallback } from "react";
import { Lock, X, AlertTriangle, Loader2, ShieldAlert, Delete, WifiOff } from "lucide-react";
import { useKiosk, UnlockResult } from "@/context/KioskContext";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface KioskExitAuthModalProps {
  isBreach?: boolean;
}

export default function KioskExitAuthModal({ isBreach = false }: KioskExitAuthModalProps) {
  const { validateAndUnlock, toggleLock, lockoutEndTime } = useKiosk();
  const [password, setPassword] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorType, setErrorType] = useState<"INVALID_PASSWORD" | "LOCKED_OUT" | "NETWORK_ERROR" | null>(null);
  const [timeLeft, setTimeLeft] = useState<number>(0);

  useEffect(() => {
    if (!lockoutEndTime) {
      setTimeLeft(0);
      setErrorType(null);
      return;
    }
    const interval = setInterval(() => {
      const remaining = Math.ceil((lockoutEndTime - Date.now()) / 1000);
      if (remaining <= 0) {
        setTimeLeft(0);
        setErrorType(null);
        clearInterval(interval);
      } else {
        setTimeLeft(remaining);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [lockoutEndTime]);

  useEffect(() => {
    if (errorType === "INVALID_PASSWORD" || errorType === "NETWORK_ERROR") {
      setErrorType(null);
    }
  }, [password]);

  const handleConfirm = async () => {
    if (timeLeft > 0 || password.length === 0 || isProcessing) return;
    
    setIsProcessing(true);
    try {
      const result = await validateAndUnlock(password);
      if (result.ok) {
        setPassword("");
        setErrorType(null);
      } else {
        setErrorType(result.reason);
        setPassword("");
        if (result.reason === "INVALID_PASSWORD" && typeof navigator !== "undefined" && navigator.vibrate) {
          navigator.vibrate([50, 50, 50]);
        }
      }
    } catch (e) {
      console.error("Unexpected error in modal:", e);
      setErrorType("NETWORK_ERROR");
    } finally {
      // GARANTIA DE DESBLOQUEIO DA UI
      setIsProcessing(false);
    }
  };

  const handleCancel = () => {
    if (isBreach) return; 
    toggleLock(); 
  };

  const handleKeypad = useCallback((key: string) => {
    if (timeLeft > 0 || isProcessing) return;
    if (key === "DEL") {
      setPassword((prev) => prev.slice(0, -1));
    } else if (key === "ENTER") {
      handleConfirm();
    } else {
      if (password.length < 8) {
        setPassword((prev) => prev + key);
      }
    }
  }, [timeLeft, isProcessing, password]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (timeLeft > 0) return;
      if (e.key >= "0" && e.key <= "9") handleKeypad(e.key);
      if (e.key === "Backspace") handleKeypad("DEL");
      if (e.key === "Enter") handleConfirm();
      if (e.key === "Escape" && !isBreach) handleCancel();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeypad, handleConfirm, handleCancel, isBreach, timeLeft]);

  const isLockedOut = timeLeft > 0;

  const renderErrorMessage = () => {
    if (isLockedOut) return null;
    switch (errorType) {
      case "INVALID_PASSWORD":
        return "SENHA INCORRETA";
      case "NETWORK_ERROR":
        return "ERRO DE CONEXÃO";
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-950/98 backdrop-blur-xl p-4 select-none">
      <AnimatePresence>
        <motion.div 
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ 
            scale: 1, 
            opacity: 1,
            x: errorType === "INVALID_PASSWORD" ? [0, -10, 10, -10, 10, 0] : 0 
          }}
          transition={{ duration: 0.3 }}
          className={cn(
            "w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden border-2 flex flex-col",
            isBreach ? "bg-red-950/30 border-red-600" : "bg-slate-900 border-slate-800"
          )}
        >
          <div className="p-8 text-center pb-4">
            <div className={cn(
              "w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 border-4 shadow-lg",
              isBreach 
                ? "bg-red-900/50 border-red-500 text-red-500 animate-pulse" 
                : isLockedOut 
                  ? "bg-yellow-900/50 border-yellow-500 text-yellow-500"
                  : errorType === "NETWORK_ERROR"
                    ? "bg-slate-800 border-slate-600 text-slate-400"
                    : "bg-slate-800 border-slate-700 text-orange-500"
            )}>
              {isBreach ? <ShieldAlert size={40} /> : 
               isLockedOut ? <AlertTriangle size={40} /> : 
               errorType === "NETWORK_ERROR" ? <WifiOff size={40} /> :
               <Lock size={36} />}
            </div>
            <h2 className="text-2xl font-black text-white mb-2 tracking-tight">
              {isBreach ? "VIOLAÇÃO DE SEGURANÇA" : "Acesso Administrativo"}
            </h2>
            <p className={cn("text-sm font-bold", isBreach ? "text-red-400" : "text-slate-400")}>
              {isLockedOut 
                ? `Sistema bloqueado temporariamente.` 
                : isBreach 
                  ? "O modo quiosque foi interrompido forçadamente." 
                  : "Digite a senha mestre para manutenção."}
            </p>
          </div>

          <div className="px-8 mb-6">
            <div className={cn(
              "h-16 rounded-2xl border-2 flex items-center justify-center gap-3 transition-all",
              errorType === "INVALID_PASSWORD" ? "border-red-500 bg-red-500/10" : 
              errorType === "NETWORK_ERROR" ? "border-yellow-500 bg-yellow-500/10" :
              "border-slate-700 bg-slate-950/50"
            )}>
              {isLockedOut ? (
                <span className="text-xl font-mono font-bold text-yellow-500 animate-pulse">
                  Aguarde {timeLeft}s
                </span>
              ) : (
                [...Array(6)].map((_, i) => (
                  <div 
                    key={i} 
                    className={cn(
                      "w-3 h-3 rounded-full transition-all duration-200",
                      i < password.length 
                        ? isBreach ? "bg-red-500 scale-125" : "bg-white scale-125" 
                        : "bg-slate-800"
                    )} 
                  />
                ))
              )}
            </div>
            {errorType && !isLockedOut && (
              <p className={cn(
                "text-center text-xs font-bold mt-2 uppercase tracking-wider",
                errorType === "NETWORK_ERROR" ? "text-yellow-500" : "text-red-500"
              )}>
                {renderErrorMessage()}
              </p>
            )}
          </div>

          <div className="px-6 pb-6 grid grid-cols-3 gap-3">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
              <button
                key={num}
                onClick={() => handleKeypad(String(num))}
                disabled={isLockedOut || isProcessing}
                className="h-16 bg-slate-800/80 hover:bg-slate-700 active:bg-slate-600 rounded-xl text-2xl font-bold text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              >
                {num}
              </button>
            ))}
            <button 
              onClick={handleCancel}
              disabled={isBreach || isLockedOut || isProcessing}
              className={cn(
                "h-16 rounded-xl text-xs font-black uppercase tracking-wider transition-colors flex items-center justify-center",
                isBreach 
                  ? "bg-transparent text-transparent cursor-default" 
                  : "bg-slate-800/50 text-slate-400 hover:bg-slate-800 hover:text-white"
              )}
            >
              {isBreach ? "" : "Cancelar"}
            </button>
            <button 
              onClick={() => handleKeypad("0")}
              disabled={isLockedOut || isProcessing}
              className="h-16 bg-slate-800/80 hover:bg-slate-800 active:bg-slate-600 rounded-xl text-2xl font-bold text-white transition-colors disabled:opacity-30"
            >
              0
            </button>
            <button 
              onClick={() => handleKeypad("DEL")}
              disabled={isLockedOut || isProcessing}
              className="h-16 bg-slate-800/50 hover:bg-slate-800 text-slate-400 hover:text-white rounded-xl flex items-center justify-center transition-colors disabled:opacity-30"
            >
              <Delete size={24} />
            </button>
          </div>

          <div className="p-6 pt-0">
            <button 
              onClick={handleConfirm}
              disabled={isLockedOut || password.length === 0 || isProcessing}
              data-testid="kiosk-unlock-confirm"
              className={cn(
                "w-full py-5 rounded-2xl font-black uppercase tracking-[0.2em] text-sm shadow-lg transition-all active:scale-[0.98] flex items-center justify-center gap-3",
                isBreach 
                  ? "bg-red-600 hover:bg-red-500 text-white shadow-red-900/20" 
                  : "bg-orange-600 hover:bg-orange-500 text-white shadow-orange-900/20",
                "disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none disabled:bg-slate-800 disabled:text-slate-500"
              )}
            >
              {isProcessing ? (
                <>
                  <Loader2 className="animate-spin" size={20} /> Verificando...
                </>
              ) : (
                isBreach ? "Restaurar Sistema" : "Desbloquear"
              )}
            </button>
          </div>
          
          <div className="pb-4 text-center">
             <p className="text-[10px] text-slate-600 font-mono uppercase tracking-widest">
                Acesso restrito • Operação registrada
             </p>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

