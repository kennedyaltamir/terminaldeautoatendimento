"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getDashboardMetrics } from "@/lib/api";
import { DollarSign, ShoppingBag, TrendingUp, Star, Clock, Download, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  BarChart, Bar
} from 'recharts';
import { toast } from "sonner";
import DashboardSkeleton from "@/components/admin/DashboardSkeleton";

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

const TrendIndicator = ({ value, isPositive = true }: { value: string, isPositive?: boolean }) => (
  <span className={`text-xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1 w-fit ${isPositive ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
    {isPositive ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
    {value}
  </span>
);

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
      // Tratamento de erro robusto
      if (err.status === 401 || err.status === 403) {
        toast.error("Sessão expirada ou sem permissão. Redirecionando...");
        setTimeout(() => router.push("/admin/login"), 1500);
      } else {
        console.error("Erro ao carregar métricas:", err);
        toast.error("Erro ao carregar dados. Tente novamente.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [period]);

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
      toast.success("Relatório baixado com sucesso!");
    } catch (e) {
      toast.error("Erro ao exportar dados");
    }
  };

  if (loading) return <DashboardSkeleton />;

  // Se falhou e não redirecionou ainda, mostra estado vazio ou erro
  if (!metrics) return (
    <div className="flex flex-col items-center justify-center h-[50vh] text-gray-500">
        <p>Não foi possível carregar os dados.</p>
        <button onClick={fetchMetrics} className="mt-4 text-orange-500 hover:underline">Tentar novamente</button>
    </div>
  );

  const revenue = metrics?.total_revenue || 0;
  const orders = metrics?.total_orders || 0;
  const ticket = metrics?.average_ticket || 0;

  const cards = [
    { title: "Faturamento", value: `R$ ${Number(revenue).toFixed(2)}`, icon: DollarSign, color: "text-green-500", bg: "bg-green-500/10", trend: "12% vs anterior" },
    { title: "Total Pedidos", value: orders, icon: ShoppingBag, color: "text-blue-500", bg: "bg-blue-500/10", trend: "5% vs anterior" },
    { title: "Ticket Médio", value: `R$ ${Number(ticket).toFixed(2)}`, icon: TrendingUp, color: "text-orange-500", bg: "bg-orange-500/10", trend: "Estável" },
  ];

  const CustomTooltip = ({ active, payload, label, prefix = "" }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 p-3 rounded-lg shadow-xl">
          <p className="text-gray-400 text-xs mb-1">{label}</p>
          <p className="text-white font-bold text-sm">
            {prefix} {Number(payload[0].value).toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500 overflow-x-hidden">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">Visão geral da operação em tempo real.</p>
        </div>

        <div className="flex gap-2">
          <div className="bg-gray-800 p-1 rounded-lg flex gap-1 border border-gray-700">
            {['today', '7d', 'month'].map((p) => (
              <button 
                key={p}
                onClick={() => setPeriod(p as Period)} 
                className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all capitalize ${period === p ? "bg-orange-600 text-white shadow-lg" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}
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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((card, i) => (
          <div key={i} className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg hover:border-gray-600 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-1">{card.title}</p>
                <h3 className="text-3xl font-black text-white mb-2">{card.value}</h3>
                <TrendIndicator value={card.trend} isPositive={true} />
              </div>
              <div className={`p-3 rounded-xl ${card.bg} ${card.color}`}>
                <card.icon size={24} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
        <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
          <TrendingUp size={18} className="text-green-500"/> Evolução de Vendas
        </h2>
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
        <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
          <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Clock size={18} className="text-blue-500"/> Horários de Pico
          </h2>
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

        <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
          <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Star size={18} className="text-yellow-500"/> Top 5 Produtos (Receita)
          </h2>
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
                <Bar dataKey="revenue" fill="#eab308" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
