"use client";
import { useState, useEffect } from "react";
import { ShoppingBag } from "lucide-react";

const events = [
  "🍔 Novo pedido de R$ 85,00 em São Paulo",
  "🎟️ Arena XP processou 1.200 pedidos na última hora",
  "🏨 Hotel Plaza ativou o modo Room Service",
  "🍕 Pizzaria do João economizou R$ 400 hoje",
  "🚀 Novo cliente Enterprise cadastrado no Rio de Janeiro"
];

export default function LiveTicker() {
  const [index, setIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % events.length);
        setVisible(true);
      }, 500);
    }, 8000); // Troca a cada 8s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`fixed bottom-6 left-6 z-40 transition-all duration-500 transform ${visible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"}`}>
      <div className="bg-white/90 backdrop-blur-md border border-gray-200 shadow-xl rounded-full px-4 py-3 flex items-center gap-3 max-w-xs md:max-w-md">
        <div className="bg-green-100 p-2 rounded-full text-green-600 animate-pulse">
          <ShoppingBag size={16} />
        </div>
        <span className="text-xs font-medium text-gray-700 truncate">
          {events[index]}
        </span>
      </div>
    </div>
  );
}