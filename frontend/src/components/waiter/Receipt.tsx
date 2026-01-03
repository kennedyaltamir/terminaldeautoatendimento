"use client";

import { Order } from "@/types";
import { Printer, Smartphone, X } from "lucide-react";
import { printOrder } from "@/lib/printer/driver";

export default function Receipt({ order, companyName, onClose }: { order: Order, companyName: string, onClose?: () => void }) {
  
  const handleNativePrint = () => {
    printOrder(order, companyName);
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-xl overflow-hidden shadow-2xl max-w-sm w-full flex flex-col max-h-[90vh]">
        
        <div className="bg-gray-900 p-4 text-white flex justify-between items-center">
          <h3 className="font-bold">Visualizar Recibo</h3>
          <button onClick={onClose || (() => window.location.reload())} className="text-gray-400 hover:text-white"><X size={20}/></button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 bg-gray-100">
          {/* Preview Visual (HTML) - Apenas para conferência visual */}
          <div className="bg-white p-4 shadow-sm text-black font-mono text-xs leading-tight mx-auto w-[80mm] border border-gray-200">
            <div className="text-center border-b border-dashed border-black pb-2 mb-2">
              <h2 className="text-sm font-bold uppercase">{companyName}</h2>
              <p className="mt-1">{new Date(order.created_at).toLocaleString()}</p>
              <p className="font-bold mt-1">#{order.id.slice(0, 6)}</p>
            </div>
            
            <div className="mb-2 border-b border-dashed border-black pb-2">
              {order.order_type === 'delivery' ? (
                  <>
                      <p className="font-bold">DELIVERY</p>
                      <p>{order.customer_name}</p>
                      <p>{order.delivery_address}</p>
                  </>
              ) : (
                  <div className="flex justify-between">
                      <span className="font-bold">MESA {order.table?.table_number}</span>
                      <span>{order.customer_name}</span>
                  </div>
              )}
            </div>

            <div className="border-b border-dashed border-black pb-2 mb-2">
              {order.items.map((item, i) => (
                <div key={i} className="mb-1">
                  <div className="flex justify-between">
                    <span>{item.quantity}x {item.product.name}</span>
                    <span>{Number(item.product.price * item.quantity).toFixed(2)}</span>
                  </div>
                  {item.selected_options?.map((o, j) => (
                    <p key={j} className="ml-2 text-[10px]">+ {o.name}</p>
                  ))}
                  {item.notes && <p className="ml-2 text-[10px] italic">({item.notes})</p>}
                </div>
              ))}
            </div>

            <div className="flex justify-between font-bold text-sm mt-2">
              <span>TOTAL</span>
              <span>R$ {Number(order.total_amount).toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="p-4 bg-white border-t border-gray-200 flex gap-3">
          <button 
            onClick={() => window.print()} 
            className="flex-1 bg-gray-100 text-gray-800 py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-gray-200"
          >
            <Printer size={18} /> PC (Browser)
          </button>
          <button 
            onClick={handleNativePrint} 
            className="flex-1 bg-orange-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-orange-700 shadow-lg active:scale-95 transition-transform"
          >
            <Smartphone size={18} /> App (RawBT)
          </button>
        </div>
      </div>
    </div>
  );
}