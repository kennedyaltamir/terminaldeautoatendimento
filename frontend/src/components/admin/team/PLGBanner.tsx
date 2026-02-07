"use client";

import { TrendingUp, Crown, Lock } from "lucide-react";

interface PLGBannerProps {
  onUpgrade: () => void;
}

export default function PLGBanner({ onUpgrade }: PLGBannerProps) {
  return (
    <div className="mt-8 bg-gradient-to-r from-slate-900 to-slate-800 border border-slate-700 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-6 relative overflow-hidden shadow-2xl group">
      {/* Micro-animação de fundo otimizada */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none group-hover:bg-orange-500/20 transition-colors duration-700 will-change-transform" />
      
      <div className="flex items-center gap-4 relative z-10">
        <div className="bg-slate-800 p-3 rounded-xl text-orange-500 border border-slate-700 group-hover:scale-110 transition-transform">
          <TrendingUp size={24} />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            Quem vende mais? <Crown size={16} className="text-yellow-500 fill-yellow-500 animate-pulse" />
          </h3>
          <p className="text-sm text-slate-400">
            Descubra qual garçom tem o melhor desempenho e otimize sua escala.
          </p>
        </div>
      </div>

      <button 
        onClick={onUpgrade}
        aria-label="Desbloquear relatórios de performance com o plano Pro"
        className="bg-white text-slate-900 px-6 py-3 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-slate-200 transition-all shadow-lg relative z-10 whitespace-nowrap flex items-center gap-2 active:scale-95 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-900 outline-none"
      >
        <Lock size={14} className="text-slate-400" /> Desbloquear Relatórios
      </button>
    </div>
  );
}
