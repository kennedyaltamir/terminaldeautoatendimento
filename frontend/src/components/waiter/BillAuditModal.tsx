"use client";

import { useState, useEffect } from "react";
import { X, DollarSign, Clock, CheckCircle2, AlertCircle } from "lucide-react";
import { getSessionDetails } from "@/lib/api";
import { TableSession } from "@/types";
import Modal from "@/components/ui/Modal";

interface BillAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: number;
  tableName: string;
}

export default function BillAuditModal({ isOpen, onClose, sessionId, tableName }: BillAuditModalProps) {
  const [session, setSession] = useState<TableSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen && sessionId) {
      setLoading(true);
      getSessionDetails(sessionId)
        .then(setSession)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [isOpen, sessionId]);

  if (!isOpen) return null;

  const subtotal = session ? Number(session.total_spent) : 0;
  const serviceFee = subtotal * 0.10;
  const total = subtotal + serviceFee;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Espião: ${tableName}`}>
      {loading ? (
        <div className="p-8 text-center text-gray-500">Carregando comanda...</div>
      ) : session ? (
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 max-h-[50vh] overflow-y-auto">
            {session.orders.map((order) => (
              <div key={order.id} className="mb-4 border-b border-gray-200 pb-4 last:border-0 last:pb-0">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs font-mono text-gray-400">#{order.id.slice(0,6)}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded uppercase ${
                    order.status === 'delivered' ? 'bg-green-100 text-green-700' : 
                    order.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {order.status}
                  </span>
                </div>
                {order.items.map((item, i) => (
                  <div key={i} className="flex justify-between text-sm mb-1">
                    <span className="text-gray-700">{item.quantity}x {item.product.name}</span>
                    <span className="font-medium">R$ {Number(item.product.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
            ))}
          </div>

          <div className="space-y-2 pt-2 border-t border-gray-200">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>R$ {subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-gray-600">
              <span>Serviço (10%)</span>
              <span>R$ {serviceFee.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-xl font-black text-gray-900 mt-2">
              <span>Total</span>
              <span>R$ {total.toFixed(2)}</span>
            </div>
          </div>

          <div className="flex gap-2">
            <button onClick={onClose} className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-xl font-bold">Voltar</button>
            <button className="flex-1 bg-green-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2">
              <DollarSign size={18} /> Cobrar
            </button>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center text-red-500">Erro ao carregar.</div>
      )}
    </Modal>
  );
}