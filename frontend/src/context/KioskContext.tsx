// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 16:35:00
"use client";
import React, { createContext, useContext, useEffect, useReducer, useCallback, useState } from "react";
import { toast } from "sonner";
import { useParams } from "next/navigation";
import { validateKioskPassword } from "@/lib/api";

type KioskState = "IDLE" | "LOCKED" | "BREACHED" | "UNLOCKING";
type KioskAction = 
  | { type: "LOCK" } | { type: "UNLOCK" } | { type: "BREACH" }
  | { type: "ATTEMPT_UNLOCK" } | { type: "CANCEL_UNLOCK" };

export type UnlockResult = 
  | { ok: true }
  | { ok: false; reason: "INVALID_PASSWORD" | "LOCKED_OUT" | "NETWORK_ERROR" };

interface KioskContextType {
  state: KioskState;
  toggleLock: () => void;
  validateAndUnlock: (password: string) => Promise<UnlockResult>;
  lockoutEndTime: number | null;
}

const kioskReducer = (state: KioskState, action: KioskAction): KioskState => {
  switch (action.type) {
    case "LOCK": return "LOCKED";
    case "BREACH": return state === "IDLE" ? "IDLE" : "BREACHED";
    case "ATTEMPT_UNLOCK": return "UNLOCKING";
    case "CANCEL_UNLOCK": return "LOCKED";
    case "UNLOCK": return "IDLE";
    default: return state;
  }
};

const KioskContext = createContext<KioskContextType | null>(null);

export function KioskProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(kioskReducer, "IDLE");
  const [lockoutEndTime, setLockoutEndTime] = useState<number | null>(null);
  const [attempts, setAttempts] = useState(0);
  const params = useParams();
  const slug = params?.slug as string;

  useEffect(() => {
    const savedState = localStorage.getItem("mesaflow_kiosk_state");
    if (savedState === "LOCKED" || savedState === "BREACHED") dispatch({ type: "LOCK" });
  }, []);

  useEffect(() => { localStorage.setItem("mesaflow_kiosk_state", state); }, [state]);

  useEffect(() => {
    const handleChange = () => {
      const isFullscreen = !!document.fullscreenElement;
      if (!isFullscreen && (state === "LOCKED" || state === "UNLOCKING")) {
        dispatch({ type: "BREACH" });
      }
    };
    document.addEventListener("fullscreenchange", handleChange);
    return () => document.removeEventListener("fullscreenchange", handleChange);
  }, [state]);

  const validateAndUnlock = async (password: string): Promise<UnlockResult> => {
    if (!slug) return { ok: false, reason: "NETWORK_ERROR" };
    const now = Date.now();
    if (lockoutEndTime && now < lockoutEndTime) return { ok: false, reason: "LOCKED_OUT" };

    try {
      const res = await validateKioskPassword(slug, password);
      if (res.valid) {
        if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
        dispatch({ type: "UNLOCK" });
        setAttempts(0);
        setLockoutEndTime(null);
        toast.success("Modo Administrativo Liberado");
        return { ok: true };
      } else {
        const nextAttempts = attempts + 1;
        setAttempts(nextAttempts);
        if (nextAttempts >= 3) {
          setLockoutEndTime(Date.now() + 30000);
          return { ok: false, reason: "LOCKED_OUT" };
        }
        return { ok: false, reason: "INVALID_PASSWORD" };
      }
    } catch (e) {
      return { ok: false, reason: "NETWORK_ERROR" };
    }
  };

  const toggleLock = useCallback(async () => {
    if (state === "IDLE") {
      if (document.documentElement.requestFullscreen) {
        await document.documentElement.requestFullscreen().catch(() => {});
        dispatch({ type: "LOCK" });
        toast.success("🔒 Modo Totem Ativado");
      }
    } else if (state === "UNLOCKING") {
      dispatch({ type: "CANCEL_UNLOCK" });
    } else {
      dispatch({ type: "ATTEMPT_UNLOCK" });
    }
  }, [state]);

  return (
    <KioskContext.Provider value={{ state, toggleLock, validateAndUnlock, lockoutEndTime }}>
      {children}
    </KioskContext.Provider>
  );
}

export const useKiosk = () => {
  const context = useContext(KioskContext);
  if (!context) throw new Error("useKiosk must be used within KioskProvider");
  return context;
};

