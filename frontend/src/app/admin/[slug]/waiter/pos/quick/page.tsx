// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 20:05:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getMenu, createOrder, getQuickProducts } from "@/lib/api";
import { Product, Category, CartItem, Option, MenuResponse } from "@/types";
import { 
  Search, ShoppingCart, Trash2, Plus, Minus, 
  CheckCircle2, Loader2, Smartphone, Clock, User, 
  CreditCard, Banknote, QrCode, ArrowLeft, Zap
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { formatCurrency } from "@/lib/utils";
import ProductModal from "@/components/menu/ProductModal";

export default function QuickPosPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [customerName, setCustomerName] = useState("");

  const fetchData = useCallback(async () => {
    try {
      const menuData = await getMenu(slug);
      setMenu(menuData);
    } catch (e) {
      toast.error("Erro ao carregar cardápio");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const addToCart = (product: Product, qty: number, notes: string, opts: Option[]) => {
    setCart(prev => [...prev, { product, quantity: qty, notes, selectedOptions: opts }]);
    setSelectedProduct(null);
  };

  const handleCheckout = async (method: string) => {
    if (cart.length === 0) return;
    setSubmitting(true);
    try {
      const payload = {
        customer_name: customerName || "Venda Rápida",
        order_type: "takeout",
        payment_method: method,
        items: cart.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(o => o.id)
        }))
      };
      await createOrder(slug, payload);
      setCart([]);
      setCustomerName("");
      toast.success("Venda concluída!");
      router.push(`/admin/${slug}/waiter`);
    } catch (e) {
      toast.error("Erro ao processar venda");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Iniciando Venda Rápida...</div>;

  const allProducts = menu?.categories.flatMap(c => c.products).filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const cartTotal = cart.reduce((acc, item) => {
    const optsPrice = item.selectedOptions.reduce((s, o) => s + Number(o.price), 0);
    return acc + (Number(item.product.price) + optsPrice) * item.quantity;
  }, 0);

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white font-sans">
      <Toaster position="top-center" richColors />
      
      <header className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-900 shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={() => router.back()} className="p-2 hover:bg-gray-800 rounded-full">
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-xl font-black flex items-center gap-2">
            <Zap className="text-orange-500" /> Venda Rápida
          </h1>
        </div>
        <div className="bg-gray-800 px-4 py-2 rounded-xl border border-gray-700">
          <span className="text-xs font-bold text-gray-500 uppercase mr-2">Total</span>
          <span className="text-xl font-black text-orange-500">{formatCurrency(cartTotal)}</span>
        </div>
      </header>

      <main className="flex-1 overflow-hidden flex">
        {/* LISTA DE PRODUTOS */}
        <div className="flex-1 flex flex-col border-r border-gray-800">
          <div className="p-4 bg-gray-900 border-b border-gray-800">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
              <input 
                type="text"
                placeholder="Buscar produto..."
                className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl outline-none focus:ring-2 focus:ring-orange-500"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 lg:grid-cols-3 gap-3 content-start">
            {allProducts.map(product => (
              <button 
                key={product.id}
                onClick={() => setSelectedProduct(product)}
                className="bg-gray-800 p-4 rounded-2xl border border-gray-700 hover:border-orange-500/50 transition-all text-left active:scale-95"
              >
                <h3 className="font-bold text-sm line-clamp-2 mb-2">{product.name}</h3>
                <p className="text-orange-500 font-black">{formatCurrency(product.price)}</p>
              </button>
            ))}
          </div>
        </div>

        {/* CARRINHO & CHECKOUT */}
        <div className="w-96 flex flex-col bg-gray-900">
          <div className="p-4 border-b border-gray-800 flex justify-between items-center">
            <span className="font-black text-xs uppercase tracking-widest text-gray-500">Carrinho</span>
            <button onClick={() => setCart([])} className="text-[10px] font-black text-red-500 uppercase">Limpar</button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {cart.map((item, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-800/50 p-3 rounded-xl border border-gray-700">
                <div className="flex-1">
                  <p className="text-sm font-bold">{item.quantity}x {item.product.name}</p>
                  <p className="text-[10px] text-gray-500 font-mono">{formatCurrency(item.product.price * item.quantity)}</p>
                </div>
                <button onClick={() => setCart(prev => prev.filter((_, idx) => idx !== i))} className="text-gray-500 hover:text-red-500 p-2">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
          <div className="p-6 bg-gray-800/50 border-t border-gray-800 space-y-4">
            <input 
              type="text"
              placeholder="Nome do Cliente"
              className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white text-sm outline-none focus:border-orange-500"
              value={customerName}
              onChange={e => setCustomerName(e.target.value)}
            />
            <div className="grid grid-cols-3 gap-2">
              <button onClick={() => handleCheckout('cash')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 hover:bg-gray-700 rounded-xl text-green-500 transition-all disabled:opacity-30">
                <Banknote size={20} />
                <span className="text-[8px] font-black uppercase">Dinheiro</span>
              </button>
              <button onClick={() => handleCheckout('card')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 hover:bg-gray-700 rounded-xl text-blue-500 transition-all disabled:opacity-30">
                <CreditCard size={20} />
                <span className="text-[8px] font-black uppercase">Cartão</span>
              </button>
              <button onClick={() => handleCheckout('pix')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 hover:bg-gray-700 rounded-xl text-purple-500 transition-all disabled:opacity-30">
                <QrCode size={20} />
                <span className="text-[8px] font-black uppercase">Pix</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      {selectedProduct && (
        <ProductModal 
          isOpen={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          product={selectedProduct}
          onConfirm={(qty: number, notes: string, opts: Option[]) => addToCart(selectedProduct, qty, notes, opts)}
          primaryColor="#ea580c"
        />
      )}
    </div>
  );
}

