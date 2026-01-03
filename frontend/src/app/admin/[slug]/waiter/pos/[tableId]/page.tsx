"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMenu, createOrder, openTable, checkTableStatus, getTableSession, getDashboardMetrics } from "@/lib/api";
import { MenuResponse, Product, Order, Category } from "@/types";
import { useCart } from "@/context/CartContext";
import { Search, ShoppingBag, Plus, Trash2, ChevronLeft, ChefHat, User, X, Printer, Zap, Eye, CreditCard, ArrowRightLeft, Star, WifiOff } from "lucide-react";
import { toast, Toaster } from "sonner";
import { useTerminology } from "@/hooks/useTerminology";
import Receipt from "@/components/waiter/Receipt";
import BillAuditModal from "@/components/waiter/BillAuditModal";
import PaymentModal from "@/components/waiter/PaymentModal";
import TransferModal from "@/components/waiter/TransferModal";
import ProductModal from "@/components/menu/ProductModal";
import { db } from "@/lib/db";

export default function WaiterPOSPage({ params }: { params: { slug: string, tableId: string } }) {
  const { slug, tableId } = params;
  const router = useRouter();
  const terms = useTerminology();
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [search, setSearch] = useState("");
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [customerName, setCustomerName] = useState("");
  const [isTableOpen, setIsTableOpen] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [sessionOrders, setSessionOrders] = useState<Order[]>([]);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  const [topProducts, setTopProducts] = useState<Product[]>([]);
  const [isAuditOpen, setIsAuditOpen] = useState(false);
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  const [isTransferOpen, setIsTransferOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const { items, addToCart, removeFromCart, clearCart, total } = useCart();

  useEffect(() => {
    clearCart();
    Promise.all([getMenu(slug).catch(() => null), getDashboardMetrics().catch(() => ({ top_products: [] }))]).then(([menuData, metricsData]) => {
      if (menuData) {
        setMenu(menuData);
        if (menuData.categories.length > 0) setActiveCategory(menuData.categories[0].id);
        const topNames = metricsData.top_products.map((p: any) => p.name);
        const tops = menuData.categories.flatMap((c: any) => c.products).filter((p: any) => topNames.includes(p.name)).slice(0, 5);
        setTopProducts(tops);
      }
    });
    checkTableStatus(slug, parseInt(tableId), "admin-override").then(async (status) => {
        if (status.status === 'active') {
          setIsTableOpen(true);
          setCustomerName(status.customer_name || "");
          if (status.session_token) {
            const session = await getTableSession(slug, status.session_token);
            setSessionId(session.id);
            setSessionOrders(session.orders);
          }
        }
      }).catch(() => console.log("Offline"));
  }, [slug, tableId]);

  const handleSendOrder = async () => {
    if (items.length === 0) return;
    const payload = { table_id: parseInt(tableId), qr_token: "staff-override", order_type: "dine_in", customer_name: customerName || "Cliente", payment_method: "cash", items: items.map(i => ({ product_id: i.product.id, quantity: i.quantity, notes: i.notes, selected_options: i.selectedOptions.map(o => o.id) })) };
    try {
      if (navigator.onLine) {
        if (!isTableOpen) await openTable(parseInt(tableId), customerName || "Cliente");
        await createOrder(slug, payload);
        toast.success("Enviado!");
      } else { throw new Error("Offline"); }
    } catch (e: any) {
      await db.pendingOrders.add({ slug: slug, payload: payload, createdAt: new Date(), status: 'pending', retryCount: 0 });
      toast.warning("Salvo Offline");
    }
    clearCart();
    router.push(`/admin/${slug}/waiter`);
  };

  if (!menu) return <div className="p-10 text-center">Carregando...</div>;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Toaster position="top-center" richColors />
      <div className="bg-gray-900 text-white p-4 flex items-center gap-4">
        <button onClick={() => router.back()}><ChevronLeft /></button>
        <h1 className="font-bold flex-1">{terms.table} {tableId}</h1>
        <div className="flex gap-2">
            {isTableOpen && <button onClick={() => setIsPaymentOpen(true)} className="bg-green-600 p-2 rounded-full"><CreditCard size={20} /></button>}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-2 grid grid-cols-2 gap-2">
        {menu.categories.find(c => c.id === activeCategory)?.products.map(p => (
          <button key={p.id} onClick={() => addToCart(p, 1)} className="bg-white p-3 rounded-xl border shadow-sm text-left">
            <span className="font-bold block">{p.name}</span>
            <span className="text-orange-600 font-bold">R$ {Number(p.price).toFixed(2)}</span>
          </button>
        ))}
      </div>
      <div className="p-4 bg-white border-t flex gap-3">
        <button onClick={handleSendOrder} className="w-full bg-green-600 text-white py-3 rounded-xl font-bold">Enviar Pedido (R$ {total.toFixed(2)})</button>
      </div>
    </div>
  );
}