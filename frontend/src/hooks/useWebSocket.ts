import { useEffect, useRef, useState, useCallback } from "react";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://192.168.0.150:8000/ws";

type MessageHandler = (data: any) => void;

export function useWebSocket(slug: string, onMessage: MessageHandler) {
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);
  const retryCount = useRef(0);

  const connect = useCallback(() => {
    if (!slug) return;
    if (ws.current?.readyState === WebSocket.OPEN) return;

    // Fecha conexão anterior se existir
    if (ws.current) {
      ws.current.close();
    }

    const socket = new WebSocket(`${WS_URL}/${slug}`);
    ws.current = socket;

    socket.onopen = () => {
      console.log("🟢 WS Conectado:", slug);
      setIsConnected(true);
      retryCount.current = 0; // Resetar tentativas
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error("Erro ao processar mensagem WS", e);
      }
    };

    socket.onclose = (event) => {
      console.log("🔴 WS Desconectado. Código:", event.code);
      setIsConnected(false);
      
      // Tentar reconectar se não foi fechamento limpo
      if (event.code !== 1000) {
        const timeout = Math.min(1000 * (2 ** retryCount.current), 10000); // Exponential backoff (max 10s)
        console.log(`🔄 Tentando reconectar em ${timeout}ms...`);
        
        reconnectTimeout.current = setTimeout(() => {
          retryCount.current += 1;
          connect();
        }, timeout);
      }
    };

    socket.onerror = (error) => {
      console.error("⚠️ Erro no WebSocket:", error);
      socket.close();
    };

  }, [slug, onMessage]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (ws.current) ws.current.close();
    };
  }, [connect]);

  return { isConnected, sendMessage: ws.current?.send.bind(ws.current) };
}