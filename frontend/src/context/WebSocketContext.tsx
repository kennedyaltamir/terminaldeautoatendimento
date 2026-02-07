"use client";
import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";

interface WebSocketContextType {
  isConnected: boolean;
  lastMessage: any;
  sendMessage: (msg: any) => void;
}

const WebSocketContext = createContext<WebSocketContextType | null>(null);

export function WebSocketProvider({ children, slug }: { children: React.ReactNode, slug: string }) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const ws = useRef<WebSocket | null>(null);
  const isMounted = useRef(false);
  
  // 🛡️ Gestão de Timers com Tipagem Cross-Platform
  const reconnectTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const heartbeatInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  /**
   * Rito de Conexão Soberana
   */
  const connect = useCallback(() => {
    if (!slug || slug === "undefined" || !isMounted.current) return;

    // Limpeza de instâncias fantasmas antes de nova tentativa
    if (ws.current) {
      if (ws.current.readyState === WebSocket.OPEN || ws.current.readyState === WebSocket.CONNECTING) {
        return;
      }
      ws.current.close();
    }

    // Resolução de URL: Prioriza ENV, Fallback para Sentinel (8001)
    const API_HOST = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
    const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || `ws://${API_HOST}:8001/api/ws`;
    const finalUrl = `${WS_BASE_URL}/${slug}`;

    // 🛡️ FIX: Removido log de debug
    
    const socket = new WebSocket(finalUrl);
    ws.current = socket;

    socket.onopen = () => {
      if (!isMounted.current) {
        socket.close();
        return;
      }
      // 🛡️ FIX: console.log -> console.info para status de conexão
      console.info(`✅ [WS_CONNECT] Canal sincronizado: ${slug}`);
      setIsConnected(true);

      // Iniciar rito de Heartbeat (Mantém o túnel aberto)
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
      heartbeatInterval.current = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({ type: "ping" }));
        }
      }, 30000);
    };

    socket.onmessage = (event) => {
      if (!isMounted.current) return;
      try {
        const data = JSON.parse(event.data);
        // Ignora respostas de heartbeat no estado global para evitar re-renders inúteis
        if (data.type === "pong") return;
        setLastMessage(data);
      } catch (e) {
        console.error("🚨 [WS_PARSE_ERROR] Falha ao processar payload:", e);
      }
    };

    socket.onclose = (event) => {
      if (!isMounted.current) return;
      setIsConnected(false);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);

      // Rito de Reconexão (Não reconecta se o fechamento for intencional - código 1000)
      if (event.code !== 1000) {
        console.warn(`⚠️ [WS_DISCONNECT] Conexão perdida (Código: ${event.code}). Tentando em 3s...`);
        if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
        reconnectTimeout.current = setTimeout(() => {
          if (isMounted.current) connect();
        }, 3000);
      }
    };

    socket.onerror = (err) => {
      console.error("❌ [WS_CRITICAL_ERROR] Falha física no soquete:", err);
      socket.close();
    };
  }, [slug]);

  useEffect(() => {
    isMounted.current = true;
    // Pequeno atraso para garantir que o rito de hidratação do Next.js terminou
    const initTimer = setTimeout(connect, 100);

    return () => {
      isMounted.current = false;
      clearTimeout(initTimer);
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
      if (ws.current) {
        // Encerramento Gracioso
        ws.current.close(1000, "Component Unmounted");
        ws.current = null;
      }
    };
  }, [connect]);

  /**
   * Método de envio seguro.
   */
  const sendMessage = useCallback((msg: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(msg));
    } else {
      console.warn("📤 [WS_SEND_SKIP] Tentativa de envio com canal fechado.");
    }
  }, []);

  return (
    <WebSocketContext.Provider value={{ isConnected, lastMessage, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
}

/**
 * Hook de acesso rápido com Fallback de Segurança.
 */
export function useWebSocketContext() {
  const context = useContext(WebSocketContext);
  if (!context) {
    // Retorna interface nula para não quebrar componentes fora do Provider
    return { 
      isConnected: false, 
      lastMessage: null, 
      sendMessage: (msg: any) => console.error("WS fora de contexto", msg) 
    };
  }
  return context;
}
