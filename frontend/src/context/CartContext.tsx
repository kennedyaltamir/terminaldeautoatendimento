"use client";
/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Gerenciamento de estado do carrinho com proteção contra Bad SetState.
 */
import  { 
  createContext, 
  useContext, 
  useState, 
  useEffect, 
  useMemo, 
  useCallback, 
  ReactNode 
} from "react";
import { CartItem, Product, Option } from "@/types";
import { toast } from "sonner";

interface CartContextType {
  items: CartItem[];
  addToCart: (product: Product, quantity: number, notes?: string, selectedOptions?: Option[]) => void;
  updateCartItem: (index: number, item: CartItem) => void;
  removeFromCart: (index: number) => void;
  clearCart: () => void;
  total: number;
  isInitialized: boolean;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);

  // 1. Restauração Inicial Segura
  useEffect(() => {
    const savedCart = localStorage.getItem("mesaflow_cart");
    if (savedCart) {
      try {
        const parsed = JSON.parse(savedCart);
        if (Array.isArray(parsed)) {
          setItems(parsed);

          setTimeout(() => {
            if (parsed.length > 0) {
            }
          }, 0);
        }
      } catch (e) {
        console.error("🚨 [CartContext] Erro ao restaurar LocalStorage:", e);
      }
    }
    setIsInitialized(true);
  }, []);

  // 2. Persistência
  useEffect(() => {
    if (isInitialized) {
      localStorage.setItem("mesaflow_cart", JSON.stringify(items));
    }
  }, [items, isInitialized]);

  // 3. Notificação (Adiamento para evitar Bad SetState durante renderização)
  const addToCart = useCallback((product: Product, quantity: number, notes: string = "", selectedOptions: Option[] = []) => {
    setItems((prev) => [...prev, { product, quantity, notes, selectedOptions }]);
    toast.success(`${product.name} adicionado!`, {
      description: quantity > 1 ? `${quantity} unidades` : undefined
    });
  }, []);

  const updateCartItem = useCallback((index: number, item: CartItem) => {
    setItems((prev) => {
      const newItems = [...prev];
      newItems[index] = item;
      return newItems;
    });
  }, []);

  const removeFromCart = useCallback((index: number) => {
    setItems((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const clearCart = useCallback(() => setItems([]), []);

  const total = useMemo(() => {
    return items.reduce((acc: number, item: CartItem) => {
      const productPrice = Number(item.product.price || 0);
      const optionsTotal = item.selectedOptions?.reduce((sum: number, opt: Option) => {
        return sum + Number(opt.price || 0);
      }, 0) || 0;
      return acc + (productPrice + optionsTotal) * item.quantity;
    }, 0);
  }, [items]);

  return (
    <CartContext.Provider value={{ items, addToCart, updateCartItem, removeFromCart, clearCart, total, isInitialized }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
