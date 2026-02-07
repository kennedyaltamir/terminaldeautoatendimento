"use client";
import { Plus, ArrowRight } from "lucide-react";
import { Product } from "@/types";

export default function UpsellModal({ isOpen, onClose, recommendations, onAdd, onFinish, primaryColor }: { isOpen: boolean, onClose: () => void, recommendations: Product[], onAdd: (product: Product) => void, onFinish: () => void, primaryColor: string }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[70] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full sm:max-w-md sm:rounded-xl rounded-t-2xl p-6 shadow-2xl">
        <div className="text-center mb-6">
          <h3 className="text-xl font-bold text-gray-900">Vai bem com...</h3>
          <p className="text-gray-500 text-sm">Complete seu pedido com estas sugestões!</p>
        </div>
        <div className="space-y-3 mb-6">
          {recommendations.map(rec => (
            <div key={rec.id} className="flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-orange-200 transition-all bg-gray-50">
              <div className="flex items-center gap-3">
                {rec.image_url ? <img src={rec.image_url} className="w-12 h-12 rounded-lg object-cover" /> : <div className="w-12 h-12 bg-gray-200 rounded-lg" />}
                <div>
                  <p className="font-bold text-gray-800 text-sm">{rec.name}</p>
                  <p className="text-orange-600 font-bold text-xs">R$ {Number(rec.price).toFixed(2)}</p>
                </div>
              </div>
              <button onClick={() => onAdd(rec)} className="bg-white border border-gray-200 hover:bg-orange-50 hover:border-orange-200 text-gray-700 hover:text-orange-700 p-2 rounded-full transition-colors shadow-sm">
                <Plus size={20} />
              </button>
            </div>
          ))}
        </div>
        <button onClick={onFinish} className="w-full text-white py-3.5 rounded-xl font-bold shadow-md flex items-center justify-center gap-2 active:scale-95 transition-transform" style={{ backgroundColor: primaryColor }}>
          Continuar para o Pedido <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}