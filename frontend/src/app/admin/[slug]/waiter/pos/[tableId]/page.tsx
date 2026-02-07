/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 16.0.0 (POS Ultimate)
 * DNA_ID: MF-WAITER-POS-V16-PLATINUM
 * Objective: High-velocity, error-proof order entry interface for waiters.
 */
"use client";

import React, { use, useState, useEffect, useMemo, useRef } from "react";
import { useRouter } from "next/navigation";
import { 
  ArrowLeft, Search, Plus, Trash2, 
  ChefHat, Send, Loader2, ShoppingCart, X,
  Utensils, AlertCircle, CheckCircle2
} from "lucide-react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

// Libs & Types
import { getMenu, getTableActiveSession, createOrder } from "@/lib/api";
import { MenuResponse, Product, TableSession, Option } from "@/types";
import { formatCurrency, cn } from "@/lib/utils";

// Components
import ProductModal from "@/components/menu/ProductModal";

interface WaiterPosPageProps {
  params: Promise<{ slug: string; tableId: string }>;
}

// Tipo local para o carrinho de lançamento (Staging)
interface StagedItem {
  tempId: number;
  product: Product;
  quantity: number;
  notes?: string;
  selectedOptions: Option[];
}

export default function WaiterPosPage({ params: paramsPromise }: WaiterPosPageProps) {
  // 🛡️ PROTOCOLO NEXT 16: Unwrapping de params
  const { slug, tableId } = use(paramsPromise);
  const router = useRouter();

  // --- ESTADOS DE DADOS ---
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [session, setSession] = useState<TableSession | null>(null);
  const [loading, setLoading] = useState(true);
  
  // --- ESTADOS DE UI ---
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isCartOpen, setIsCartOpen] = useState(false); // Mobile Drawer
  const [sending, setSending] = useState(false);

  // --- CARRINHO LOCAL (STAGING) ---
  const [stagedItems, setStagedItems] = useState<StagedItem[]>([]);

  // 1. BOOTSTRAP (Carregamento Inicial)
  useEffect(() => {
    const init = async () => {
      try {
        const [menuData, sessionData] = await Promise.all([
          getMenu(slug),
          getTableActiveSession(parseInt(tableId)).catch(() => null)
        ]);
        
        setMenu(menuData);
        setSession(sessionData);
        
        // Seleciona a primeira categoria por padrão
        if (menuData.categories.length > 0) {
          setActiveCategory(menuData.categories[0].id);
        }
      } catch (e) {
        console.error(e);
        toast.error("Erro ao carregar dados do POS.");
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [slug, tableId]);

  // 2. LÓGICA DE FILTRO (Busca Global vs Categoria)
  const filteredProducts = useMemo(() => {
    if (!menu) return [];
    
    let products: Product[] = [];
    
    // Se tiver busca, ignora categoria e busca em todo o cardápio
    if (searchTerm.trim().length > 0) {
      menu.categories.forEach(cat => {
        products.push(...cat.products.filter(p => 
          p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          p.short_code?.toLowerCase().includes(searchTerm.toLowerCase())
        ));
      });
    } else {
      // Senão, filtra pela categoria ativa
      const cat = menu.categories.find(c => c.id === activeCategory);
      if (cat) products = cat.products;
    }

    return products;
  }, [menu, activeCategory, searchTerm]);

  // 3. MANIPULAÇÃO DO CARRINHO LOCAL
  const handleAddItem = (product: Product, quantity: number, notes: string, options: Option[]) => {
    const newItem: StagedItem = {
      tempId: Date.now(),
      product,
      quantity,
      notes,
      selectedOptions: options
    };
    setStagedItems(prev => [...prev, newItem]);
    setSelectedProduct(null);
    
    // Feedback visual rápido
    toast.success(`${quantity}x ${product.name} lançado!`, {
      position: "bottom-center",
      duration: 1500
    });
    
    // Abre o carrinho automaticamente no mobile se for o primeiro item
    if (window.innerWidth < 768 && stagedItems.length === 0) {
      setIsCartOpen(true);
    }
  };

  const handleRemoveItem = (tempId: number) => {
    setStagedItems(prev => prev.filter(i => i.tempId !== tempId));
  };

  // 4. ENVIO PARA COZINHA (Commit)
  const handleSendOrder = async () => {
    if (stagedItems.length === 0) return;
    setSending(true);

    try {
      const payload = {
        table_id: parseInt(tableId),
        customer_name: session?.customer_name || `Mesa ${tableId}`,
        order_type: "dine_in",
        origin: "waiter",
        payment_method: "cash", // Será consolidado no fechamento da mesa
        items: stagedItems.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(o => o.id)
        }))
      };

      await createOrder(slug, payload);
      
      toast.success(
        <div className="flex flex-col">
          <span className="font-bold">Pedido Enviado! 🚀</span>
          <span className="text-xs">A cozinha já recebeu a comanda.</span>
        </div>
      );
      
      setStagedItems([]); // Limpa carrinho local
      setIsCartOpen(false);
      
      // Atualiza sessão para mostrar o novo total acumulado
      const updatedSession = await getTableActiveSession(parseInt(tableId));
      setSession(updatedSession);

    } catch (e) {
      toast.error("Erro ao enviar pedido. Tente novamente.");
    } finally {
      setSending(false);
    }
  };

  // Cálculo do total do carrinho local (Staging)
  const stagedTotal = stagedItems.reduce((acc, item) => {
    const optsPrice = item.selectedOptions.reduce((s, o) => s + Number(o.price), 0);
    return acc + ((Number(item.product.price) + optsPrice) * item.quantity);
  }, 0);

  if (loading) return (
    <div className="h-screen w-full flex flex-col items-center justify-center bg-slate-950 gap-4">
      <Loader2 className="animate-spin text-orange-500" size={48} />
      <p className="text-slate-500 font-bold text-xs uppercase tracking-widest">Carregando Terminal...</p>
    </div>
  );

  return (
    <div className="flex h-screen bg-slate-950 text-white overflow-hidden font-sans selection:bg-orange-500 selection:text-white">
      
      {/* === ÁREA ESQUERDA: CATÁLOGO (Flex-1) === */}
      <div className="flex-1 flex flex-col min-w-0 border-r border-slate-800 relative">
        
        {/* Header */}
        <header className="p-4 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md flex items-center gap-4 z-20">
          <button 
            onClick={() => router.back()} 
            className="p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors active:scale-95"
          >
            <ArrowLeft size={20} />
          </button>
          <div className="flex-1">
            <h1 className="text-xl font-black uppercase tracking-tight flex items-center gap-2">
              Mesa {tableId}
              {session && <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />}
            </h1>
            <p className="text-xs text-slate-400 font-bold uppercase tracking-widest truncate">
              {session?.customer_name || "Novo Atendimento"}
            </p>
          </div>
          
          {/* Barra de Busca Desktop */}
          <div className="relative w-64 hidden md:block group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-orange-500 transition-colors" size={18} />
            <input 
              type="text" 
              placeholder="Buscar produto..." 
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-orange-500 outline-none transition-all placeholder:text-slate-600"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </header>

        {/* Barra de Busca Mobile (Aparece abaixo do header) */}
        <div className="md:hidden p-4 pb-0">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input 
              type="text" 
              placeholder="Buscar produto..." 
              className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-11 pr-4 py-3 text-sm focus:border-orange-500 outline-none transition-all"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {/* Categorias (Scroll Horizontal) */}
        <div className="px-4 py-4 border-b border-slate-800/50 overflow-x-auto no-scrollbar flex gap-2 sticky top-0 bg-slate-950 z-10">
          <button
             onClick={() => { setActiveCategory(0); setSearchTerm(""); }}
             className={cn(
               "px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest whitespace-nowrap transition-all border",
               searchTerm === "" && activeCategory === 0
                 ? "bg-white text-slate-950 border-white" 
                 : "bg-slate-900 text-slate-500 border-slate-800 hover:border-slate-700"
             )}
          >
            Todos
          </button>
          {menu?.categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => { setActiveCategory(cat.id); setSearchTerm(""); }}
              className={cn(
                "px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest whitespace-nowrap transition-all border",
                activeCategory === cat.id && searchTerm === ""
                  ? "bg-orange-600 text-white border-orange-500 shadow-lg shadow-orange-900/20" 
                  : "bg-slate-900 text-slate-500 border-slate-800 hover:border-slate-700"
              )}
            >
              {cat.name}
            </button>
          ))}
        </div>

        {/* Grid de Produtos */}
        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar bg-slate-950">
          {filteredProducts.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-600 opacity-50">
              <Utensils size={64} className="mb-4" />
              <p className="text-sm font-bold uppercase tracking-widest">Nenhum produto encontrado</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-24 md:pb-4">
              {filteredProducts.map(product => (
                <button
                  key={product.id}
                  onClick={() => setSelectedProduct(product)}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-start text-left hover:border-orange-500/50 hover:bg-slate-800 transition-all active:scale-95 group h-full relative overflow-hidden"
                >
                  {/* Badge de Código Curto */}
                  {product.short_code && (
                    <span className="absolute top-2 right-2 bg-slate-950 text-slate-500 text-[9px] font-mono px-1.5 py-0.5 rounded border border-slate-800">
                      {product.short_code}
                    </span>
                  )}
                  
                  <div className="w-full aspect-video bg-slate-950 rounded-xl mb-3 overflow-hidden relative border border-slate-800/50">
                    {product.image_url ? (
                      <img src={product.image_url} alt={product.name} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-slate-800">
                        <ChefHat size={32} />
                      </div>
                    )}
                  </div>
                  
                  <h3 className="font-bold text-sm text-slate-200 line-clamp-2 mb-1 leading-tight">{product.name}</h3>
                  <p className="text-lg font-black text-orange-500 mt-auto">{formatCurrency(product.price)}</p>
                  
                  {/* Botão Plus Flutuante (Hover) */}
                  <div className="absolute bottom-3 right-3 bg-white text-slate-900 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity shadow-lg">
                    <Plus size={16} />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* === ÁREA DIREITA: CARRINHO / COMANDA (Sidebar em Desktop) === */}
      <div className={cn(
        "fixed inset-y-0 right-0 w-full md:w-96 bg-slate-900 border-l border-slate-800 shadow-2xl transform transition-transform duration-300 z-50 flex flex-col",
        isCartOpen ? "translate-x-0" : "translate-x-full md:translate-x-0"
      )}>
        {/* Header Carrinho */}
        <div className="p-5 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <div className="flex items-center gap-3">
            <div className="bg-orange-500/10 p-2 rounded-lg text-orange-500">
              <ShoppingCart size={20} />
            </div>
            <div>
              <h2 className="font-black text-lg uppercase tracking-tight text-white">Novo Pedido</h2>
              <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                {stagedItems.length} Itens na bandeja
              </p>
            </div>
          </div>
          <button onClick={() => setIsCartOpen(false)} className="md:hidden p-2 text-slate-400 hover:text-white">
            <X size={24} />
          </button>
        </div>

        {/* Lista de Itens */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar bg-slate-900/50">
          {stagedItems.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-700 opacity-50">
              <ChefHat size={64} className="mb-4 stroke-1" />
              <p className="text-sm font-bold uppercase tracking-widest">Bandeja Vazia</p>
              <p className="text-xs mt-2">Selecione itens no menu</p>
            </div>
          ) : (
            <AnimatePresence initial={false}>
              {stagedItems.map((item) => (
                <motion.div 
                  key={item.tempId}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="bg-slate-950 border border-slate-800 p-3 rounded-xl flex gap-3 group"
                >
                  <div className="bg-slate-900 w-10 h-10 rounded-lg flex items-center justify-center font-black text-slate-400 shrink-0 border border-slate-800">
                    {item.quantity}x
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-sm text-white truncate">{item.product.name}</p>
                    {item.selectedOptions.length > 0 && (
                      <p className="text-[10px] text-slate-500 truncate">
                        + {item.selectedOptions.map(o => o.name).join(", ")}
                      </p>
                    )}
                    {item.notes && (
                      <p className="text-[10px] text-orange-400 italic truncate">"{item.notes}"</p>
                    )}
                  </div>
                  <div className="flex flex-col items-end justify-between">
                    <p className="font-mono font-bold text-sm text-white">
                      {formatCurrency((Number(item.product.price) * item.quantity))}
                    </p>
                    <button 
                      onClick={() => handleRemoveItem(item.tempId)}
                      className="text-slate-600 hover:text-red-500 p-1 transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </div>

        {/* Footer de Ação */}
        <div className="p-5 bg-slate-950 border-t border-slate-800">
          <div className="flex justify-between items-end mb-4">
            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Total do Pedido</p>
              {session && (
                <p className="text-[10px] text-slate-600">
                  Acumulado na mesa: {formatCurrency(session.total_spent)}
                </p>
              )}
            </div>
            <p className="text-3xl font-black text-emerald-500 tracking-tighter">{formatCurrency(stagedTotal)}</p>
          </div>
          
          <button 
            onClick={handleSendOrder}
            disabled={stagedItems.length === 0 || sending}
            className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-black uppercase text-sm tracking-widest shadow-lg shadow-emerald-900/20 flex items-center justify-center gap-3 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-slate-800"
          >
            {sending ? <Loader2 className="animate-spin" /> : <Send size={20} />}
            ENVIAR PARA COZINHA
          </button>
        </div>
      </div>

      {/* Mobile Floating Action Button (Abre o Carrinho) */}
      <div className="md:hidden fixed bottom-6 right-6 z-40">
        <AnimatePresence>
          {stagedItems.length > 0 && (
            <motion.button 
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0 }}
              onClick={() => setIsCartOpen(true)}
              className="bg-orange-600 text-white p-4 rounded-full shadow-2xl shadow-orange-900/50 flex items-center gap-3 font-bold pr-6 border-2 border-white/10"
            >
              <div className="bg-white text-orange-600 w-6 h-6 rounded-full flex items-center justify-center text-xs font-black">
                {stagedItems.length}
              </div>
              <span>Ver Pedido</span>
            </motion.button>
          )}
        </AnimatePresence>
      </div>

      {/* Modal de Produto */}
      <ProductModal 
        isOpen={!!selectedProduct}
        onClose={() => setSelectedProduct(null)}
        product={selectedProduct}
        onAdd={handleAddItem}
        primaryColor="#ea580c"
      />
    </div>
  );
}
