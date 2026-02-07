
"use client";
import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import { 
  ArrowLeft, ShoppingCart, Zap, CreditCard, 
  Banknote, QrCode, CheckCircle2, Loader2 
} from "lucide-react";
import { toast } from "sonner";
import { formatCurrency, cn } from "@/lib/utils";
import { getMenu, createOrder } from "@/lib/api";
import { MenuResponse, Product, Option } from "@/types";
// Components
import ProductModal from "@/components/menu/ProductModal";
import PixPaymentModal from "@/components/menu/PixPaymentModal";

export default function QuickPosPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  const router = useRouter();
  
  // State
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [cart, setCart] = useState<{product: Product, quantity: number, options: Option[]}[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [pixData, setPixData] = useState<any>(null);
  const [activeOrderId, setActiveOrderId] = useState<string | null>(null);

  useEffect(() => {
    getMenu(slug).then(setMenu).catch(() => toast.error("Erro ao carregar cardápio"));
  }, [slug]);

  const addToCart = (product: Product, quantity: number, notes: string, options: Option[]) => {
    setCart(prev => [...prev, { product, quantity, options }]);
    setSelectedProduct(null);
    toast.success("Item adicionado!");
  };

  const total = cart.reduce((acc, item) => {
    const opts = item.options.reduce((s, o) => s + Number(o.price), 0);
    return acc + (Number(item.product.price) + opts) * item.quantity;
  }, 0);

  const handleCheckout = async (method: string) => {
    if (cart.length === 0) return;
    setIsProcessing(true);
    try {
      const order = await createOrder(slug, {
        customer_name: "Venda Rápida (Balcão)",
        order_type: "takeout",
        origin: "waiter",
        payment_method: method,
        items: cart.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          selected_options: i.options.map(o => o.id)
        }))
      });

      if (method === 'pix' && order.mp_qr_code) {
        setPixData({ qr_code: order.mp_qr_code, total: order.total_amount });
        setActiveOrderId(order.id);
      } else {
        toast.success("Venda registrada!");
        setCart([]);
        router.back();
      }
    } catch (e) {
      toast.error("Erro ao registrar venda.");
    } finally {
      setIsProcessing(false);
    }
  };

  if (!menu) return <div className="flex h-screen items-center justify-center bg-slate-950"><Loader2 className="animate-spin text-orange-500" /></div>;

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      {/* Header */}
      <header className="p-4 border-b border-slate-800 flex items-center gap-4 bg-slate-900">
        <button onClick={() => router.back()} className="p-2 bg-slate-800 rounded-xl hover:bg-slate-700">
          <ArrowLeft />
        </button>
        <div>
          <h1 className="font-black text-xl flex items-center gap-2">
            <Zap className="text-yellow-500" size={20} /> Venda Rápida
          </h1>
          <p className="text-xs text-slate-400">Sem vínculo de mesa</p>
        </div>
        <div className="ml-auto bg-slate-800 px-4 py-2 rounded-xl border border-slate-700">
          <span className="text-xs text-slate-400 font-bold uppercase mr-2">Total</span>
          <span className="text-xl font-black text-emerald-500">{formatCurrency(total)}</span>
        </div>
      </header>

      {/* Grid de Produtos */}
      <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 md:grid-cols-3 gap-3 content-start">
        {menu.categories.flatMap(c => c.products).map(product => (
          <button
            key={product.id}
            onClick={() => setSelectedProduct(product)}
            className="bg-slate-900 border border-slate-800 p-4 rounded-2xl text-left hover:border-orange-500/50 transition-all active:scale-95 flex flex-col justify-between h-32"
            data-testid="product-card" // 🛡️ FIX: Adicionado para o teste forense
          >
            <span className="font-bold text-sm line-clamp-2">{product.name}</span>
            <span className="font-black text-lg text-orange-500">{formatCurrency(product.price)}</span>
          </button>
        ))}
      </div>

      {/* Footer Actions */}
      <div className="p-4 bg-slate-900 border-t border-slate-800 safe-area-bottom">
        <div className="grid grid-cols-3 gap-3">
          <button 
            onClick={() => handleCheckout('cash')}
            disabled={cart.length === 0 || isProcessing}
            className="flex flex-col items-center justify-center p-3 bg-green-600 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-green-500 active:scale-95 disabled:opacity-50"
          >
            <Banknote size={24} className="mb-1" /> Dinheiro
          </button>
          <button 
            onClick={() => handleCheckout('card')}
            disabled={cart.length === 0 || isProcessing}
            className="flex flex-col items-center justify-center p-3 bg-blue-600 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-blue-500 active:scale-95 disabled:opacity-50"
          >
            <CreditCard size={24} className="mb-1" /> Cartão
          </button>
          <button 
            onClick={() => handleCheckout('pix')}
            disabled={cart.length === 0 || isProcessing}
            className="flex flex-col items-center justify-center p-3 bg-purple-600 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-purple-500 active:scale-95 disabled:opacity-50"
          >
            <QrCode size={24} className="mb-1" /> Pix
          </button>
        </div>
      </div>

      {/* Modais */}
      <ProductModal 
        isOpen={!!selectedProduct}
        onClose={() => setSelectedProduct(null)}
        product={selectedProduct}
        onAdd={addToCart}
        primaryColor="#ea580c"
      />

      {pixData && activeOrderId && (
        <PixPaymentModal 
          isOpen={!!pixData}
          pixCode={pixData.qr_code}
          total={pixData.total}
          orderId={activeOrderId}
          slug={slug}
          onPaymentConfirmed={() => {
            setPixData(null);
            setCart([]);
            toast.success("Pix Confirmado!");
            router.back();
          }}
        />
      )}
    </div>
  );
}
