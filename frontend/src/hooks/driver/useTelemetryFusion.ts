/**
 * DOMAIN: TELEMETRY / SENSORS
 * LOGIC: Sensor Fusion (GPS + Accelerometer) & Outlier Detection
 */
import { useState, useEffect, useRef } from 'react';

interface TelemetryPoint {
  lat: number;
  lng: number;
  speed: number; // m/s
  accuracy: number;
  timestamp: number;
  isTrusted: boolean;
}

export function useTelemetryFusion(isTracking: boolean) {
  const [currentPoint, setCurrentPoint] = useState<TelemetryPoint | null>(null);
  const [isMotionDetected, setIsMotionDetected] = useState(false);
  
  // Refs para cálculo de Dead Reckoning
  const lastAccel = useRef({ x: 0, y: 0, z: 0 });
  const stationaryTime = useRef(0);

  useEffect(() => {
    if (!isTracking || typeof window === 'undefined') return;

    // 1. Acelerômetro (Motion Detection)
    const handleMotion = (event: DeviceMotionEvent) => {
      const { x, y, z } = event.accelerationIncludingGravity || { x:0, y:0, z:0 };
      const magnitude = Math.sqrt((x||0)**2 + (y||0)**2 + (z||0)**2);
      
      // Threshold de movimento (ex: > 10.5 m/s² considerando gravidade)
      if (magnitude > 10.5 || magnitude < 9.5) {
        setIsMotionDetected(true);
        stationaryTime.current = 0;
      } else {
        stationaryTime.current += 100; // assumindo ~100ms de intervalo
        if (stationaryTime.current > 3000) setIsMotionDetected(false);
      }
      lastAccel.current = { x: x||0, y: y||0, z: z||0 };
    };

    // 2. GPS (Positioning)
    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        const { latitude, longitude, speed, accuracy } = pos.coords;
        
        // 🛡️ Filtro de Drift/Outlier
        if (accuracy > 100) {
          console.warn("[TELEMETRY] Discarding low accuracy point:", accuracy);
          return;
        }

        // 🛡️ Anti-Spoofing Check
        // Se GPS diz que está rápido (>20km/h) mas acelerômetro diz parado por >5s
        const isSpoofSuspect = (speed || 0) > 5.5 && !isMotionDetected && stationaryTime.current > 5000;
        
        const point: TelemetryPoint = {
          lat: latitude,
          lng: longitude,
          speed: speed || 0,
          accuracy,
          timestamp: Date.now(),
          isTrusted: !isSpoofSuspect
        };

        if (isSpoofSuspect) {
            // Logar em tabela de ruído para auditoria
            // api.logTelemetryNoise(point);
        }

        setCurrentPoint(point);
      },
      (err) => console.error("[GPS] Error:", err),
      { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
    );

    window.addEventListener('devicemotion', handleMotion);

    return () => {
      navigator.geolocation.clearWatch(watchId);
      window.removeEventListener('devicemotion', handleMotion);
    };
  }, [isTracking, isMotionDetected]);

  return { currentPoint, isMotionDetected };
}