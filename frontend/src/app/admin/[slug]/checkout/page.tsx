"use client";

import { createSovereignPage } from '@/app/SovereignPageFactory';
import * as api from '@/lib/api';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default createSovereignPage({
  id: "ADMIN_CHECKOUT_V1",
  domain: "finance",
  authRequired: true, // Protegido por login
  render: ({ items, total, params, clearCart }) => (
    <div className="p-8 bg-slate-950 min-h-screen text-white">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Link 
            href={`/admin/${params.slug}/menu`} 
            className="p-2 bg-slate-800 rounded-xl hover:bg-slate-700 transition-colors"
          >
            <ArrowLeft size={20} />
          </Link>
          <div>
            <h1 className="text-3xl font-black tracking-tight">Checkout Administrativo</h1>
            <p className="text-slate-400 text-sm">Lançamento manual de pedido</p>
          </div>
        </div>

        {items.length === 0 ? (
          <div className="text-center py-20 bg-slate-900 rounded-3xl border border-slate-800 border-dashed">
            <p className="text-slate-500 font-bold">O carrinho está vazio.</p>
            <Link 
              href={`/admin/${params.slug}/menu`}
              className="text-orange-500 font-bold hover:underline mt-2 inline-block"
            >
              Adicionar itens no Cardápio
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4">Resumo</h3>
              <div className="space-y-3">
                {items.map((item: any, i: number) => (
                  <div key={i} className="flex justify-between items-center border-b border-slate-800 pb-3 last:border-0 last:pb-0">
                    <div className="flex items-center gap-3">
                      <span className="bg-slate-800 px-2 py-1 rounded text-xs font-bold">{item.quantity}x</span>
                      <span>{item.product.name}</span>
                    </div>
                    <span className="font-mono text-slate-300">
                      R$ {(item.product.price * item.quantity / 100).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
              <div className="mt-6 pt-4 border-t border-slate-800 flex justify-between items-center">
                <span className="text-lg font-bold">Total</span>
                <span className="text-3xl font-black text-emerald-500">
                  R$ {(total / 100).toFixed(2)}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={clearCart}
                className="py-4 rounded-xl font-bold text-slate-400 hover:bg-slate-900 border border-slate-800 transition-all"
              >
                Limpar
              </button>
              <button 
                onClick={async () => {
                  try {
                    await api.createOrder(params.slug, { 
                      items, 
                      total,
                      customer_name: "Venda Balcão (Admin)",
                      payment_method: "cash", // Default para admin
                      order_type: "takeout"
                    });
                    clearCart();
                    // Redireciona para o KDS ou Dashboard
                    window.location.href = `/admin/${params.slug}/kitchen`;
                  } catch (e) {
                    console.error(e);
                    alert("Erro ao criar pedido");
                  }
                }}
                className="py-4 rounded-xl font-black text-white bg-orange-600 hover:bg-orange-700 shadow-lg shadow-orange-900/20 transition-all active:scale-95"
              >
                Confirmar Pedido
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
});

