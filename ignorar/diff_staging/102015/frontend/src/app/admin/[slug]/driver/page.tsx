// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 13:35:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { getToken } from "@/lib/auth";
import { toast } from "sonner";
// ... outros imports

export default function DriverPage({ params }: { params: { slug: string } }) {
  const [orders, setOrders] = useState<any[]>([]);
  
  const handlePickup = async (orderId: string) => {
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
        // RESILIÊNCIA L6: Força atualização local imediata caso o WebSocket falhe
        setOrders(prev => prev.map(o => 
          o.id === orderId ? { ...o, status: 'delivering' } : o
        ));
      }
    } catch (e) { 
      toast.error("Erro ao iniciar rota"); 
    }
  };

  // ... restante do componente
  return (
    // JSX do componente
    <div>{/* ... */}</div>
  );
}
