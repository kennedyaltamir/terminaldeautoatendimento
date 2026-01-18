
"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { CartItem, Product, Option } from "@/types";

interface CartContextType {
  items: CartItem[];
  addToCart: (product: Product, quantity: number, notes?: string, selectedOptions?: Option[]) => void;
  updateCartItem: (index: number, item: CartItem) => void;
  removeFromCart: (index: number) => void;
  clearCart: () => void;
  total: number; // Em centavos
}

const CartContext = createContext<CartContextType>({} as CartContextType);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const savedCart = localStorage.getItem("mesaflow_cart");
    if (savedCart) {
      try {
        setItems(JSON.parse(savedCart));
      } catch (e) {
        console.error("Erro ao carregar carrinho", e);
      }
    }
    setIsLoaded(true);
  }, []);

  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("mesaflow_cart", JSON.stringify(items));
    }
  }, [items, isLoaded]);

  const addToCart = (product: Product, quantity: number, notes?: string, selectedOptions: Option[] = []) => {
    setItems((prev) => [...prev, { product, quantity, notes, selectedOptions }]);
  };

  const updateCartItem = (index: number, item: CartItem) => {
    setItems((prev) => {
      const newItems = [...prev];
      newItems[index] = item;
      return newItems;
    });
  };

  const removeFromCart = (index: number) => {
    setItems((prev) => prev.filter((_, i) => i !== index));
  };

  const clearCart = () => setItems([]);

  const total = items.reduce((acc, item) => {
    const productPrice = Number(item.product.price);
    const optionsTotal = item.selectedOptions.reduce((sum, opt) => sum + Number(opt.price), 0);
    return acc + (productPrice + optionsTotal) * item.quantity;
  }, 0);

  return (
    <CartContext.Provider value={{ items, addToCart, updateCartItem, removeFromCart, clearCart, total }}>
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext);

