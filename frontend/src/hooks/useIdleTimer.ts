import { useState, useEffect, useRef, useCallback } from 'react';

interface UseIdleTimerProps {
  timeout: number; // Tempo em ms para considerar inativo
  onIdle: () => void; // Callback quando ficar inativo
  onActive?: () => void; // Callback quando voltar a ser ativo
}

export function useIdleTimer({ timeout, onIdle, onActive }: UseIdleTimerProps) {
  const [isIdle, setIsIdle] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

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
    // Eventos que resetam o timer
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    const handleEvent = () => resetTimer();

    events.forEach(event => {
      window.addEventListener(event, handleEvent);
    });

    // Inicia o timer
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
