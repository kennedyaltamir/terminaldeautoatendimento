// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 21:25:00
"use client";
import { useEffect, useState, useCallback, useMemo } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { 
  getMenu, createOrder, getOrder, requestService, 
  checkTableStatus, joinTable, validateCoupon, getWallet 
} from "@/lib/api";
import { MenuResponse, Product, Category, Order, CartItem, Option } from "@/types";
import { 
  Search, ShoppingBag, Plus, Trash2, ChevronRight, 
  ChefHat, User, X, Printer, Zap, Eye, CreditCard, 
  ArrowRightLeft, Star, WifiOff, Wallet, Calculator,
  Bell, Info, CheckCircle2, AlertCircle
} from "lucide-react";
import { useCart } from "@/context/CartContext";
import { toast, Toaster } from "sonner";
import { formatCurrency } from "@/lib/utils";
import ProductModal from "@/components/menu/ProductModal";
import OrderStatusView from "./OrderStatusView";
import CategoryNav from "./CategoryNav";
import SearchBar from "./SearchBar";
import WalletWidget from "./WalletWidget";
import ServiceModal from "./ServiceModal";
import FeedbackModal from "./FeedbackModal";

export default function MenuClient({ slug }: { slug: string }) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const tableId = searchParams.get("table");
  const qrToken = searchParams.get("token");
  const activeOrderId = searchParams.get("order");

  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isServiceOpen, setIsServiceOpen] = useState(false);
  const [activeOrder, setActiveOrder] = useState<Order | null>(null);
  const [customerName, setCustomerName] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [walletBalance, setWalletBalance] = useState(0);
  const [useBalance, setUseBalance] = useState(false);

  const { items, addToCart, removeFromCart, clearCart, total } = useCart();

  const fetchData = useCallback(async () => {
    try {
      const data = await getMenu(slug);
      setMenu(data);
      if (data.categories.length > 0) setActiveCategory(data.categories[0].id);
      
      if (activeOrderId) {
        const orderData = await getOrder(activeOrderId);
        setActiveOrder(orderData);
      }
    } catch (e) {
      toast.error("Erro ao carregar cardápio");
    } finally {
      setLoading(false);
    }
  }, [slug, activeOrderId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleAddToCart = (qty: number, notes: string, opts: Option[]) => {
    if (selectedProduct) {
      addToCart(selectedProduct, qty, notes, opts);
      setSelectedProduct(null);
      toast.success(`${selectedProduct.name} adicionado!`);
    }
  };

  const handleCheckout = async () => {
    if (items.length === 0) return;
    try {
      const payload = {
        table_id: tableId ? parseInt(tableId) : null,
        qr_token: qrToken || "public",
        customer_name: customerName || "Cliente",
        customer_phone: customerPhone,
        use_balance: useBalance,
        items: items.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          notes: i.notes,
          selected_options: i.selectedOptions.map(o => o.id)
        }))
      };
      const res = await createOrder(slug, payload);
      clearCart();
      router.push(`/${slug}/menu?order=${res.id}`);
    } catch (e: any) {
      toast.error(e.message || "Erro ao enviar pedido");
    }
  };

  const handleServiceRequest = async (type: string, notes: string) => {
    if (!tableId) return;
    try {
      await requestService(slug, parseInt(tableId), type, notes);
      toast.success("Solicitação enviada!");
      setIsServiceOpen(false);
    } catch (e) {
      toast.error("Erro ao solicitar serviço");
    }
  };

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Preparando cardápio...</div>;
  if (activeOrder) return <OrderStatusView order={activeOrder} onNewOrder={() => setActiveOrder(null)} primaryColor={menu?.company.primary_color || "#ea580c"} />;

  const filteredProducts = menu?.categories
    .find(c => c.id === activeCategory)
    ?.products.filter(p => p.name.toLowerCase().includes(searchTerm.toLowerCase())) || [];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-32">
      <Toaster position="top-center" richColors />
      
      {/* HEADER */}
      <header className="bg-white dark:bg-gray-900 p-6 border-b border-gray-100 dark:border-gray-800 sticky top-0 z-40">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            {menu?.company.logo_url ? (
              <img src={menu.company.logo_url} className="w-12 h-12 rounded-2xl object-cover shadow-md" alt="Logo" />
            ) : (
              <div className="w-12 h-12 bg-orange-600 rounded-2xl flex items-center justify-center text-white shadow-lg">
                <ChefHat size={28} />
              </div>
            )}
            <div>
              <h1 className="text-xl font-black text-gray-900 dark:text-white tracking-tight uppercase">{menu?.company.name}</h1>
              {tableId && <p className="text-[10px] font-black text-orange-600 uppercase tracking-widest">Mesa {tableId}</p>}
            </div>
          </div>
          <button onClick={() => setIsServiceOpen(true)} className="p-3 bg-gray-100 dark:bg-gray-800 rounded-2xl text-gray-600 dark:text-gray-400 active:scale-95 transition-all">
            <Bell size={24} />
          </button>
        </div>
        <SearchBar value={searchTerm} onChange={setSearchTerm} />
      </header>

      <CategoryNav 
        categories={menu?.categories || []} 
        activeId={activeCategory} 
        onSelect={setActiveCategory} 
        primaryColor={menu?.company.primary_color || "#ea580c"} 
      />

      <main className="p-4 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredProducts.map(product => (
            <button 
              key={product.id}
              onClick={() => setSelectedProduct(product)}
              className="bg-white dark:bg-gray-900 p-4 rounded-[2rem] border border-gray-100 dark:border-gray-800 shadow-sm flex justify-between items-center text-left active:scale-[0.98] transition-all group"
            >
              <div className="flex-1 pr-4">
                <h3 className="font-bold text-gray-900 dark:text-white mb-1 group-hover:text-orange-600 transition-colors">{product.name}</h3>
                <p className="text-xs text-gray-500 line-clamp-2 mb-3">{product.description}</p>
                <p className="text-orange-600 font-black">{formatCurrency(product.price)}</p>
              </div>
              {product.image_url && (
                <img src={product.image_url} className="w-24 h-24 rounded-2xl object-cover shadow-inner" alt={product.name} />
              )}
            </button>
          ))}
        </div>
      </main>

      {/* FOOTER CARRINHO */}
      {items.length > 0 && (
        <div className="fixed bottom-6 left-4 right-4 z-50 animate-in slide-in-from-bottom-4">
          <button 
            onClick={() => setIsCartOpen(true)}
            className="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 p-5 rounded-[2rem] shadow-2xl flex justify-between items-center group active:scale-95 transition-all"
          >
            <div className="flex items-center gap-4">
              <div className="bg-orange-600 text-white w-10 h-10 rounded-xl flex items-center justify-center font-black">
                {items.length}
              </div>
              <div className="text-left">
                <p className="text-[10px] font-black uppercase tracking-widest opacity-50">Ver Pedido</p>
                <p className="text-lg font-black">{formatCurrency(total)}</p>
              </div>
            </div>
            <ChevronRight size={24} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      )}

      {/* MODAL PRODUTO */}
      <ProductModal 
        isOpen={!!selectedProduct}
        onClose={() => setSelectedProduct(null)}
        product={selectedProduct}
        onConfirm={handleAddToCart}
        primaryColor={menu?.company.primary_color || "#ea580c"}
      />

      {/* MODAL CARRINHO (FULLSCREEN) */}
      {isCartOpen && (
        <div className="fixed inset-0 z-[60] bg-white dark:bg-gray-950 flex flex-col animate-in slide-in-from-right duration-300">
          <header className="p-6 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center">
            <h2 className="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Meu Pedido</h2>
            <button onClick={() => setIsCartOpen(false)} className="p-2 bg-gray-100 dark:bg-gray-800 rounded-full"><X size={24}/></button>
          </header>
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {items.map((item, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-50 dark:bg-gray-900 p-4 rounded-2xl border border-gray-100 dark:border-gray-800">
                <div>
                  <p className="font-bold text-gray-900 dark:text-white">{item.quantity}x {item.product.name}</p>
                  <p className="text-xs text-orange-600 font-black">{formatCurrency(item.product.price * item.quantity)}</p>
                </div>
                <button onClick={() => removeFromCart(i)} className="text-red-500 p-2"><Trash2 size={20}/></button>
              </div>
            ))}
            
            <div className="pt-6 space-y-4">
              <input 
                type="text" 
                placeholder="Seu Nome"
                className="w-full bg-gray-100 dark:bg-gray-800 border-none rounded-2xl p-4 text-sm outline-none focus:ring-2 focus:ring-orange-500/50"
                value={customerName}
                onChange={e => setCustomerName(e.target.value)}
              />
              <input 
                type="tel" 
                placeholder="Telefone (Opcional)"
                className="w-full bg-gray-100 dark:bg-gray-800 border-none rounded-2xl p-4 text-sm outline-none focus:ring-2 focus:ring-orange-500/50"
                value={customerPhone}
                onChange={e => setCustomerPhone(e.target.value)}
              />
            </div>
          </div>
          <footer className="p-6 border-t border-gray-100 dark:border-gray-800 safe-area-bottom">
            <div className="flex justify-between items-end mb-6">
              <span className="text-gray-500 font-bold uppercase text-xs tracking-widest">Total</span>
              <span className="text-4xl font-black text-gray-900 dark:text-white">{formatCurrency(total)}</span>
            </div>
            <button 
              onClick={handleCheckout}
              className="w-full py-5 rounded-2xl text-white font-black text-xl shadow-2xl active:scale-95 transition-all"
              style={{ backgroundColor: menu?.company.primary_color || "#ea580c" }}
            >
              Enviar Pedido
            </button>
          </footer>
        </div>
      )}

      <ServiceModal 
        isOpen={isServiceOpen} 
        onClose={() => setIsServiceOpen(false)} 
        onConfirm={handleServiceRequest}
        primaryColor={menu?.company.primary_color || "#ea580c"}
        segment={menu?.company.segment}
      />
    </div>
  );
}

