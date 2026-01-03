"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getDashboardMetrics } from "@/lib/api";
import { DollarSign, ShoppingBag, TrendingUp, Star, Clock, BarChart2 } from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  BarChart, Bar, LineChart, Line
} from 'recharts';

interface ChartData {
  date: string;
  value: number;
}

interface SalesByHour {
  hour: number;
  total: number;
  count: number;
}

interface ProductPerformance {
  name: string;
  revenue: number;
  quantity: number;
}

interface TicketData {
  date: string;
  ticket: number;
}

interface Metrics {
  total_revenue: number;
  total_orders: number;
  average_ticket: number;
  top_products: { name: string; count: number }[];
  sales_chart: ChartData[];
  sales_by_hour: SalesByHour[];
  product_performance: ProductPerformance[];
  ticket_evolution: TicketData[];
}

type Period = "today" | "7d" | "30d" | "all";

export default function DashboardPage() {
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
      }

      const data = await getDashboardMetrics(startDate, endDate);
      setMetrics(data);
    } catch (err: any) {
      console.error(err);
      if (err.message === "Unauthorized") {
        router.push("/admin/login");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [period, router]);

  const revenue = metrics?.total_revenue || 0;
  const orders = metrics?.total_orders || 0;
  const ticket = metrics?.average_ticket || 0;

  const cards = [
    { title: "Faturamento", value: `R$ ${Number(revenue).toFixed(2)}`, icon: DollarSign, color: "text-green-500" },
    { title: "Total Pedidos", value: orders, icon: ShoppingBag, color: "text-blue-500" },
    { title: "Ticket Médio", value: `R$ ${Number(ticket).toFixed(2)}`, icon: TrendingUp, color: "text-orange-500" },
  ];

  return (
    <div className="space-y-8 pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-3xl font-bold text-white">Dashboard Executivo</h1>
        
        <div className="bg-gray-800 p-1 rounded-lg flex gap-1 border border-gray-700">
          <button onClick={() => setPeriod("today")} className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${period === "today" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>Hoje</button>
          <button onClick={() => setPeriod("7d")} className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${period === "7d" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>7 Dias</button>
          <button onClick={() => setPeriod("30d")} className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${period === "30d" ? "bg-orange-600 text-white shadow" : "text-gray-400 hover:text-white hover:bg-gray-700"}`}>30 Dias</button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-gray-500 animate-pulse">Atualizando dados...</div>
      ) : (
        <>
          {/* CARDS PRINCIPAIS */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {cards.map((card, i) => (
              <div key={i} className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-gray-400 text-sm font-medium">{card.title}</p>
                    <h3 className="text-3xl font-bold mt-2 text-white">{card.value}</h3>
                  </div>
                  <div className={`p-3 bg-gray-900 rounded-xl ${card.color}`}>
                    <card.icon size={24} />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* GRÁFICO DE VENDAS */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2"><TrendingUp size={20} className="text-green-500"/> Evolução de Vendas</h2>
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
                    contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff' }}
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
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2"><Clock size={20} className="text-blue-500"/> Horários de Pico</h2>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metrics?.sales_by_hour || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <XAxis dataKey="hour" stroke="#9ca3af" tickFormatter={(val: any) => `${val}h`} />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff' }}
                      cursor={{fill: '#374151', opacity: 0.4}}
                    />
                    <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Pedidos" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* EVOLUÇÃO TICKET MÉDIO */}
            <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2"><BarChart2 size={20} className="text-purple-500"/> Ticket Médio Diário</h2>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={metrics?.ticket_evolution || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <XAxis dataKey="date" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" domain={['auto', 'auto']} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff' }}
                      formatter={(value: any) => [`R$ ${Number(value).toFixed(2)}`, 'Ticket Médio']}
                    />
                    <Line type="monotone" dataKey="ticket" stroke="#a855f7" strokeWidth={3} dot={{r: 4}} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* CURVA ABC (PRODUTOS) */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg overflow-hidden">
            <div className="p-6 border-b border-gray-700 flex items-center gap-2">
              <Star className="text-yellow-500" size={20} />
              <h2 className="text-xl font-bold text-white">Ranking de Produtos (Receita)</h2>
            </div>
            <div className="p-6">
              {!metrics || metrics.product_performance.length === 0 ? (
                <p className="text-gray-500 text-center py-4">Nenhuma venda registrada.</p>
              ) : (
                <div className="space-y-4">
                  {metrics.product_performance.map((product, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-900/50 p-4 rounded-xl border border-gray-700/50 hover:bg-gray-900 transition-colors">
                      <div className="flex items-center gap-4">
                        <span className={`text-lg font-black w-8 h-8 flex items-center justify-center rounded-full ${index < 3 ? 'bg-yellow-500/20 text-yellow-500' : 'bg-gray-700 text-gray-400'}`}>
                          {index + 1}
                        </span>
                        <div>
                          <p className="font-bold text-gray-200">{product.name}</p>
                          <p className="text-xs text-gray-500">{product.quantity} unidades vendidas</p>
                        </div>
                      </div>
                      <span className="text-green-400 font-mono font-bold">
                        R$ {Number(product.revenue).toFixed(2)}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}