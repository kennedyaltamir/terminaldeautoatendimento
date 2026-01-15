// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 14:35:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { getToken } from "@/lib/auth";
import { toast } from "sonner";
// ... outros imports

export default function DriverPage({ params }: { params: { slug: string } }) {
  const [orders, setOrders] = useState<any[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handlePickup = async (orderId: string) => {
    if (isProcessing) return;
    setIsProcessing(true);
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${getToken()}`,
          "Content-Type": "application/json" 
        }
      });
      
      if (res.ok) {
        toast.success("Rota iniciada!");
        // RESILIÊNCIA L6: Atualização local imediata (Optimistic/Redundant)
        // Isso garante que a UI mude mesmo se o WebSocket falhar.
        setOrders(prev => prev.map(o => 
          o.id === orderId ? { ...o, status: 'delivering' } : o
        ));
      } else {
        const err = await res.json();
        toast.error(err.detail || "Falha ao coletar pedido");
      }
    } catch (e) { 
      toast.error("Erro de conexão"); 
    } finally {
      setIsProcessing(false);
    }
  };

  // ... restante do componente (renderização do mapa baseada no status 'delivering')
  return (
    <div>{/* JSX existente */}</div>
  );
}
