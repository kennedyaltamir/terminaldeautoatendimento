// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 15:25:00
"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useCart } from "@/context/CartContext";
import { createOrder } from "@/lib/api"; 
import KioskHeader from "@/components/kiosk/KioskHeader"; // Import corrigido
import { 
  ShoppingBag, 
  Trash2, 
  CreditCard, 
  Banknote, 
  QrCode, 
  User, 
  Loader2, 
  CheckCircle2, 
  ArrowLeft 
} from "lucide-react";
import { toast } from "sonner";
import { motion } from "framer-motion";

export default function CheckoutClient({ slug }: { slug: string }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isKiosk = searchParams.get("kiosk") === "true";
  
  const { items, total, removeFromCart, clearCart } = useCart();
  
  const [step, setStep] = useState<"review" | "payment" | "success">("review");
  const [customerName, setCustomerName] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("pix");
  const [loading, setLoading] = useState(false);
  
  const companyColor = "#ea580c"; 
  const companyName = "Hamburgueria Zé";

  useEffect(() => {
    if (items.length === 0 && step !== "success") {
      router.replace(`/${slug}/menu${isKiosk ? '?kiosk=true' : ''}`);
    }
  }, [items, router, slug, isKiosk, step]);

  const handleFinish = async () => {
    if (!customerName.trim()) {
      toast.error("Por favor, digite seu nome para retirada.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        customer_name: customerName,
        payment_method: paymentMethod,
        order_type: "takeout", 
        items: items.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          notes: item.notes,
          selected_options: item.selectedOptions.map(opt => opt.id)
        }))
      };

      await createOrder(slug, payload);
      setStep("success");
      clearCart();
      
      if (isKiosk) {
        setTimeout(() => {
          router.push(`/${slug}/kiosk`);
        }, 5000);
      }
    } catch (e: any) {
      toast.error(e.message || "Erro ao enviar pedido.");
    } finally {
      setLoading(false);
    }
  };

  const containerClass = isKiosk ? "bg-slate-950 text-white" : "bg-gray-50 text-gray-900";
  const cardClass = isKiosk ? "bg-slate-900 border-slate-800" : "bg-white border-gray-200 shadow-sm";

  if (step === "success") {
    return (
      <div className={`${containerClass} min-h-screen flex flex-col items-center justify-center p-8 text-center`}>
        <motion.div 
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-32 h-32 bg-green-500 rounded-full flex items-center justify-center mb-8 shadow-[0_0_50px_rgba(34,197,94,0.4)]"
        >
          <CheckCircle2 size={64} className="text-white" />
        </motion.div>
        <h1 className="text-4xl font-black mb-4">Pedido Confirmado!</h1>
        <p className="text-xl opacity-70 mb-8">
          Aguarde a chamada pelo nome: <span className="font-bold text-orange-500">{customerName}</span>
        </p>
        {!isKiosk && (
          <button 
            onClick={() => router.push(`/${slug}/menu`)}
            className="bg-orange-600 text-white px-8 py-4 rounded-xl font-bold"
          >
            Voltar ao Cardápio
          </button>
        )}
        {isKiosk && <p className="text-sm opacity-50 animate-pulse">Retornando à tela inicial em instantes...</p>}
      </div>
    );
  }

  return (
    <div className={`${containerClass} min-h-screen pb-32`}>
      {isKiosk ? (
        <KioskHeader companyName={companyName} primaryColor={companyColor} />
      ) : (
        <header className="p-4 bg-white border-b sticky top-0 z-40 flex items-center gap-4">
          <button onClick={() => router.back()}><ArrowLeft /></button>
          <h1 className="font-bold">Finalizar Pedido</h1>
        </header>
      )}

      <main className="max-w-3xl mx-auto p-4 md:p-8 space-y-6">
        <section className={`p-6 rounded-[2rem] border ${cardClass}`}>
          <h2 className="text-xl font-black mb-6 flex items-center gap-2">
            <ShoppingBag className="text-orange-500" /> Resumo
          </h2>
          <div className="space-y-4">
            {items.map((item, idx) => (
              <div key={idx} className="flex justify-between items-start border-b border-white/10 pb-4 last:border-0">
                <div className="flex gap-4">
                  <div className="bg-orange-500/20 text-orange-500 w-8 h-8 rounded-lg flex items-center justify-center font-bold">
                    {item.quantity}x
                  </div>
                  <div>
                    <p className="font-bold text-lg">{item.product.name}</p>
                    <p className="text-sm opacity-60">
                      {item.selectedOptions.map(o => o.name).join(", ")}
                    </p>
                    {item.notes && <p className="text-xs text-yellow-500 mt-1">Obs: {item.notes}</p>}
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span className="font-bold">
                    R$ {((Number(item.product.price) + item.selectedOptions.reduce((a,b)=>a+Number(b.price),0)) * item.quantity / 100).toFixed(2)}
                  </span>
                  <button 
                    onClick={() => removeFromCart(idx)}
                    className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 pt-6 border-t border-white/10 flex justify-between items-end">
            <span className="opacity-60 font-bold uppercase tracking-widest text-sm">Total a Pagar</span>
            <span className="text-4xl font-black text-orange-500">R$ {(total / 100).toFixed(2)}</span>
          </div>
        </section>

        <section className={`p-6 rounded-[2rem] border ${cardClass}`}>
          <h2 className="text-xl font-black mb-6 flex items-center gap-2">
            <User className="text-blue-500" /> Identificação
          </h2>
          <div>
            <label className="block text-sm font-bold opacity-70 mb-2">Seu Nome (Para chamar no balcão)</label>
            <input 
              type="text" 
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              placeholder="Ex: João Silva"
              className={`w-full p-4 rounded-xl text-lg font-bold outline-none border-2 focus:border-orange-500 transition-all ${isKiosk ? 'bg-slate-950 border-slate-800 text-white' : 'bg-gray-100 border-gray-200'}`}
            />
          </div>
        </section>

        <section className={`p-6 rounded-[2rem] border ${cardClass}`}>
          <h2 className="text-xl font-black mb-6 flex items-center gap-2">
            <CreditCard className="text-green-500" /> Forma de Pagamento
          </h2>
          <div className="grid grid-cols-3 gap-4">
            {[
              { id: 'pix', label: 'Pix', icon: QrCode },
              { id: 'card', label: 'Cartão', icon: CreditCard },
              { id: 'cash', label: 'Dinheiro', icon: Banknote },
            ].map(method => (
              <button
                key={method.id}
                onClick={() => setPaymentMethod(method.id)}
                className={`
                  p-6 rounded-2xl border-2 flex flex-col items-center gap-3 transition-all active:scale-95
                  ${paymentMethod === method.id 
                    ? 'border-orange-500 bg-orange-500/10 text-orange-500' 
                    : isKiosk ? 'border-slate-800 bg-slate-950 text-slate-400' : 'border-gray-200 bg-gray-50 text-gray-500'}
                `}
              >
                <method.icon size={32} />
                <span className="font-bold">{method.label}</span>
              </button>
            ))}
          </div>
        </section>

      </main>

      <div className={`fixed bottom-0 left-0 w-full p-6 z-50 ${isKiosk ? 'bg-slate-900 border-t border-slate-800' : 'bg-white border-t border-gray-200'}`}>
        <div className="max-w-3xl mx-auto flex gap-4">
          <button 
            onClick={() => router.back()}
            className={`flex-1 py-4 rounded-xl font-bold border-2 ${isKiosk ? 'border-slate-700 text-slate-300' : 'border-gray-300 text-gray-600'}`}
          >
            Voltar
          </button>
          <button 
            onClick={handleFinish}
            disabled={loading}
            className="flex-[2] bg-green-600 hover:bg-green-700 text-white py-4 rounded-xl font-black text-xl uppercase tracking-widest shadow-lg flex items-center justify-center gap-3 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? <Loader2 className="animate-spin" /> : "Confirmar Pedido"}
          </button>
        </div>
      </div>
    </div>
  );
}

