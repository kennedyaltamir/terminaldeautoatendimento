/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Modal de Pagamento Pix com Feedback em Tempo Real.
 * FEATURES: QR Code, Copia e Cola, Listener de WebSocket.
 */
"use client";
import { useState, useEffect } from "react";
import { QRCodeSVG } from "qrcode.react";
import { Copy, CheckCircle2, Loader2, Smartphone } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";
import { formatCurrency } from "@/lib/utils";
import { useWebSocket } from "@/hooks/useWebSocket";

interface PixPaymentModalProps {
  isOpen: boolean;
  pixCode: string; // Payload Copia e Cola
  total: number;
  orderId: string;
  slug: string;
  onPaymentConfirmed: () => void;
}

export default function PixPaymentModal({ 
  isOpen, 
  pixCode, 
  total, 
  orderId,
  slug,
  onPaymentConfirmed 
}: PixPaymentModalProps) {
  const [copied, setCopied] = useState(false);
  const [isPaid, setIsPaid] = useState(false);

  // Listener de WebSocket para confirmação automática
  useWebSocket(slug, (data) => {
    if (data.type === "payment_confirmed" && data.order_id === orderId) {
      setIsPaid(true);
      toast.success("Pagamento recebido!");
      setTimeout(() => {
        onPaymentConfirmed();
      }, 2000); // Delay para o usuário ver o sucesso
    }
  });

  const handleCopy = () => {
    navigator.clipboard.writeText(pixCode);
    setCopied(true);
    toast.success("Código Pix copiado!");
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={() => {}} title="Pagamento via Pix">
      <div className="text-center space-y-6 py-4">
        {isPaid ? (
          <div className="flex flex-col items-center justify-center py-10 animate-in zoom-in">
            <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <CheckCircle2 size={48} className="text-green-600" />
            </div>
            <h3 className="text-2xl font-black text-slate-900">Pagamento Confirmado!</h3>
            <p className="text-slate-500">Enviando seu pedido para a cozinha...</p>
          </div>
        ) : (
          <>
            <div className="bg-white p-4 rounded-2xl inline-block border-4 border-orange-500 shadow-xl relative">
              <QRCodeSVG value={pixCode} size={220} level="M" />
              <div className="absolute -bottom-4 -right-4 bg-orange-600 text-white p-3 rounded-full shadow-lg animate-bounce">
                <Smartphone size={24} />
              </div>
            </div>

            <div>
              <p className="text-gray-500 text-xs font-bold uppercase mb-1">Valor Total</p>
              <p className="text-4xl font-black text-slate-900">{formatCurrency(total)}</p>
            </div>

            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 text-sm text-blue-700 flex items-center gap-3 text-left">
              <Loader2 size={20} className="animate-spin shrink-0" />
              <div>
                <p className="font-bold">Aguardando pagamento...</p>
                <p className="text-xs opacity-80">Abra o app do seu banco e escaneie o QR Code.</p>
              </div>
            </div>

            <button 
              onClick={handleCopy}
              className={`w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-95 ${copied ? "bg-green-100 text-green-700 border border-green-200" : "bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200"}`}
            >
              {copied ? <CheckCircle2 size={18} /> : <Copy size={18} />}
              {copied ? "Código Copiado!" : "Copiar Código Pix"}
            </button>
            
            {/* Botão de Bypass para Dev (Visível apenas em localhost) */}
            {process.env.NODE_ENV === 'development' && (
                <button 
                  onClick={() => { setIsPaid(true); setTimeout(onPaymentConfirmed, 1000); }}
                  className="text-[10px] text-gray-300 hover:text-gray-500 uppercase font-bold tracking-widest"
                >
                  [DEV] Simular Pagamento
                </button>
            )}
          </>
        )}
      </div>
    </Modal>
  );
}
