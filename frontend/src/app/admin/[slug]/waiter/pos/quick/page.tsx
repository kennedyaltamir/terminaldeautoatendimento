"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getMenu, createOrder, getDashboardMetrics } from "@/lib/api";
import { MenuResponse, Product, Category } from "@/types";
import { useCart } from "@/context/CartContext";
import { Search, ShoppingBag, Plus, Trash2, ChevronLeft, ChefHat, User, X, MapPin, Phone, Star, Bike, Store, Loader2 } from "lucide-react";
import { toast, Toaster } from "sonner";
import ProductModal from "@/components/menu/ProductModal";

export default function QuickPOSPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const searchParams = useSearchParams();
  const mode = searchParams.get("mode") as "delivery" | "takeout" || "takeout";
  
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [activeCategory, setActiveCategory] = useState<number>(0);
  const [search, setSearch] = useState("");
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [topProducts, setTopProducts] = useState<Product[]>([]);
  
  // Form Data
  const [customerName, setCustomerName] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [deliveryAddress, setDeliveryAddress] = useState("");
  const [processing, setProcessing] = useState(false);

  // Modal Produto
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  
  const { items, addToCart, removeFromCart, clearCart, total } = useCart();

  useEffect(() => {
    clearCart();
    
    Promise.all([
      getMenu(slug),
      getDashboardMetrics()
    ]).then(([menuData, metricsData]) => {
      setMenu(menuData);
      if (menuData.categories.length > 0) setActiveCategory(menuData.categories[0].id);
      
      // Tipagem segura para evitar erros de 'any'
      const topNames = metricsData.top_products.map((p: { name: string }) => p.name);
      const tops = menuData.categories
        .flatMap((c: Category) => c.products)
        .filter((p: Product) => topNames.includes(p.name))
        .slice(0, 5);
      setTopProducts(tops);
    });
  }, [slug]);

  const handleSendOrder = async () => {
    if (items.length === 0) return toast.error("Carrinho vazio");
    
    if (mode === "delivery") {
        if (!customerName) return toast.error("Nome do cliente é obrigatório");
        if (!customerPhone) return toast.error("Telefone é obrigatório");
        if (!deliveryAddress) return toast.error("Endereço é obrigatório");
    }

    setProcessing(true);
    try {
      const payload = {
        table_id: null, // Sem mesa
        qr_token: "staff-override",
        order_type: mode,
        customer_name: customerName || (mode === 'takeout' ? "Balcão" : "Cliente"),
        customer_phone: customerPhone,
        delivery_address: deliveryAddress,
        payment_method: "cash", // Default, será ajustado no pagamento
        items: items.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          notes: i.notes,
          selected_options: i.selectedOptions.map(o => o.id)
        }))
      };
      
      await createOrder(slug, payload);
      toast.success(mode === 'delivery' ? "Delivery lançado!" : "Venda registrada!");
      clearCart();
      router.push(`/admin/${slug}/waiter/orders`); // Vai para lista de pedidos
    } catch (e: any) {
      toast.error("Erro ao enviar pedido: " + e.message);
    } finally {
      setProcessing(false);
    }
  };

  const filteredProducts = menu?.categories
    .find(c => c.id === activeCategory)
    ?.products.filter(p => {
        const term = search.toLowerCase();
        return p.name.toLowerCase().includes(term) || (p.short_code && p.short_code.toLowerCase() === term);
    }) || [];

  if (!menu) return <div className="p-10 text-center">Carregando...</div>;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Toaster position="top-center" richColors />
      
      {/* HEADER */}
      <div className={`p-4 shadow-md shrink-0 flex items-center gap-4 text-white ${mode === 'delivery' ? 'bg-blue-600' : 'bg-orange-600'}`}>
        <button onClick={() => router.back()} className="p-2 hover:bg-white/20 rounded-full"><ChevronLeft /></button>
        <div className="flex-1">
          <h1 className="font-bold text-lg flex items-center gap-2">
            {mode === 'delivery' ? <><Bike size={20}/> Novo Delivery</> : <><Store size={20}/> Venda Balcão</>}
          </h1>
          <p className="text-xs opacity-80">Lançamento Rápido</p>
        </div>
      </div>

      {/* DADOS DO CLIENTE */}
      <div className="bg-white p-4 border-b border-gray-200 space-y-3">
        <div className="flex gap-2">
            <div className="flex-1 relative">
                <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input 
                    type="text" 
                    placeholder="Nome do Cliente" 
                    className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-9 pr-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500" 
                    value={customerName} 
                    onChange={e => setCustomerName(e.target.value)} 
                />
            </div>
            {mode === 'delivery' && (
                <div className="flex-1 relative">
                    <Phone size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input 
                        type="tel" 
                        placeholder="Telefone" 
                        className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-9 pr-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500" 
                        value={customerPhone} 
                        onChange={e => setCustomerPhone(e.target.value)} 
                    />
                </div>
            )}
        </div>
        {mode === 'delivery' && (
            <div className="relative animate-in slide-in-from-top-2">
                <MapPin size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input 
                    type="text" 
                    placeholder="Endereço de Entrega" 
                    className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-9 pr-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500" 
                    value={deliveryAddress} 
                    onChange={e => setDeliveryAddress(e.target.value)} 
                />
            </div>
        )}
      </div>

      {/* BUSCA */}
      <div className="p-2 bg-white border-b border-gray-200">
        <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input type="text" placeholder="Buscar produto..." className="w-full bg-gray-100 border-none rounded-lg pl-10 pr-4 py-3 text-sm outline-none" value={search} onChange={e => setSearch(e.target.value)} />
        </div>
      </div>

      {/* ATALHOS RÁPIDOS */}
      {topProducts.length > 0 && (
        <div className="bg-gray-50 border-b border-gray-200 p-2 overflow-x-auto no-scrollbar shrink-0">
          <div className="flex gap-2">
            {topProducts.map(p => (
              <button 
                key={p.id} 
                onClick={() => p.option_groups.length > 0 ? setSelectedProduct(p) : addToCart(p, 1)}
                className="bg-white border border-gray-200 rounded-lg p-2 min-w-[100px] flex items-center gap-2 shadow-sm active:scale-95 transition-transform"
              >
                <div className="w-8 h-8 bg-gray-100 rounded-md shrink-0 overflow-hidden">
                  {p.image_url && <img src={p.image_url} className="w-full h-full object-cover" />}
                </div>
                <div className="text-left overflow-hidden">
                  <p className="text-xs font-bold truncate">{p.name}</p>
                  <p className="text-[10px] text-orange-600 font-bold">R$ {Number(p.price).toFixed(2)}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* CATEGORIAS */}
      <div className="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar shrink-0">
        <div className="flex p-2 gap-2">
          {menu.categories.map(cat => (
            <button key={cat.id} onClick={() => setActiveCategory(cat.id)} className={`whitespace-nowrap px-4 py-3 rounded-lg text-sm font-bold ${activeCategory === cat.id ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600'}`}>{cat.name}</button>
          ))}
        </div>
      </div>

      {/* GRID DE PRODUTOS */}
      <div className="flex-1 overflow-y-auto p-2 grid grid-cols-2 gap-2 content-start">
        {filteredProducts.map(product => (
          <button 
            key={product.id} 
            onClick={() => product.option_groups.length > 0 ? setSelectedProduct(product) : addToCart(product, 1)} 
            className="bg-white p-3 rounded-xl border border-gray-200 shadow-sm text-left active:scale-95 transition-transform flex flex-col justify-between h-32 relative overflow-hidden"
          >
            {product.short_code && <span className="absolute top-0 right-0 bg-gray-100 text-gray-500 text-[10px] px-2 py-0.5 rounded-bl-lg font-mono">#{product.short_code}</span>}
            <span className="font-bold text-gray-800 line-clamp-2 mt-2">{product.name}</span>
            <div className="flex justify-between items-end mt-2">
              <span className="font-mono font-bold text-orange-600">R$ {Number(product.price).toFixed(2)}</span>
              <div className="bg-gray-100 p-1.5 rounded-full text-gray-600"><Plus size={16} /></div>
            </div>
          </button>
        ))}
      </div>

      {/* FOOTER CARRINHO */}
      <div className="bg-white border-t border-gray-200 p-4 safe-area-bottom shadow-[0_-4px_10px_rgba(0,0,0,0.1)]">
        <div className="flex justify-between items-center mb-3">
          <span className="text-gray-500 font-medium">{items.length} itens</span>
          <span className="text-2xl font-black text-gray-900">R$ {total.toFixed(2)}</span>
        </div>
        <div className="flex gap-3">
          <button onClick={() => setIsCartOpen(true)} className="flex-1 bg-gray-200 text-gray-800 py-3.5 rounded-xl font-bold flex items-center justify-center gap-2"><ShoppingBag size={20} /> Ver</button>
          <button 
            onClick={handleSendOrder} 
            disabled={items.length === 0 || processing} 
            className={`flex-[2] text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg ${mode === 'delivery' ? 'bg-blue-600 shadow-blue-200' : 'bg-orange-600 shadow-orange-200'}`}
          >
            {processing ? <Loader2 className="animate-spin"/> : <ChefHat size={20} />} 
            {mode === 'delivery' ? 'Lançar Delivery' : 'Finalizar Venda'}
          </button>
        </div>
      </div>

      {/* MODAL CARRINHO */}
      {isCartOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 flex justify-end">
          <div className="w-full max-w-md bg-white h-full flex flex-col animate-in slide-in-from-right">
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
              <h2 className="font-bold text-lg">Resumo</h2>
              <button onClick={() => setIsCartOpen(false)}><X /></button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {items.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center border-b pb-2">
                  <div><p className="font-bold">{item.product.name}</p><p className="text-sm text-gray-500">R$ {Number(item.product.price).toFixed(2)}</p></div>
                  <div className="flex items-center gap-3"><span className="font-bold text-lg">x{item.quantity}</span><button onClick={() => removeFromCart(idx)} className="text-red-500 p-2"><Trash2 size={18}/></button></div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t"><button onClick={() => setIsCartOpen(false)} className="w-full bg-gray-900 text-white py-3 rounded-xl font-bold">Voltar</button></div>
          </div>
        </div>
      )}

      <ProductModal 
        product={selectedProduct} 
        isOpen={!!selectedProduct} 
        onClose={() => setSelectedProduct(null)} 
        onConfirm={(qty, notes, opts) => {
            if(selectedProduct) addToCart(selectedProduct, qty, notes, opts);
            setSelectedProduct(null);
        }} 
        primaryColor={mode === 'delivery' ? '#2563eb' : '#ea580c'}
      />
    </div>
  );
}