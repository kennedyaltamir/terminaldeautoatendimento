"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMenu, createOrder, openTable, checkTableStatus, getTableSession, getDashboardMetrics, getWallet } from "@/lib/api";
import { MenuResponse, Product, Order, Category, Option } from "@/types";
import { useCart } from "@/context/CartContext";
import { Search, ShoppingBag, Plus, Trash2, ChevronLeft, ChefHat, User, X, Printer, Zap, Eye, CreditCard, ArrowRightLeft, Star, WifiOff, Wallet, Calculator } from "lucide-react";
import { toast, Toaster } from "sonner";
import { useTerminology } from "@/hooks/useTerminology";
import Receipt from "@/components/waiter/Receipt";
import BillAuditModal from "@/components/waiter/BillAuditModal";
import PaymentModal from "@/components/waiter/PaymentModal";
import TransferModal from "@/components/waiter/TransferModal";
import ProductModal from "@/components/menu/ProductModal";
import SuggestionToast from "@/components/waiter/SuggestionToast";
import SplitBillModal from "@/components/menu/SplitBillModal";
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
  const [customerPhone, setCustomerPhone] = useState("");
  const [walletData, setWalletData] = useState<{balance: number, loyalty_percentage: number} | null>(null);

  const [isTableOpen, setIsTableOpen] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [sessionOrders, setSessionOrders] = useState<Order[]>([]);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  const [topProducts, setTopProducts] = useState<Product[]>([]);

  const [isAuditOpen, setIsAuditOpen] = useState(false);
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  const [isTransferOpen, setIsTransferOpen] = useState(false);
  const [isSplitOpen, setIsSplitOpen] = useState(false);
  const [partialAmount, setPartialAmount] = useState<number | null>(null);

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [currentSuggestion, setCurrentSuggestion] = useState<Product | null>(null);

  const { items, addToCart, removeFromCart, clearCart, total } = useCart();

  const refreshSession = async () => {
    if (sessionId) {
        // Se já temos sessão, recarrega
        // Mas precisamos do token. Vamos pegar do checkTableStatus
        const status = await checkTableStatus(slug, parseInt(tableId), "admin-override");
        if (status.session_token) {
            const session = await getTableSession(slug, status.session_token);
            setSessionOrders(session.orders);
        }
    }
  };

  useEffect(() => {
    clearCart();
    Promise.all([
      getMenu(slug).catch(() => null),
      getDashboardMetrics().catch(() => ({ top_products: [] }))
    ]).then(([menuData, metricsData]) => {
      if (menuData) {
        setMenu(menuData);
        if (menuData.categories.length > 0) setActiveCategory(menuData.categories[0].id);
        const topNames = metricsData.top_products.map((p: { name: string }) => p.name);
        const tops = menuData.categories.flatMap((c: Category) => c.products).filter((p: Product) => topNames.includes(p.name)).slice(0, 5);
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
      }).catch(() => console.log("Offline: Não foi possível verificar status da mesa"));
  }, [slug, tableId]);

  const handlePhoneSearch = async (phone: string) => {
    setCustomerPhone(phone);
    if (phone.length >= 8) {
        try {
            const data = await getWallet(slug, phone);
            setWalletData(data);
            if (data.balance > 0) {
                toast.success(`Cliente Fidelidade: Saldo R$ ${data.balance.toFixed(2)}`);
            }
        } catch (e) {
            setWalletData(null);
        }
    } else {
        setWalletData(null);
    }
  };

  const handleOpenTable = async () => {
    if (!customerName) return toast.error("Informe o nome do cliente");
    try {
      await openTable(parseInt(tableId), customerName);
      setIsTableOpen(true);
    } catch (e) {
      toast.error("Erro ao abrir mesa (Verifique conexão)");
    }
  };

  const handleAddToCart = (product: Product, quantity: number, notes?: string, options?: Option[]) => {
    addToCart(product, quantity, notes, options);
    if (product.recommendations && product.recommendations.length > 0) {
      const suggestion = product.recommendations.find(rec => !items.some(item => item.product.id === rec.id));
      if (suggestion) setCurrentSuggestion(suggestion);
    }
  };

  const handleAddSuggestion = (product: Product) => {
    addToCart(product, 1);
    setCurrentSuggestion(null);
    toast.success(`${product.name} adicionado!`);
  };

  const handleSendOrder = async () => {
    if (items.length === 0) return;
    const payload = {
      table_id: parseInt(tableId),
      qr_token: "staff-override",
      order_type: "dine_in",
      customer_name: customerName || "Cliente",
      customer_phone: customerPhone,
      payment_method: "cash",
      items: items.map(i => ({ product_id: i.product.id, quantity: i.quantity, notes: i.notes, selected_options: i.selectedOptions.map(o => o.id) }))
    };

    try {
      if (navigator.onLine) {
        if (!isTableOpen) await openTable(parseInt(tableId), customerName || "Cliente");
        await createOrder(slug, payload);
        toast.success("Pedido enviado!");
      } else { throw new Error("Offline"); }
    } catch (e: any) {
      await db.pendingOrders.add({ slug: slug, payload: payload, createdAt: new Date(), status: 'pending', retryCount: 0 });
      toast.warning(<div className="flex flex-col"><span className="font-bold">Modo Offline Ativo</span><span className="text-xs">Pedido salvo no dispositivo.</span></div>, { icon: <WifiOff className="text-orange-500" /> });
    }
    clearCart();
    router.push(`/admin/${slug}/waiter`);
  };

  const handlePrintBill = () => {
    if (sessionOrders.length === 0) return toast.error("Nenhum pedido");
    const consolidatedOrder: any = { id: `MESA-${tableId}`, created_at: new Date().toISOString(), table: { table_number: parseInt(tableId) }, customer_name: customerName, order_type: 'dine_in', payment_method: 'A PAGAR', payment_status: 'pending', total_amount: sessionOrders.reduce((acc, o) => acc + Number(o.total_amount), 0), items: sessionOrders.flatMap(o => o.items) };
    setPrintingOrder(consolidatedOrder);
  };

  const handlePartialPayment = (amount: number) => {
    setPartialAmount(amount);
    setIsSplitOpen(false);
    setIsPaymentOpen(true);
  };

  const handlePaymentSuccess = () => {
    if (partialAmount) {
        // Se foi parcial, apenas recarrega a sessão
        setPartialAmount(null);
        refreshSession();
    } else {
        // Se foi total, sai da mesa
        router.push(`/admin/${slug}/waiter`);
    }
  };

  const filteredProducts = menu?.categories.find(c => c.id === activeCategory)?.products.filter(p => {
        const term = search.toLowerCase();
        return p.name.toLowerCase().includes(term) || (p.short_code && p.short_code.toLowerCase() === term);
    }) || [];

  // Calcula apenas o que falta pagar
  const sessionTotal = sessionOrders
    .filter(o => o.payment_status !== 'paid')
    .reduce((acc, o) => acc + Number(o.total_amount), 0);

  if (!menu) return <div className="p-10 text-center">Carregando...</div>;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Toaster position="top-center" richColors />
      <div className="bg-gray-900 text-white p-4 shadow-md shrink-0 flex items-center gap-4 print:hidden">
        <button onClick={() => router.back()} className="p-2 hover:bg-gray-800 rounded-full"><ChevronLeft /></button>
        <div className="flex-1"><h1 className="font-bold text-lg">{terms.table} {tableId}</h1>{isTableOpen ? <div className="flex items-center gap-2"><p className="text-xs text-gray-400">{customerName}</p><span className="bg-green-500 w-2 h-2 rounded-full animate-pulse"></span></div> : <p className="text-xs text-gray-400">Livre</p>}</div>
        <div className="flex gap-2">
            {isTableOpen && (
                <>
                    <button onClick={() => setIsTransferOpen(true)} className="bg-orange-600 p-2 rounded-full hover:bg-orange-500 text-white" title="Transferir Mesa"><ArrowRightLeft size={20} /></button>
                    <button onClick={() => setIsSplitOpen(true)} className="bg-blue-600 p-2 rounded-full hover:bg-blue-500 text-white" title="Dividir Conta"><Calculator size={20} /></button>
                    <button onClick={() => { setPartialAmount(null); setIsPaymentOpen(true); }} className="bg-green-600 p-2 rounded-full hover:bg-green-500 text-white shadow-lg" title="Fechar Conta"><CreditCard size={20} /></button>
                    <button onClick={() => setIsAuditOpen(true)} className="bg-gray-700 p-2 rounded-full hover:bg-gray-600 text-blue-400" title="Ver Comanda"><Eye size={20} /></button>
                    <button onClick={handlePrintBill} className="bg-gray-700 p-2 rounded-full hover:bg-gray-600" title="Imprimir Parcial"><Printer size={20} /></button>
                </>
            )}
        </div>
      </div>
      
      {!isTableOpen && (
        <div className="bg-orange-100 p-4 border-b border-orange-200 flex flex-col gap-3 print:hidden">
            <div className="flex gap-2 items-center">
                <User size={20} className="text-orange-600" />
                <input type="text" placeholder="Nome do Cliente" className="flex-1 bg-white border border-orange-300 rounded px-3 py-2 text-sm outline-none" value={customerName} onChange={e => setCustomerName(e.target.value)} />
            </div>
            <div className="flex gap-2 items-center">
                <Wallet size={20} className="text-orange-600" />
                <input type="tel" placeholder="Telefone (Busca Saldo)" className="flex-1 bg-white border border-orange-300 rounded px-3 py-2 text-sm outline-none" value={customerPhone} onChange={e => handlePhoneSearch(e.target.value)} />
            </div>
            {walletData && walletData.balance > 0 && (
                <div className="bg-green-100 text-green-800 text-xs p-2 rounded border border-green-200 flex justify-between items-center">
                    <span className="font-bold">Saldo Cashback: R$ {walletData.balance.toFixed(2)}</span>
                    <span className="bg-green-200 px-2 py-0.5 rounded-full text-[10px]">Fidelidade</span>
                </div>
            )}
            <button onClick={handleOpenTable} className="bg-orange-600 text-white px-4 py-2 rounded font-bold text-sm w-full">Abrir Mesa</button>
        </div>
      )}

      <div className="p-2 bg-white border-b border-gray-200 print:hidden"><div className="relative"><Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} /><input type="text" placeholder="Buscar por nome ou código..." className="w-full bg-gray-100 border-none rounded-lg pl-10 pr-4 py-3 text-sm outline-none" value={search} onChange={e => setSearch(e.target.value)} /></div></div>
      {topProducts.length > 0 && <div className="bg-gray-50 border-b border-gray-200 p-2 overflow-x-auto no-scrollbar shrink-0 print:hidden"><p className="text-[10px] font-bold text-gray-400 uppercase mb-1 px-1 flex items-center gap-1"><Star size={10}/> Mais Vendidos</p><div className="flex gap-2">{topProducts.map(p => (<button key={p.id} onClick={() => p.option_groups?.length > 0 ? setSelectedProduct(p) : handleAddToCart(p, 1)} className="bg-white border border-gray-200 rounded-lg p-2 min-w-[100px] flex items-center gap-2 shadow-sm active:scale-95 transition-transform"><div className="w-8 h-8 bg-gray-100 rounded-md shrink-0 overflow-hidden">{p.image_url && <img src={p.image_url} className="w-full h-full object-cover" />}</div><div className="text-left overflow-hidden"><p className="text-xs font-bold truncate">{p.name}</p><p className="text-[10px] text-orange-600 font-bold">R$ {Number(p.price).toFixed(2)}</p></div></button>))}</div></div>}
      <div className="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar shrink-0 print:hidden"><div className="flex p-2 gap-2"><button onClick={() => setActiveCategory(-1)} className={`whitespace-nowrap px-4 py-3 rounded-lg text-sm font-bold ${activeCategory === -1 ? 'bg-orange-600 text-white' : 'bg-orange-50 text-orange-700'}`}><Zap size={14} /> Rápidos</button>{menu.categories.map(cat => (<button key={cat.id} onClick={() => setActiveCategory(cat.id)} className={`whitespace-nowrap px-4 py-3 rounded-lg text-sm font-bold ${activeCategory === cat.id ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600'}`}>{cat.name}</button>))}</div></div>
      <div className="flex-1 overflow-y-auto p-2 grid grid-cols-2 gap-2 content-start print:hidden">{filteredProducts.map(product => (<button key={product.id} onClick={() => product.option_groups?.length > 0 ? setSelectedProduct(product) : handleAddToCart(product, 1)} className="bg-white p-3 rounded-xl border border-gray-200 shadow-sm text-left active:scale-95 transition-transform flex flex-col justify-between h-32 relative overflow-hidden">{product.short_code && <span className="absolute top-0 right-0 bg-gray-100 text-gray-500 text-[10px] px-2 py-0.5 rounded-bl-lg font-mono">#{product.short_code}</span>}<span className="font-bold text-gray-800 line-clamp-2 mt-2">{product.name}</span><div className="flex justify-between items-end mt-2"><span className="font-mono font-bold text-orange-600">R$ {Number(product.price).toFixed(2)}</span><div className="bg-gray-100 p-1.5 rounded-full text-gray-600"><Plus size={16} /></div></div></button>))}</div>
      <div className="bg-white border-t border-gray-200 p-4 safe-area-bottom shadow-[0_-4px_10px_rgba(0,0,0,0.1)] print:hidden"><div className="flex justify-between items-center mb-3"><span className="text-gray-500 font-medium">{items.length} itens</span><span className="text-2xl font-black text-gray-900">R$ {total.toFixed(2)}</span></div><div className="flex gap-3"><button onClick={() => setIsCartOpen(true)} className="flex-1 bg-gray-200 text-gray-800 py-3.5 rounded-xl font-bold flex items-center justify-center gap-2"><ShoppingBag size={20} /> Ver Pedido</button><button onClick={handleSendOrder} disabled={items.length === 0} className="flex-[2] bg-green-600 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-green-200"><ChefHat size={20} /> Enviar</button></div></div>
      {isCartOpen && (<div className="fixed inset-0 z-50 bg-black/50 flex justify-end print:hidden"><div className="w-full max-w-md bg-white h-full flex flex-col animate-in slide-in-from-right"><div className="p-4 border-b flex justify-between items-center bg-gray-50"><h2 className="font-bold text-lg">Resumo do Pedido</h2><button onClick={() => setIsCartOpen(false)}><X /></button></div><div className="flex-1 overflow-y-auto p-4 space-y-4">{items.map((item, idx) => (<div key={idx} className="flex justify-between items-center border-b pb-2"><div><p className="font-bold">{item.product.name}</p><p className="text-sm text-gray-500">R$ {Number(item.product.price).toFixed(2)}</p></div><div className="flex items-center gap-3"><span className="font-bold text-lg">x{item.quantity}</span><button onClick={() => removeFromCart(idx)} className="text-red-500 p-2"><Trash2 size={18}/></button></div></div>))}</div><div className="p-4 border-t"><button onClick={() => setIsCartOpen(false)} className="w-full bg-gray-900 text-white py-3 rounded-xl font-bold">Voltar</button></div></div></div>)}
      {printingOrder && <Receipt order={printingOrder} companyName={menu.company.name} />}
      
      {sessionId && (
        <>
            <BillAuditModal isOpen={isAuditOpen} onClose={() => setIsAuditOpen(false)} sessionId={sessionId} tableName={`${terms.table} ${tableId}`} />
            <PaymentModal 
                isOpen={isPaymentOpen} 
                onClose={() => setIsPaymentOpen(false)} 
                tableId={parseInt(tableId)} 
                tableName={`${terms.table} ${tableId}`} 
                totalAmount={partialAmount || sessionTotal} 
                onSuccess={handlePaymentSuccess}
                isPartial={!!partialAmount}
            />
            <TransferModal isOpen={isTransferOpen} onClose={() => setIsTransferOpen(false)} fromTableId={parseInt(tableId)} fromTableName={`${terms.table} ${tableId}`} slug={slug} onSuccess={() => router.push(`/admin/${slug}/waiter`)} />
            <SplitBillModal 
                isOpen={isSplitOpen} 
                onClose={() => setIsSplitOpen(false)} 
                orders={sessionOrders.filter(o => o.payment_status !== 'paid')} 
                totalAmount={sessionTotal} 
                primaryColor="#ea580c" 
                onPayPartial={handlePartialPayment} 
            />
        </>
      )}
      
      <ProductModal product={selectedProduct} isOpen={!!selectedProduct} onClose={() => setSelectedProduct(null)} onConfirm={(qty, notes, opts) => { if(selectedProduct) handleAddToCart(selectedProduct, qty, notes, opts); setSelectedProduct(null); }} primaryColor="#ea580c" />
      <SuggestionToast suggestion={currentSuggestion} onAdd={handleAddSuggestion} onClose={() => setCurrentSuggestion(null)} />
    </div>
  );
}
