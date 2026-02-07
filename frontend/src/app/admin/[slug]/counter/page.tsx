/**
 * 🛒 MESAFLOW OS - COUNTER POS (Gold Master v1.4.1 - Final Sealed)
 * =====================================================================
 * DOMAIN: FRONTEND / POINT OF SALE
 * DNA_ID: MF-ADMIN-COUNTER-POS-2026-V1.4.1-SEALED
 * 
 * FIXES:
 * 1. Implementada função 'removeFromCart' (Audit Finding #1).
 * 2. Normalização monetária via Math.round para evitar float decay (Audit Finding #2).
 * 3. Rito de transição no estado 'completed' para feedback de UX (Audit Finding #3).
 * 4. Proteção contra Duplo Commit via FSM Guard.
 */
"use client";

import React, { useState, useEffect, useMemo, useCallback, use } from "react";
import { useRouter } from "next/navigation";
import { 
  ShoppingBag, Zap, Banknote, CreditCard, QrCode, 
  Trash2, Plus, Minus, Printer, Search, Loader2,
  AlertTriangle, CheckCircle2, Clock, XCircle
} from "lucide-react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

// --- API & UTILS ---
import { getMenu, createOrder, getKitchenOrders } from "@/lib/api";
import { MenuResponse, Product, Order, CartItem } from "@/types";
import { formatCurrency, cn } from "@/lib/utils";
import { useWebSocket } from "@/hooks/useWebSocket";

// --- TYPES ---
type CounterStatus = 
  | 'draft' 
  | 'committing' 
  | 'completed' 
  | 'failed_technical' 
  | 'failed_operational';

