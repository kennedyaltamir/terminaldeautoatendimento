"use client";
import { useCart } from "@/context/CartContext";
import { formatCurrency } from "@/lib/utils";
import { X, Trash2, ArrowRight, Minus, Plus } from "lucide-react";
import { useRouter, usePathname } from "next/navigation";
import { useState } from "react";

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  primaryColor: string;
  slug: string;
  tableId?: number;
  sessionToken?: string;
  onCheckout?: () => void;
}

export default function CartDrawer({ 
  isOpen, 
  onClose, 
  primaryColor, 
  slug, 
  tableId, 
  sessionToken, 
  onCheckout 
}: CartDrawerProps) {
  const { items, total, updateCartItem, removeFromCart } = useCart();
  const router = useRouter();
  const pathname = usePathname();
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleCheckoutAction = () => {
    if (onCheckout) {
      // Modo Kiosk/SPA: Delega para o pai
      onCheckout();
    } else {
      // Modo Web Padrão: Navega para página de checkout
      const query = new URLSearchParams();
      if (tableId) query.set("table", tableId.toString());
      if (sessionToken) query.set("token", sessionToken);
      
      // 🛡️ FIX: Detecção de contexto Admin vs Público
      const isAdmin = pathname?.startsWith("/admin");
      const checkoutPath = isAdmin 
        ? `/admin/${slug}/checkout` 
        : `/${slug}/checkout`; // Rota pública
      
      router.push(`${checkoutPath}?${query.toString()}`);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="relative w-full max-w-md bg-white dark:bg-slate-900 h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-300">
        <div className="p-4 border-b border-gray-100 dark:border-slate-800 flex justify-between items-center">
          <h2 className="font-black text-xl text-gray-900 dark:text-white">Seu Pedido</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-full transition-colors">
            <X size={24} className="text-gray-500" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400 space-y-4">
              <p>Seu carrinho está vazio.</p>
              <button 
                onClick={onClose}
                className="text-sm font-bold underline"
                style={{ color: primaryColor }}
              >
                Voltar ao cardápio
              </button>
            </div>
          ) : (
            items.map((item, index) => (
              <div key={index} className="flex gap-4 bg-gray-50 dark:bg-slate-800/50 p-3 rounded-xl border border-gray-100 dark:border-slate-800">
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <h3 className="font-bold text-gray-900 dark:text-white">{item.product.name}</h3>
                    <p className="font-bold text-gray-900 dark:text-white">
                      {formatCurrency((Number(item.product.price) * item.quantity))}
                    </p>
                  </div>
                  {item.selectedOptions && item.selectedOptions.length > 0 && (
                    <p className="text-xs text-gray-500 mt-1">
                      {item.selectedOptions.map(o => o.name).join(", ")}
                    </p>
                  )}
                  {item.notes && (
                    <p className="text-xs text-orange-600 mt-1 italic">
                      Obs: {item.notes}
                    </p>
                  )}
                  <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center gap-3 bg-white dark:bg-slate-900 rounded-lg p-1 border border-gray-200 dark:border-slate-700">
                      <button 
                        onClick={() => {
                          if (item.quantity > 1) {
                            updateCartItem(index, { ...item, quantity: item.quantity - 1 });
                          } else {
                            removeFromCart(index);
                          }
                        }}
                        className="w-6 h-6 flex items-center justify-center hover:bg-gray-100 dark:hover:bg-slate-800 rounded"
                      >
                        <Minus size={14} />
                      </button>
                      <span className="text-sm font-bold w-4 text-center">{item.quantity}</span>
                      <button 
                        onClick={() => updateCartItem(index, { ...item, quantity: item.quantity + 1 })}
                        className="w-6 h-6 flex items-center justify-center hover:bg-gray-100 dark:hover:bg-slate-800 rounded"
                      >
                        <Plus size={14} />
                      </button>
                    </div>
                    <button 
                      onClick={() => removeFromCart(index)}
                      className="text-red-500 p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {items.length > 0 && (
          <div className="p-4 border-t border-gray-100 dark:border-slate-800 bg-white dark:bg-slate-900 safe-area-bottom">
            <div className="flex justify-between items-center mb-4">
              <span className="text-gray-500 font-medium">Total</span>
              <span className="text-2xl font-black text-gray-900 dark:text-white">
                {formatCurrency(total)}
              </span>
            </div>
            <button
              onClick={handleCheckoutAction}
              disabled={isSubmitting}
              className="w-full py-4 rounded-xl font-black text-white shadow-lg active:scale-95 transition-all flex items-center justify-center gap-2"
              style={{ backgroundColor: primaryColor }}
              data-testid="checkout-button"
            >
              Finalizar Pedido <ArrowRight size={20} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
