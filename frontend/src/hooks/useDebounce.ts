/**
 * Author: MESAFLOW_AI
 * Version: 1.0
 * DNA_ID: hook-debounce-v1
 * Objective: Optimize search inputs and prevent excessive re-renders.
 */
import { useEffect, useState } from "react";

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

