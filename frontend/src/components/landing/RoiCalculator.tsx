"use client";
import { useState, useEffect } from "react";
import { DollarSign, Users, Utensils } from "lucide-react";

export default function RoiCalculator() {
  const [orders, setOrders] = useState(1500); // Pedidos/mês
  const [ticket, setTicket] = useState(45);   // Ticket Médio
  const [staff, setStaff] = useState(3);      // Garçons atuais

  const [savings, setSavings] = useState(0);
  const [revenueIncrease, setRevenueIncrease] = useState(0);

  useEffect(() => {
    // Lógica: MesaFlow economiza 30% do tempo da equipe + Aumenta ticket em 15% (Upsell)
    const staffCost = staff * 2500; // Custo estimado por funcionário
    const operationalSavings = staffCost * 0.30; 
    
    const currentRevenue = orders * ticket;
    const newRevenue = currentRevenue * 1.15; // +15% com upsell
    const increase = newRevenue - currentRevenue;

    setSavings(operationalSavings + increase);
  }, [orders, ticket, staff]);

  return (
    <section className="py-24 bg-white dark:bg-gray-900 transition-colors">
      <div className="max-w-7xl mx-auto px-6">
        <div className="bg-gray-900 dark:bg-gray-800 rounded-3xl p-8 md:p-12 text-white shadow-2xl overflow-hidden relative">
          {/* Background Glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-orange-600/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>

          <div className="grid md:grid-cols-2 gap-12 relative z-10">
            <div>
              <h2 className="text-3xl font-bold mb-6">Calcule seu ROI</h2>
              <p className="text-gray-400 mb-8">Veja quanto você deixa na mesa por não usar um sistema de fluxo automatizado.</p>
              
              <div className="space-y-6">
                <div>
                  <label className="flex justify-between text-sm font-medium mb-2">
                    <span className="flex items-center gap-2"><Utensils size={16}/> Pedidos por Mês</span>
                    <span className="text-orange-400">{orders}</span>
                  </label>
                  <input type="range" min="500" max="10000" step="100" value={orders} onChange={(e) => setOrders(Number(e.target.value))} className="w-full accent-orange-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer" />
                </div>

                <div>
                  <label className="flex justify-between text-sm font-medium mb-2">
                    <span className="flex items-center gap-2"><DollarSign size={16}/> Ticket Médio (R$)</span>
                    <span className="text-orange-400">R$ {ticket}</span>
                  </label>
                  <input type="range" min="15" max="200" step="5" value={ticket} onChange={(e) => setTicket(Number(e.target.value))} className="w-full accent-orange-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer" />
                </div>

                <div>
                  <label className="flex justify-between text-sm font-medium mb-2">
                    <span className="flex items-center gap-2"><Users size={16}/> Equipe de Atendimento</span>
                    <span className="text-orange-400">{staff} pessoas</span>
                  </label>
                  <input type="range" min="1" max="20" step="1" value={staff} onChange={(e) => setStaff(Number(e.target.value))} className="w-full accent-orange-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer" />
                </div>
              </div>
            </div>

            <div className="flex flex-col justify-center items-center bg-white/5 rounded-2xl p-8 border border-white/10 backdrop-blur-sm">
              <p className="text-gray-400 text-sm uppercase tracking-widest font-bold mb-2">Potencial de Ganho Mensal</p>
              <div className="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600 mb-4">
                R$ {savings.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
              </div>
              <p className="text-center text-gray-400 text-sm">
                *Baseado em média de mercado: 15% de aumento no ticket médio (Upsell) e 30% de otimização operacional.
              </p>
              <button className="mt-8 bg-white text-gray-900 px-8 py-3 rounded-xl font-bold hover:bg-gray-100 transition-colors w-full">
                Começar Agora
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}