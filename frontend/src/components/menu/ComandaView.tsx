"use client";
import { useState } from "react";
import { X, Calculator } from "lucide-react";
import { TableSession } from "@/types";
import SplitBillModal from "./SplitBillModal"; // NOVO

export default function ComandaView({ session, onClose, primaryColor }: { session: TableSession, onClose: () => void, primaryColor: string }) {
  const [isSplitOpen, setIsSplitOpen] = useState(false);

  return (
    <div className="fixed inset-0 z-[80] bg-gray-50 flex flex-col animate-in slide-in-from-bottom duration-300">
      <div className="bg-white p-4 shadow-sm flex justify-between items-center sticky top-0 z-10">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Minha Comanda</h2>
          <p className="text-xs text-gray-500">Mesa de {session.customer_name}</p>
        </div>
        <button onClick={onClose} className="bg-gray-100 p-2 rounded-full hover:bg-gray-200 transition-colors"><X size={20}/></button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {session.orders.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p>Nenhum pedido realizado ainda.</p>
          </div>
        ) : (
          session.orders.map((order) => (
            <div key={order.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="flex justify-between items-center mb-3 border-b border-gray-100 pb-2">
                <span className="text-xs font-mono text-gray-400">#{order.id.slice(0,6)}</span>
                <span className={`text-xs font-bold px-2 py-1 rounded uppercase ${order.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : order.status === 'ready' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                  {order.status}
                </span>
              </div>
              <div className="space-y-2">
                {order.items.map((item, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span className="text-gray-700">{item.quantity}x {item.product.name}</span>
                    <span className="font-medium">R$ {Number(item.product.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
              <div className="mt-3 pt-2 border-t border-dashed border-gray-200 flex justify-between items-center">
                <span className="text-xs text-gray-500">{new Date(order.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                <span className="font-bold text-gray-900">Total: R$ {Number(order.total_amount).toFixed(2)}</span>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="bg-white p-6 border-t border-gray-200 safe-area-bottom space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-lg font-medium text-gray-600">Total da Mesa</span>
          <span className="text-3xl font-black text-gray-900">R$ {Number(session.total_spent).toFixed(2)}</span>
        </div>
        
        <div className="flex gap-3">
          <button 
            onClick={() => setIsSplitOpen(true)}
            className="flex-1 py-3.5 rounded-xl font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
          >
            <Calculator size={18} /> Dividir Conta
          </button>
          <button onClick={onClose} className="flex-1 py-3.5 rounded-xl font-bold text-white shadow-lg active:scale-95 transition-transform" style={{ backgroundColor: primaryColor }}>
            Voltar ao Cardápio
          </button>
        </div>
      </div>

      {/* MODAL DE DIVISÃO */}
      <SplitBillModal 
        isOpen={isSplitOpen} 
        onClose={() => setIsSplitOpen(false)} 
        orders={session.orders} 
        totalAmount={Number(session.total_spent)} 
        primaryColor={primaryColor} 
      />
    </div>
  );
}