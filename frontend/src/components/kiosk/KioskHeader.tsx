"use client";

import React from "react";
import { ArrowLeft, ChefHat, Info } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

interface KioskHeaderProps {
  companyName: string;
  primaryColor: string;
}

/**
 * KioskHeader: Cabeçalho simplificado para modo totem.
 * Remove navegações externas e foca na marca e retorno ao attract screen.
 */
export default function KioskHeader({ companyName, primaryColor }: KioskHeaderProps) {
  const router = useRouter();

  return (
    <header className="bg-slate-900 border-b border-slate-800 p-6 flex justify-between items-center sticky top-0 z-40">
      <button 
        onClick={() => router.back()}
        className="bg-slate-800 text-white p-4 rounded-2xl flex items-center gap-3 font-bold hover:bg-slate-700 transition-all active:scale-95"
      >
        <ArrowLeft size={24} />
        Voltar
      </button>

      <div className="flex items-center gap-4">
        <div 
          className="p-3 rounded-2xl shadow-lg"
          style={{ backgroundColor: primaryColor }}
        >
          <ChefHat size={32} className="text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight uppercase">{companyName}</h2>
          <div className="flex items-center gap-1.5 text-orange-500 text-[10px] font-black tracking-widest">
             <div className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-ping" />
             AUTOATENDIMENTO ATIVO
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 px-6 py-3 rounded-2xl border border-slate-700 flex items-center gap-3 text-slate-400">
        <Info size={20} />
        <span className="text-sm font-bold uppercase tracking-wider">Toque nos itens para adicionar</span>
      </div>
    </header>
  );
}

