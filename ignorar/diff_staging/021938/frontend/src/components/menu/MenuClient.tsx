"use client";

import { useState, useMemo } from "react";
import { Category, Product, Company, Option } from "@/types";
import { Search, ShoppingCart, Bell, ChevronRight, Info, Clock } from "lucide-react";
import CategoryNav from "./CategoryNav";
import SearchBar from "./SearchBar";
import ProductModal from "./ProductModal";
import { useCart } from "@/context/CartContext";
import { formatCurrency } from "@/lib/utils";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface MenuClientProps {
  slug: string;
  initialData: {
    company: Company;
    categories: Category[];
  };
}

export default function MenuClient({ slug, initialData }: MenuClientProps) {
  const [activeCategory, setActiveCategory] = useState(initialData.categories[0]?.id);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const { items, total, addToCart } = useCart();

  const filteredCategories = useMemo(() => {
    return initialData.categories.map(cat => ({
      ...cat,
      products: cat.products.filter(p => 
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.description?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    })).filter(cat => cat.products.length > 0);
  }, [initialData.categories, searchTerm]);

  const handleCallWaiter = () => {
    toast.info("Chamando atendente...", {
      description: "Um membro da equipe virá até sua mesa em breve."
    });
  };

  const handleAddToCart = (quantity: number, notes: string, opts: Option[]) => {
    if (selectedProduct) {
      addToCart(selectedProduct, quantity, notes, opts);
      setSelectedProduct(null);
      toast.success(`${selectedProduct.name} adicionado!`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 pb-32">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 p-4">
        <div className="max-w-2xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            {initialData.company.logo_url ? (
              <img src={initialData.company.logo_url} alt={initialData.company.name} className="w-10 h-10 rounded-xl object-cover" />
            ) : (
              <div className="w-10 h-10 bg-orange-600 rounded-xl flex items-center justify-center text-white font-black">
                {initialData.company.name[0]}
              </div>
            )}
            <div>
              <h1 className="font-black text-slate-900 dark:text-white leading-none">{initialData.company.name}</h1>
              <div className="flex items-center gap-1 mt-1">
                <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Aberto agora</span>
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <button 
              type="button"
              onClick={handleCallWaiter}
              className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-orange-100 hover:text-orange-600 transition-all"
              aria-label="Chamar Atendente"
            >
              <Bell size={20} />
            </button>
          </div>
        </div>
        <div className="max-w-2xl mx-auto mt-4">
          <SearchBar value={searchTerm} onChange={setSearchTerm} />
        </div>
      </header>

      {/* Nav de Categorias */}
      <div className="sticky top-[120px] z-30 bg-slate-50/80 dark:bg-slate-950/80 backdrop-blur-md py-2">
        <CategoryNav 
          categories={initialData.categories} 
          activeId={activeCategory} 
          onSelect={setActiveCategory}
          primaryColor={initialData.company.primary_color}
        />
      </div>

      {/* Lista de Produtos */}
      <main className="max-w-2xl mx-auto p-4 space-y-10">
        {filteredCategories.map(category => (
          <section key={category.id} id={`cat-${category.id}`} className="space-y-4">
            <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center gap-2">
              <div className="w-1 h-6 rounded-full bg-orange-500"></div>
              {category.name}
            </h2>
            <div className="grid gap-4">
              {category.products.map(product => (
                <button
                  key={product.id}
                  type="button"
                  onClick={() => setSelectedProduct(product)}
                  className="flex items-center justify-between p-4 bg-white dark:bg-slate-900 rounded-[1.5rem] border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all text-left group active:scale-[0.98]"
                >
                  <div className="flex-1 pr-4">
                    <h3 className="font-bold text-slate-900 dark:text-white group-hover:text-orange-600 transition-colors">{product.name}</h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                      {product.description}
                    </p>
                    <p className="text-lg font-black text-slate-900 dark:text-white mt-3">
                      {formatCurrency(product.price)}
                    </p>
                  </div>
                  {product.image_url && (
                    <img src={product.image_url} alt={product.name} className="w-24 h-24 rounded-2xl object-cover shadow-inner" />
                  )}
                </button>
              ))}
            </div>
          </section>
        ))}
      </main>

      {/* Footer / Carrinho */}
      {items.length > 0 && (
        <div className="fixed bottom-6 left-4 right-4 z-50 max-w-2xl mx-auto">
          <button
            type="button"
            onClick={() => toast.info("Abrindo carrinho...")}
            className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 p-5 rounded-2xl shadow-2xl flex items-center justify-between group active:scale-95 transition-all"
          >
            <div className="flex items-center gap-4">
              <div className="bg-orange-600 text-white w-8 h-8 rounded-lg flex items-center justify-center font-black text-sm">
                {items.length}
              </div>
              <span className="font-black uppercase text-xs tracking-widest">Ver meu pedido</span>
            </div>
            <span className="font-black text-lg">{formatCurrency(total)}</span>
          </button>
        </div>
      )}

      <ProductModal 
        product={selectedProduct} 
        isOpen={!!selectedProduct} 
        onClose={() => setSelectedProduct(null)}
        onConfirm={handleAddToCart}
        primaryColor={initialData.company.primary_color}
      />
    </div>
  );
}
