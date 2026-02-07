/**
 * Author: MESAFLOW_AI
 * Version: 12.4 (Cleaned)
 * FIX: Removido log de debug residual.
 */
"use client";
import { useState, useEffect, useCallback } from "react";
import { useKiosk } from "@/context/KioskContext";

export default function KioskStealthTrigger() {
  const { toggleLock, state } = useKiosk();
  const [sequence, setSequence] = useState<number[]>([]);

  useEffect(() => {
    if (sequence.length === 0) return;
    const timer = setTimeout(() => setSequence([]), 3000);

    if (sequence.length === 4) {
      const target = [1, 2, 3, 4];
      const isMatch = sequence.every((val, index) => val === target[index]);
      if (isMatch) {
        toggleLock();
      }
      setSequence([]);
    }
    return () => clearTimeout(timer);
  }, [sequence, toggleLock]);

  const handleTap = useCallback((zone: number, e: React.MouseEvent | React.TouchEvent) => {
    e.stopPropagation();
    // Não usamos preventDefault para permitir que o browser registre a interação física
    setSequence(prev => [...prev, zone]);
  }, []);

  if (state === "IDLE") {
    return (
      <button 
        onClick={toggleLock}
        className="fixed bottom-4 right-4 bg-red-600 text-white px-6 py-3 rounded-full text-xs font-black z-[200000] shadow-2xl animate-pulse"
      >
        ATIVAR MODO TOTEM
      </button>
    );
  }

  // Z-index 200.000 e pointer-events: auto garantem que o clique chegue aqui
  const zoneClass = "fixed w-40 h-40 z-[200000] cursor-none opacity-0 pointer-events-auto";

  return (
    <>
      <div className={zoneClass + " top-0 left-0"} onMouseDown={(e) => handleTap(1, e)} onTouchStart={(e) => handleTap(1, e)} />
      <div className={zoneClass + " top-0 right-0"} onMouseDown={(e) => handleTap(2, e)} onTouchStart={(e) => handleTap(2, e)} />
      <div className={zoneClass + " bottom-0 right-0"} onMouseDown={(e) => handleTap(3, e)} onTouchStart={(e) => handleTap(3, e)} />
      <div className={zoneClass + " bottom-0 left-0"} onMouseDown={(e) => handleTap(4, e)} onTouchStart={(e) => handleTap(4, e)} />
    </>
  );
}