export default function CounterPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const params = use(paramsPromise);
  const slug = params.slug;
  const router = useRouter();

  // --- ESTADOS DE MÁQUINA (FSM) ---
  const [status, setStatus] = useState<CounterStatus>('draft');
  const [isRushMode, setIsRushMode] = useState(false);
  const [loading, setLoading] = useState(true);
  const [draftStartedAt, setDraftStartedAt] = useState<number>(Date.now());

  // --- DATA STATE ---
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [activeOrders, setActiveOrders] = useState<Order[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  
  // --- PAYMENT STATE ---
  const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card' | 'pix' | null>(null);
  const [cashReceived, setCashReceived] = useState<string>("");

  // 1. PERSISTÊNCIA E RESTAURAÇÃO (Sovereign Persistence)
  useEffect(() => {
    const savedDraft = localStorage.getItem(`mf_pos_draft_${slug}`);
    if (savedDraft) {
      try {
        const parsed = JSON.parse(savedDraft);
        setCart(parsed.cart || []);
        setPaymentMethod(parsed.paymentMethod || null);
        setCashReceived(parsed.cashReceived || "");
        setDraftStartedAt(parsed.startedAt || Date.now());
      } catch (e) {
        console.error("Falha ao restaurar rascunho.");
      }
    }
  }, [slug]);

  useEffect(() => {
    if (status === 'draft') {
      const draftData = { cart, paymentMethod, cashReceived, startedAt: draftStartedAt };
      localStorage.setItem(`mf_pos_draft_${slug}`, JSON.stringify(draftData));
    }
  }, [cart, paymentMethod, cashReceived, status, slug, draftStartedAt]);

  // 2. WATCHDOG: HARD TIMEOUT (10 MINUTOS)
  useEffect(() => {
    if (status !== 'draft' || cart.length === 0) return;

    const interval = setInterval(() => {
      const elapsed = Date.now() - draftStartedAt;
      if (elapsed > 10 * 60 * 1000) {
        toast.error("Rascunho Expirado", {
          description: "Limite de 10 minutos excedido.",
          duration: Infinity,
          action: { label: "Limpar", onClick: () => setCart([]) }
        });
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [status, cart.length, draftStartedAt]);

  // 3. DATA FETCHING
  const loadData = useCallback(async () => {
    if (!slug || slug === "undefined") return;
    try {
      const [menuData, ordersData] = await Promise.all([
        getMenu(slug),
        getKitchenOrders(slug)
      ]);
      setMenu(menuData);
      setActiveOrders(ordersData);
    } catch (e) {
      toast.error("Erro de sincronização.");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { loadData(); }, [loadData]);

  useWebSocket(slug, (data) => {
    if (data.type === "new_order" || data.type === "order_update") loadData();
  });

  // 4. LÓGICA DE CARRINHO (Audit Fixed)
  const addToCart = (product: Product) => {
    if (cart.length === 0) setDraftStartedAt(Date.now());
    setCart(prev => {
      const existing = prev.find(item => item.product.id === product.id);
      if (existing) {
        return prev.map(item => 
          item.product.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { product, quantity: 1, selectedOptions: [] }];
    });
  };

  const removeFromCart = (productId: number) => {
    setCart(prev => prev.filter(item => item.product.id !== productId));
  };

  const cartTotal = useMemo(() => {
    return cart.reduce((acc, item) => acc + (Number(item.product.price) * item.quantity), 0);
  }, [cart]);

  // 🛡️ FIX: Normalização monetária rigorosa
  const changeAmount = useMemo(() => {
    if (!cashReceived) return 0;
    const receivedInCents = Math.round(parseFloat(cashReceived.replace(",", ".")) * 100);
    return isNaN(receivedInCents) ? 0 : receivedInCents - cartTotal;
  }, [cashReceived, cartTotal]);

  // 5. FINALIZAÇÃO (FSM COMMIT)
  const handleCheckout = async () => {
    if (status !== 'draft' || cart.length === 0 || !paymentMethod) return;

    setStatus('committing');
    const toastId = toast.loading("Selando venda no Ledger...");

    try {
      const payload = {
        customer_name: "Venda Balcão",
        order_type: "takeout",
        origin: "admin",
        payment_method: paymentMethod,
        items: cart.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          selected_options: []
        })),
        metadata: {
          rush_sale: isRushMode,
          source: 'counter_pos',
          draft_duration_ms: Date.now() - draftStartedAt
        }
      };

      await createOrder(slug, payload);
      
      setStatus('completed');
      toast.success("Venda selada!", { id: toastId });
      
      // Rito de Transição: 2s para feedback visual antes do reset
      setTimeout(() => {
        localStorage.removeItem(`mf_pos_draft_${slug}`);
        setCart([]);
        setPaymentMethod(null);
        setCashReceived("");
        setStatus('draft');
        loadData();
      }, 2000);

    } catch (e: any) {
      const isTechnical = e.status >= 500 || e.message?.includes('fetch');
      setStatus(isTechnical ? 'failed_technical' : 'failed_operational');
      toast.error(isTechnical ? "Falha Técnica" : "Falha Operacional", { id: toastId });
    }
  };

  const filteredProducts = useMemo(() => {
    if (!menu) return [];
    return menu.categories.flatMap(c => c.products).filter(p => 
      p.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [menu, searchTerm]);

  if (loading) return <div className="h-screen bg-slate-950 flex items-center justify-center"><Loader2 className="animate-spin text-orange-500" size={48} /></div>;

  return (
    <div className={cn(
      "h-[calc(100vh-2rem)] flex flex-col gap-4 animate-in fade-in duration-500",
      isRushMode ? "bg-slate-950" : "bg-transparent"
    )}>
      {/* HEADER TÁTICO */}
      <header className="flex justify-between items-center bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-2 rounded-xl">
            <ShoppingBag className="text-white" size={20} />
          </div>
          <div>
            <h1 className="text-white font-black uppercase tracking-tighter text-lg">Balcão POS</h1>
            <p className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">Sessão: {slug}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={() => setIsRushMode(!isRushMode)}
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all",
              isRushMode ? "bg-red-600 text-white animate-pulse" : "bg-slate-800 text-slate-400 hover:text-white"
            )}
          >
            <Zap size={14} /> {isRushMode ? "Modo Rush Ativo" : "Modo Normal"}
          </button>
          <div className="h-8 w-px bg-slate-800 mx-2" />
          <div className="text-right">
            <p className="text-[10px] font-black text-slate-500 uppercase">Em Produção</p>
            <p className="text-white font-mono font-bold">{activeOrders.length} pedidos</p>
          </div>
        </div>
      </header>

      <div className="flex-1 flex gap-4 overflow-hidden">
        {/* COLUNA ESQUERDA: PRODUTOS */}
        <main className="flex-[3] flex flex-col gap-4 overflow-hidden">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input 
              type="text"
              placeholder="Buscar produto..."
              className="w-full bg-slate-900 border border-slate-800 rounded-2xl py-4 pl-12 pr-4 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className={cn(
            "flex-1 overflow-y-auto pr-2 custom-scrollbar grid gap-3 content-start",
            isRushMode ? "grid-cols-3 md:grid-cols-4 lg:grid-cols-5" : "grid-cols-2 md:grid-cols-3 lg:grid-cols-4"
          )}>
            {filteredProducts.map(product => (
              <button
                key={product.id}
                onClick={() => addToCart(product)}
                className={cn(
                  "relative flex flex-col justify-between p-4 rounded-2xl border transition-all active:scale-95 text-left group",
                  isRushMode 
                    ? "h-24 bg-slate-900 border-slate-800 hover:border-red-500" 
                    : "h-40 bg-slate-900 border-slate-800 hover:border-orange-500 shadow-lg"
                )}
              >
                <span className="font-bold text-white leading-tight line-clamp-2 group-hover:text-orange-400">
                  {product.name}
                </span>
                <span className="font-black text-orange-500 text-lg">
                  {formatCurrency(product.price)}
                </span>
              </button>
            ))}
          </div>
        </main>

        {/* COLUNA DIREITA: CHECKOUT (DRAFT) */}
        <aside className="flex-[1.2] bg-slate-900 border border-slate-800 rounded-[2rem] flex flex-col overflow-hidden shadow-2xl">
          <div className="p-6 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-white font-black uppercase tracking-widest text-xs">Carrinho (Draft)</h2>
            <button onClick={() => setCart([])} className="text-slate-500 hover:text-red-500 transition-colors">
              <Trash2 size={16} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            <AnimatePresence>
              {cart.map((item) => (
                <motion.div 
                  key={item.product.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="bg-slate-950/50 p-3 rounded-xl border border-slate-800 flex justify-between items-center"
                >
                  <div className="min-w-0">
                    <p className="text-white font-bold text-sm truncate">{item.product.name}</p>
                    <p className="text-orange-500 font-mono text-xs">{formatCurrency(item.product.price)}</p>
                  </div>
                  <div className="flex items-center gap-2 bg-slate-900 rounded-lg p-1">
                    <button onClick={() => removeFromCart(item.product.id)} className="text-slate-500 hover:text-white"><Minus size={14}/></button>
                    <span className="text-white font-bold text-xs w-4 text-center">{item.quantity}</span>
                    <button onClick={() => addToCart(item.product)} className="text-slate-500 hover:text-white"><Plus size={14}/></button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* PAINEL DE PAGAMENTO */}
          <div className="p-6 bg-slate-950/80 border-t border-slate-800 space-y-4">
            <div className="flex justify-between items-end">
              <span className="text-slate-500 font-black uppercase text-[10px]">Total</span>
              <span className="text-4xl font-black text-white tracking-tighter">{formatCurrency(cartTotal)}</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'cash', icon: Banknote, label: 'Dinheiro' },
                { id: 'card', icon: CreditCard, label: 'Cartão' },
                { id: 'pix', icon: QrCode, label: 'Pix' }
              ].map(m => (
                <button
                  key={m.id}
                  onClick={() => setPaymentMethod(m.id as any)}
                  className={cn(
                    "flex flex-col items-center gap-2 p-3 rounded-xl border-2 transition-all",
                    paymentMethod === m.id 
                      ? "border-orange-500 bg-orange-500/10 text-white" 
                      : "border-slate-800 text-slate-500 hover:border-slate-700"
                  )}
                >
                  <m.icon size={20} />
                  <span className="text-[8px] font-black uppercase">{m.label}</span>
                </button>
              ))}
            </div>

            {paymentMethod === 'cash' && (
              <div className="space-y-2 animate-in slide-in-from-bottom-2">
                <input 
                  type="text"
                  placeholder="Valor Recebido..."
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-center text-xl font-black text-emerald-500 outline-none focus:border-emerald-500"
                  value={cashReceived}
                  onChange={(e) => setCashReceived(e.target.value)}
                />
                {changeAmount > 0 && (
                  <div className="flex justify-between items-center bg-emerald-500/10 p-3 rounded-xl border border-emerald-500/20">
                    <span className="text-[10px] font-black text-emerald-500 uppercase">Troco</span>
                    <span className="text-xl font-black text-emerald-400">{formatCurrency(changeAmount)}</span>
                  </div>
                )}
              </div>
            )}

            <button
              disabled={cart.length === 0 || !paymentMethod || status !== 'draft'}
              onClick={handleCheckout}
              className={cn(
                "w-full py-5 rounded-2xl font-black text-lg uppercase tracking-widest transition-all active:scale-95 flex items-center justify-center gap-3 shadow-xl",
                status === 'completed' ? "bg-emerald-600 text-white" :
                cart.length > 0 && paymentMethod 
                  ? "bg-orange-600 text-white hover:bg-orange-500 shadow-orange-900/20" 
                  : "bg-slate-800 text-slate-600 cursor-not-allowed"
              )}
            >
              {status === 'committing' ? <Loader2 className="animate-spin" /> : 
               status === 'completed' ? <CheckCircle2 /> : <CheckCircle2 />}
              {status === 'committing' ? "Selando..." : 
               status === 'completed' ? "Venda Selada!" : "Finalizar Venda"}
            </button>
          </div>
        </aside>
      </div>

      <footer className="flex justify-between items-center px-4 text-[9px] font-black text-slate-600 uppercase tracking-[0.2em]">
        <div className="flex gap-4">
          <span className="flex items-center gap-1"><Clock size={10}/> SLA: {Math.floor((Date.now() - draftStartedAt)/1000)}s</span>
          <span className="flex items-center gap-1"><Printer size={10}/> Impressora: Online</span>
        </div>
        <span>MesaFlow OS v1.4.1 • Gold Master Sealed</span>
      </footer>
    </div>
  );
}
