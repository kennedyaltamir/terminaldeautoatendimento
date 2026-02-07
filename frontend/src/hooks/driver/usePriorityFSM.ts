/**
 * Author: MESAFLOW_AI
 * Version: 1.1.0 (Type Safe Timers)
 * DNA_ID: MF-HOOK-PRIO-FSM-V1
 */
import { useState, useRef, useCallback } from 'react';
import { toast } from 'sonner';

type EventType = 'INCIDENT' | 'CANCEL' | 'ARRIVED' | 'POD_ATTEMPT';
interface PriorityEvent {
  type: EventType;
  payload: any;
  timestamp: number;
  priority: number;
}

export function usePriorityFSM() {
  const [queue, setQueue] = useState<PriorityEvent[]>([]);
  const [podAttempts, setPodAttempts] = useState(0);
  const [isPodLocked, setIsPodLocked] = useState(false);
  
  // 🛡️ FIX: Usando ReturnType para compatibilidade universal de Timers
  const lockoutTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const enqueueEvent = useCallback((type: EventType, payload: any) => {
    const priorityMap: Record<EventType, number> = {
      'INCIDENT': 0,
      'CANCEL': 1,
      'ARRIVED': 2,
      'POD_ATTEMPT': 3
    };

    const newEvent: PriorityEvent = {
      type,
      payload,
      timestamp: Date.now(),
      priority: priorityMap[type]
    };

    setQueue(prev => [...prev, newEvent].sort((a, b) => a.priority - b.priority));
  }, []);

  const validatePOD = useCallback(async (inputCode: string, correctCode: string) => {
    if (isPodLocked) {
      toast.error("Validação bloqueada temporariamente.");
      return false;
    }

    if (inputCode === correctCode) {
      setPodAttempts(0);
      return true;
    } else {
      const newAttempts = podAttempts + 1;
      setPodAttempts(newAttempts);
      
      if (newAttempts >= 3) {
        setIsPodLocked(true);
        toast.error("Muitas tentativas. Bloqueio de 60s.");
        
        lockoutTimer.current = setTimeout(() => {
          setIsPodLocked(false);
          setPodAttempts(0);
        }, 60000);
      }
      return false;
    }
  }, [podAttempts, isPodLocked]);

  return { queue, enqueueEvent, validatePOD, isPodLocked };
}
