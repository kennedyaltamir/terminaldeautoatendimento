// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 19:55:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { 
  getMenu, createOrder, checkTableStatus, 
  getSessionDetails, getWallet, getTableSession 
} from "@/lib/api";
import { Product, Category, CartItem, Option, TableSession, MenuResponse } from "@/types";
import { 
  Search, ShoppingCart, Trash2, Plus, Minus, 
  CheckCircle2, Loader2, Smartphone, Clock, User, 
  CreditCard, Banknote, QrCode, ArrowLeft, Receipt, Calculator
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { formatCurrency } from "@/lib/utils";
import ProductModal from "@/components/menu/ProductModal";
import PaymentModal from "@/components/waiter/PaymentModal";
import BillAuditModal from "@/components/waiter/BillAuditModal";

export default function WaiterPosPage({ params }: { params: { slug: string, tableId: string } }) {
  const { slug, tableId } = params;
  const router = useRouter();
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [session, setSession] = useState<TableSession | null>(null);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  const [isAuditOpen, setIsAuditOpen] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      const [menuData, tableData] = await Promise.all([
        getMenu(slug),
        checkTableStatus(slug, parseInt(tableId), "staff-override")
      ]);
      
      setMenu(menuData);
      
      if (tableData.status === 'active' && tableData.session_token) {
        const sessionData = await getTableSession(slug, tableData.session_token);
        setSession(sessionData);
      } else {
        setSession(null);
      }
    } catch (e) {
      toast.error("Erro ao carregar dados da mesa");
    } finally {
      setLoading(false);
    }
  }, [slug, tableId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const addToCart = (product: Product, qty: number, notes: string, opts: Option[]) => {
    setCart(prev => [...prev, { product, quantity: qty, notes, selectedOptions: opts }]);
    setSelectedProduct(null);
  };

  const handleSendOrder = async () => {
    if (cart.length === 0) return;
    setSubmitting(true);
    try {
      const payload = {
        table_id: parseInt(tableId),
        qr_token: "staff-override",
        customer_name: session?.customer_name || "Cliente",
        order_type: "dine_in",
        items: cart.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(o => o.id)
        }))
      };
      await createOrder(slug, payload);
      setCart([]);
      toast.success("Pedido enviado!");
      fetchData();
    } catch (e) {
      toast.error("Erro ao enviar pedido");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Carregando mesa...</div>;

  const allProducts = menu?.categories.flatMap(c => c.products).filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-950 font-sans">
      <Toaster position="top-center" richColors />
      {/* HEADER MOBILE-OPTIMIZED */}
      <header className="bg-white dark:bg-gray-900 p-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <button onClick={() => router.back()} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full">
            <ArrowLeft size={24} />
          </button>
          <div>
            <h1 className="text-xl font-black text-gray-900 dark:text-white">Mesa {tableId}</h1>
            <p className="text-[10px] font-bold text-orange-600 uppercase tracking-widest">
              {session ? `Atendimento: ${session.customer_name}` : 'Mesa Livre'}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setIsAuditOpen(true)} className="p-3 bg-gray-100 dark:bg-gray-800 rounded-xl text-gray-600 dark:text-gray-400" title="Conferir Conta">
            <Receipt size={20} />
          </button>
          <button onClick={() => setIsPaymentOpen(true)} className="p-3 bg-orange-600 text-white rounded-xl shadow-lg shadow-orange-900/20" title="Fechar Conta">
            <Calculator size={20} />
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-hidden flex flex-col md:flex-row">
        {/* LISTA DE PRODUTOS */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="p-4 bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-800">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
              <input 
                type="text"
                placeholder="Buscar no cardápio..."
                className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-800 border-none rounded-xl text-sm outline-none focus:ring-2 focus:ring-orange-500/50"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 gap-3">
            {allProducts.map(product => (
              <button 
                key={product.id}
                onClick={() => setSelectedProduct(product)}
                className="bg-white dark:bg-gray-900 p-3 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm text-left active:scale-95 transition-all"
              >
                <h3 className="font-bold text-sm text-gray-900 dark:text-white line-clamp-2 mb-2">{product.name}</h3>
                <p className="text-orange-600 font-black text-sm">{formatCurrency(product.price)}</p>
              </button>
            ))}
          </div>
        </div>

        {/* CARRINHO LATERAL (DESKTOP) / BOTTOM SHEET (MOBILE) */}
        <div className="w-full md:w-80 bg-white dark:bg-gray-900 border-t md:border-t-0 md:border-l border-gray-200 dark:border-gray-800 flex flex-col shadow-2xl">
          <div className="p-4 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center">
            <span className="font-black text-xs uppercase tracking-widest text-gray-500">Itens a Lançar</span>
            <span className="bg-orange-100 text-orange-700 text-[10px] font-black px-2 py-0.5 rounded-full">{cart.length}</span>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {cart.map((item, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-50 dark:bg-gray-800/50 p-3 rounded-xl">
                <div className="flex-1">
                  <p className="text-sm font-bold text-gray-900 dark:text-white">{item.quantity}x {item.product.name}</p>
                  {item.selectedOptions.length > 0 && (
                    <p className="text-[10px] text-gray-500">+{item.selectedOptions.length} opcionais</p>
                  )}
                </div>
                <button onClick={() => setCart(prev => prev.filter((_, idx) => idx !== i))} className="text-gray-400 hover:text-red-500 p-2">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
          <div className="p-4 bg-gray-50 dark:bg-gray-800/30 border-t border-gray-100 dark:border-gray-800">
            <button 
              onClick={handleSendOrder}
              disabled={submitting || cart.length === 0}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white py-4 rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-orange-900/20 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {submitting ? <Loader2 className="animate-spin" /> : <CheckCircle2 size={18} />}
              Enviar para Cozinha
            </button>
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

      {session && (
        <>
          <PaymentModal 
            isOpen={isPaymentOpen}
            onClose={() => setIsPaymentOpen(false)}
            tableId={parseInt(tableId)}
            tableName={`Mesa ${tableId}`}
            totalAmount={Number(session.total_spent)}
            onSuccess={fetchData}
          />
          <BillAuditModal 
            isOpen={isAuditOpen}
            onClose={() => setIsAuditOpen(false)}
            sessionId={session.id}
            tableName={`Mesa ${tableId}`}
          />
        </>
      )}
    </div>
  );
}

