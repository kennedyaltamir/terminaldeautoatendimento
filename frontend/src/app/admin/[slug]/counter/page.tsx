// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 21:45:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { getMenu, createOrder, getKitchenOrders } from "@/lib/api";
import { Product, Order, CartItem, Option, MenuResponse } from "@/types";
import { 
  Search, ShoppingCart, Trash2, Plus, 
  CheckCircle2, Loader2, Clock, User, 
  CreditCard, Banknote, QrCode
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { useWebSocket } from "@/hooks/useWebSocket";
import { formatCurrency } from "@/lib/utils";
import ProductModal from "@/components/menu/ProductModal";

export default function CounterPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [customerName, setCustomerName] = useState("");

  const fetchData = useCallback(async () => {
    try {
      const [menuData, ordersData] = await Promise.all([
        getMenu(slug),
        getKitchenOrders(slug)
      ]);
      setMenu(menuData);
      setOrders(ordersData);
    } catch (e) {
      toast.error("Erro ao carregar dados do balcão");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { fetchData(); }, [fetchData]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      fetchData();
    }
  });

  const addToCart = (quantity: number, notes: string, selectedOptions: Option[]) => {
    if (selectedProduct) {
      setCart(prev => [...prev, { 
        product: selectedProduct, 
        quantity, 
        notes, 
        selectedOptions 
      }]);
      setSelectedProduct(null);
      toast.success(`${selectedProduct.name} adicionado`);
    }
  };

  const removeFromCart = (index: number) => {
    setCart(prev => prev.filter((_, i) => i !== index));
  };

  const cartTotal = cart.reduce((acc, item) => {
    const optsPrice = item.selectedOptions.reduce((s, o) => s + Number(o.price), 0);
    return acc + (Number(item.product.price) + optsPrice) * item.quantity;
  }, 0);

  const handleCheckout = async (method: string) => {
    if (cart.length === 0) return;
    setSubmitting(true);
    try {
      const payload = {
        customer_name: customerName || "Balcão",
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
      toast.success("Pedido realizado com sucesso!");
      fetchData();
    } catch (e) {
      toast.error("Erro ao finalizar pedido");
    } finally {
      setSubmitting(false);
    }
  };

  const filteredProducts = menu?.categories.flatMap(c => c.products).filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Iniciando PDV Balcão...</div>;

  return (
    <div className="flex h-[calc(100vh-120px)] gap-6 animate-in fade-in duration-500">
      <Toaster position="top-center" richColors />
      <div className="flex-1 flex flex-col bg-white dark:bg-gray-900 rounded-3xl border border-gray-200 dark:border-gray-800 shadow-xl overflow-hidden">
        <div className="p-6 border-b border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input 
              type="text"
              placeholder="Buscar produto..."
              className="w-full pl-12 pr-4 py-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-orange-500 outline-none transition-all font-bold"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-2 xl:grid-cols-3 gap-4">
          {filteredProducts.map(product => (
            <button 
              key={product.id}
              onClick={() => setSelectedProduct(product)}
              className="flex flex-col text-left bg-gray-50 dark:bg-gray-800/30 border border-gray-100 dark:border-gray-800 rounded-2xl p-4 hover:border-orange-500 transition-all group"
            >
              <h3 className="font-bold text-gray-900 dark:text-white mb-1 line-clamp-2">{product.name}</h3>
              <p className="text-orange-600 font-black mt-auto">{formatCurrency(product.price)}</p>
            </button>
          ))}
        </div>
      </div>

      <div className="w-96 flex flex-col gap-6">
        <div className="flex-1 bg-gray-900 rounded-3xl border border-gray-800 shadow-2xl flex flex-col overflow-hidden">
          <div className="p-6 border-b border-gray-800 flex justify-between items-center">
            <h2 className="text-white font-black flex items-center gap-2 uppercase tracking-widest text-sm">
              <ShoppingCart size={18} className="text-orange-500" /> Carrinho
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {cart.map((item, i) => (
              <div key={i} className="bg-gray-800/50 p-3 rounded-xl border border-gray-700 flex justify-between items-center">
                <div>
                  <p className="text-white text-sm font-bold">{item.quantity}x {item.product.name}</p>
                  <p className="text-[10px] text-gray-500">{formatCurrency(item.product.price * item.quantity)}</p>
                </div>
                <button onClick={() => removeFromCart(i)} className="text-gray-600 hover:text-red-500 p-2">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
          <div className="p-6 bg-gray-800/50 border-t border-gray-800 space-y-4">
            <div className="flex justify-between items-end">
              <span className="text-gray-500 text-xs font-bold uppercase">Total</span>
              <span className="text-3xl font-black text-white">{formatCurrency(cartTotal)}</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <button onClick={() => handleCheckout('cash')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 rounded-xl text-green-500">
                <Banknote size={20} /> <span className="text-[8px] font-black">DINHEIRO</span>
              </button>
              <button onClick={() => handleCheckout('card')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 rounded-xl text-blue-500">
                <CreditCard size={20} /> <span className="text-[8px] font-black">CARTÃO</span>
              </button>
              <button onClick={() => handleCheckout('pix')} disabled={submitting || cart.length === 0} className="flex flex-col items-center gap-1 p-3 bg-gray-800 rounded-xl text-purple-500">
                <QrCode size={20} /> <span className="text-[8px] font-black">PIX</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {selectedProduct && (
        <ProductModal 
          isOpen={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          product={selectedProduct}
          onConfirm={addToCart}
          primaryColor="#ea580c"
        />
      )}
    </div>
  );
}

