"use client";

import React, { useState, useEffect, use } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useCart } from "@/context/CartContext";
import { createOrder } from "@/lib/api";
import { ArrowLeft, Loader2, CreditCard, Banknote, QrCode } from "lucide-react";
import { toast } from "sonner";
import { formatCurrency, cn } from "@/lib/utils";
import PixPaymentModal from "@/components/menu/PixPaymentModal";

export default function CheckoutPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  const router = useRouter();
  const searchParams = useSearchParams();
  const { items, total, clearCart } = useCart();
  
  const [loading, setLoading] = useState(false);
  const [pixData, setPixData] = useState<any>(null);
  const [activeOrderId, setActiveOrderId] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    customerName: "",
    customerPhone: "",
    pickupNote: "",
    paymentMethod: "pix"
  });

  const tableId = searchParams.get("table");
  const sessionToken = searchParams.get("token");

  useEffect(() => {
    if (items.length === 0) {
      router.replace(`/${slug}/menu`);
    }
  }, [items, slug, router]);

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.customerName || !formData.customerPhone) {
      toast.error("Preencha nome e telefone.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        table_id: tableId ? parseInt(tableId) : undefined,
        session_token: sessionToken,
        customer_name: formData.customerName,
        customer_phone: formData.customerPhone,
        pickup_note: formData.pickupNote || (tableId ? `Mesa ${tableId}` : "Balcão"),
        payment_method: formData.paymentMethod,
        order_type: tableId ? "dine_in" : "takeout",
        origin: tableId ? "mobile" : "kiosk",
        items: items.map(i => ({
          product_id: i.product.id,
          quantity: i.quantity,
          notes: i.notes,
          selected_options: i.selectedOptions.map(o => o.id)
        }))
      };

      const order = await createOrder(slug, payload);

      if (formData.paymentMethod === 'pix' && order.mp_qr_code) {
        setPixData({ qr_code: order.mp_qr_code, total: order.total_amount });
        setActiveOrderId(order.id);
      } else {
        toast.success("Pedido realizado com sucesso!");
        clearCart();
        router.push(`/${slug}/menu?order=${order.id}`);
      }
    } catch (err: any) {
      console.error(err);
      toast.error("Erro ao criar pedido. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 p-4 font-sans">
      <header className="flex items-center gap-4 mb-6">
        <button onClick={() => router.back()} className="p-2 bg-white dark:bg-slate-900 rounded-xl shadow-sm">
          <ArrowLeft size={20} className="text-slate-700 dark:text-slate-200" />
        </button>
        <h1 className="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight">Finalizar Pedido</h1>
      </header>

      <form onSubmit={handleCheckout} className="space-y-6 max-w-md mx-auto">
        <section className="bg-white dark:bg-slate-900 p-5 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-800">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Identificação</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-1">Nome</label>
              <input 
                name="customerName"
                value={formData.customerName}
                onChange={e => setFormData({...formData, customerName: e.target.value})}
                className="w-full p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Seu nome"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-1">Telefone / WhatsApp</label>
              <input 
                name="customerPhone"
                value={formData.customerPhone}
                onChange={e => setFormData({...formData, customerPhone: e.target.value})}
                className="w-full p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="11999999999"
                type="tel"
                required
              />
            </div>
          </div>
        </section>

        {!tableId && (
          <section className="bg-white dark:bg-slate-900 p-5 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-800">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Localização</h2>
            <input 
              name="pickupNote"
              value={formData.pickupNote}
              onChange={e => setFormData({...formData, pickupNote: e.target.value})}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Onde você está? (Ex: Balcão, Mesa 5)"
            />
          </section>
        )}

        <section className="bg-white dark:bg-slate-900 p-5 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-800">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Pagamento</h2>
          <div className="grid grid-cols-3 gap-3">
            {[
              { id: 'pix', label: 'Pix', icon: QrCode },
              { id: 'card', label: 'Cartão', icon: CreditCard },
              { id: 'cash', label: 'Dinheiro', icon: Banknote }
            ].map(method => (
              <button
                key={method.id}
                type="button"
                onClick={() => setFormData({...formData, paymentMethod: method.id})}
                className={cn(
                  "flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all",
                  formData.paymentMethod === method.id 
                    ? "border-orange-500 bg-orange-50 dark:bg-orange-900/20 text-orange-600" 
                    : "border-slate-100 dark:border-slate-800 text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800"
                )}
              >
                <method.icon size={24} className="mb-1" />
                <span className="text-[10px] font-black uppercase">{method.label}</span>
              </button>
            ))}
          </div>
        </section>

        <div className="fixed bottom-0 left-0 w-full bg-white dark:bg-slate-900 p-4 border-t border-slate-100 dark:border-slate-800 safe-area-bottom">
          <div className="max-w-md mx-auto flex items-center justify-between gap-4">
            <div>
              <p className="text-xs text-slate-400 font-bold uppercase">Total</p>
              <p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(total)}</p>
            </div>
            <button 
              type="submit"
              disabled={loading}
              className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-xl font-black uppercase tracking-widest shadow-lg active:scale-95 transition-all disabled:opacity-70 flex items-center gap-2"
            >
              {loading && <Loader2 className="animate-spin" size={18} />}
              Confirmar Pedido
            </button>
          </div>
        </div>
      </form>

      {pixData && activeOrderId && (
        <PixPaymentModal 
          isOpen={!!pixData}
          pixCode={pixData.qr_code}
          total={pixData.total}
          orderId={activeOrderId}
          slug={slug}
          onPaymentConfirmed={() => {
            setPixData(null);
            clearCart();
            toast.success("Pagamento confirmado!");
            router.push(`/${slug}/menu?order=${activeOrderId}`);
          }}
        />
      )}
    </div>
  );
}
