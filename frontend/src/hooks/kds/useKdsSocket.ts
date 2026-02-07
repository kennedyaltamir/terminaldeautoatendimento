/**
 * DOMAIN: INFRASTRUCTURE
 * OBJECTIVE: WebSocket management with null-safe context access.
 * VERSION: 17.2.1 (Type Safe)
 */
import { useState, useEffect, useRef } from 'react';
import { useWebSocketContext } from '@/context/WebSocketContext';

export type ConnectionState = 'LIVE' | 'DEGRADED' | 'OFFLINE';

export function useKdsSocket(slug: string, onEvent: (data: any) => void) {
  const context = useWebSocketContext();
  const [status, setStatus] = useState<ConnectionState>('OFFLINE');
  const lastHeartbeat = useRef<number>(Date.now());

  // 🛡️ FIX TS2339: Uso de optional chaining e null checks
  useEffect(() => {
    if (context?.isConnected) {
      setStatus('LIVE');
      lastHeartbeat.current = Date.now();
    } else {
      setStatus('OFFLINE');
    }
  }, [context?.isConnected]);

  useEffect(() => {
    if (context?.lastMessage) {
      lastHeartbeat.current = Date.now();
      if (status !== 'LIVE') setStatus('LIVE');
      onEvent(context.lastMessage);
    }
  }, [context?.lastMessage, onEvent, status]);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      if (context?.isConnected) {
        if (now - lastHeartbeat.current > 120000) {
          // Heartbeat logic
        }
      } else {
        setStatus('OFFLINE');
      }
    }, 10000);
    return () => clearInterval(interval);
  }, [context?.isConnected]);

  return { status };
}
