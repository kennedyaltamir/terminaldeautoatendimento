import { useState, useEffect, useRef } from "react";

export function useDriverTimers(isEnRoute: boolean, waitingSince: number | null) {
  const [shiftDuration, setShiftDuration] = useState("00:00");
  const [elapsedWait, setElapsedWait] = useState("00:00");
  const shiftStartRef = useRef(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      
      const shiftDiff = Math.floor((now - shiftStartRef.current) / 60000);
      const h = Math.floor(shiftDiff / 60).toString().padStart(2, '0');
      const m = (shiftDiff % 60).toString().padStart(2, '0');
      setShiftDuration(`${h}:${m}`);

      if (waitingSince) {
        const waitDiff = Math.floor((now - waitingSince) / 1000);
        const wm = Math.floor(waitDiff / 60).toString().padStart(2, '0');
        const ws = (waitDiff % 60).toString().padStart(2, '0');
        setElapsedWait(`${wm}:${ws}`);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [waitingSince]);

  return { shiftDuration, elapsedWait };
}
