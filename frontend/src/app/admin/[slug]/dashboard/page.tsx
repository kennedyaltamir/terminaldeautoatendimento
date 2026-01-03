"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getDashboardMetrics } from "@/lib/api";
import { DollarSign, ShoppingBag, TrendingUp, Star, Clock, BarChart2, Download, Calendar, AlertCircle } from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell
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
      console.error(err);
      if (err.message === "Unauthorized" || err.message === "Sessão expirada") {
        router.push("/admin/login");
      } else {
        toast.error("Erro ao carregar dados");
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
      a.download = `relatorio_vendas_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      toast.success("Relatório baixado com sucesso!");
    } catch (e) {
      toast.error("Erro ao exportar relatório");
    }
  };

  const revenue = metrics?.total_revenue || 0;
  const orders = metrics?.total_orders || 0;
  const ticket = metrics?.average_ticket || 0;

  const cards = [
    { title: "Faturamento", value: `R$ ${Number(revenue).toFixed(2)}`, icon: DollarSign, color: "text-green-500", bg: "bg-green-500/10" },
    { title: "Total Pedidos", value: orders, icon: ShoppingBag, color: "text-blue-500", bg: "bg-blue-500/10" },
    { title: "Ticket Médio", value: `R$ ${Number(ticket).toFixed(2)}`, icon: TrendingUp, color: "text-orange-500", bg: "bg-orange-500/10" },
  ];

  const COLORS = ['#ea580c', '#f97316', '#fb923c', '#fdba74', '#fed7aa'];

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard Financeiro</h1>
          <p className="text-gray-400 text-sm">Visão geral da saúde do seu negócio.</p>
        </div>
        
        <div className="flex gap-2">
          <div className="bg-gray-800 p-1 rounded-lg flex gap-1 border border-gray-700">
            <button onClick={() => setPeriod("today")} className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${period === "today" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>Hoje</button>
            <button onClick={() => setPeriod("7d")} className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${period === "7d" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>7 Dias</button>
            <button onClick={() => setPeriod("month")} className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${period === "month" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>Este Mês</button>
          </div>
          <button onClick={handleExport} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-700 flex items-center gap-2 text-xs font-bold transition-colors">
            <Download size={16} /> Exportar CSV
          </button>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1,2,3].map(i => <div key={i} className="h-32 bg-gray-800 rounded-2xl animate-pulse"></div>)}
        </div>
      ) : (
        <>
          {/* CARDS PRINCIPAIS */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {cards.map((card, i) => (
              <div key={i} className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg hover:border-gray-600 transition-colors">
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

          {/* GRÁFICO DE VENDAS */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
            <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><TrendingUp size={18} className="text-green-500"/> Evolução de Faturamento</h2>
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
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff', borderRadius: '8px' }}
                    itemStyle={{ color: '#ea580c' }}
                    formatter={(value: any) => [`R$ ${Number(value).toFixed(2)}`, 'Vendas']}
                  />
                  <Area type="monotone" dataKey="value" stroke="#ea580c" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* VENDAS POR HORA */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
              <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><Clock size={18} className="text-blue-500"/> Horários de Pico (Vendas)</h2>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metrics?.sales_by_hour || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <XAxis dataKey="hour" stroke="#9ca3af" tickFormatter={(val: any) => `${val}h`} />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff', borderRadius: '8px' }}
                      cursor={{fill: '#374151', opacity: 0.4}}
                    />
                    <Bar dataKey="total" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Total (R$)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* EVOLUÇÃO TICKET MÉDIO */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
              <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><BarChart2 size={18} className="text-purple-500"/> Ticket Médio Diário</h2>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={metrics?.ticket_evolution || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <XAxis dataKey="date" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" domain={['auto', 'auto']} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff', borderRadius: '8px' }}
                      formatter={(value: any) => [`R$ ${Number(value).toFixed(2)}`, 'Ticket Médio']}
                    />
                    <Line type="monotone" dataKey="ticket" stroke="#a855f7" strokeWidth={3} dot={{r: 4, fill: '#a855f7'}} activeDot={{r: 6}} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* CURVA ABC (PRODUTOS) */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-gray-800 border border-gray-700 rounded-2xl shadow-lg overflow-hidden">
              <div className="p-6 border-b border-gray-700 flex items-center gap-2">
                <Star className="text-yellow-500" size={18} />
                <h2 className="text-lg font-bold text-white">Ranking de Produtos (Receita)</h2>
              </div>
              <div className="p-6">
                {!metrics || metrics.product_performance.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-10 text-gray-500">
                    <AlertCircle size={32} className="mb-2 opacity-50" />
                    <p>Nenhuma venda registrada no período.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {metrics.product_performance.slice(0, 5).map((product, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-900/50 p-4 rounded-xl border border-gray-700/50 hover:bg-gray-900 transition-colors">
                        <div className="flex items-center gap-4">
                          <span className={`text-sm font-black w-6 h-6 flex items-center justify-center rounded-full ${index < 3 ? 'bg-yellow-500/20 text-yellow-500' : 'bg-gray-700 text-gray-400'}`}>
                            {index + 1}
                          </span>
                          <div>
                            <p className="font-bold text-gray-200 text-sm">{product.name}</p>
                            <p className="text-xs text-gray-500">{product.quantity} unidades vendidas</p>
                          </div>
                        </div>
                        <span className="text-green-400 font-mono font-bold text-sm">
                          R$ {Number(product.revenue).toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* GRÁFICO DE PIZZA (TOP 5) */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6 flex flex-col">
              <h2 className="text-lg font-bold text-white mb-4">Distribuição de Vendas</h2>
              <div className="flex-1 min-h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={metrics?.top_products || []}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="revenue"
                    >
                      {metrics?.top_products.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff', borderRadius: '8px' }}
                      formatter={(value: any) => [`R$ ${Number(value).toFixed(2)}`, 'Receita']}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 space-y-2">
                {metrics?.top_products.slice(0, 3).map((entry, index) => (
                  <div key={index} className="flex items-center gap-2 text-xs text-gray-400">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }}></div>
                    <span className="truncate flex-1">{entry.name}</span>
                    <span className="font-bold text-white">{((entry.revenue / revenue) * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}