"use client";
import { useState, useEffect } from "react";
import { Clock } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface InactivityModalProps {
  isOpen: boolean;
  onStay: () => void;
  onTimeout: () => void;
  countdownDuration?: number;
}

export default function InactivityModal({ isOpen, onStay, onTimeout, countdownDuration = 15 }: InactivityModalProps) {
  const [timeLeft, setTimeLeft] = useState(countdownDuration);

  useEffect(() => {
    if (isOpen) {
      setTimeLeft(countdownDuration);
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            onTimeout();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [isOpen, countdownDuration, onTimeout]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-950/90 backdrop-blur-md p-6">
      <AnimatePresence>
        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-white rounded-[3rem] p-12 max-w-lg w-full text-center shadow-2xl border-8 border-orange-500 relative overflow-hidden"
        >
          {/* Círculo de Progresso de Fundo */}
          <div className="absolute top-0 left-0 h-2 bg-orange-200 w-full">
            <motion.div 
              initial={{ width: "100%" }}
              animate={{ width: "0%" }}
              transition={{ duration: countdownDuration, ease: "linear" }}
              className="h-full bg-orange-600"
            />
          </div>

          <div className="w-24 h-24 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-8 animate-pulse">
            <Clock size={48} className="text-orange-600" />
          </div>
          
          <h2 className="text-4xl font-black text-slate-900 mb-4 tracking-tight">Ainda está aí?</h2>
          <p className="text-slate-500 text-xl mb-10 font-medium">
            Sua sessão será encerrada em <br/>
            <span className="text-6xl font-black text-orange-600 tabular-nums">{timeLeft}</span>
            <br/> segundos.
          </p>
          
          <button 
            onClick={onStay}
            className="w-full bg-slate-900 text-white py-6 rounded-3xl font-black text-2xl uppercase tracking-widest shadow-xl hover:bg-slate-800 transition-transform active:scale-95"
          >
            Continuar Comprando
          </button>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
