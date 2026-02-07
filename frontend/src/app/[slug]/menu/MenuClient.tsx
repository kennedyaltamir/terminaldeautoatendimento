/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 26.1.0 (API Sync Fix)
 * DNA_ID: MF-MENU-CLIENT-V26-1
 * Objective: Fix build error "Export getTableSession doesn't exist". 
 * Corrected import to getSessionDetails which handles session tokens.
 */
"use client";

import React, { useEffect, useState, useRef, useMemo, useCallback, use } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { 
  Loader2, ShoppingBag, ChevronDown, Lock, 
  ArrowLeft, Search, Sparkles, CheckCircle2, Plus 
} from "lucide-react";
import { 
  getMenu, 
  checkTableStatus, 
  getSessionDetails, // 🛡️ FIX: Replaced getTableSession
  joinTable,
  createOrder 
} from "@/lib/api";
import { MenuResponse, Product, Category, TableSession, Option, Order } from "@/types";
import { useCart } from "@/context/CartContext";
import { formatCurrency, cn } from "@/lib/utils";
import CategoryNav from "@/components/menu/CategoryNav";
import ProductCard from "@/components/menu/ProductCard";
import ProductModal from "@/components/menu/ProductModal";
import CartDrawer from "@/components/menu/CartDrawer";
import SearchBar from "@/components/menu/SearchBar"; 
import ComandaView from "@/components/menu/ComandaView";
import KioskHeader from "@/components/kiosk/KioskHeader";
import KioskCheckoutModal from "@/components/kiosk/KioskCheckoutModal";
import PixPaymentModal from "@/components/menu/PixPaymentModal";
import PinEntryModal from "@/components/menu/PinEntryModal";

// --- ANIMATION HELPERS ---
const FlyingItem = ({ start, end, onComplete }: { start: {x:number, y:number}, end: {x:number, y:number}, onComplete: () => void }) => (
  <motion.div
    initial={{ x: start.x, y: start.y, scale: 1, opacity: 1 }}
    animate={{ x: end.x, y: end.y, scale: 0.2, opacity: 0.5 }}
    transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    onAnimationComplete={onComplete}
    className="fixed z-[9999] w-12 h-12 bg-orange-500 rounded-full shadow-xl pointer-events-none flex items-center justify-center text-white"
  >
    <ShoppingBag size={20} />
  </motion.div>
);

