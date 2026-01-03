"use client";

import { useState, useEffect } from "react";
import { X, Search, Box, AlertCircle } from "lucide-react";
import { Product } from "@/types";
import { getQuickProducts, updateProduct } from "@/lib/api";
import Modal from "@/components/ui/Modal";

interface StockModalProps {
  isOpen: boolean;
  onClose: () => void;
  slug: string;
}

export default function StockModal({ isOpen, onClose, slug }: StockModalProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      getQuickProducts(slug)
        .then(setProducts)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [isOpen, slug]);

  const toggleAvailability = async (product: Product) => {
    // Optimistic Update
    const newStatus = !product.is_available;
    setProducts(prev => prev.map(p => p.id === product.id ? { ...p, is_available: newStatus } : p));

    try {
      await updateProduct(product.id, { is_available: newStatus });
    } catch (e) {
      // Revert on error
      setProducts(prev => prev.map(p => p.id === product.id ? { ...p, is_available: !newStatus } : p));
      alert("Erro ao atualizar estoque");
    }
  };

  const filteredProducts = products.filter(p => 
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Gestão Rápida de Estoque (86)">
      <div className="space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            type="text" 
            placeholder="Buscar produto..." 
            className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={search}
            onChange={e => setSearch(e.target.value)}
            autoFocus
          />
        </div>

        <div className="max-h-[60vh] overflow-y-auto space-y-2 pr-1">
          {loading ? (
            <p className="text-center text-gray-500 py-4">Carregando produtos...</p>
          ) : filteredProducts.length === 0 ? (
            <p className="text-center text-gray-500 py-4">Nenhum produto encontrado.</p>
          ) : (
            filteredProducts.map(product => (
              <div key={product.id} className={`flex items-center justify-between p-3 rounded-lg border transition-all ${product.is_available ? 'bg-gray-800 border-gray-700' : 'bg-red-900/20 border-red-800'}`}>
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${product.is_available ? 'bg-gray-700 text-gray-400' : 'bg-red-800 text-red-200'}`}>
                    {product.is_available ? <Box size={20} /> : <AlertCircle size={20} />}
                  </div>
                  <div>
                    <p className={`font-bold ${product.is_available ? 'text-white' : 'text-red-400 line-through'}`}>{product.name}</p>
                    <p className="text-xs text-gray-500">R$ {Number(product.price).toFixed(2)}</p>
                  </div>
                </div>
                
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" checked={product.is_available} onChange={() => toggleAvailability(product)} />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                </label>
              </div>
            ))
          )}
        </div>
      </div>
    </Modal>
  );
}