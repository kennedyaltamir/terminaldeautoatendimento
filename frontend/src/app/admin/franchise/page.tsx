"use client";

import { useEffect, useState } from "react";
import { getFranchiseDashboard } from "@/lib/api";
import { Building2, DollarSign, ShoppingBag, TrendingUp, ArrowRight, Loader2 } from "lucide-react";
import Link from "next/link";
import { toast, Toaster } from "sonner";

interface StoreSummary {
  id: string;
  name: string;
  slug: string;
  revenue: number;
  orders: number;
}

interface FranchiseData {
  total_revenue: number;
  total_orders: number;
  stores: StoreSummary[];
}

export default function FranchisePage() {
  const [data, setData] = useState<FranchiseData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFranchiseDashboard()
      .then(setData)
      .catch((err) => {
        console.error(err);
        toast.error("Erro ao carregar dados da franquia");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center text-white">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 font-sans">
      <Toaster position="top-right" richColors />
      
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-purple-600 p-3 rounded-xl shadow-lg shadow-purple-500/20">
            <Building2 size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">Visão Multi-loja</h1>
            <p className="text-gray-400 text-sm">Desempenho consolidado da rede (Hoje).</p>
          </div>
        </div>

        {/* CARDS DE TOTAIS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Faturamento Global</p>
                <h3 className="text-3xl font-black mt-2 text-green-400">R$ {data.total_revenue.toFixed(2)}</h3>
              </div>
              <div className="p-3 rounded-xl bg-green-500/10 text-green-500">
                <DollarSign size={24} />
              </div>
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Total de Pedidos</p>
                <h3 className="text-3xl font-black mt-2 text-blue-400">{data.total_orders}</h3>
              </div>
              <div className="p-3 rounded-xl bg-blue-500/10 text-blue-500">
                <ShoppingBag size={24} />
              </div>
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">Lojas Ativas</p>
                <h3 className="text-3xl font-black mt-2 text-purple-400">{data.stores.length}</h3>
              </div>
              <div className="p-3 rounded-xl bg-purple-500/10 text-purple-500">
                <Building2 size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* RANKING DE LOJAS */}
        <div className="bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden shadow-xl">
          <div className="p-6 border-b border-gray-700 flex justify-between items-center">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <TrendingUp size={20} className="text-orange-500" /> Ranking de Desempenho
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-gray-400">
              <thead className="bg-gray-900/50 text-gray-500 uppercase font-bold text-xs">
                <tr>
                  <th className="px-6 py-4">Loja</th>
                  <th className="px-6 py-4">Faturamento</th>
                  <th className="px-6 py-4">Pedidos</th>
                  <th className="px-6 py-4">Ticket Médio</th>
                  <th className="px-6 py-4 text-right">Ação</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {data.stores.map((store) => {
                  const ticket = store.orders > 0 ? store.revenue / store.orders : 0;
                  return (
                    <tr key={store.id} className="hover:bg-gray-700/30 transition-colors">
                      <td className="px-6 py-4 font-bold text-white">{store.name}</td>
                      <td className="px-6 py-4 text-green-400 font-mono font-bold">R$ {store.revenue.toFixed(2)}</td>
                      <td className="px-6 py-4">{store.orders}</td>
                      <td className="px-6 py-4">R$ {ticket.toFixed(2)}</td>
                      <td className="px-6 py-4 text-right">
                        <Link 
                          href={`/admin/${store.slug}/dashboard`}
                          className="inline-flex items-center gap-1 text-xs font-bold bg-gray-700 hover:bg-gray-600 text-white px-3 py-1.5 rounded-lg transition-colors"
                        >
                          Acessar <ArrowRight size={14} />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}