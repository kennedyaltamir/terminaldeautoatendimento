"use client";

import { useState, useEffect } from "react";
import { useKiosk } from "@/context/KioskContext";

/**
 * Stealth Trigger
 * Padrão de Desbloqueio: Top-Left -> Top-Right -> Bottom-Right -> Bottom-Left (Sentido Horário)
 * Timeout: 3 segundos para completar a sequência.
 */
export default function KioskStealthTrigger() {
  const { toggleLock, state } = useKiosk();
  const [sequence, setSequence] = useState<number[]>([]);

  useEffect(() => {
    if (sequence.length === 0) return;

    // Reset se demorar muito
    const timer = setTimeout(() => setSequence([]), 3000);
    
    // Valida sequência: 1 -> 2 -> 3 -> 4
    const target = [1, 2, 3, 4];
    const isMatch = sequence.every((val, index) => val === target[index]);

    if (!isMatch) {
      setSequence([]); // Errou, reseta
    } else if (sequence.length === 4) {
      toggleLock();
      setSequence([]);
    }

    return () => clearTimeout(timer);
  }, [sequence, toggleLock]);

  const handleTap = (zone: number) => {
    setSequence(prev => [...prev, zone]);
  };

  // Se já estiver destravado (IDLE), mostra um botão visível para facilitar o setup inicial
  if (state === "IDLE") {
    return (
      <button 
        onClick={toggleLock}
        className="fixed bottom-4 right-4 bg-red-600 text-white px-4 py-2 rounded-full text-xs font-bold z-[9999] shadow-lg animate-pulse"
      >
        ATIVAR MODO TOTEM
      </button>
    );
  }

  // Zonas Invisíveis (Z-Index Máximo)
  return (
    <>
      {/* Top Left (1) */}
      <div className="fixed top-0 left-0 w-20 h-20 z-[9999]" onClick={() => handleTap(1)} />
      {/* Top Right (2) */}
      <div className="fixed top-0 right-0 w-20 h-20 z-[9999]" onClick={() => handleTap(2)} />
      {/* Bottom Right (3) */}
      <div className="fixed bottom-0 right-0 w-20 h-20 z-[9999]" onClick={() => handleTap(3)} />
      {/* Bottom Left (4) */}
      <div className="fixed bottom-0 left-0 w-20 h-20 z-[9999]" onClick={() => handleTap(4)} />
    </>
  );
}

