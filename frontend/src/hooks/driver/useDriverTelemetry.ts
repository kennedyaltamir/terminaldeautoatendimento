/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 3.3.0 (Adaptive Hybrid Engine)
 * DNA_ID: MF-DRIVER-TELEMETRY-V3-HYBRID
 * 
 * OBJETIVO: 
 * Motor de telemetria adaptativo que suporta alta precisão em Mobile (GPS Real)
 * e baixa precisão em Desktop (Wi-Fi/IP) para fins de desenvolvimento e testes.
 * 
 * MUDANÇAS TÁTICAS:
 * 1. Detecção de User Agent: Diferencia regras para Mobile vs Desktop.
 * 2. Filtro de Outliers Seletivo: Rigoroso no Mobile (>200m rejeita), Permissivo no Desktop.
 * 3. Signal Grading: Classificação de sinal (GOOD/WEAK) sem bloquear o fluxo de dados.
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { useWebSocketContext } from '@/context/WebSocketContext';
import { DRIVER_CONSTANTS } from '@/lib/constants/driver';
import { db } from '@/lib/db';
import { toast } from "sonner";

const SYNC_INTERVAL_MS = 4000;
const MIN_MOVE_METERS = 3;

// Limites de Precisão (Metros)
const MOBILE_REJECT_THRESHOLD = 200; // Mobile: Rejeita se precisão > 200m (Pulo de GPS)
const SIGNAL_GOOD_THRESHOLD = 30;    // Abaixo de 30m é sinal excelente

const calculateDistance = (c1: [number, number], c2: [number, number]): number => {
  const R = 6371000; 
  const dLat = ((c2[0] - c1[0]) * Math.PI) / 180;
  const dLon = ((c2[1] - c1[1]) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((c1[0] * Math.PI) / 180) *
      Math.cos((c2[0] * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
};

export function useDriverTelemetry(
  enabled: boolean, 
  journeyId: string = "unassigned",
  routePolyline?: any
) {
  const context = useWebSocketContext();
  
  const [coords, setCoords] = useState<[number, number] | null>(null);
  const [currentSpeed, setCurrentSpeed] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(DRIVER_CONSTANTS.ZOOM_LEVELS.SLOW);
  const [gpsSignal, setGpsSignal] = useState<'GOOD' | 'WEAK' | 'LOST' | 'DENIED' | 'INSECURE'>('WEAK');
  const [isOffRoute, setIsOffRoute] = useState(false);

  const lastSyncTime = useRef(0);
  const lastCoords = useRef<[number, number] | null>(null);
  const watchId = useRef<number | null>(null);

  const handlePosition = useCallback((pos: GeolocationPosition) => {
    const { latitude, longitude, speed, accuracy } = pos.coords;
    const now = Date.now();
    
    // 🛡️ DETECÇÃO DE AMBIENTE
    const isMobile = typeof navigator !== 'undefined' && /Android|iPhone|iPad/i.test(navigator.userAgent);

    // 1. CLASSIFICAÇÃO DE SINAL (Visual apenas, não bloqueante)
    let signalQuality: 'GOOD' | 'WEAK' = 'WEAK';
    if (accuracy <= SIGNAL_GOOD_THRESHOLD) {
        signalQuality = 'GOOD';
    }

    // 2. FILTRO DE OUTLIERS (Lógica Híbrida)
    // No Mobile: Se a precisão for muito ruim (>200m), ignoramos para evitar "pulos" no mapa.
    // No Desktop: Aceitamos qualquer precisão, pois Wi-Fi/IP Geolocation é impreciso por natureza.
    if (isMobile && accuracy > MOBILE_REJECT_THRESHOLD) {
      setGpsSignal('WEAK');
      // console.warn(`[GPS] Ignorando ponto impreciso (${accuracy}m) no mobile.`);
      return; 
    }

    // Atualiza estado visual
    setGpsSignal(signalQuality);

    const newCoords: [number, number] = [latitude, longitude];
    const kmh = (speed || 0) * 3.6;

    setCoords(newCoords);
    setCurrentSpeed(kmh);

    // 3. AUTO-ZOOM
    if (kmh <= 20) setZoomLevel(DRIVER_CONSTANTS.ZOOM_LEVELS.SLOW);
    else if (kmh <= 60) setZoomLevel(DRIVER_CONSTANTS.ZOOM_LEVELS.MEDIUM);
    else setZoomLevel(DRIVER_CONSTANTS.ZOOM_LEVELS.FAST);

    // 4. SINCRONIZAÇÃO (Throttling)
    const distanceMoved = lastCoords.current 
      ? calculateDistance(lastCoords.current, newCoords) 
      : MIN_MOVE_METERS + 1;
    const timeElapsed = now - lastSyncTime.current;

    if (distanceMoved >= MIN_MOVE_METERS || timeElapsed >= SYNC_INTERVAL_MS) {
      const telemetryPayload = {
        journey_id: journeyId,
        lat: latitude,
        lng: longitude,
        speed: kmh,
        accuracy,
        timestamp: now,
        ts: new Date().toISOString(),
        device_type: isMobile ? 'MOBILE' : 'DESKTOP' // Útil para debug no backend
      };

      if (context && context.isConnected) {
        context.sendMessage({
          type: 'TELEMETRY_UPDATE',
          payload: telemetryPayload
        });
      }

      // Persistência Local (Audit Trail)
      db.telemetry.add({
        ...telemetryPayload,
        sync_status: context?.isConnected ? 'synced' : 'pending',
        checksum: `tlm_${now}_${Math.random().toString(36).substring(7)}`
      }).catch(e => console.error("IndexedDB Telemetry Error:", e));

      lastSyncTime.current = now;
      lastCoords.current = newCoords;
    }
  }, [context, journeyId]);

  const handleError = useCallback((error: GeolocationPositionError) => {
    console.error("📡 [TELEMETRY_HARDWARE_FAIL]", error.message);
    setGpsSignal(error.code === 1 ? 'DENIED' : 'LOST');
    if (error.code === 1) {
      toast.error("Permissão de GPS Negada", { 
        description: "O cockpit precisa de acesso à localização para funcionar." 
      });
    }
  }, []);

  useEffect(() => {
    if (!enabled || typeof window === 'undefined' || !navigator.geolocation) {
      setGpsSignal('LOST');
      return;
    }

    // 🛡️ SECURITY CHECK: Secure Context (Chrome Requirement)
    // Permitimos localhost para desenvolvimento
    if (!window.isSecureContext && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      setGpsSignal('INSECURE');
      toast.error("Segurança de Contexto", { 
        description: "A telemetria exige conexão HTTPS estável." 
      });
      return;
    }

    watchId.current = navigator.geolocation.watchPosition(handlePosition, handleError, {
      enableHighAccuracy: true,
      timeout: 20000,
      maximumAge: 0 
    });

    const heartbeat = setInterval(() => {
      if (context?.isConnected) {
        context.sendMessage({ type: 'HEARTBEAT', ts: Date.now() });
      }
    }, 30000);

    return () => {
      if (watchId.current !== null) navigator.geolocation.clearWatch(watchId.current);
      clearInterval(heartbeat);
    };
  }, [enabled, handlePosition, handleError, context]);

  return { 
    coords, 
    currentSpeed, 
    zoomLevel, 
    gpsSignal, 
    isOffRoute, 
    isConnected: context?.isConnected ?? false 
  };
}