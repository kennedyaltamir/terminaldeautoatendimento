/**
 * DOMAIN: FRONTEND / UX
 * OBJECTIVE: Centralized Haptic Feedback Engine (Config-Driven).
 */
"use client";

import { useCallback } from "react";
import { DRIVER_CONSTANTS } from "@/lib/constants/driver";

type HapticPattern = 'success' | 'warning' | 'error' | 'click' | 'heavy';

export function useDriverHaptics() {
  const trigger = useCallback((pattern: HapticPattern) => {
    if (typeof navigator === 'undefined' || !navigator.vibrate) return;

    const vibration = DRIVER_CONSTANTS.HAPTIC[pattern.toUpperCase() as keyof typeof DRIVER_CONSTANTS.HAPTIC];
    if (vibration) navigator.vibrate(vibration);
  }, []);

  return { trigger };
}
