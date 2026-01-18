"use client";

import { useState, useRef, useEffect } from "react";
import { Maximize, Lock } from "lucide-react";
import { useKiosk } from "@/context/KioskContext";

export default function KioskFullscreenToggle() {
  const { state, toggleLock } = useKiosk();
  const [sequence, setSequence] = useState<number[]>([]);

  const isLocked = state === "LOCKED" || state === "BREACHED" || state === "UNLOCKING";

  useEffect(() => {
    if (sequence.length === 0) return;

    const timer = setTimeout(() => setSequence([]), 3000);
    
    const target = [1, 2, 3, 4];
    const isMatch = sequence.every((val, index) => val === target[index]);

    if (!isMatch) {
      setSequence([]); 
    } else if (sequence.length === 4) {
      toggleLock();
      setSequence([]);
    }

    return () => clearTimeout(timer);
  }, [sequence, toggleLock]);

  const handleTap = (zone: number) => {
    setSequence(prev => [...prev, zone]);
  };

  return (
    <>
      {/* Botão Visível (Apenas IDLE) */}
      {state === "IDLE" && (
        <button 
          onClick={toggleLock}
          className="fixed bottom-4 right-4 bg-red-600 text-white px-4 py-2 rounded-full text-xs font-bold z-[9998] shadow-lg animate-pulse"
        >
          ATIVAR MODO TOTEM
        </button>
      )}

      {/* Zonas Invisíveis (Sempre Ativas para Manutenção) */}
      {/* Z-Index 9999 garante que fiquem acima de tudo, inclusive do botão visível se sobreposto */}
      <div className="fixed top-0 left-0 w-20 h-20 z-[9999]" onClick={() => handleTap(1)} />
      <div className="fixed top-0 right-0 w-20 h-20 z-[9999]" onClick={() => handleTap(2)} />
      <div className="fixed bottom-0 right-0 w-20 h-20 z-[9999]" onClick={() => handleTap(3)} />
      <div className="fixed bottom-0 left-0 w-20 h-20 z-[9999]" onClick={() => handleTap(4)} />
      
      {/* Ícone de Status (Apenas Locked) */}
      {isLocked && (
        <div className="fixed bottom-0 right-0 w-24 h-24 z-[9990] flex items-end justify-end p-4 opacity-0 hover:opacity-100 transition-opacity duration-500 pointer-events-none">
          <div className="bg-white/10 backdrop-blur-md p-2 rounded-full text-white/20 border border-white/5">
            <Lock size={20} />
          </div>
        </div>
      )}
    </>
  );
}