export default function MenuClient({ slug }: { slug: string }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { addToCart, items, total, clearCart } = useCart();
  const cartBtnRef = useRef<HTMLDivElement>(null);
  
  const [menuData, setMenuData] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [sessionData, setSessionData] = useState<TableSession | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isComandaOpen, setIsComandaOpen] = useState(false);
  const [flyingItems, setFlyingItems] = useState<{id: number, start: {x:number, y:number}}[]>([]);
  const [isPinModalOpen, setIsPinModalOpen] = useState(false);
  const [blockedCustomerName, setBlockedCustomerName] = useState("");
  const [isKioskCheckoutOpen, setIsKioskCheckoutOpen] = useState(false);
  const [activeOrder, setActiveOrder] = useState<Order | null>(null);
  const [isPixModalOpen, setIsPixModalOpen] = useState(false);

  const tableId = searchParams.get("table");
  const qrToken = searchParams.get("token");
  const isKiosk = searchParams.get("kiosk") === "true";

  // 1. INITIAL LOAD & RESILIENT HANDSHAKE
  useEffect(() => {
    if (!slug || slug === "undefined") return;
    const init = async () => {
      try {
        const menu = await getMenu(slug);
        setMenuData(menu);
        if (menu.categories.length > 0) setActiveCategory(menu.categories[0].id);

        if (tableId) {
          const storageKey = `mesaflow_session_${slug}_${tableId}`;
          const storedToken = localStorage.getItem(storageKey);
          
          try {
            const statusData = await checkTableStatus(slug, parseInt(tableId), qrToken || undefined, storedToken);
            
            if (statusData.status === 'active' && statusData.session_token) {
              localStorage.setItem(storageKey, statusData.session_token);
              // 🛡️ FIX: Correct API call to getSessionDetails
              const session = await getSessionDetails(statusData.session_token);
              setSessionData(session);
            } 
            else if (statusData.status === 'blocked') {
              setBlockedCustomerName(statusData.customer_name || "Outro Cliente");
              setIsPinModalOpen(true);
            }
            else if (statusData.status === 'free') {
              const joinRes = await joinTable(slug, {
                table_id: parseInt(tableId),
                qr_token: qrToken || "staff-override",
                customer_name: "Cliente Mesa " + tableId
              });
              localStorage.setItem(storageKey, joinRes.session_token);
              setSessionData(joinRes);
            }
          } catch (err: any) {
            if (err.status === 403) {
              localStorage.removeItem(storageKey);
              if (qrToken) window.location.reload(); 
            } else {
              throw err;
            }
          }
        }
      } catch (error) {
        console.error("MesaFlow Boot Error:", error);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [slug, tableId, qrToken]);

  // 2. SCROLL SPY LOGIC
  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('section[id^="cat-"]');
      let currentId = activeCategory;

      sections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top >= 0 && rect.top <= 300) {
          currentId = parseInt(section.id.replace('cat-', ''));
        }
      });

      if (currentId !== activeCategory) setActiveCategory(currentId);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [activeCategory]);

  // 3. HANDLERS
  const handleAddToCart = useCallback((product: Product, quantity: number, notes: string, options: Option[]) => {
    addToCart(product, quantity, notes, options); 
    setSelectedProduct(null);
    
    const startX = typeof window !== 'undefined' ? window.innerWidth / 2 : 0;
    const startY = typeof window !== 'undefined' ? window.innerHeight / 2 : 0;
    setFlyingItems(prev => [...prev, { id: Date.now(), start: { x: startX, y: startY } }]);
  }, [addToCart]);

  const handlePinConfirm = async (pin: string) => {
    try {
      const joinRes = await joinTable(slug, {
        table_id: parseInt(tableId!),
        qr_token: qrToken!,
        customer_name: "Convidado",
        pin: pin
      });
      localStorage.setItem(`mesaflow_session_${slug}_${tableId}`, joinRes.session_token);
      setSessionData(joinRes);
      setIsPinModalOpen(false);
      toast.success("Acesso autorizado!");
    } catch (e) {
      throw new Error("PIN Inválido");
    }
  };

  const handleKioskCheckout = () => {
    setIsCartOpen(false);
    setIsKioskCheckoutOpen(true);
  };

  const handleConfirmOrder = async (data: any) => {
    setIsKioskCheckoutOpen(false);
    const toastId = toast.loading("Processando pedido...");
    try {
      const payload = {
        customer_name: data.customerName,
        customer_phone: data.customerPhone,
        pickup_note: data.pickupNote,
        payment_method: data.paymentMethod,
        order_type: "on_site",
        origin: "kiosk",
        items: items.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(o => o.id)
        }))
      };
      const order = await createOrder(slug, payload);
      setActiveOrder(order);
      toast.dismiss(toastId);
      if (data.paymentMethod === "pix" && order.mp_qr_code) {
        setIsPixModalOpen(true);
      } else {
        toast.success("Pedido realizado com sucesso!");
        clearCart();
        setTimeout(() => router.push(`/${slug}/kiosk`), 5000);
      }
    } catch (e) {
      toast.dismiss(toastId);
      toast.error("Falha ao criar pedido.");
    }
  };

  const filteredCategories = useMemo(() => {
    return menuData?.categories.map(cat => ({
      ...cat,
      products: cat.products.filter(p => 
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) && p.is_available
      )
    })).filter(cat => cat.products.length > 0) || [];
  }, [menuData, searchTerm]);

  const primaryColor = menuData?.company.primary_color || "#ea580c";
  const cartRect = cartBtnRef.current?.getBoundingClientRect() || { x: 0, y: 0 };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <Loader2 className="animate-spin text-orange-500" size={48} />
    </div>
  );

  if (!menuData) return null;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 pb-32 font-sans">
      {isKiosk ? (
        <KioskHeader 
          companyName={menuData.company.name} 
          primaryColor={primaryColor} 
          logoUrl={menuData.company.logo_url} 
        />
      ) : (
        <header className="sticky top-0 z-30 bg-white dark:bg-slate-900 shadow-sm border-b border-gray-100 dark:border-slate-800">
          <div className="px-4 py-3 flex justify-between items-center">
            <div className="flex items-center gap-3">
              {menuData.company.logo_url ? (
                <img src={menuData.company.logo_url} alt="Logo" className="w-10 h-10 rounded-lg object-cover" />
              ) : (
                <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center text-orange-600 font-bold">
                  {menuData.company.name.charAt(0)}
                </div>
              )}
              <div>
                <h1 className="font-bold text-gray-900 dark:text-white leading-tight">{menuData.company.name}</h1>
                {tableId && <p className="text-xs text-green-600 font-medium">Mesa {tableId}</p>}
              </div>
            </div>
            {sessionData && (
              <button 
                onClick={() => setIsComandaOpen(true)}
                className="text-xs font-bold bg-gray-100 dark:bg-slate-800 px-3 py-1.5 rounded-full text-gray-600 dark:text-gray-300"
              >
                Ver Comanda
              </button>
            )}
          </div>
          <div className="px-4 pb-3">
            <SearchBar value={searchTerm} onChange={setSearchTerm} primaryColor={primaryColor} />
          </div>
          <CategoryNav 
            categories={filteredCategories} 
            activeId={activeCategory} 
            onSelect={(id) => {
              setActiveCategory(id);
              document.getElementById(`cat-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
            primaryColor={primaryColor}
          />
        </header>
      )}

      <main className="p-4 space-y-12 max-w-7xl mx-auto">
        {filteredCategories.map(category => (
          <section key={category.id} id={`cat-${category.id}`} className="scroll-mt-48">
            <div className="flex items-center gap-4 mb-6">
              <h2 className="text-3xl font-black text-slate-900 dark:text-white uppercase tracking-tight">{category.name}</h2>
              <div className="h-1 flex-1 bg-slate-200 dark:bg-slate-800 rounded-full" />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {category.products.map(product => (
                <ProductCard 
                  key={product.id} 
                  product={product} 
                  onClick={() => setSelectedProduct(product)}
                  primaryColor={primaryColor}
                />
              ))}
            </div>
          </section>
        ))}
      </main>

      <AnimatePresence>
        {items.length > 0 && (
          <motion.div 
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="fixed bottom-6 left-4 right-4 z-40 md:left-auto md:right-6 md:w-96"
          >
            <div ref={cartBtnRef}>
              <button
                onClick={() => setIsCartOpen(true)}
                className="w-full text-white p-4 rounded-[2rem] shadow-2xl flex justify-between items-center hover:scale-[1.02] transition-transform active:scale-95 border-2 border-white/10"
                style={{ backgroundColor: primaryColor }}
                data-testid="cart-button"
              >
                <div className="flex items-center gap-4">
                  <div className="bg-white text-slate-900 w-12 h-12 rounded-full flex items-center justify-center font-black text-lg">
                    {items.reduce((acc, item) => acc + item.quantity, 0)}
                  </div>
                  <div className="text-left">
                    <p className="font-black text-sm uppercase tracking-widest opacity-80">Meu Pedido</p>
                    <p className="font-bold text-xs">Ver itens</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 bg-black/20 px-4 py-2 rounded-xl">
                  <span className="font-black text-xl">{formatCurrency(total)}</span>
                  <ChevronDown className="rotate-[-90deg]" />
                </div>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {flyingItems.map(item => (
        <FlyingItem 
          key={item.id} 
          start={item.start} 
          end={{ x: cartRect.x + 20, y: cartRect.y + 20 }} 
          onComplete={() => setFlyingItems(prev => prev.filter(i => i.id !== item.id))}
        />
      ))}

      <ProductModal 
        isOpen={!!selectedProduct} 
        onClose={() => setSelectedProduct(null)} 
        product={selectedProduct} 
        onAdd={handleAddToCart}
        primaryColor={primaryColor}
      />

      <CartDrawer 
        isOpen={isCartOpen} 
        onClose={() => setIsCartOpen(false)} 
        primaryColor={primaryColor}
        slug={slug}
        tableId={tableId ? parseInt(tableId) : undefined}
        sessionToken={sessionData?.session_token}
        onCheckout={isKiosk ? handleKioskCheckout : undefined}
      />

      <PinEntryModal 
        isOpen={isPinModalOpen}
        customerName={blockedCustomerName}
        onConfirm={handlePinConfirm}
        onCancel={() => router.push('/')}
      />

      <KioskCheckoutModal 
        isOpen={isKioskCheckoutOpen}
        onClose={() => setIsKioskCheckoutOpen(false)}
        onConfirm={handleConfirmOrder}
        primaryColor={primaryColor}
      />

      {activeOrder && (
        <PixPaymentModal 
          isOpen={isPixModalOpen}
          pixCode={activeOrder.mp_qr_code || ""}
          total={activeOrder.total_amount}
          orderId={activeOrder.id}
          slug={slug}
          onPaymentConfirmed={() => {
             setIsPixModalOpen(false);
             clearCart();
             toast.success("Pagamento confirmado!");
             setTimeout(() => router.push(`/${slug}/kiosk`), 5000);
          }}
        />
      )}

      {sessionData && isComandaOpen && (
        <ComandaView 
          session={sessionData} 
          onClose={() => setIsComandaOpen(false)} 
          primaryColor={primaryColor} 
        />
      )}
    </div>
  );
}
