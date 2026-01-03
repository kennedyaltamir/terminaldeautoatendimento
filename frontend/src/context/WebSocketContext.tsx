"use client";

import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";

interface WebSocketContextType {
  isConnected: boolean;
  lastMessage: any;
  sendMessage: (msg: any) => void;
}

const WebSocketContext = createContext<WebSocketContextType | null>(null);

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

export function WebSocketProvider({ children, slug }: { children: React.ReactNode, slug?: string }) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);
  const heartbeatInterval = useRef<NodeJS.Timeout | null>(null);
  const isMounted = useRef(false);

  const connect = useCallback(() => {
    if (!slug || !isMounted.current) return;

    if (ws.current) {
      if (ws.current.readyState === WebSocket.OPEN || ws.current.readyState === WebSocket.CONNECTING) {
        return;
      }
      ws.current.close();
    }

    const socket = new WebSocket(`${WS_URL}/${slug}`);
    ws.current = socket;

    socket.onopen = () => {
      if (isMounted.current) {
        console.log("🟢 WS Conectado:", slug);
        setIsConnected(true);
        
        // Iniciar Heartbeat (Batida de coração) para evitar timeout de inatividade (1012)
        if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
        heartbeatInterval.current = setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ type: "ping" }));
          }
        }, 30000); // 30 segundos
      } else {
        socket.close();
      }
    };

    socket.onmessage = (event) => {
      if (!isMounted.current) return;
      try {
        const data = JSON.parse(event.data);
        if (data.type === "pong") return; // Ignora resposta de heartbeat
        setLastMessage(data);
      } catch (e) {
        console.error("Erro ao processar mensagem WS", e);
      }
    };

    socket.onclose = (event) => {
      if (!isMounted.current) return;
      setIsConnected(false);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
      
      if (event.code !== 1000) {
        if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
        reconnectTimeout.current = setTimeout(() => {
          if (isMounted.current) connect();
        }, 3000);
      }
    };

    socket.onerror = () => {
        // Erros são tratados pelo onclose
    };

  }, [slug]);

  useEffect(() => {
    isMounted.current = true;
    
    const connectionTimer = setTimeout(() => {
      if (slug) connect();
    }, 150);

    return () => {
      isMounted.current = false;
      clearTimeout(connectionTimer);
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
      
      if (ws.current) {
        if (ws.current.readyState === WebSocket.OPEN) {
            ws.current.close(1000, "Unmount");
        }
        ws.current = null;
      }
    };
  }, [connect, slug]);

  const sendMessage = (msg: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(msg));
    }
  };

  return (
    <WebSocketContext.Provider value={{ isConnected, lastMessage, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketContext() {
  const context = useContext(WebSocketContext);
  if (!context) {
    return { isConnected: false, lastMessage: null, sendMessage: () => {} };
  }
  return context;
}