/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.0.0 (Fintech Initialized)
 * DNA_ID: MF-DRIVER-EARNINGS-V1
 * Objective: Financial dashboard for drivers with payout control.
 */
"use client";

import React, { useState } from "react";
import { 
  Wallet, TrendingUp, ArrowUpRight, ArrowDownRight, 
  Calendar, DollarSign, Download, ChevronRight,
  Target, PieChart
} from "lucide-react";
import { formatCurrency, cn } from "@/lib/utils";
import { motion } from "framer-motion";

export default function EarningsView() {
  const [period, setPeriod] = useState<'day' | 'week' | 'month'>('day');

  const stats = {
    balance: 85.50,
    pending: 1240.00,
    deliveries: 12,
    tips: 15.00,
    history: [
      { id: 1, label: 'Taxa de Entrega', value: 12.50, date: '14:20', type: 'credit' },
      { id: 2, label: 'Gorjeta Extra', value: 5.00, date: '13:15', type: 'credit' },
      { id: 3, label: 'Resgate para Conta', value: -150.00, date: 'Ontem', type: 'debit' },
    ]
  };

  return (
    <div className="p-6 space-y-8 pb-32 pt-20 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-black text-white uppercase tracking-tight">Financeiro</h2>
        <button className="bg-slate-900 border border-slate-800 p-2 rounded-xl text-slate-400">
          <Calendar size={20} />
        </button>
      </div>

      {/* 💰 SALDO ATUAL (HERO) */}
      <div className="bg-gradient-to-br from-emerald-600 to-emerald-800 rounded-[2.5rem] p-8 shadow-2xl shadow-emerald-900/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-20"><Wallet size={80} /></div>
        <div className="relative z-10">
          <p className="text-emerald-100 font-black uppercase text-[10px] tracking-[0.2em] mb-2">Disponível para Resgate</p>
          <h3 className="text-5xl font-black text-white tracking-tighter mb-6">{formatCurrency(stats.balance * 100)}</h3>
          <button className="w-full bg-white text-emerald-700 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all">
            Transferir para o Banco
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-900 border border-white/5 p-5 rounded-3xl">
          <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">A Receber</p>
          <p className="text-xl font-black text-white">{formatCurrency(stats.pending * 100)}</p>
        </div>
        <div className="bg-slate-900 border border-white/5 p-5 rounded-3xl">
          <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Gorjetas</p>
          <p className="text-xl font-black text-emerald-400">{formatCurrency(stats.tips * 100)}</p>
        </div>
      </div>

      {/* 📝 ÚLTIMOS LANÇAMENTOS */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest">Atividade Recente</h3>
          <button className="text-[10px] font-bold text-orange-500 uppercase">Ver tudo</button>
        </div>
        
        <div className="space-y-2">
          {stats.history.map(item => (
            <div key={item.id} className="bg-slate-900/50 border border-white/5 p-4 rounded-2xl flex justify-between items-center">
              <div className="flex items-center gap-4">
                <div className={cn(
                  "p-2 rounded-xl",
                  item.type === 'credit' ? "bg-emerald-500/10 text-emerald-500" : "bg-red-500/10 text-red-500"
                )}>
                  {item.type === 'credit' ? <ArrowUpRight size={18} /> : <ArrowDownRight size={18} />}
                </div>
                <div>
                  <p className="text-sm font-bold text-white">{item.label}</p>
                  <p className="text-[10px] text-slate-500">{item.date}</p>
                </div>
              </div>
              <span className={cn("font-black", item.type === 'credit' ? "text-white" : "text-red-500")}>
                {item.type === 'credit' ? '+' : ''}{formatCurrency(Math.abs(item.value) * 100)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

