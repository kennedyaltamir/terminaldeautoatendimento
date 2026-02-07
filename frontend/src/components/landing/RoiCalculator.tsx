
/**
 * 📊 ROI CALCULATOR - VERSION 2.5 (Automation Friendly)
 * DOMAIN: FRONTEND / LANDING
 * DESCRIPTION: Simulador de economia com inputs acessíveis para scripts forenses.
 */
"use client";
import { useState, useEffect } from "react";
import { DollarSign, Users, Utensils, TrendingUp, Zap, BarChart3 } from "lucide-react";
import { motion } from "framer-motion";

export default function RoiCalculator() {
  const [orders, setOrders] = useState(1500);
  const [ticket, setTicket] = useState(45);
  const [staff, setStaff] = useState(3);
  const [savings, setSavings] = useState(0);

  useEffect(() => {
    const staffCost = staff * 2800;
    const efficiency = staffCost * 0.30;
    const currentRevenue = orders * ticket;
    const upsell = currentRevenue * 0.15;
    setSavings(efficiency + upsell);
  }, [orders, ticket, staff]);

  return (
    <section id="roi-simulator" className="py-24 bg-slate-950 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid lg:grid-cols-12 gap-12">
          <div className="lg:col-span-7 bg-slate-900/50 p-10 rounded-[3.5rem] border border-slate-800">
            <div className="space-y-12">
              {/* Pedidos */}
              <div className="space-y-4">
                <div className="flex justify-between">
                  <label className="text-slate-300 font-bold text-xs uppercase tracking-widest flex items-center gap-2">
                    <Utensils size={16} className="text-orange-500" /> Pedidos Mensais
                  </label>
                  <input 
                    type="number"
                    value={orders}
                    onChange={(e) => setOrders(Number(e.target.value))}
                    className="bg-transparent text-right text-2xl font-black text-white outline-none w-24"
                    data-testid="input-orders-manual"
                  />
                </div>
                <input 
                  type="range" min="100" max="10000" step="100" 
                  value={orders} 
                  onChange={(e) => setOrders(Number(e.target.value))}
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500"
                />
              </div>

              {/* Ticket */}
              <div className="space-y-4">
                <div className="flex justify-between">
                  <label className="text-slate-300 font-bold text-xs uppercase tracking-widest flex items-center gap-2">
                    <DollarSign size={16} className="text-orange-500" /> Ticket Médio
                  </label>
                  <input 
                    type="number"
                    value={ticket}
                    onChange={(e) => setTicket(Number(e.target.value))}
                    className="bg-transparent text-right text-2xl font-black text-white outline-none w-24"
                    data-testid="input-ticket-manual"
                  />
                </div>
                <input 
                  type="range" min="10" max="500" step="5" 
                  value={ticket} 
                  onChange={(e) => setTicket(Number(e.target.value))}
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500"
                />
              </div>
            </div>
          </div>

          <div className="lg:col-span-5">
            <div className="bg-orange-600 p-12 rounded-[3.5rem] h-full flex flex-col justify-center text-white shadow-2xl shadow-orange-900/20">
              <p className="text-orange-100 font-black uppercase text-xs tracking-widest mb-4">Economia Estimada</p>
              <motion.div 
                key={savings}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="text-6xl md:text-7xl font-black tracking-tighter"
              >
                R$ {savings.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
              </motion.div>
              <p className="mt-8 text-orange-100 text-sm leading-relaxed">
                Baseado em otimização de staff e aumento de 15% no giro de mesa via autoatendimento.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
