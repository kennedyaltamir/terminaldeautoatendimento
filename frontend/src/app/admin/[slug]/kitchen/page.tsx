"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders, updateOrderStatus, updateOrderPayment, getServiceRequests, resolveServiceRequest, getRecentCompletedOrders } from "../../../../lib/api";
import { Order, ServiceRequest, OrderItemResponse } from "../../../../types";
import { ChefHat, RefreshCw, LogOut, ArrowRightCircle, CheckCircle2, Volume2, VolumeX, DollarSign, Printer, Bike, BellRing, XCircle, Utensils, Wine, Layers, History, Undo2, Box, AlertTriangle, IceCream } from "lucide-react";
import { removeToken } from "../../../../lib/auth";
import { useWebSocket } from "../../../../hooks/useWebSocket";
import OrderTimer from "../../../../components/admin/OrderTimer";
import Modal from "../../../../components/ui/Modal";
import StockModal from "../../../../components/admin/StockModal";

type StationFilter = 'all' | 'kitchen' | 'bar' | 'dessert';

export default function KitchenPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [serviceRequests, setServiceRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [isMuted, setIsMuted] = useState(false);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  const [activeTab, setActiveTab] = useState<StationFilter>('all');
  const [isRecallOpen, setIsRecallOpen] = useState(false);
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const savedStation = localStorage.getItem("mesaflow_kds_station") as StationFilter;
    if (savedStation) setActiveTab(savedStation);
  }, []);

  const handleTabChange = (station: StationFilter) => {
    setActiveTab(station);
    localStorage.setItem("mesaflow_kds_station", station);
  };

  const fetchOrders = useCallback(async () => {
    try {
      const [ordersData, requestsData] = await Promise.all([
        getKitchenOrders(slug),
        getServiceRequests(slug)
      ]);
      setOrders(ordersData);
      setServiceRequests(requestsData);
      setLastUpdated(new Date());
    } catch (error: any) {
      if (error.message === "Unauthorized") router.push("/admin/login");
    } finally {
      setLoading(false);
    }
  }, [slug, router]);

  useEffect(() => { fetchOrders(); }, [fetchOrders]);

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.type === "new_order" || data.type === "waiter_call") {
      if (!isMuted && audioRef.current) { audioRef.current.play().catch(() => {}); }
      fetchOrders();
    } else if (data.type === "order_update") {
      fetchOrders();
    }
  }, [fetchOrders, isMuted]);

  useWebSocket(slug, handleWebSocketMessage);

  const handleAdvanceStatus = async (orderId: string, currentStatus: string) => {
    const nextStatus = currentStatus === "pending" ? "preparing" : "ready";
    let newStatusApi = currentStatus === "pending" ? "preparing" : "ready";
    if (currentStatus === "preparing" || currentStatus === "ready") newStatusApi = "delivered";
    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: newStatusApi as any } : o).filter(o => o.status !== 'delivered'));
    try { await updateOrderStatus(slug, orderId, newStatusApi); } catch (e) { fetchOrders(); }
  };

  const handleConfirmPayment = async (orderId: string) => {
    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, payment_status: 'paid' as any } : o));
    try { await updateOrderPayment(orderId, 'paid'); } catch (e) { fetchOrders(); }
  };

  const handleResolveRequest = async (id: number) => {
    setServiceRequests(prev => prev.filter(r => r.id !== id));
    try { await resolveServiceRequest(id); } catch (e) { fetchOrders(); }
  };

  const handlePrint = (order: Order) => {
    setPrintingOrder(order);
    setTimeout(() => { window.print(); setPrintingOrder(null); }, 100);
  };

  const openRecallModal = async () => {
    setIsRecallOpen(true);
    try { const data = await getRecentCompletedOrders(slug); setRecentOrders(data); } catch (e) { console.error(e); }
  };

  const handleRestoreOrder = async (orderId: string) => {
    if(!confirm("Restaurar este pedido?")) return;
    try { await updateOrderStatus(slug, orderId, "preparing"); setIsRecallOpen(false); fetchOrders(); } catch (e) { alert("Erro ao restaurar"); }
  };

  const filteredOrders = orders.filter(order => activeTab === 'all' || order.items.some(item => item.product.station === activeTab));

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-gray-500">Carregando KDS...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4 md:p-6">
      <audio ref={audioRef} src="/notification.mp3" />
      <header className="flex flex-col xl:flex-row justify-between items-start xl:items-center mb-6 border-b border-gray-800 pb-4 gap-4">
        <h1 className="text-2xl font-bold flex items-center gap-2"><ChefHat className="text-orange-500" /> Monitor</h1>
        <div className="flex bg-gray-800 p-1.5 rounded-xl">
          {['all', 'kitchen', 'bar', 'dessert'].map((t) => (
            <button key={t} onClick={() => handleTabChange(t as any)} className={`px-4 py-2 rounded-lg text-sm font-bold capitalize ${activeTab === t ? 'bg-orange-600 text-white' : 'text-gray-400'}`}>{t}</button>
          ))}
        </div>
        <div className="flex gap-2">
          <button onClick={() => setIsStockOpen(true)} className="p-3 bg-gray-800 rounded-xl text-orange-400"><Box size={20} /></button>
          <button onClick={openRecallModal} className="p-3 bg-gray-800 rounded-xl text-blue-400"><History size={20} /></button>
          <button onClick={() => setIsMuted(!isMuted)} className="p-3 bg-gray-800 rounded-xl">{isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}</button>
          <button onClick={fetchOrders} className="p-3 bg-gray-800 rounded-xl"><RefreshCw size={20} /></button>
          <button onClick={() => { removeToken(); router.push("/admin/login"); }} className="p-3 bg-red-900/20 text-red-400 rounded-xl"><LogOut size={20} /></button>
        </div>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredOrders.map((order) => (
          <div key={order.id} className="rounded-2xl border-t-8 bg-gray-800 border-orange-500 p-4">
            <div className="flex justify-between mb-4">
              <h2 className="text-xl font-bold">Mesa {order.table?.table_number || "DLV"}</h2>
              <OrderTimer createdAt={order.created_at} />
            </div>
            <ul className="space-y-2 mb-4">
              {order.items.filter(i => activeTab === 'all' || i.product.station === activeTab).map(item => (
                <li key={item.id} className="text-sm"><b>{item.quantity}x</b> {item.product.name}</li>
              ))}
            </ul>
            <button onClick={() => handleAdvanceStatus(order.id, order.status)} className="w-full py-3 rounded-xl font-bold bg-green-600 text-white">Avançar</button>
          </div>
        ))}
      </div>
      <StockModal isOpen={isStockOpen} onClose={() => setIsStockOpen(false)} slug={slug} />
    </div>
  );
}