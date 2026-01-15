# DOMAIN: FRONTEND
# LAST_MODIFIED: 2026-01-15 02:50:00
"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { getMenu, createOrder, getOrder, requestService, getWallet, checkTableStatus, getTableSession, joinTable, validateCoupon } from "@/lib/api";
import { MenuResponse, Product, Option, Order, TableSession, Category } from "@/types";
import { CartProvider, useCart } from "@/context/CartContext";
import { Plus, X, AlertCircle, ShoppingBag, CreditCard, Banknote, QrCode, Phone, Bell, FileText, Edit2, Loader2, MapPin, Smartphone, ArrowUp, Tag, Check } from "lucide-react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { getSegmentLabels } from "@/lib/segment-utils";
import { generatePaymentIntent, detectSmartPOS, PaymentScheme } from "@/lib/smartpos";
import ProductModal from "@/components/menu/ProductModal";
import ServiceModal from "@/components/menu/ServiceModal";
import UpsellModal from "@/components/menu/UpsellModal";
import BlockedTableScreen from "@/components/menu/BlockedTableScreen";
import CheckInScreen from "@/components/menu/CheckInScreen";
import ComandaView from "@/components/menu/ComandaView";
import OrderStatusView from "@/components/menu/OrderStatusView";
import CategoryNav from "@/components/menu/CategoryNav";
import SearchBar from "@/components/menu/SearchBar";
import WalletWidget from "@/components/menu/WalletWidget";
import MenuSkeleton from "@/components/menu/MenuSkeleton";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

