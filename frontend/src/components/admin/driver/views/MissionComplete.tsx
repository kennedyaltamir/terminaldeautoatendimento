"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Trophy, Clock, MapPin, ArrowRight, Star } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import confetti from "canvas-confetti";

interface MissionCompleteProps {
  earnings: number;
  timeMinutes: number;
  distanceKm: number;
  onDone: () => void;
}

export default function MissionComplete({ earnings, timeMinutes, distanceKm, onDone }: MissionCompleteProps) {
  const [timeLeft, setTimeLeft] = useState(5);

  useEffect(() => {
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#10b981', '#fb923c', '#ffffff']
    });

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          onDone();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [onDone]);

  return (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      className="fixed inset-0 z-[9999] bg-black flex flex-col items-center justify-center p-6 text-center font-sans"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_#10b98115_0%,_transparent_70%)]" />
      
      <motion.div 
        initial={{ scale: 0.5, rotate: -20 }} 
        animate={{ scale: 1, rotate: 0 }} 
        transition={{ type: "spring", stiffness: 260, damping: 20 }}
        className="w-32 h-32 bg-emerald-500 text-white rounded-full flex items-center justify-center mb-8 shadow-[0_0_50px_rgba(16,185,129,0.4)] relative z-10"
      >
        <CheckCircle2 size={64} strokeWidth={3} />
      </motion.div>

      <h1 className="text-5xl font-black uppercase tracking-tighter mb-2 bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-500 relative z-10">
        Missão Finalizada
      </h1>

      <div className="flex items-center justify-center gap-2 text-emerald-500 font-black uppercase text-xs tracking-[0.3em] mb-10 relative z-10">
        <Star size={14} fill="currentColor" /> Entrega Confirmada <Star size={14} fill="currentColor" />
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ delay: 0.3 }}
        className="bg-slate-900 border border-white/10 p-8 rounded-[3rem] w-full max-w-sm space-y-6 shadow-2xl relative z-10"
      >
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500/20 p-2 rounded-xl text-emerald-400">
              <Trophy size={20} />
            </div>
            <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Ganhos</span>
          </div>
          <span className="text-3xl font-black text-emerald-400 tabular-nums">{formatCurrency(earnings * 100)}</span>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-6 border-t border-white/5">
          <div className="text-left">
            <div className="flex items-center gap-2 text-slate-500 mb-1">
              <Clock size={12} />
              <span className="text-[9px] font-black uppercase tracking-widest">Tempo</span>
            </div>
            <p className="text-xl font-black text-white">{timeMinutes} <span className="text-xs text-slate-500">min</span></p>
          </div>
          <div className="text-right">
            <div className="flex items-center gap-2 text-slate-500 mb-1 justify-end">
              <MapPin size={12} />
              <span className="text-[9px] font-black uppercase tracking-widest">Km</span>
            </div>
            <p className="text-xl font-black text-white">{distanceKm} <span className="text-xs text-slate-500">km</span></p>
          </div>
        </div>
      </motion.div>

      <div className="mt-12 flex flex-col items-center gap-4 relative z-10">
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-600">
          Voltando ao radar em <span className="text-orange-500 font-mono">{timeLeft}s</span>
        </p>
        <button 
          onClick={onDone}
          className="flex items-center gap-2 text-orange-500 font-black uppercase text-xs tracking-widest hover:text-orange-400 transition-colors group"
        >
          Pular Espera <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </motion.div>
  );
}
