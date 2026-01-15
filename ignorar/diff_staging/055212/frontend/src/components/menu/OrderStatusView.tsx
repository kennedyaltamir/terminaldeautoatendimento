// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 09:50:00
"use client";
import { Clock, ChefHat, CheckCircle2, Banknote, Copy, Loader2, Utensils, Plus, MapPin, Navigation, Star } from "lucide-react";
import { Order } from "@/types";
import { QRCodeSVG } from "qrcode.react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState, useCallback, useEffect } from "react";
import FeedbackModal from "@/components/menu/FeedbackModal";
import { formatCurrency } from "@/lib/utils";

export default function OrderStatusView({ order, onNewOrder, primaryColor }: { order: Order, onNewOrder: () => void, primaryColor: string }) {
  const [localStatus, setLocalStatus] = useState(order.status);
  const [driverLocation, setDriverLocation] = useState<{lat: number, lng: number} | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);

  const isPaid = order.payment_status === 'paid';
  const isOnline = order.payment_method === 'online';

  // Resolve o slug da URL para o WebSocket
  const slug = typeof window !== 'undefined' ? window.location.pathname.split('/')[1] : "";

  useEffect(() => {
    setLocalStatus(order.status);
  }, [order.status]);

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.order_id === order.id) {
      if (data.type === "order_update") {
        setLocalStatus(data.status);
      } else if (data.type === "driver_location") {
        setDriverLocation({ lat: data.lat, lng: data.lng });
      }
    }
  }, [order.id]);

  useWebSocket(slug, handleWebSocketMessage); 

  const steps = [
    { id: 'pending', label: 'Recebido', icon: Clock },
    { id: 'preparing', label: 'Preparando', icon: ChefHat },
    { id: 'ready', label: 'Pronto', icon: CheckCircle2 },
  ];

  if (order.order_type === 'delivery') {
    steps.push({ id: 'delivering', label: 'Em Rota', icon: MapPin });
  }

  const currentStepIndex = steps.findIndex(s => s.id === localStatus) === -1 
    ? (localStatus === 'accepted' ? 0 : (localStatus === 'delivered' ? steps.length : 0)) 
    : steps.findIndex(s => s.id === localStatus);

  const openTrackingMap = () => {
    if (driverLocation) {
      window.open(`https://www.google.com/maps/search/?api=1&query=${driverLocation.lat},${driverLocation.lng}`, '_blank');
    }
  };

  const canRate = !order.feedback && (localStatus === 'delivered' || order.payment_status === 'paid');

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col pb-10 font-sans">
      <div className="bg-white p-6 shadow-sm border-b border-gray-100">
        <h1 className="text-2xl font-bold text-gray-900">Olá, {order.customer_name?.split(' ')[0] || 'Cliente'}!</h1>
        <p className="text-gray-50 text-sm mt-1">Acompanhe seu pedido <span className="font-mono font-bold text-gray-700">#{order.id.slice(0, 6)}</span></p>
      </div>

      <div className="p-6 space-y-6 max-w-md mx-auto w-full">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div className="flex justify-between relative">
            <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-100 -z-10 -translate-y-1/2 rounded-full"></div>
            <div className="absolute top-1/2 left-0 h-1 bg-green-500 -z-10 -translate-y-1/2 rounded-full transition-all duration-1000" style={{ width: `${(currentStepIndex / (steps.length - 1)) * 100}%` }}></div>
            {steps.map((step, idx) => {
              const isActive = idx <= currentStepIndex;
              const isCurrent = idx === currentStepIndex;
              return (
                <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-1">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${isActive ? 'bg-green-500 text-white shadow-lg shadow-green-200' : 'bg-gray-200 text-gray-400'}`}>
                    <step.icon size={20} />
                  </div>
                  <span className={`text-[10px] font-bold ${isCurrent ? 'text-green-600' : 'text-gray-400'}`}>{step.label}</span>
                </div>
              );
            })}
          </div>

          {localStatus === 'ready' && order.order_type !== 'delivery' && (
            <div className="mt-6 bg-green-50 text-green-800 p-3 rounded-xl text-center font-bold animate-bounce">🍽️ Seu pedido está pronto!</div>
          )}

          {localStatus === 'delivering' && (
            <div className="mt-6 space-y-3">
              <div className="bg-blue-50 text-blue-800 p-3 rounded-xl text-center font-bold flex items-center justify-center gap-2">
                <Navigation size={18} className="animate-pulse"/> Motorista a caminho!
              </div>
              {driverLocation && (
                <div className="bg-white border border-blue-100 p-4 rounded-xl shadow-sm text-center animate-in fade-in">
                   <p className="text-xs text-blue-600 font-bold uppercase mb-2">Localização em Tempo Real</p>
                   <div className="flex justify-center gap-4 mb-4">
                      <div className="text-center"><p className="text-[10px] text-gray-400">Lat</p><p className="font-mono text-sm">{driverLocation.lat.toFixed(4)}</p></div>
                      <div className="text-center"><p className="text-[10px] text-gray-400">Lng</p><p className="font-mono text-sm">{driverLocation.lng.toFixed(4)}</p></div>
                   </div>
                   <button onClick={openTrackingMap} className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-blue-700 transition-all"><MapPin size={18} /> Abrir no Google Maps</button>
                </div>
              )}
            </div>
          )}
        </div>

        {!isPaid && (
          <>
            {isOnline && order.mp_qr_code ? (
              <div className="bg-white p-6 rounded-2xl shadow-lg border-2 border-orange-100">
                <h3 className="text-lg font-bold text-center mb-4">Pagamento Pendente</h3>
                <div className="flex justify-center mb-4"><QRCodeSVG value={order.mp_qr_code} size={180} /></div>
                <div className="flex gap-2">
                  <input readOnly value={order.mp_qr_code} className="flex-1 bg-gray-100 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-600 truncate" />
                  <button onClick={() => {navigator.clipboard.writeText(order.mp_qr_code!); alert("Copiado!")}} className="bg-gray-900 text-white p-2 rounded-lg hover:bg-gray-800"><Copy size={16} /></button>
                </div>
              </div>
            ) : (
              <div className="bg-orange-50 p-6 rounded-2xl border border-orange-100 text-center">
                <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4"><Banknote className="text-orange-600" size={32} /></div>
                <h3 className="font-bold text-orange-900 text-lg">Aguardando Pagamento</h3>
              </div>
            )}
          </>
        )}

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-4 border-b border-gray-100 bg-gray-50/50"><h3 className="font-bold text-gray-900 flex items-center gap-2"><Utensils size={16}/> Resumo do Pedido</h3></div>
          <div className="p-4 space-y-4">
            {order.items.map((item, i) => (
              <div key={i} className="flex justify-between items-start">
                <div className="flex gap-3">
                  <div className="bg-gray-100 w-8 h-8 rounded flex items-center justify-center text-xs font-bold text-gray-600">{item.quantity}x</div>
                  <div><p className="text-sm font-medium text-gray-900">{item.product.name}</p></div>
                </div>
              </div>
            ))}
            <div className="border-t border-dashed border-gray-200 pt-4 mt-4 flex justify-between text-lg font-black text-gray-900">
              <span>Total</span><span>{formatCurrency(order.total_amount)}</span>
            </div>
          </div>
        </div>

        {canRate && (
          <button data-testid="btn-avaliar" onClick={() => setShowFeedback(true)} className="w-full py-3 rounded-xl border-2 border-yellow-400 text-yellow-600 font-bold flex items-center justify-center gap-2 hover:bg-yellow-50 transition-colors"><Star size={20} /> Avaliar Pedido</button>
        )}

        <button onClick={onNewOrder} className="w-full py-4 rounded-xl font-bold text-white shadow-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2 active:scale-95" style={{ backgroundColor: primaryColor }}><Plus size={20} /> Fazer Novo Pedido</button>
      </div>

      <FeedbackModal isOpen={showFeedback} onClose={() => setShowFeedback(false)} orderId={order.id} slug={slug} />
    </div>
  );
}
