"use client";

import { useEffect, useState } from "react";
import { getFranchiseDashboard } from "@/lib/api";
import { Building2, DollarSign, TrendingUp, ArrowRight, Loader2, PieChart, ArrowUpRight, ArrowDownRight, Target } from "lucide-react";
import Link from "next/link";
import { toast, Toaster } from "sonner";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts';

interface StoreSummary {
  id: string;
  name: string;
  slug: string;
  revenue: number;
  cmv: number;
  profit: number;
  margin_percent: number;
  orders_count: number;
}

interface FranchiseData {
  total_revenue: number;
  total_profit: number;
  avg_margin: number;
  stores: StoreSummary[];
}

export default function FranchisePage() {
  const [data, setData] = useState<FranchiseData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFranchiseDashboard()
      .then(setData)
      .catch(() => toast.error("Erro ao carregar dados da franquia"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-white"><Loader2 className="animate-spin" size={32} /></div>;
  if (!data) return null;

  const bestStore = data.stores[0];
  const worstStore = data.stores[data.stores.length - 1];

  return (
    <div className="space-y-8 pb-20 animate-in fade-in">
      <Toaster position="top-right" richColors />

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-purple-600 p-3 rounded-xl shadow-lg">
            <Building2 size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard de Franquia</h1>
            <p className="text-gray-400 text-sm">Análise de lucratividade da rede (Hoje).</p>
          </div>
        </div>
      </div>

      {/* CARDS DE PERFORMANCE GLOBAL */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
          <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Faturamento Total</p>
          <h3 className="text-3xl font-black mt-2 text-white">R$ {data.total_revenue.toLocaleString()}</h3>
          <div className="mt-4 flex items-center gap-2 text-green-400 text-sm font-bold">
            <ArrowUpRight size={16} /> <span>Rede em crescimento</span>
          </div>
        </div>

        <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
          <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Lucro Operacional</p>
          <h3 className="text-3xl font-black mt-2 text-green-400">R$ {data.total_profit.toLocaleString()}</h3>
          <p className="text-xs text-gray-500 mt-4">Após descontar CMV e Taxas</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
          <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Margem Média</p>
          <h3 className="text-3xl font-black mt-2 text-purple-400">{data.avg_margin.toFixed(1)}%</h3>
          <div className="mt-4 flex items-center gap-2 text-gray-400 text-sm">
            <Target size={16} /> <span>Meta: 70%</span>
          </div>
        </div>
      </div>

      {/* GRÁFICO COMPARATIVO */}
      <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl">
        <h2 className="text-xl font-bold text-white mb-8 flex items-center gap-2">
          <TrendingUp size={20} className="text-orange-500" /> Faturamento vs Lucro por Unidade
        </h2>
        <div className="h-[350px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.stores}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
              <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
              />
              <Legend />
              <Bar dataKey="revenue" name="Faturamento" fill="#ea580c" radius={[4, 4, 0, 0]} />
              <Bar dataKey="profit" name="Lucro Líquido" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* TABELA DETALHADA */}
      <div className="bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-bold text-white">Análise de Eficiência</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-gray-900/50 text-gray-500 uppercase font-bold text-xs">
              <tr>
                <th className="px-6 py-4">Loja</th>
                <th className="px-6 py-4">Vendas</th>
                <th className="px-6 py-4">CMV (%)</th>
                <th className="px-6 py-4">Lucro (R$)</th>
                <th className="px-6 py-4">Margem</th>
                <th className="px-6 py-4 text-right">Ação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {data.stores.map((store) => (
                <tr key={store.id} className="hover:bg-gray-700/30 transition-colors">
                  <td className="px-6 py-4 font-bold text-white">{store.name}</td>
                  <td className="px-6 py-4">{store.orders_count} pedidos</td>
                  <td className="px-6 py-4">
                    <span className={store.cmv / store.revenue > 0.35 ? 'text-red-400' : 'text-green-400'}>
                      {((store.cmv / store.revenue) * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="px-6 py-4 font-mono font-bold text-white">R$ {store.profit.toFixed(2)}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div className="h-full bg-purple-500" style={{ width: `${store.margin_percent}%` }}></div>
                      </div>
                      <span className="text-xs font-bold">{store.margin_percent.toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link href={`/admin/${store.slug}/dashboard`} className="text-orange-500 hover:text-orange-400 font-bold flex items-center justify-end gap-1">
                      Ver <ArrowRight size={14} />
                    </Link>
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
