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

  // 1. Efeito de Montagem (Confetes)
  useEffect(() => {
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };
    const randomInRange = (min: number, max: number) => Math.random() * (max - min) + min;

    const interval: any = setInterval(function() {
      const timeLeft = animationEnd - Date.now();
      if (timeLeft <= 0) return clearInterval(interval);
      const particleCount = 50 * (timeLeft / duration);
      confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
      confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
    }, 250);

    return () => clearInterval(interval);
  }, []);

  // 2. Efeito de Timer (Contagem Regressiva Pura)
  useEffect(() => {
    if (timeLeft === 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  // 3. Efeito de Gatilho (Side Effect Seguro)
  // 🛡️ FIX: Dispara o onDone apenas quando o estado timeLeft muda para 0, fora do render loop.
  useEffect(() => {
    if (timeLeft === 0) {
      onDone();
    }
  }, [timeLeft, onDone]);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }} 
      animate={{ opacity: 1, scale: 1 }} 
      className="fixed inset-0 z-[9999] bg-black flex flex-col items-center justify-center p-6 text-center font-sans relative overflow-hidden"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_#10b98115_0%,_transparent_70%)]" />
      
      <motion.div 
        initial={{ scale: 0, rotate: -180 }} 
        animate={{ scale: 1, rotate: 0 }} 
        transition={{ type: "spring", stiffness: 260, damping: 20 }} 
        className="w-32 h-32 bg-emerald-500 text-white rounded-full flex items-center justify-center mb-8 shadow-[0_0_50px_rgba(16,185,129,0.4)] relative z-10 border-4 border-white/20"
      >
        <CheckCircle2 size={64} strokeWidth={3} />
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="z-10">
        <h1 className="text-5xl font-black uppercase tracking-tighter mb-2 bg-clip-text text-transparent bg-gradient-to-b from-white to-emerald-400">
          Missão Cumprida!
        </h1>
        <div className="flex items-center justify-center gap-2 text-emerald-500 font-black uppercase text-xs tracking-[0.3em] mb-10">
          <Star size={14} fill="currentColor" /> Entrega Finalizada <Star size={14} fill="currentColor" />
        </div>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ delay: 0.4 }} 
        className="bg-slate-900/50 backdrop-blur-xl p-8 rounded-[3rem] border border-white/10 w-full max-w-sm space-y-8 shadow-2xl relative z-10"
      >
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500/20 p-2 rounded-xl text-emerald-400">
              <Trophy size={20} />
            </div>
            <span className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Seu Ganho</span>
          </div>
          <span className="text-4xl font-black text-white tracking-tighter">{formatCurrency(earnings)}</span>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
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
              <span className="text-[9px] font-black uppercase tracking-widest">Distância</span>
            </div>
            <p className="text-xl font-black text-white">{distanceKm} <span className="text-xs text-slate-500">km</span></p>
          </div>
        </div>
      </motion.div>

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }} className="mt-12 space-y-4 z-10">
        <div className="flex flex-col items-center gap-2">
          <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">
            Retornando à base em
          </p>
          <div className="text-4xl font-mono font-black text-orange-500">
            {timeLeft}s
          </div>
        </div>
        <button 
          onClick={onDone}
          className="flex items-center gap-2 text-white/40 hover:text-white transition-colors text-xs font-bold uppercase tracking-widest group"
        >
          Pular Espera <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </motion.div>
    </motion.div>
  );
}
