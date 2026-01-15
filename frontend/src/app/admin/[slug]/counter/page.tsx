"use client";

import { useEffect, useState, useCallback } from "react";
import { getMenu, createOrder, getKitchenOrders } from "@/lib/api";
import { MenuResponse, Product, Order } from "@/types";
import { useCart } from "@/context/CartContext";
import { Search, Plus, Trash2, ShoppingBag, CreditCard, Banknote, QrCode, User, Loader2, Clock, CheckCircle2, AlertCircle, X } from "lucide-react";
import { toast, Toaster } from "sonner";
import ProductModal from "@/components/menu/ProductModal";
import { useWebSocket } from "@/hooks/useWebSocket";
import { openCashDrawer } from "@/lib/printer/driver";
import { formatCurrency } from "@/lib/utils";

export default function CounterPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [activeOrders, setActiveOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [customerName, setCustomerName] = useState("");
  const [processing, setProcessing] = useState(false);

  const { items, addToCart, removeFromCart, clearCart, total } = useCart();

  const fetchData = useCallback(async () => {
    try {
      const [menuData, ordersData] = await Promise.all([
        getMenu(slug),
        getKitchenOrders(slug)
      ]);
      setMenu(menuData);
      setActiveOrders(ordersData);
      if (menuData.categories.length > 0 && activeCategory === 0) {
        setActiveCategory(menuData.categories[0].id);
      }
    } catch (e) {
      toast.error("Erro ao carregar dados");
    } finally {
      setLoading(false);
    }
  }, [slug, activeCategory]);

  useEffect(() => { fetchData(); }, [fetchData]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      getKitchenOrders(slug).then(setActiveOrders);
    }
  });

  const handleCheckout = async (method: "cash" | "card" | "pix") => {
    if (items.length === 0) return toast.error("Carrinho vazio");
    setProcessing(true);
    try {
      await createOrder(slug, {
        table_id: null,
        qr_token: "staff-override",
        order_type: "takeout",
        customer_name: customerName || "Balcão",
        payment_method: method,
        items: items.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          notes: i.notes,
          selected_options: i.selectedOptions.map(o => o.id)
        }))
      });

      toast.success("Venda registrada!");

      // GAVETA DE DINHEIRO
      if (method === 'cash') {
        openCashDrawer();
        toast.info("Abrindo gaveta...");
      }

      clearCart();
      setCustomerName("");
      fetchData();
    } catch (e: any) {
      toast.error(e.message || "Erro ao vender");
    } finally {
      setProcessing(false);
    }
  };

  const filteredProducts = menu?.categories
    .find(c => c.id === activeCategory)
    ?.products.filter(p => p.name.toLowerCase().includes(searchTerm.toLowerCase())) || [];

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-white"><Loader2 className="animate-spin" /></div>;

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 overflow-hidden font-sans">
      <Toaster position="top-center" richColors />

      {/* COLUNA 1: CARDÁPIO (50%) */}
      <div className="flex-1 flex flex-col border-r border-gray-800 relative">
        <div className="p-4 border-b border-gray-800 bg-gray-900">
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
            <input
              type="text"
              placeholder="Buscar produto (F3)"
              className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              autoFocus
            />
          </div>
          <div className="flex gap-2 overflow-x-auto no-scrollbar pb-2">
            {menu?.categories.map(cat => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`whitespace-nowrap px-4 py-2 rounded-lg text-sm font-bold transition-colors ${activeCategory === cat.id ? 'bg-orange-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}      
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 lg:grid-cols-3 gap-3 content-start bg-gray-900">
          {filteredProducts.map(product => (
            <button
              key={product.id}
              onClick={() => product.option_groups.length > 0 ? setSelectedProduct(product) : addToCart(product, 1)}
              className="bg-gray-800 p-3 rounded-xl border border-gray-700 hover:border-orange-500/50 transition-all text-left flex flex-col justify-between h-28 group active:scale-95 relative overflow-hidden"       
            >
              <span className="font-bold text-gray-200 text-sm line-clamp-2 group-hover:text-orange-400 transition-colors">{product.name}</span>
              <div className="flex justify-between items-end mt-2">
                <span className="font-mono font-bold text-orange-500 text-sm">{formatCurrency(product.price)}</span>
                <div className="bg-gray-700 p-1 rounded text-gray-400 group-hover:bg-orange-600 group-hover:text-white transition-colors"><Plus size={14} /></div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* COLUNA 2: MONITOR DE PEDIDOS (25%) - AGORA FIXO */}
      <div className="w-80 flex flex-col border-r border-gray-800 bg-gray-900/50 hidden lg:flex">
        <div className="p-4 border-b border-gray-800 bg-gray-900">
          <h2 className="font-bold text-sm text-gray-400 uppercase tracking-wider flex items-center gap-2"> 
            <Clock size={16} /> Em Produção
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {activeOrders.map(order => (
            <div key={order.id} className="bg-gray-800 p-3 rounded-lg border border-gray-700 text-xs hover:border-gray-600 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="font-bold text-white truncate max-w-[120px]">{order.customer_name}</span>  
                <span className={`px-1.5 py-0.5 rounded font-bold uppercase text-[9px] ${order.status === 'ready' ? 'bg-green-900 text-green-400' : 'bg-yellow-900 text-yellow-400'}`}>
                  {order.status}
                </span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>#{order.id.slice(0,4)}</span>
                <span className="flex items-center gap-1"><Clock size={10}/> {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* COLUNA 3: CARRINHO (25%) */}
      <div className="w-96 flex flex-col bg-gray-800 shadow-2xl z-10">
        <div className="p-4 border-b border-gray-700 bg-gray-800 flex justify-between items-center">        
          <h2 className="font-bold text-lg flex items-center gap-2 text-white"><ShoppingBag size={18} className="text-orange-500"/> Venda Atual</h2>
          <button onClick={clearCart} className="text-xs text-red-400 hover:text-red-300 font-bold uppercase">Limpar</button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-600 gap-2">
                <ShoppingBag size={32} className="opacity-20" />
                <p className="text-xs">Caixa Livre</p>
            </div>
          ) : (
            items.map((item, idx) => (
              <div key={idx} className="bg-gray-700/50 p-2 rounded border border-gray-700 flex justify-between items-center group">
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between">
                    <p className="font-bold text-sm text-white truncate">{item.product.name}</p>
                    <p className="text-xs text-gray-400 font-mono">{formatCurrency(item.product.price)}</p>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-xs text-orange-400 font-bold">x{item.quantity}</span>
                    <button onClick={() => removeFromCart(idx)} className="text-red-400 hover:text-red-300 opacity-0 group-hover:opacity-100 transition-opacity"><Trash2 size={14}/></button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="p-4 bg-gray-900 border-t border-gray-800 space-y-3">
          <div className="bg-gray-800 p-2 rounded border border-gray-700 flex items-center gap-2">
            <User size={14} className="text-gray-500" />
            <input
              type="text"
              placeholder="Cliente (Opcional)"
              className="bg-transparent text-white text-sm outline-none w-full placeholder-gray-600"        
              value={customerName}
              onChange={e => setCustomerName(e.target.value)}
            />
          </div>

          <div className="flex justify-between items-end">
            <span className="text-gray-400 text-xs uppercase font-bold">Total a Pagar</span>
            <span className="text-3xl font-black text-white">{formatCurrency(total)}</span>
          </div>

          <div className="grid grid-cols-3 gap-2">
            <button onClick={() => handleCheckout('cash')} disabled={processing} className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-lg flex flex-col items-center gap-1 text-[10px] font-bold transition-colors disabled:opacity-50 active:scale-95">
              <Banknote size={20} /> DINHEIRO
            </button>
            <button onClick={() => handleCheckout('card')} disabled={processing} className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg flex flex-col items-center gap-1 text-[10px] font-bold transition-colors disabled:opacity-50 active:scale-95">
              <CreditCard size={20} /> CARTÃO
            </button>
            <button onClick={() => handleCheckout('pix')} disabled={processing} className="bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-lg flex flex-col items-center gap-1 text-[10px] font-bold transition-colors disabled:opacity-50 active:scale-95">
              <QrCode size={20} /> PIX
            </button>
          </div>
        </div>
      </div>

      <ProductModal
        product={selectedProduct}
        isOpen={!!selectedProduct}
        onClose={() => setSelectedProduct(null)}
        onConfirm={(qty, notes, opts) => {
            if(selectedProduct) addToCart(selectedProduct, qty, notes, opts);
            setSelectedProduct(null);
        }}
        primaryColor="#ea580c"
      />
    </div>
  );
}