function MenuContent({ slug }: { slug: string }) {
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isServiceModalOpen, setIsServiceModalOpen] = useState(false);
  const [isComandaOpen, setIsComandaOpen] = useState(false);
  const [sessionStatus, setSessionStatus] = useState<'loading' | 'free' | 'active' | 'blocked'>('loading');
  const [sessionData, setSessionData] = useState<TableSession | null>(null);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [customerName, setCustomerName] = useState("");
  const [tableOwnerName, setTableOwnerName] = useState("");
  const [activeOrder, setActiveOrder] = useState<Order | null>(null);
  const [customerPhone, setCustomerPhone] = useState("");
  const [deliveryAddress, setDeliveryAddress] = useState("");
  const [paymentMethod, setPaymentMethod] = useState<"pix" | "card" | "cash" | "online">("online");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [processing, setProcessing] = useState(false);
  const [walletBalance, setWalletBalance] = useState(0);
  const [loyaltyPercent, setLoyaltyPercent] = useState(0);
  const [useBalance, setUseBalance] = useState(false);
  
  // Cupom State
  const [couponCode, setCouponCode] = useState("");
  const [couponDiscount, setCouponDiscount] = useState(0);
  const [couponMessage, setCouponMessage] = useState("");
  const [isValidatingCoupon, setIsValidatingCoupon] = useState(false);
  const [appliedCouponId, setAppliedCouponId] = useState<string | null>(null);

  const [isUpsellOpen, setIsUpsellOpen] = useState(false);
  const [pendingItem, setPendingItem] = useState<any>(null);
  const [currentRecommendations, setCurrentRecommendations] = useState<Product[]>([]);
  const [activeCategoryId, setActiveCategoryId] = useState<number>(0);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [editingCartIndex, setEditingCartIndex] = useState<number | null>(null);
  const [showBackToTop, setShowBackToTop] = useState(false);
  
  // SmartPOS
  const [smartPosType, setSmartPosType] = useState<PaymentScheme | null>(null);

  const searchParams = useSearchParams();
  const { items, addToCart, updateCartItem, removeFromCart, total, clearCart } = useCart();
  const tableId = searchParams.get("mesa");
  const qrToken = searchParams.get("token");
  const isKiosk = searchParams.get("kiosk") === "true";

  // Lógica de Tipo de Pedido
  const isDelivery = !tableId && !isKiosk;
  const isTakeout = isKiosk || (!tableId && !isDelivery);
  const labels = getSegmentLabels(menu?.company.segment);

  // Resetar cupom se o carrinho mudar (para revalidar regras de mínimo)
  useEffect(() => {
    if (appliedCouponId) {
      setCouponDiscount(0);
      setAppliedCouponId(null);
      setCouponMessage("Carrinho alterado. Valide o cupom novamente.");
    }
  }, [items, total]);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 400) {
        setShowBackToTop(true);
      } else {
        setShowBackToTop(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  useEffect(() => {
    const init = async () => {
      try {
        const menuData = await getMenu(slug);
        setMenu(menuData);
        if (menuData.categories.length > 0) {
            setActiveCategoryId(menuData.categories[0].id);
        }
        
        // Detecta SmartPOS
        setSmartPosType(detectSmartPOS());

        if (!isDelivery && !isTakeout && tableId && qrToken) {
          const storedToken = localStorage.getItem(`mesaflow_session_${tableId}`);
          const statusData = await checkTableStatus(slug, parseInt(tableId), qrToken, storedToken);
          
          if (statusData.status === 'blocked') {
            setSessionStatus('blocked');
            setTableOwnerName(statusData.customer_name || "Alguém");
          } else if (statusData.status === 'active') {
            setSessionStatus('active');
            setSessionToken(statusData.session_token || null);
            setCustomerName(statusData.customer_name || "");
            
            if (statusData.session_token) {
                localStorage.setItem(`mesaflow_session_${tableId}`, statusData.session_token);
                const session = await getTableSession(slug, statusData.session_token);
                setSessionData(session);
            }
          } else {
            setSessionStatus('free');
          }
        } else {
          setSessionStatus('free');
        }

        const savedOrderId = localStorage.getItem("mesaflow_active_order");
        if (savedOrderId) {
          try {
            const orderData = await getOrder(savedOrderId);
            if (orderData.status !== 'canceled') {
              setActiveOrder(orderData);
            } else {
              localStorage.removeItem("mesaflow_active_order");
            }
          } catch (e) {
            localStorage.removeItem("mesaflow_active_order");
          }
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [slug, tableId, qrToken, isDelivery, isTakeout]);

  useEffect(() => {
    if (loading || !menu) return;

    const handleIntersect = (entries: IntersectionObserverEntry[]) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = parseInt(entry.target.getAttribute("data-category-id") || "0");
          if (id) setActiveCategoryId(id);
        }
      });
    };

    observerRef.current = new IntersectionObserver(handleIntersect, {
      root: null,
      rootMargin: "-20% 0px -60% 0px",
      threshold: 0
    });

    menu.categories.forEach((cat) => {
      const el = document.getElementById(`category-${cat.id}`);
      if (el && observerRef.current) observerRef.current.observe(el);
    });

    return () => {
      if (observerRef.current) observerRef.current.disconnect();
    };
  }, [loading, menu]);

  const scrollToCategory = (id: number) => {
    setActiveCategoryId(id);
    const el = document.getElementById(`category-${id}`);
    if (el) {
      const headerOffset = 180;
      const elementPosition = el.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth"
      });
    }
  };

  const handleWebSocketMessage = useCallback((data: any) => {
    if (sessionToken && (data.type === "order_update" || data.type === "new_order")) {
      getTableSession(slug, sessionToken).then(setSessionData);
    }
    if (data.type === "order_update" && activeOrder && data.order_id === activeOrder.id) {
      setActiveOrder(prev => prev ? { ...prev, status: data.status, payment_status: data.payment_status } : null);
    }
  }, [sessionToken, activeOrder, slug]);

  useWebSocket(slug, handleWebSocketMessage);

  useEffect(() => {
    if (customerPhone.length >= 8) {
      const timer = setTimeout(() => {
        getWallet(slug, customerPhone).then(data => {
          setWalletBalance(data.balance);
          setLoyaltyPercent(data.loyalty_percentage);
        });
      }, 500);
      return () => clearTimeout(timer);
    } else {
      setWalletBalance(0);
    }
  }, [customerPhone, slug]);

  const handleAddToCart = (product: Product, quantity: number, notes: string = "", options: Option[] = []) => {
    if (product.recommendations && product.recommendations.length > 0) {
      setPendingItem({ product, quantity, notes, options });
      setCurrentRecommendations(product.recommendations);
      setIsUpsellOpen(true);
    } else {
      addToCart(product, quantity, notes, options);
    }
  };

  const handleEditCartItem = (index: number) => {
    const item = items[index];
    setEditingCartIndex(index);
    setSelectedProduct(item.product);
  };

  const handleProductModalConfirm = (qty: number, notes: string, opts: Option[]) => {
    if (editingCartIndex !== null && selectedProduct) {
      updateCartItem(editingCartIndex, {
        product: selectedProduct,
        quantity: qty,
        notes: notes,
        selectedOptions: opts
      });
      setEditingCartIndex(null);
    } else if (selectedProduct) {
      handleAddToCart(selectedProduct, qty, notes, opts);
    }
    setSelectedProduct(null);
  };

  const handleUpsellFinish = () => {
    if (pendingItem) {
      addToCart(pendingItem.product, pendingItem.quantity, pendingItem.notes, pendingItem.options);
      setPendingItem(null);
      setIsUpsellOpen(false);
    }
  };

  const handleAddRecommendation = (rec: Product) => {
    addToCart(rec, 1);
    toast.success(`${rec.name} adicionado!`);
  };

  const handleJoinTable = async (name: string, pin?: string) => {
    if (!tableId || !qrToken) return;
    try {
      const session = await joinTable(slug, parseInt(tableId), qrToken, name, pin);
      setSessionToken(session.session_token);
      setCustomerName(name);
      setSessionData(session);
      setSessionStatus('active');
      localStorage.setItem(`mesaflow_session_${tableId}`, session.session_token);
    } catch (e: any) {
      toast.error(e.message || "Erro ao entrar na mesa");
    }
  };

  const handleRecoverSession = async (token: string) => {
    setSessionToken(token);
    localStorage.setItem(`mesaflow_session_${tableId}`, token);
    setSessionStatus('active');
    const session = await getTableSession(slug, token);
    setSessionData(session);
    setCustomerName(session.customer_name);
  };

  const handleApplyCoupon = async () => {
    if (!couponCode) return;
    setIsValidatingCoupon(true);
    setCouponMessage("");
    try {
      const res = await validateCoupon(slug, couponCode, total);
      if (res.valid) {
        setCouponDiscount(res.discount_amount);
        setAppliedCouponId(res.promotion_id || null);
        setCouponMessage(`Desconto de R$ ${res.discount_amount.toFixed(2)} aplicado!`);
      } else {
        setCouponDiscount(0);
        setAppliedCouponId(null);
        setCouponMessage(res.message);
      }
    } catch (e: any) {
      setCouponDiscount(0);
      setAppliedCouponId(null);
      setCouponMessage(e.message || "Cupom inválido");
    } finally {
      setIsValidatingCoupon(false);
    }
  };

  const handleCheckout = async () => {
    if (!isDelivery && !isTakeout && (!tableId || !qrToken)) return toast.error("Erro: QR Code inválido.");
    if (sessionStatus === 'blocked') return toast.error("Mesa ocupada.");
    if (!customerName && !isKiosk) return toast.error("Por favor, informe seu nome.");

    setProcessing(true);
    try {
      const payload = {
        table_id: tableId ? parseInt(tableId) : null,
        qr_token: qrToken || (isKiosk ? "staff-override" : null),
        order_type: isDelivery ? "delivery" : (isTakeout ? "takeout" : "dine_in"),
        customer_name: customerName || (isKiosk ? "Totem" : "Cliente"),
        customer_phone: customerPhone,
        delivery_address: deliveryAddress,
        payment_method: paymentMethod,
        use_balance: useBalance,
        coupon_code: appliedCouponId ? couponCode : null,
        items: items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(o => o.id)
        })),
      };

      const order = await createOrder(slug, payload);

      if (smartPosType && paymentMethod === 'card') {
        const intentUrl = generatePaymentIntent({
          scheme: smartPosType,
          amount: total - couponDiscount,
          type: 'credit',
          orderId: order.id
        });
        window.location.href = intentUrl;
      }

      if (sessionStatus === 'free' && !isDelivery && !isTakeout) {
        const statusData = await checkTableStatus(slug, parseInt(tableId!), qrToken!, null);
        if (statusData.session_token) {
            setSessionToken(statusData.session_token);
            localStorage.setItem(`mesaflow_session_${tableId}`, statusData.session_token);
            setSessionStatus('active');
            const session = await getTableSession(slug, statusData.session_token);
            setSessionData(session);
        }
      } else if (sessionToken) {
          const session = await getTableSession(slug, sessionToken);
          setSessionData(session);
      }

      localStorage.setItem("mesaflow_active_order", order.id);
      setActiveOrder(order);
      clearCart();
      setCouponCode("");
      setCouponDiscount(0);
      setAppliedCouponId(null);
      setIsCartOpen(false);
      toast.success("Pedido enviado com sucesso!");
    } catch (error: any) {
      toast.error("Erro: " + error.message);
    } finally {
      setProcessing(false);
    }
  };

  const handleServiceRequest = async (type: string, notes: string) => {
    if (!tableId || !qrToken) return;
    try {
      await requestService(slug, {
        table_id: parseInt(tableId),
        qr_token: qrToken,
        service_type: type,
        notes: notes
      });
      toast.success("Solicitação enviada! Aguarde um instante.");
      setIsServiceModalOpen(false);
    } catch (e) {
      toast.error("Erro ao chamar garçom.");
    }
  };

  const handleNewOrder = () => {
    if (confirm("Deseja iniciar um novo pedido?")) {
      localStorage.removeItem("mesaflow_active_order");
      setActiveOrder(null);
    }
  };

  const getFilteredCategories = () => {
    if (!menu) return [];
    return menu.categories.map(cat => {
      const filteredProducts = cat.products.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                              (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesTag = activeTag ? p.tags?.includes(activeTag) : true; 
        return matchesSearch && matchesTag;
      });
      return { ...cat, products: filteredProducts };
    }).filter(cat => cat.products.length > 0);
  };

  const filteredCategories = getFilteredCategories();
  const allTags = Array.from(new Set(menu?.categories.flatMap(c => c.products.flatMap(p => p.tags || [])) || [])); 

  if (loading) return <MenuSkeleton />;

  if (sessionStatus === 'blocked') {
    return (
      <BlockedTableScreen 
        customerName={tableOwnerName} 
        tableId={tableId!} 
        slug={slug} 
        qrToken={qrToken!} 
        onSuccess={handleRecoverSession} 
      />
    );
  }

  if (!isDelivery && !isTakeout && sessionStatus === 'free') return <CheckInScreen tableId={tableId!} status="free" onJoin={handleJoinTable} segment={menu?.company.segment} />;

  if (!menu) return <div className="p-8 text-center">Restaurante não encontrado.</div>;

  const isClosed = (() => {
    if (!menu.company.opens_at || !menu.company.closes_at) return false;
    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes();
    const [openH, openM] = menu.company.opens_at.split(":").map(Number);
    const [closeH, closeM] = menu.company.closes_at.split(":").map(Number);
    const openTime = openH * 60 + openM;
    const closeTime = closeH * 60 + closeM;
    
    if (openTime < closeTime) return currentTime < openTime || currentTime > closeTime;
    return currentTime < openTime && currentTime > closeTime;
  })();

  const primaryColor = menu.company.primary_color || "#ea580c";
  const bgColor = menu.company.background_color || "#f9fafb";
  const textColor = menu.company.text_color || "#111827";

  if (activeOrder) {
    return <OrderStatusView order={activeOrder} onNewOrder={handleNewOrder} primaryColor={primaryColor} />;
  }

  const finalTotalDisplay = Math.max(0, total - couponDiscount);

  return (
    <div className="min-h-screen pb-24 font-sans transition-colors duration-300" style={{ backgroundColor: bgColor, color: textColor }}>
      <div className="sticky top-0 z-30 bg-white/95 backdrop-blur-sm shadow-sm">
        <header className="p-4 flex justify-between items-center border-b border-gray-100">
            <div className="flex items-center gap-2">
                {menu.company.logo_url && <img src={menu.company.logo_url} className="w-10 h-10 object-contain rounded-lg" alt="Logo" />}
                <h1 className="font-bold text-lg truncate max-w-[150px]" style={{ color: textColor }}>{menu.company.name}</h1>
            </div>
            <div className="flex items-center gap-3">
                {!isDelivery && !isTakeout && sessionStatus === 'active' && (
                    <button type="button" onClick={() => setIsComandaOpen(true)} className="text-xs font-bold bg-gray-100 px-3 py-1.5 rounded-full flex items-center gap-1 hover:bg-gray-200 transition-colors text-gray-800">
                    <FileText size={14} /> {labels.bill}
                    </button>
                )}
                {!isDelivery && !isTakeout && !isClosed && (
                    <button 
                    type="button"
                    onClick={() => setIsServiceModalOpen(true)}
                    className="p-2 rounded-full border transition-colors"
                    style={{ borderColor: primaryColor, color: primaryColor, backgroundColor: `${primaryColor}10` }}
                    >
                    <Bell size={18} />
                    </button>
                )}
            </div>
        </header>

        <div className="px-4 pt-4 pb-2">
            <SearchBar value={searchTerm} onChange={setSearchTerm} primaryColor={primaryColor} />
        </div>

        {allTags.length > 0 && (
            <div className="flex overflow-x-auto no-scrollbar px-4 pb-2 gap-2">
                <button 
                    type="button"
                    onClick={() => setActiveTag(null)}
                    className={`whitespace-nowrap px-3 py-1 rounded-full text-xs font-bold border transition-all ${!activeTag ? 'text-white' : 'bg-white text-gray-500 border-gray-200'}`}
                    style={{ backgroundColor: !activeTag ? primaryColor : undefined, borderColor: !activeTag ? primaryColor : undefined }}
                >
                    Todos
                </button>
                {allTags.map((tag: string) => (
                    <button 
                        key={tag}
                        type="button"
                        onClick={() => setActiveTag(activeTag === tag ? null : tag)}
                        className={`whitespace-nowrap px-3 py-1 rounded-full text-xs font-bold border transition-all capitalize ${activeTag === tag ? 'text-white border-transparent' : 'bg-white text-gray-500 border-gray-200'}`}
                        style={{ backgroundColor: activeTag === tag ? primaryColor : undefined }}
                    >
                        {tag}
                    </button>
                ))}
            </div>
        )}

        <div className="sticky top-[130px] z-20 bg-white/95 backdrop-blur-sm">
            <CategoryNav 
                categories={filteredCategories} 
                activeId={activeCategoryId} 
                onSelect={scrollToCategory} 
                primaryColor={primaryColor} 
            />
        </div>
      </div>

      {menu.company.banner_url && (
        <div className="w-full h-40 md:h-64 relative">
            <img src={menu.company.banner_url} className="w-full h-full object-cover" alt="Banner" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
        </div>
      )}

      {isClosed && (
        <div className="bg-red-100 border-b border-red-200 p-4 flex items-center gap-3 text-red-800">
          <AlertCircle size={20} />
          <p className="text-sm font-medium">Estamos fechados no momento. Pedidos desativados.</p>
        </div>
      )}

      <main className="p-4 space-y-8">
        {filteredCategories.length === 0 ? (
            <div className="text-center py-10 opacity-60">
                <p>Nenhum produto encontrado.</p>
            </div>
        ) : (
            filteredCategories.map((category: Category) => (
            <section 
                key={category.id} 
                id={`category-${category.id}`} 
                data-category-id={category.id}
                className="scroll-mt-48"
            >
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2" style={{ color: textColor }}>
                    <div className="w-1 h-6 rounded-full" style={{ backgroundColor: primaryColor }}></div>
                    {category.name}
                </h2>
                <div className="space-y-4">
                {category.products.map((product: Product) => {
                    const isOutOfStock = product.track_stock && product.stock_quantity <= 0;
                    return (
                    <div 
                        key={product.id} 
                        onClick={() => {
                            if (!isClosed && !isOutOfStock) {
                                product.option_groups.length > 0 ? setSelectedProduct(product) : handleAddToCart(product, 1);
                            }
                        }}
                        className={`bg-white p-4 rounded-xl shadow-sm flex justify-between items-center border border-gray-100 cursor-pointer active:scale-[0.98] transition-transform ${isOutOfStock ? 'opacity-60 grayscale' : ''}`}
                    >
                        <div className="flex-1 pr-4">
                        <h3 className="font-bold text-gray-900">{product.name}</h3>
                        <p className="text-sm text-gray-500 line-clamp-2 mt-1">{product.description}</p>
                        {product.tags?.length > 0 && (
                            <div className="flex gap-1 mt-2 flex-wrap">
                                {product.tags.map((tag: string) => (
                                    <span key={tag} className="text-[10px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded font-medium capitalize">{tag}</span>
                                ))}
                            </div>
                        )}
                        <div className="flex items-center gap-2 mt-2">
                            <p className="font-bold" style={{ color: primaryColor }}>R$ {Number(product.price).toFixed(2)}</p>
                            {isOutOfStock && <span className="text-[10px] bg-red-100 text-red-600 px-2 py-0.5 rounded font-bold uppercase">Esgotado</span>}
                        </div>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            {product.image_url && (
                                <img src={product.image_url} className="w-20 h-20 object-cover rounded-lg mb-2" alt={product.name} />
                            )}
                            <button
                            type="button"
                            disabled={isClosed || isOutOfStock}
                            onClick={(e) => {
                                e.stopPropagation();
                                if (!isClosed && !isOutOfStock) {
                                    product.option_groups.length > 0 ? setSelectedProduct(product) : handleAddToCart(product, 1);
                                }
                            }}
                            className={`text-white w-8 h-8 flex items-center justify-center rounded-full shadow-md ${isClosed || isOutOfStock ? 'bg-gray-300 cursor-not-allowed' : ''}`}
                            style={{ backgroundColor: (isClosed || isOutOfStock) ? undefined : primaryColor }}
                            >
                            <Plus size={18} />
                            </button>
                        </div>
                    </div>
                    );
                })}
                </div>
            </section>
            ))
        )}
      </main>

      {items.length > 0 && (
        <div className="fixed bottom-0 left-0 w-full bg-white border-t p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-20 safe-area-bottom">
          <div className="flex justify-between items-center max-w-md mx-auto">
            <div className="flex flex-col">
                <span className="text-xs text-gray-500 font-medium">Total do Pedido</span>
                <span className="font-black text-xl text-gray-900">R$ {total.toFixed(2)}</span>
            </div>
            <button type="button" onClick={() => setIsCartOpen(true)} className="text-white px-6 py-3 rounded-xl font-bold shadow-lg flex items-center gap-2 active:scale-95 transition-transform" style={{ backgroundColor: primaryColor }}>
              <ShoppingBag size={18} /> Ver Carrinho ({items.length})
            </button>
          </div>
        </div>
      )}

      {showBackToTop && (
        <button 
            type="button"
            onClick={scrollToTop}
            className="fixed bottom-24 right-4 bg-white p-3 rounded-full shadow-lg border border-gray-200 z-20 animate-in fade-in slide-in-from-bottom-4"
            style={{ color: primaryColor }}
        >
            <ArrowUp size={20} />
        </button>
      )}

      <ProductModal 
        product={selectedProduct} 
        isOpen={!!selectedProduct} 
        onClose={() => { setSelectedProduct(null); setEditingCartIndex(null); }} 
        onConfirm={handleProductModalConfirm} 
        primaryColor={primaryColor}
        initialValues={editingCartIndex !== null ? items[editingCartIndex] : null}
      />

      <ServiceModal 
        isOpen={isServiceModalOpen} 
        onClose={() => setIsServiceModalOpen(false)} 
        onConfirm={handleServiceRequest} 
        primaryColor={primaryColor}
        segment={menu?.company.segment}
      />

      <UpsellModal isOpen={isUpsellOpen} onClose={() => handleUpsellFinish()} recommendations={currentRecommendations} onAdd={handleAddRecommendation} onFinish={handleUpsellFinish} primaryColor={primaryColor} />

      {isComandaOpen && sessionData && (
        <ComandaView session={sessionData} onClose={() => setIsComandaOpen(false)} primaryColor={primaryColor} />
      )}

      {isCartOpen && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end sm:items-center justify-center p-4">
          <div className="bg-white w-full max-w-md p-6 rounded-xl max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
                <h2 className="text-xl font-bold text-gray-900">Seu Pedido</h2>
                <button type="button" onClick={() => setIsCartOpen(false)} className="text-gray-400"><X size={24}/></button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-4">
                {items.map((item, idx) => (
                <div key={idx} className="flex justify-between py-3 border-b last:border-0 group">
                    <div className="cursor-pointer flex-1" onClick={() => handleEditCartItem(idx)}>
                        <p className="font-medium flex items-center gap-2 text-gray-900">
                            {item.quantity}x {item.product.name}
                            <Edit2 size={12} className="text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </p>
                        {item.selectedOptions.length > 0 && <p className="text-xs text-gray-500">+ {item.selectedOptions.map(o => o.name).join(", ")}</p>}
                        {item.notes && <p className="text-xs text-orange-600 italic">Obs: {item.notes}</p>}
                    </div>
                    <div className="text-right">
                        <p className="text-sm font-bold text-gray-900">R$ {((Number(item.product.price) + item.selectedOptions.reduce((a,b)=>a+Number(b.price),0)) * item.quantity).toFixed(2)}</p>
                        <button type="button" onClick={() => removeFromCart(idx)} className="text-red-500 text-xs mt-1 hover:underline">Remover</button>
                    </div>
                </div>
                ))}
            </div>

            <div className="mt-6 space-y-4 bg-gray-50 p-4 rounded-xl">
              {!customerName && !isKiosk && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Seu Nome (Para a Comanda)</label>
                  <input type="text" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder="Ex: João" value={customerName} onChange={(e) => setCustomerName(e.target.value)} />
                </div>
              )}

              {isDelivery && (
                <div className="animate-in slide-in-from-top-2 space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-1"><Phone size={14}/> Telefone / WhatsApp</label>
                    <input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder="(00) 90000-0000" value={customerPhone} onChange={(e) => setCustomerPhone(e.target.value)} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-1"><MapPin size={14}/> Endereço de Entrega</label>
                    <textarea className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder="Rua, Número, Bairro, Complemento" rows={2} value={deliveryAddress} onChange={(e) => setDeliveryAddress(e.target.value)} />
                  </div>
                </div>
              )}

              {!isDelivery && !isKiosk && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-1"><Phone size={14}/> Telefone (Opcional)</label>
                  <input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder="Para ganhar cashback" value={customerPhone} onChange={(e) => setCustomerPhone(e.target.value)} />
                </div>
              )}

              {loyaltyPercent > 0 && (
                <WalletWidget 
                  balance={walletBalance} 
                  loyaltyPercent={loyaltyPercent} 
                  customerPhone={customerPhone} 
                  onUseBalance={setUseBalance} 
                  useBalance={useBalance} 
                />
              )}

              <div className="bg-white p-3 rounded-lg border border-gray-200">
                <label className="block text-xs font-bold text-gray-500 uppercase mb-2 flex items-center gap-1">
                  <Tag size={12} /> Cupom de Desconto
                </label>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm uppercase font-mono outline-none focus:ring-2 focus:ring-orange-500"
                    placeholder="CÓDIGO"
                    value={couponCode}
                    onChange={e => setCouponCode(e.target.value.toUpperCase())}
                    disabled={!!appliedCouponId}
                  />
                  {appliedCouponId ? (
                    <button 
                      type="button"
                      onClick={() => { setAppliedCouponId(null); setCouponDiscount(0); setCouponCode(""); setCouponMessage(""); }}
                      className="bg-red-100 text-red-600 px-3 py-2 rounded-lg hover:bg-red-200 transition-colors"
                    >
                      <X size={16} />
                    </button>
                  ) : (
                    <button 
                      type="button"
                      onClick={handleApplyCoupon}
                      disabled={!couponCode || isValidatingCoupon}
                      className="bg-gray-900 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-gray-800 transition-colors disabled:opacity-50"
                    >
                      {isValidatingCoupon ? <Loader2 className="animate-spin" size={14} /> : "Aplicar"}
                    </button>
                  )}
                </div>
                {couponMessage && (
                  <p className={`text-xs mt-2 font-medium ${appliedCouponId ? 'text-green-600 flex items-center gap-1' : 'text-red-500'}`}>
                    {appliedCouponId && <Check size={12} />} {couponMessage}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Forma de Pagamento</label>
                <div className="grid grid-cols-2 gap-2">
                    <button type="button" onClick={() => setPaymentMethod("online")} className={`flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === 'online' ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-200 bg-white text-gray-400'}`}>
                        <QrCode size={20} /> <span className="text-[10px] font-bold">PIX AUTOMÁTICO</span>
                    </button>
                    {smartPosType ? (
                      <button type="button" onClick={() => setPaymentMethod("card")} className={`flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === 'card' ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-gray-200 bg-white text-gray-400'}`}>
                          <Smartphone size={20} /> <span className="text-[10px] font-bold">MAQUININHA</span>
                      </button>
                    ) : (
                      <button type="button" onClick={() => setPaymentMethod("card")} className={`flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === 'card' ? 'border-orange-500 bg-orange-50 text-orange-600' : 'border-gray-200 bg-white text-gray-400'}`}>
                          <CreditCard size={20} /> <span className="text-[10px] font-bold">CARTÃO</span>
                      </button>
                    )}
                    <button type="button" onClick={() => setPaymentMethod("pix")} className={`flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === 'pix' ? 'border-orange-500 bg-orange-50 text-orange-600' : 'border-gray-200 bg-white text-gray-400'}`}>
                        <Banknote size={20} /> <span className="text-[10px] font-bold">PIX (BALCÃO)</span>
                    </button>
                    <button type="button" onClick={() => setPaymentMethod("cash")} className={`flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === 'cash' ? 'border-orange-500 bg-orange-50 text-orange-600' : 'border-gray-200 bg-white text-gray-400'}`}>
                        <Banknote size={20} /> <span className="text-[10px] font-bold">DINHEIRO</span>
                    </button>
                </div>
              </div>
            </div>

            <div className="mt-4 px-4">
              <div className="flex justify-between text-sm text-gray-500 mb-1">
                <span>Subtotal</span>
                <span>R$ {total.toFixed(2)}</span>
              </div>
              {couponDiscount > 0 && (
                <div className="flex justify-between text-sm text-green-600 font-bold mb-1">
                  <span>Desconto</span>
                  <span>- R$ {couponDiscount.toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between text-xl font-black text-gray-900 border-t pt-2">
                <span>Total</span>
                <span>R$ {finalTotalDisplay.toFixed(2)}</span>
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button type="button" onClick={() => setIsCartOpen(false)} className="flex-1 border border-gray-300 py-3 rounded-lg font-medium text-gray-700">Voltar</button>
              <button 
                type="button"
                onClick={handleCheckout} 
                disabled={processing}
                className="flex-1 text-white py-3 rounded-lg font-bold shadow-md flex items-center justify-center gap-2 disabled:opacity-70" 
                style={{ backgroundColor: primaryColor }}
              >
                {processing ? <Loader2 className="animate-spin" /> : (paymentMethod === 'online' ? 'Gerar Pix' : (smartPosType && paymentMethod === 'card' ? 'Pagar na Máquina' : 'Enviar Pedido'))}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function MenuClient({ slug }: { slug: string }) {
  return (
    <CartProvider>
      <MenuContent slug={slug} />
    </CartProvider>
  );
}
