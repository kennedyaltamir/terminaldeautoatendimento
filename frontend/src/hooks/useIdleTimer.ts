/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Idle Timer with environment-agnostic typing.
 */
import { useState, useEffect, useRef, useCallback } from 'react';

interface UseIdleTimerProps {
  timeout: number;
  onIdle: () => void;
  onActive?: () => void;
}

export function useIdleTimer({ timeout, onIdle, onActive }: UseIdleTimerProps) {
  const [isIdle, setIsIdle] = useState(false);
  // 🛡️ FIX TS2322: ReturnType garante compatibilidade entre Browser e Node
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const resetTimer = useCallback(() => {
    if (isIdle) {
      setIsIdle(false);
      onActive?.();
    }
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
    timerRef.current = setTimeout(() => {
      setIsIdle(true);
      onIdle();
    }, timeout);
  }, [timeout, onIdle, onActive, isIdle]);

  useEffect(() => {
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    const handleEvent = () => resetTimer();
    
    events.forEach(event => {
      window.addEventListener(event, handleEvent);
    });

    resetTimer();

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      events.forEach(event => {
        window.removeEventListener(event, handleEvent);
      });
    };
  }, [resetTimer]);

  return { isIdle, resetTimer };
}
