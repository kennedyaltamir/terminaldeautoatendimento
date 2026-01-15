"use client";

import { useEffect, useState } from "react";
import { Plus, Edit2, Trash2, ChevronRight, ChevronDown, Image as ImageIcon } from "lucide-react";
import { getMenu } from "@/lib/api";
import { Category, Product } from "@/types";
import { toast, Toaster } from "sonner";
import ProductModal from "@/components/menu/ProductModal";
import MenuAdminSkeleton from "@/components/admin/MenuAdminSkeleton";

export default function MenuPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedCats, setExpandedCats] = useState<number[]>([]);
  const [isProductModalOpen, setIsProductModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  const fetchMenu = async () => {
    try {
      const data = await getMenu(slug);
      setCategories(data.categories);
      // Expande todas as categorias por padrão para melhor UX
      setExpandedCats(data.categories.map((c: Category) => c.id));
    } catch (e) {
      toast.error("Erro ao carregar cardápio");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenu();
  }, [slug]);

  const toggleCat = (id: number) => {
    if (expandedCats.includes(id)) {
      setExpandedCats(prev => prev.filter(c => c !== id));
    } else {
      setExpandedCats(prev => [...prev, id]);
    }
  };

  if (loading) return <MenuAdminSkeleton />;

  return (
    <div className="space-y-6 pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Cardápio Digital</h1>
          <p className="text-gray-400 text-sm">Gerencie produtos, preços e disponibilidade.</p>
        </div>
        <button 
          onClick={() => { setEditingProduct(null); setIsProductModalOpen(true); }}
          className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg active:scale-95"
        >
          <Plus size={20} /> Novo Produto
        </button>
      </div>

      <div className="space-y-4">
        {categories.map((category: Category) => (
          <div key={category.id} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
            <div 
              className="p-4 bg-gray-800/50 flex justify-between items-center cursor-pointer hover:bg-gray-700/50 transition-colors"
              onClick={() => toggleCat(category.id)}
            >
              <div className="flex items-center gap-3">
                {expandedCats.includes(category.id) ? <ChevronDown size={20} className="text-gray-400" /> : <ChevronRight size={20} className="text-gray-400" />}
                <h3 className="font-bold text-lg text-white">{category.name}</h3>
                <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded-full">{category.products.length} itens</span>
              </div>
              <div className="flex gap-2">
                <button className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg"><Edit2 size={16} /></button>
              </div>
            </div>

            {expandedCats.includes(category.id) && (
              <div className="p-2 space-y-2 bg-gray-900/30 border-t border-gray-700">
                {category.products.map((product: Product) => (
                  <div key={product.id} className="flex items-center justify-between p-3 rounded-lg bg-gray-800 border border-gray-700 hover:border-gray-600 transition-all group">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-700 rounded-lg flex items-center justify-center overflow-hidden">
                        {product.image_url ? (
                          <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
                        ) : (
                          <ImageIcon size={20} className="text-gray-500" />
                        )}
                      </div>
                      <div>
                        <p className="font-bold text-white">{product.name}</p>
                        <p className="text-sm text-orange-500 font-mono">R$ {(product.price / 100).toFixed(2)}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => { setEditingProduct(product); setIsProductModalOpen(true); }}
                        className="p-2 text-blue-400 hover:bg-blue-400/10 rounded-lg transition-colors"
                      >
                        <Edit2 size={18} />
                      </button>
                      <button 
                        className="p-2 text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                ))}
                {category.products.length === 0 && (
                  <div className="text-center py-8 text-gray-500 text-sm">
                    Nenhum produto nesta categoria.
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <ProductModal 
        isOpen={isProductModalOpen} 
        onClose={() => setIsProductModalOpen(false)} 
        product={editingProduct}
        categories={categories}
        onSuccess={fetchMenu}
      />
    </div>
  );
}
