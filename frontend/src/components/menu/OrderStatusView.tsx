"use client";
import { Clock, ChefHat, CheckCircle2, Banknote, Copy, Loader2, Utensils, Plus, MapPin, Navigation, Star } from "lucide-react";
import { Order } from "@/types";
import { QRCodeSVG } from "qrcode.react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState, useCallback, useEffect } from "react";
import FeedbackModal from "@/components/menu/FeedbackModal";

export default function OrderStatusView({ order, onNewOrder, primaryColor }: { order: Order, onNewOrder: () => void, primaryColor: string }) {
  const isPaid = order.payment_status === 'paid';
  const isOnline = order.payment_method === 'online';
  const [driverLocation, setDriverLocation] = useState<{lat: number, lng: number} | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);

  // Gatilho para Feedback: Se o pedido foi entregue ou pago e ainda não tem feedback
  useEffect(() => {
    if ((order.status === 'delivered' || order.payment_status === 'paid') && !order.feedback) {
      const timer = setTimeout(() => setShowFeedback(true), 2000);
      return () => clearTimeout(timer);
    }
  }, [order.status, order.payment_status, order.feedback]);

  const steps = [
    { id: 'pending', label: 'Recebido', icon: Clock },
    { id: 'preparing', label: 'Preparando', icon: ChefHat },
    { id: 'ready', label: 'Pronto', icon: CheckCircle2 },
  ];

  if (order.order_type === 'delivery') {
    steps.push({ id: 'delivering', label: 'Em Rota', icon: MapPin });
  }

  const currentStepIndex = steps.findIndex(s => s.id === order.status) === -1 
    ? (order.status === 'accepted' ? 0 : (order.status === 'delivered' ? steps.length : 0)) 
    : steps.findIndex(s => s.id === order.status);

  const copyToClipboard = () => {
    if (order.mp_qr_code) {
      navigator.clipboard.writeText(order.mp_qr_code);
      alert("Código Pix copiado!");
    }
  };

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.type === "driver_location" && data.order_id === order.id) {
      setDriverLocation({ lat: data.lat, lng: data.lng });
    }
  }, [order.id]);

  useWebSocket("", handleWebSocketMessage); 

  const openTrackingMap = () => {
    if (driverLocation) {
      window.open(`https://www.google.com/maps/search/?api=1&query=${driverLocation.lat},${driverLocation.lng}`, '_blank');
    }
  };

  const canRate = !order.feedback && (order.status === 'delivered' || order.payment_status === 'paid');

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col pb-10 font-sans">
      <div className="bg-white p-6 shadow-sm border-b border-gray-100">
        <h1 className="text-2xl font-bold text-gray-900">
          Olá, {order.customer_name?.split(' ')[0] || 'Cliente'}!
        </h1>
        <p className="text-gray-50 text-sm mt-1">
          Acompanhe seu pedido <span className="font-mono font-bold text-gray-700">#{order.id.slice(0, 6)}</span>
        </p>
      </div>

      <div className="p-6 space-y-6 max-w-md mx-auto w-full">

        {isPaid && (
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex justify-between relative">
              <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-100 -z-10 -translate-y-1/2 rounded-full"></div>
              <div 
                className="absolute top-1/2 left-0 h-1 bg-green-500 -z-10 -translate-y-1/2 rounded-full transition-all duration-1000"
                style={{ width: `${(currentStepIndex / (steps.length - 1)) * 100}%` }}
              ></div>

              {steps.map((step, idx) => {
                const isActive = idx <= currentStepIndex;
                const isCurrent = idx === currentStepIndex;
                return (
                  <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-1">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${isActive ? 'bg-green-500 text-white shadow-lg shadow-green-200' : 'bg-gray-200 text-gray-400'}`}>
                      <step.icon size={20} />
                    </div>
                    <span className={`text-xs font-bold ${isCurrent ? 'text-green-600' : 'text-gray-400'}`}>{step.label}</span>
                  </div>
                );
              })}
            </div>

            {order.status === 'ready' && order.order_type !== 'delivery' && (
              <div className="mt-6 bg-green-50 text-green-800 p-3 rounded-xl text-center font-bold animate-bounce">
                🍽️ Seu pedido está pronto!
              </div>
            )}

            {order.status === 'delivering' && (
              <div className="mt-6 space-y-3">
                <div className="bg-blue-50 text-blue-800 p-3 rounded-xl text-center font-bold flex items-center justify-center gap-2">
                  <Navigation size={18} className="animate-pulse"/> Motorista a caminho!
                </div>

                {driverLocation && (
                  <button 
                    onClick={openTrackingMap}
                    className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold shadow-lg flex items-center justify-center gap-2 hover:bg-blue-700 transition-colors"
                  >
                    <MapPin size={18} /> Ver Localização Atual
                  </button>
                )}

                {order.delivery_code && (
                  <div className="bg-gray-100 p-4 rounded-xl text-center border border-gray-200">
                    <p className="text-xs text-gray-500 uppercase font-bold mb-1">Código de Entrega</p>
                    <p className="text-3xl font-mono font-black tracking-widest text-gray-900">{order.delivery_code}</p>
                    <p className="text-[10px] text-gray-400 mt-1">Informe ao entregador</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {!isPaid && isOnline && order.mp_qr_code && (
          <div className="bg-white p-6 rounded-2xl shadow-lg border-2 border-orange-100">
            <h3 className="text-lg font-bold text-center mb-4">Pagamento Pendente</h3>
            <div className="flex justify-center mb-4">
              <QRCodeSVG value={order.mp_qr_code} size={180} />
            </div>
            <div className="flex gap-2">
              <input readOnly value={order.mp_qr_code} className="flex-1 bg-gray-100 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-600 truncate" />
              <button onClick={copyToClipboard} className="bg-gray-900 text-white p-2 rounded-lg hover:bg-gray-800"><Copy size={16} /></button>
            </div>
            <div className="mt-4 flex items-center justify-center gap-2 text-orange-600 bg-orange-50 p-2 rounded-lg">
              <Loader2 className="animate-spin" size={16} />
              <span className="text-xs font-bold">Aguardando confirmação...</span>
            </div>
          </div>
        )}

        {!isPaid && !isOnline && (
          <div className="bg-orange-50 p-6 rounded-2xl border border-orange-100 text-center">
            <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Banknote className="text-orange-600" size={32} />
            </div>
            <h3 className="font-bold text-orange-900 text-lg">Aguardando Pagamento</h3>
            <p className="text-orange-700 text-sm mt-1">
              {order.order_type === 'delivery' ? 'Pagamento na entrega.' : 'O garçom irá até sua mesa.'}
            </p>
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-4 border-b border-gray-100 bg-gray-50/50">
            <h3 className="font-bold text-gray-900 flex items-center gap-2"><Utensils size={16}/> Resumo do Pedido</h3>
          </div>
          <div className="p-4 space-y-4">
            {order.items.map((item, i) => (
              <div key={i} className="flex justify-between items-start">
                <div className="flex gap-3">
                  <div className="bg-gray-100 w-8 h-8 rounded flex items-center justify-center text-xs font-bold text-gray-600">{item.quantity}x</div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{item.product.name}</p>
                    {item.selected_options.length > 0 && (
                      <p className="text-xs text-gray-500">+ {item.selected_options.map(o => o.name).join(", ")}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}

            <div className="border-t border-dashed border-gray-200 pt-4 mt-4 space-y-2">
              {Number(order.delivery_fee) > 0 && (
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Taxa de Entrega</span>
                  <span>R$ {Number(order.delivery_fee).toFixed(2)}</span>
                </div>
              )}
              {Number(order.discount_amount) > 0 && (
                <div className="flex justify-between text-sm text-green-600">
                  <span>Desconto Fidelidade</span>
                  <span>- R$ {Number(order.discount_amount).toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between text-lg font-black text-gray-900">
                <span>Total</span>
                <span>R$ {Number(order.total_amount).toFixed(2)}</span>
              </div>
              {Number(order.cashback_earned) > 0 && (
                <div className="bg-purple-50 text-purple-700 text-xs p-2 rounded-lg text-center font-bold mt-2">
                  🎉 Você ganhou R$ {Number(order.cashback_earned).toFixed(2)} de cashback!
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Botão de Avaliação Manual */}
        {canRate && (
          <button 
            data-testid="btn-avaliar"
            onClick={() => setShowFeedback(true)}
            className="w-full py-3 rounded-xl border-2 border-yellow-400 text-yellow-600 font-bold flex items-center justify-center gap-2 hover:bg-yellow-50 transition-colors"
          >
            <Star size={20} /> Avaliar Pedido
          </button>
        )}

        <button 
          onClick={onNewOrder}
          className="w-full py-4 rounded-xl font-bold text-white shadow-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2 active:scale-95"
          style={{ backgroundColor: primaryColor }}
        >
          <Plus size={20} /> Fazer Novo Pedido
        </button>

      </div>

      {/* Modal de Feedback */}
      <FeedbackModal 
        isOpen={showFeedback} 
        onClose={() => setShowFeedback(false)} 
        orderId={order.id}
        slug="hamburgueria-ze" 
      />
    </div>
  );
}
