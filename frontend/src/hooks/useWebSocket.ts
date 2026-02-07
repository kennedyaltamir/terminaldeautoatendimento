/**
 * 📡 MESAFLOW OS — WEBSOCKET HOOK
 * Version: 2.2.0 (Null-Safe Context)
 */
import { useEffect } from "react";
import { useWebSocketContext } from "@/context/WebSocketContext";

export function useWebSocket(slug: string, onMessage?: (data: any) => void) {
  const context = useWebSocketContext();

  useEffect(() => {
    // 🛡️ FIX TS2339: Guard clause para contexto nulo
    if (context && context.lastMessage && onMessage) {
      onMessage(context.lastMessage);
    }
  }, [context, onMessage]);

  return { 
    isConnected: context?.isConnected ?? false 
  };
}
