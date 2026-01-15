"use client";
import { useState, useEffect } from "react";
import { DollarSign, Users, Utensils, ArrowRight, TrendingUp, Zap, ShieldCheck, BarChart3 } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function RoiCalculator() {
  const [orders, setOrders] = useState(1500); // Pedidos/mês
  const [ticket, setTicket] = useState(45);   // Ticket Médio
  const [staff, setStaff] = useState(3);      // Garçons atuais

  const [savings, setSavings] = useState(0);
  const [efficiencyGain, setEfficiencyGain] = useState(0);
  const [upsellGain, setUpsellGain] = useState(0);

  useEffect(() => {
    // Lógica de Negócio MesaFlow (Baseada em benchmarks reais):
    // 1. Economia de 30% no custo de staff (otimização de tempo e redução de erros)
    const staffCost = staff * 2800; // Custo médio CLT + Encargos
    const efficiency = staffCost * 0.30;
    
    // 2. Aumento de 15% no faturamento via Upsell Automatizado e Giro de Mesa
    const currentRevenue = orders * ticket;
    const upsell = currentRevenue * 0.15;

    setEfficiencyGain(efficiency);
    setUpsellGain(upsell);
    setSavings(efficiency + upsell);
  }, [orders, ticket, staff]);

  return (
    <section className="py-24 bg-slate-950 relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-orange-600/10 rounded-full blur-[150px] -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 w-[800px] h-[800px] bg-blue-600/5 rounded-full blur-[150px] translate-y-1/2 -translate-x-1/2 pointer-events-none"></div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-20">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-xs font-black text-orange-500 uppercase tracking-[0.2em] mb-6"
          >
            <BarChart3 size={14} /> Simulador de Lucratividade
          </motion.div>
          <h2 className="text-5xl md:text-7xl font-black text-white tracking-tighter mb-6 leading-[0.95]">
            Quanto dinheiro você está <br/>
            <span className="text-orange-500">deixando na mesa?</span>
          </h2>
          <p className="text-slate-400 text-xl max-w-2xl mx-auto font-medium">
            Ajuste os controles abaixo e veja o impacto financeiro imediato ao implementar o MesaFlow OS.
          </p>
        </div>

        <div className="grid lg:grid-cols-12 gap-12 items-stretch">
          {/* Painel de Controles */}
          <div className="lg:col-span-7 bg-slate-900/50 backdrop-blur-2xl border border-slate-800 p-10 md:p-16 rounded-[3.5rem] shadow-2xl">
            <div className="space-y-12">
              {/* Slider 1: Pedidos */}
              <div className="space-y-6">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-black uppercase text-xs tracking-widest flex items-center gap-2">
                    <Utensils size={18} className="text-orange-500" /> Pedidos Mensais
                  </label>
                  <span className="text-3xl font-black text-white tabular-nums">{orders.toLocaleString()}</span>
                </div>
                <input 
                  type="range" min="100" max="10000" step="100" 
                  value={orders} 
                  onChange={(e) => setOrders(Number(e.target.value))} 
                  className="w-full h-2.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-600 font-black uppercase tracking-widest">
                  <span>100</span>
                  <span>5.000</span>
                  <span>10.000</span>
                </div>
              </div>

              {/* Slider 2: Ticket */}
              <div className="space-y-6">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-black uppercase text-xs tracking-widest flex items-center gap-2">
                    <DollarSign size={18} className="text-orange-500" /> Ticket Médio
                  </label>
                  <span className="text-3xl font-black text-white tabular-nums">R$ {ticket}</span>
                </div>
                <input 
                  type="range" min="10" max="500" step="5" 
                  value={ticket} 
                  onChange={(e) => setTicket(Number(e.target.value))} 
                  className="w-full h-2.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-600 font-black uppercase tracking-widest">
                  <span>R$ 10</span>
                  <span>R$ 250</span>
                  <span>R$ 500</span>
                </div>
              </div>

              {/* Slider 3: Staff */}
              <div className="space-y-6">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-black uppercase text-xs tracking-widest flex items-center gap-2">
                    <Users size={18} className="text-orange-500" /> Equipe de Salão
                  </label>
                  <span className="text-3xl font-black text-white tabular-nums">{staff} pessoas</span>
                </div>
                <input 
                  type="range" min="1" max="50" step="1" 
                  value={staff} 
                  onChange={(e) => setStaff(Number(e.target.value))} 
                  className="w-full h-2.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-600 font-black uppercase tracking-widest">
                  <span>1</span>
                  <span>25</span>
                  <span>50</span>
                </div>
              </div>
            </div>
          </div>

          {/* Painel de Resultado */}
          <div className="lg:col-span-5 flex flex-col">
            <div className="flex-1 bg-gradient-to-br from-orange-600 to-orange-700 p-12 rounded-[3.5rem] shadow-2xl shadow-orange-900/30 flex flex-col justify-between relative overflow-hidden border border-white/10">
              <div className="absolute top-0 right-0 p-10 opacity-10">
                <TrendingUp size={160} />
              </div>
              
              <div className="relative z-10">
                <p className="text-orange-100 font-black uppercase tracking-[0.2em] text-xs mb-4">Economia Estimada Mensal</p>
                <motion.div 
                  key={savings}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="text-7xl md:text-8xl font-black text-white tracking-tighter tabular-nums"
                >
                  R$ {savings.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
                </motion.div>
              </div>

              <div className="space-y-5 mt-16 relative z-10">
                <div className="flex justify-between items-center bg-white/10 backdrop-blur-xl p-5 rounded-3xl border border-white/10 shadow-lg">
                  <span className="text-orange-100 text-sm font-bold flex items-center gap-3">
                    <Zap size={20} className="fill-orange-100" /> Eficiência Operacional
                  </span>
                  <span className="text-white font-black text-lg">+ R$ {efficiencyGain.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}</span>
                </div>
                <div className="flex justify-between items-center bg-white/10 backdrop-blur-xl p-5 rounded-3xl border border-white/10 shadow-lg">
                  <span className="text-orange-100 text-sm font-bold flex items-center gap-3">
                    <TrendingUp size={20} /> Upsell Automatizado
                  </span>
                  <span className="text-white font-black text-lg">+ R$ {upsellGain.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}</span>
                </div>
              </div>

              <Link 
                href="/admin/register"
                className="mt-12 bg-white text-slate-950 px-8 py-6 rounded-2xl font-black text-2xl hover:bg-orange-50 transition-all w-full text-center flex items-center justify-center gap-4 group shadow-2xl active:scale-[0.98]"
              >
                Começar Agora <ArrowRight size={28} className="group-hover:translate-x-2 transition-transform" />
              </Link>
            </div>
            
            <div className="mt-6 flex items-center gap-2 justify-center text-slate-500 text-[10px] font-black uppercase tracking-[0.2em]">
              <ShieldCheck size={16} className="text-emerald-500" /> Cálculos baseados em médias de mercado (ABRASEL 2025)
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

