"use client";
import { useEffect, useRef } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { toast } from "sonner";
import { CheckCircle2, BellRing } from "lucide-react";

export default function NotificationManager({ slug }: { slug: string }) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Função para tocar som e vibrar
  const notifyUser = (pattern: number[] = [200, 100, 200]) => {
    // 1. Som
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      // 🛡️ FIX: console.log -> console.warn
      audioRef.current.play().catch(e => console.warn("Autoplay bloqueado:", e));
    }
    // 2. Vibração (Apenas Mobile/Android)
    if (typeof navigator !== "undefined" && navigator.vibrate) {
      navigator.vibrate(pattern);
    }
  };

  useWebSocket(slug, (data) => {
    // 1. Pedido Pronto (Cozinha -> Garçom)
    if (data.type === "order_update" && data.status === "ready") {
      notifyUser([200, 100, 200, 100, 500]); // Vibração longa
      const title = data.table === "Delivery" 
        ? `Delivery: ${data.customer}` 
        : `Mesa ${data.table}`;
      
      toast.success(
        <div className="flex flex-col">
          <span className="font-bold text-lg">{title}</span>
          <span className="text-sm">Pedido pronto na cozinha! 🍳</span>
        </div>,
        { 
          duration: 10000,
          icon: <CheckCircle2 size={24} className="text-green-500" />
        }
      );
    }

    // 2. Chamado de Mesa (Cliente -> Garçom)
    if (data.type === "waiter_call") {
      notifyUser([500, 200, 500]); // Vibração de alerta
      const typeMap: any = {
        bill: "Pediu a Conta 💸",
        help: "Chamou Ajuda 🙋",
        cleaning: "Limpeza ✨",
        other: "Outros 💬"
      };

      toast(
        <div className="flex flex-col">
          <span className="font-bold text-lg text-red-600">Mesa {data.table}</span>
          <span className="text-sm font-bold">{typeMap[data.service_type] || "Chamado"}</span>
          {data.notes && <span className="text-xs italic mt-1">"{data.notes}"</span>}
        </div>,
        {
          duration: Infinity,
          action: {
            label: "OK",
            onClick: () => {}
          },
          icon: <BellRing size={24} className="text-red-500 animate-bounce" />
        }
      );
    }
  });

  return (
    <audio ref={audioRef} src="/notification.mp3" preload="auto" />
  );
}
