"use client";
import { useState, useEffect } from "react";
import { getQuickProducts, updateProduct } from "@/lib/api";
import { Product } from "@/types";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";
import { Loader2, Package, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils"; // FIX: Import adicionado

interface StockModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function StockModal({ isOpen, onClose }: StockModalProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      getQuickProducts()
        .then(setProducts)
        .catch((e: Error) => {
          console.error("Erro ao buscar produtos:", e);
          toast.error("Falha ao carregar lista de produtos.");
        })
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  const toggleAvailability = async (product: Product) => {
    setUpdatingId(product.id);
    const newStatus = !product.is_available;
    try {
      await updateProduct(product.id, { is_available: newStatus });
      setProducts(prev => prev.map(p => 
        p.id === product.id ? { ...p, is_available: newStatus } : p
      ));
      toast.success(`${product.name} ${newStatus ? 'ativado' : 'pausado'}`);
    } catch (e) {
      toast.error("Erro ao atualizar disponibilidade.");
    } finally {
      setUpdatingId(null);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Gestão Rápida de Estoque">
      <div className="space-y-6">
        <div className="bg-orange-50 border border-orange-200 p-4 rounded-xl flex gap-3">
          <AlertCircle className="text-orange-600 shrink-0" size={20} />
          <p className="text-xs text-orange-800 leading-relaxed font-medium">
            Pause produtos que acabaram para removê-los instantaneamente do cardápio digital dos clientes.
          </p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <Loader2 className="animate-spin text-orange-600" size={32} />
            <p className="text-xs font-black text-slate-400 uppercase tracking-widest">Sincronizando Inventário</p>
          </div>
        ) : (
          <div className="max-h-[50vh] overflow-y-auto space-y-2 pr-2 custom-scrollbar">
            {products.length === 0 ? (
              <div className="text-center py-10 text-slate-400">
                <Package size={40} className="mx-auto mb-2 opacity-20" />
                <p className="text-sm">Nenhum produto cadastrado.</p>
              </div>
            ) : (
              products.map(product => (
                <div key={product.id} className="flex items-center justify-between p-4 bg-slate-50 border border-slate-200 rounded-2xl transition-all hover:bg-white hover:shadow-sm">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${product.is_available ? 'bg-green-500' : 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]'}`} />
                    <div>
                      <p className="text-sm font-bold text-slate-900">{product.name}</p>
                      <p className="text-[10px] text-slate-500 font-mono">ID: {product.id}</p>
                    </div>
                  </div>
                  <button 
                    onClick={() => toggleAvailability(product)}
                    disabled={updatingId === product.id}
                    className={cn(
                      "px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all active:scale-95 disabled:opacity-50",
                      product.is_available 
                        ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    )}
                  >
                    {updatingId === product.id ? (
                      <Loader2 size={14} className="animate-spin" />
                    ) : (
                      product.is_available ? "Pausar" : "Ativar"
                    )}
                  </button>
                </div>
              ))
            )}
          </div>
        )}
        <div className="pt-4 border-t border-slate-100">
          <button 
            onClick={onClose} 
            className="w-full bg-slate-900 text-white py-4 rounded-2xl font-black uppercase tracking-widest text-xs hover:bg-slate-800 transition-all shadow-lg active:scale-[0.98]"
          >
            Concluir Ajustes
          </button>
        </div>
      </div>
    </Modal>
  );
}