"use client";
import { useState, useEffect } from "react";
import { DollarSign, Users, Utensils, ArrowRight, TrendingUp, Zap, ShieldCheck } from "lucide-react";
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
    // Lógica de Negócio MesaFlow:
    // 1. Economia de 30% no custo de staff (otimização de tempo)
    const staffCost = staff * 2800; // Custo médio CLT + Encargos
    const efficiency = staffCost * 0.30;
    
    // 2. Aumento de 15% no faturamento via Upsell Automatizado
    const currentRevenue = orders * ticket;
    const upsell = currentRevenue * 0.15;

    setEfficiencyGain(efficiency);
    setUpsellGain(upsell);
    setSavings(efficiency + upsell);
  }, [orders, ticket, staff]);

  return (
    <section className="py-24 bg-slate-950 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-orange-600/10 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/2"></div>
      <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[120px] translate-y-1/2 -translate-x-1/2"></div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-white tracking-tighter mb-4">
            Quanto dinheiro você está <br/>
            <span className="text-orange-500">deixando na mesa?</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Simule o impacto financeiro imediato ao implementar o MesaFlow na sua operação.
          </p>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 items-stretch">
          {/* Controles */}
          <div className="lg:col-span-7 bg-slate-900/50 backdrop-blur-xl border border-slate-800 p-8 md:p-12 rounded-[2.5rem] shadow-2xl">
            <div className="space-y-10">
              {/* Slider 1 */}
              <div className="space-y-4">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-bold flex items-center gap-2">
                    <Utensils size={18} className="text-orange-500" /> Pedidos Mensais
                  </label>
                  <span className="text-2xl font-black text-white">{orders.toLocaleString()}</span>
                </div>
                <input 
                  type="range" min="100" max="10000" step="100" 
                  value={orders} 
                  onChange={(e) => setOrders(Number(e.target.value))} 
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                  <span>100</span>
                  <span>5.000</span>
                  <span>10.000</span>
                </div>
              </div>

              {/* Slider 2 */}
              <div className="space-y-4">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-bold flex items-center gap-2">
                    <DollarSign size={18} className="text-orange-500" /> Ticket Médio
                  </label>
                  <span className="text-2xl font-black text-white">R$ {ticket}</span>
                </div>
                <input 
                  type="range" min="10" max="300" step="5" 
                  value={ticket} 
                  onChange={(e) => setTicket(Number(e.target.value))} 
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                  <span>R$ 10</span>
                  <span>R$ 150</span>
                  <span>R$ 300</span>
                </div>
              </div>

              {/* Slider 3 */}
              <div className="space-y-4">
                <div className="flex justify-between items-end">
                  <label className="text-slate-300 font-bold flex items-center gap-2">
                    <Users size={18} className="text-orange-500" /> Equipe de Salão
                  </label>
                  <span className="text-2xl font-black text-white">{staff} pessoas</span>
                </div>
                <input 
                  type="range" min="1" max="30" step="1" 
                  value={staff} 
                  onChange={(e) => setStaff(Number(e.target.value))} 
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500" 
                />
                <div className="flex justify-between text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                  <span>1</span>
                  <span>15</span>
                  <span>30</span>
                </div>
              </div>
            </div>
          </div>

          {/* Resultado */}
          <div className="lg:col-span-5 flex flex-col">
            <div className="flex-1 bg-gradient-to-br from-orange-600 to-orange-700 p-10 rounded-[2.5rem] shadow-2xl shadow-orange-900/20 flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-10">
                <TrendingUp size={120} />
              </div>
              
              <div className="relative z-10">
                <p className="text-orange-100 font-black uppercase tracking-widest text-sm mb-2">Economia Estimada Mensal</p>
                <motion.div 
                  key={savings}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="text-6xl md:text-7xl font-black text-white tracking-tighter"
                >
                  R$ {savings.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
                </motion.div>
              </div>

              <div className="space-y-4 mt-12 relative z-10">
                <div className="flex justify-between items-center bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
                  <span className="text-orange-100 text-sm font-bold flex items-center gap-2">
                    <Zap size={16} /> Eficiência Operacional
                  </span>
                  <span className="text-white font-black">+ R$ {efficiencyGain.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}</span>
                </div>
                <div className="flex justify-between items-center bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
                  <span className="text-orange-100 text-sm font-bold flex items-center gap-2">
                    <TrendingUp size={16} /> Upsell Automatizado
                  </span>
                  <span className="text-white font-black">+ R$ {upsellGain.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}</span>
                </div>
              </div>

              <Link 
                href="/admin/register"
                className="mt-10 bg-white text-slate-900 px-8 py-5 rounded-2xl font-black text-xl hover:bg-orange-50 transition-all w-full text-center flex items-center justify-center gap-3 group shadow-xl"
              >
                Começar Agora <ArrowRight size={24} className="group-hover:translate-x-2 transition-transform" />
              </Link>
            </div>
            
            <div className="mt-4 flex items-center gap-2 justify-center text-slate-500 text-[10px] font-bold uppercase tracking-widest">
              <ShieldCheck size={14} className="text-emerald-500" /> Cálculos baseados em médias de mercado (ABRASEL 2025)
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
