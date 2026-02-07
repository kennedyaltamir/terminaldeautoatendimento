/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.0.0 (Fintech Cockpit)
 * Objective: Advanced payout management with financial vitals.
 */
"use client";

import React, { use, useState } from "react";
import { 
  Wallet, ArrowUpRight, Clock, CheckCircle2, 
  AlertCircle, DollarSign, TrendingUp, ArrowDownLeft,
  ShieldCheck, Landmark
} from "lucide-react";
import { formatCurrency, cn } from "@/lib/utils";

export default function PayoutsPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  const [balance] = useState(125050); // R$ 1.250,50
  const [pending] = useState(45000);  // R$ 450,00

  const history = [
    { id: 1, date: "02/02/2026", amount: 85000, status: "completed", bank: "Itaú (***4421)" },
    { id: 2, date: "28/01/2026", amount: 120000, status: "completed", bank: "Nubank (***9910)" },
    { id: 3, date: "03/02/2026", amount: 30000, status: "processing", bank: "Inter (***0021)" }
  ];

  return (
    <div className="space-y-8 p-8 animate-in fade-in duration-700">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tighter uppercase">Financeiro</h1>
          <p className="text-slate-500 text-sm font-bold uppercase tracking-widest mt-1">Gestão de Liquidez e Repasses</p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-full">
          <ShieldCheck size={16} className="text-emerald-500" />
          <span className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Ambiente Seguro</span>
        </div>
      </header>

      {/* Vitals Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-orange-600 rounded-[2.5rem] p-8 text-white shadow-2xl shadow-orange-900/20 relative overflow-hidden group">
          <Wallet className="absolute -right-4 -bottom-4 opacity-20 group-hover:scale-110 transition-transform duration-700" size={140} />
          <p className="text-orange-100 text-[10px] font-black uppercase tracking-[0.2em] mb-2">Disponível para Saque</p>
          <h2 className="text-5xl font-black tracking-tighter mb-8">{formatCurrency(balance)}</h2>
          <button className="w-full bg-white text-orange-600 py-4 rounded-2xl font-black uppercase text-xs tracking-widest hover:bg-slate-100 transition-all active:scale-95 shadow-lg">
            Solicitar Resgate Imediato
          </button>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-[2.5rem] p-8 flex flex-col justify-between">
          <div>
            <p className="text-slate-500 text-[10px] font-black uppercase tracking-[0.2em] mb-2">Aguardando Liberação</p>
            <h3 className="text-3xl font-black text-white tracking-tighter">{formatCurrency(pending)}</h3>
          </div>
          <div className="mt-4 flex items-center gap-2 text-slate-500 text-xs font-medium">
            <Clock size={14} /> Liberação em D+1 (Pix)
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-[2.5rem] p-8 flex flex-col justify-between">
          <div>
            <p className="text-slate-500 text-[10px] font-black uppercase tracking-[0.2em] mb-2">Volume Mensal (Bruto)</p>
            <h3 className="text-3xl font-black text-emerald-500 tracking-tighter">{formatCurrency(845000)}</h3>
          </div>
          <div className="mt-4 flex items-center gap-2 text-emerald-500 text-xs font-bold">
            <TrendingUp size={14} /> +12.5% que o mês anterior
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-[2.5rem] overflow-hidden shadow-2xl">
        <div className="p-8 border-b border-slate-800 bg-slate-950/30 flex justify-between items-center">
          <h3 className="text-white font-black text-xs uppercase tracking-[0.2em] flex items-center gap-2">
            <Landmark size={16} className="text-orange-500" /> Histórico de Transferências
          </h3>
          <button className="text-[10px] font-black text-slate-500 uppercase hover:text-white transition-colors">Ver Tudo</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-[10px] font-black text-slate-600 uppercase tracking-widest border-b border-slate-800">
                <th className="p-6">Data</th>
                <th className="p-6">Destino</th>
                <th className="p-6">Valor</th>
                <th className="p-6 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {history.map(item => (
                <tr key={item.id} className="hover:bg-white/5 transition-colors group">
                  <td className="p-6 text-sm font-bold text-slate-400">{item.date}</td>
                  <td className="p-6">
                    <p className="text-sm font-bold text-white">{item.bank}</p>
                    <p className="text-[10px] text-slate-500 uppercase font-black">Transferência Pix</p>
                  </td>
                  <td className="p-6 text-sm font-black text-white">{formatCurrency(item.amount)}</td>
                  <td className="p-6 text-right">
                    <span className={cn(
                      "px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest border",
                      item.status === 'completed' ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : "bg-blue-500/10 text-blue-500 border-blue-500/20 animate-pulse"
                    )}>
                      {item.status === 'completed' ? "Concluído" : "Processando"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
