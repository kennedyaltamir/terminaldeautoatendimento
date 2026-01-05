"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getDashboardMetrics } from "@/lib/api";
import { DollarSign, ShoppingBag, TrendingUp, Star, Clock, BarChart2, Download, Calendar, AlertCircle } from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  BarChart, Bar, LineChart, Line, Legend
} from 'recharts';
import { toast } from "sonner";

interface Metrics {
  total_revenue: number;
  total_orders: number;
  average_ticket: number;
  top_products: { name: string; count: number; revenue: number }[];
  sales_chart: { date: string; value: number }[];
  sales_by_hour: { hour: number; total: number; count: number }[];
  product_performance: { name: string; revenue: number; quantity: number }[];
  ticket_evolution: { date: string; ticket: number }[];
}

type Period = "today" | "7d" | "30d" | "month";

export default function DashboardPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<Period>("7d");
  const router = useRouter();

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      let startDate = "";
      let endDate = "";
      const now = new Date();

      if (period === "today") {
        startDate = now.toISOString().split("T")[0];
        endDate = startDate;
      } else if (period === "7d") {
        const past = new Date();
        past.setDate(now.getDate() - 6);
        startDate = past.toISOString().split("T")[0];
        endDate = now.toISOString().split("T")[0];
      } else if (period === "30d") {
        const past = new Date();
        past.setDate(now.getDate() - 29);
        startDate = past.toISOString().split("T")[0];
        endDate = now.toISOString().split("T")[0];
      } else if (period === "month") {
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
        startDate = firstDay.toISOString().split("T")[0];
        endDate = now.toISOString().split("T")[0];
      }

      const data = await getDashboardMetrics(startDate, endDate);
      setMetrics(data);
    } catch (err: any) {
      if (err.message === "Unauthorized") router.push("/admin/login");
      else toast.error("Erro ao carregar dados");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchMetrics(); }, [period]);

  const handleExport = async () => {
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/metrics/export`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Falha no download");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `vendas_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      toast.success("Relatório baixado!");
    } catch (e) { toast.error("Erro ao exportar"); }
  };

  const revenue = metrics?.total_revenue || 0;
  const orders = metrics?.total_orders || 0;
  const ticket = metrics?.average_ticket || 0;

  const cards = [
    { title: "Faturamento", value: `R$ ${Number(revenue).toFixed(2)}`, icon: DollarSign, color: "text-green-500", bg: "bg-green-500/10" },
    { title: "Total Pedidos", value: orders, icon: ShoppingBag, color: "text-blue-500", bg: "bg-blue-500/10" },
    { title: "Ticket Médio", value: `R$ ${Number(ticket).toFixed(2)}`, icon: TrendingUp, color: "text-orange-500", bg: "bg-orange-500/10" },
  ];

  // Custom Tooltip para gráficos
  const CustomTooltip = ({ active, payload, label, prefix = "" }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 p-3 rounded-lg shadow-xl">
          <p className="text-gray-400 text-xs mb-1">{label}</p>
          <p className="text-white font-bold text-sm">
            {prefix} {payload[0].value}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 text-sm">Visão geral da operação.</p>
        </div>
        
        <div className="flex gap-2">
          <div className="bg-gray-800 p-1 rounded-lg flex gap-1 border border-gray-700">
            {['today', '7d', 'month'].map((p) => (
              <button 
                key={p}
                onClick={() => setPeriod(p as Period)} 
                className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all capitalize ${period === p ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}
              >
                {p === 'today' ? 'Hoje' : p === '7d' ? '7 Dias' : 'Mês'}
              </button>
            ))}
          </div>
          <button onClick={handleExport} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-700 flex items-center gap-2 text-xs font-bold transition-colors">
            <Download size={16} /> CSV
          </button>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1,2,3].map(i => <div key={i} className="h-32 bg-gray-800 rounded-2xl animate-pulse"></div>)}
        </div>
      ) : (
        <>
          {/* CARDS KPI */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {cards.map((card, i) => (
              <div key={i} className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">{card.title}</p>
                    <h3 className="text-3xl font-black mt-2 text-white">{card.value}</h3>
                  </div>
                  <div className={`p-3 rounded-xl ${card.bg} ${card.color}`}>
                    <card.icon size={24} />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* GRÁFICO DE EVOLUÇÃO (LINHA/ÁREA) */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
            <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><TrendingUp size={18} className="text-green-500"/> Evolução de Vendas</h2>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={metrics?.sales_chart || []}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ea580c" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ea580c" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                  <XAxis dataKey="date" stroke="#9ca3af" tick={{fontSize: 12}} tickLine={false} axisLine={false} />
                  <YAxis stroke="#9ca3af" tick={{fontSize: 12}} tickLine={false} axisLine={false} tickFormatter={(value: any) => `R$${value}`} />
                  <Tooltip content={<CustomTooltip prefix="R$" />} cursor={{ stroke: '#ea580c', strokeWidth: 1 }} />
                  <Area type="monotone" dataKey="value" stroke="#ea580c" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* VENDAS POR HORA (BARRAS) */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
              <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><Clock size={18} className="text-blue-500"/> Horários de Pico</h2>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metrics?.sales_by_hour || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <XAxis dataKey="hour" stroke="#9ca3af" tickFormatter={(val: any) => `${val}h`} />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip content={<CustomTooltip prefix="R$" />} cursor={{fill: '#374151', opacity: 0.4}} />
                    <Bar dataKey="total" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Total (R$)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* TOP PRODUTOS (BARRAS HORIZONTAIS) - Substitui Pizza */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
              <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><Star size={18} className="text-yellow-500"/> Top 5 Produtos (Receita)</h2>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart 
                    layout="vertical" 
                    data={metrics?.top_products.slice(0, 5) || []} 
                    margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" horizontal={false} />
                    <XAxis type="number" stroke="#9ca3af" hide />
                    <YAxis type="category" dataKey="name" stroke="#9ca3af" width={100} tick={{fontSize: 11}} />
                    <Tooltip content={<CustomTooltip prefix="R$" />} cursor={{fill: '#374151', opacity: 0.4}} />
                    <Bar dataKey="revenue" fill="#eab308" radius={[0, 4, 4, 0]} barSize={20}>
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}