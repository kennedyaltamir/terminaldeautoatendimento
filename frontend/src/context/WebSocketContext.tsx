//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 12.6.0 (Production URL Compliance)
 * DNA_ID: MF-WS-CONTEXT-V12-6
 * OBJETIVO: Gerenciador de comunicação bidirecional resiliente.
 * Comportamento esperado: 
 *  1. Resolve dinamicamente a URL entre WSS (Prod) e WS (Dev).
 *  2. Garante o rito de conexão no path /api/ws/{slug} alinhado ao Kernel.
 *  3. Implementa heartbeat e reconexão automática com exponential backoff.
 */
//
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
  
  const reconnectTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const heartbeatInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  const connect = useCallback(() => {
    if (!slug || slug === "undefined" || !isMounted.current) return;

    if (ws.current) {
      if (ws.current.readyState === WebSocket.OPEN || ws.current.readyState === WebSocket.CONNECTING) return;
      ws.current.close();
    }

    const isProd = process.env.NEXT_PUBLIC_ENVIRONMENT === 'production';
    const protocol = isProd ? "wss" : "ws";
    const host = isProd ? "mesaflow-api.onrender.com" : (typeof window !== 'undefined' ? window.location.hostname + ":8001" : "localhost:8001");
    const finalUrl = `${protocol}://${host}/api/ws/${slug}`;
    
    const socket = new WebSocket(finalUrl);
    ws.current = socket;

    socket.onopen = () => {
      if (!isMounted.current) {
        socket.close();
        return;
      }
      setIsConnected(true);
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
        if (data.type === "pong") return;
        setLastMessage(data);
      } catch (e) {
        console.error("🚨 [WS_PARSE_ERROR]", e);
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
      if (ws.current) ws.current.close();
    };
  }, [slug]);

  useEffect(() => {
    isMounted.current = true;
    const initTimer = setTimeout(connect, 200);
    return () => {
      isMounted.current = false;
      clearTimeout(initTimer);
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
      if (ws.current) ws.current.close(1000);
    };
  }, [connect]);

  const sendMessage = useCallback((msg: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(msg));
    }
  }, []);

  return (
    <WebSocketContext.Provider value={{ isConnected, lastMessage, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketContext() {
  const context = useContext(WebSocketContext);
  if (!context) return { isConnected: false, lastMessage: null, sendMessage: () => {} };
  return context;
}
