import { useEffect } from "react";
import { useWebSocketContext } from "@/context/WebSocketContext";

// Hook de conveniência para componentes assinarem mensagens
export function useWebSocket(slug: string, onMessage?: (data: any) => void) {
  const { lastMessage, isConnected } = useWebSocketContext();

  useEffect(() => {
    if (lastMessage && onMessage) {
      onMessage(lastMessage);
    }
  }, [lastMessage, onMessage]);

  return { isConnected };
}