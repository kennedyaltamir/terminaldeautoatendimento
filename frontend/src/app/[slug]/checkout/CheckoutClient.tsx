"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useCart } from "@/context/CartContext";
import { createOrder, getMenu } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import KioskHeader from "@/components/kiosk/KioskHeader";
import { 
  ShoppingBag, User, CheckCircle2, Loader2, ArrowLeft, 
  QrCode, Copy, Star, MapPin, CreditCard, Banknote,
  ChevronRight, Trash2, Info
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { QRCodeSVG } from "qrcode.react";

export default function CheckoutClient({ slug }: { slug: string }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const tableId = searchParams.get("table");
  const qrToken = searchParams.get("token");
  const isKiosk = searchParams.get("kiosk") === "true";
  
  const { items = [], total = 0, removeFromCart, clearCart } = useCart();
  
  const [step, setStep] = useState<"review" | "pix" | "survey">("review");
  const [loading, setLoading] = useState(false);
  const [pixKey, setPixKey] = useState("");
  const [orderId, setOrderId] = useState("");
  const [rating, setRating] = useState(0);
  
  const [formData, setFormData] = useState({
    customer_name: "",
    customer_phone: "",
    order_type: tableId ? "dine_in" : "delivery",
    delivery_address: "",
    payment_method: "pix"
  });

  useEffect(() => {
    getMenu(slug).then(data => {
      if (data?.company?.pix_key) setPixKey(data.company.pix_key);
    });
  }, [slug]);

  if (items.length === 0 && step !== "survey") return null;

  const handleFinalize = async () => {
    if (!formData.customer_name.trim()) return toast.error("Informe seu nome.");
    if (formData.order_type === "delivery" && !formData.delivery_address.trim()) return toast.error("Informe o endereço.");

    setLoading(true);
    try {
      const payload = {
        ...formData,
        table_id: tableId ? parseInt(tableId) : null,
        qr_token: qrToken || null,
        items: items.map(i => ({ product_id: i.product.id, quantity: i.quantity, notes: i.notes || "" }))
      };
      const order = await createOrder(slug, payload);
      setOrderId(order.id);
      setStep(formData.payment_method === "pix" ? "pix" : "survey");
    } catch (error: any) {
      toast.error(error.message);
    } finally { setLoading(false); }
  };

  const finish = () => {
    clearCart();
    router.push(`/${slug}/menu?order=${orderId}`);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white" data-testid="checkout-page">
      <AnimatePresence mode="wait">
        {step === "review" && (
          <motion.div key="review" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {isKiosk ? <KioskHeader companyName="MesaFlow Totem" primaryColor="#ea580c" /> : (
              <header className="p-6 border-b border-white/5 flex items-center gap-4">
                <button onClick={() => router.back()} className="p-2 bg-slate-800 rounded-xl"><ArrowLeft size={20}/></button>
                <h1 className="font-black text-xl uppercase">Finalizar Pedido</h1>
              </header>
            )}
            <main className="max-w-2xl mx-auto p-6 space-y-6 pb-40">
              <section className="bg-slate-900 rounded-[2rem] border border-slate-800 p-6 shadow-2xl">
                <h2 className="text-orange-500 font-black uppercase text-xs tracking-widest mb-6 flex items-center gap-2"><ShoppingBag size={16}/> Resumo</h2>
                {items.map((item, idx) => (
                  <div key={idx} className="flex justify-between items-center mb-4 border-b border-white/5 pb-4 last:border-0">
                    <div className="flex gap-3">
                      <span className="bg-orange-600/20 text-orange-500 w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm">{item.quantity}x</span>
                      <div>
                        <p className="font-bold">{item.product.name}</p>
                        <p className="text-[10px] text-slate-500">{item.selectedOptions?.map(o => o.name).join(", ")}</p>
                      </div>
                    </div>
                    <span className="font-black">{formatCurrency(item.product.price * item.quantity)}</span>
                  </div>
                ))}
              </section>

              <section className="bg-slate-900 rounded-[2rem] border border-slate-800 p-6 shadow-2xl space-y-4">
                <h2 className="text-blue-500 font-black uppercase text-xs tracking-widest flex items-center gap-2"><User size={16}/> Identificação</h2>
                <input name="customer_name" required className="w-full bg-slate-950 border border-slate-800 p-4 rounded-2xl outline-none focus:border-orange-500 transition-all font-bold" placeholder="Seu Nome" value={formData.customer_name} onChange={e => setFormData({...formData, customer_name: e.target.value})} />
                <input name="customer_phone" required className="w-full bg-slate-950 border border-slate-800 p-4 rounded-2xl outline-none focus:border-orange-500 transition-all font-bold" placeholder="WhatsApp" value={formData.customer_phone} onChange={e => setFormData({...formData, customer_phone: e.target.value})} />
              </section>

              {formData.order_type === 'delivery' && (
                <section className="bg-slate-900 rounded-[2rem] border border-slate-800 p-6 shadow-2xl space-y-4">
                  <h2 className="text-orange-500 font-black uppercase text-xs tracking-widest flex items-center gap-2"><MapPin size={16}/> Endereço</h2>
                  <textarea name="delivery_address" required className="w-full bg-slate-950 border border-slate-800 p-4 rounded-2xl outline-none focus:border-orange-500 transition-all font-bold h-24 resize-none" placeholder="Rua, Número, Bairro..." value={formData.delivery_address} onChange={e => setFormData({...formData, delivery_address: e.target.value})} />
                </section>
              )}

              <section className="bg-slate-900 rounded-[2rem] border border-slate-800 p-6 shadow-2xl space-y-4">
                <h2 className="text-emerald-500 font-black uppercase text-xs tracking-widest flex items-center gap-2"><CreditCard size={16}/> Pagamento</h2>
                <div className="grid grid-cols-2 gap-3">
                  <button type="button" onClick={() => setFormData({...formData, payment_method: 'pix'})} className={`p-4 rounded-2xl border-2 flex flex-col items-center gap-2 transition-all ${formData.payment_method === 'pix' ? 'border-orange-500 bg-orange-500/10 text-orange-500' : 'border-transparent bg-slate-950 text-slate-600'}`}><QrCode size={24}/> <span className="text-[10px] font-black uppercase">Pix</span></button>
                  <button type="button" onClick={() => setFormData({...formData, payment_method: 'cash'})} className={`p-4 rounded-2xl border-2 flex flex-col items-center gap-2 transition-all ${formData.payment_method === 'cash' ? 'border-orange-500 bg-orange-500/10 text-orange-500' : 'border-transparent bg-slate-950 text-slate-600'}`}><Banknote size={24}/> <span className="text-[10px] font-black uppercase">Dinheiro</span></button>
                </div>
              </section>
            </main>
            <footer className="fixed bottom-0 left-0 w-full p-6 bg-slate-900/90 backdrop-blur-xl border-t border-white/5 z-50">
              <div className="max-w-2xl mx-auto flex justify-between items-center">
                <div className="text-left"><p className="text-[10px] font-black text-slate-500 uppercase">Total</p><p className="text-3xl font-black text-orange-500">{formatCurrency(total)}</p></div>
                <button onClick={handleFinalize} disabled={loading} className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-5 rounded-2xl font-black uppercase text-sm shadow-xl flex items-center gap-3 disabled:opacity-50">{loading ? <Loader2 className="animate-spin"/> : <>Finalizar <ChevronRight size={20}/></>}</button>
              </div>
            </footer>
          </motion.div>
        )}

        {step === "pix" && (
          <motion.div key="pix" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="min-h-screen flex flex-col items-center justify-center p-8 text-center" data-testid="pix-modal">
            <div className="bg-white p-6 rounded-[3rem] mb-8 shadow-2xl"><QRCodeSVG value={pixKey || "MesaFlow"} size={200} /></div>
            <h2 className="text-3xl font-black mb-2">Pagamento Pix</h2>
            <p className="text-orange-500 font-black text-2xl mb-10">{formatCurrency(total)}</p>
            <button onClick={() => setStep("survey")} data-testid="btn-confirm-pix" className="w-full max-w-xs bg-green-600 p-5 rounded-2xl font-black uppercase tracking-widest shadow-lg">Já paguei</button>
          </motion.div>
        )}

        {step === "survey" && (
          <motion.div key="survey" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="min-h-screen flex flex-col items-center justify-center p-8 text-center" data-testid="survey-step">
            <div className="bg-orange-600/20 p-6 rounded-full mb-8 text-orange-500"><Star size={48} fill="currentColor"/></div>
            <h2 className="text-3xl font-black mb-4">O que achou da experiência?</h2>
            <div className="flex gap-3 mb-12">
              {[1,2,3,4,5].map(s => (
                <button key={s} onClick={() => setRating(s)} className={`w-14 h-14 rounded-2xl border-2 transition-all ${rating >= s ? 'bg-orange-600 border-orange-500' : 'bg-slate-900 border-slate-800'}`}><Star size={28} fill={rating >= s ? "white" : "none"}/></button>
              ))}
            </div>
            <button onClick={finish} data-testid="btn-finish-survey" className="w-full max-w-xs bg-white text-slate-950 p-5 rounded-2xl font-black uppercase tracking-widest">Ver Status do Pedido</button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}