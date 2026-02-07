/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Botão de Ativação do Modo Totem.
 * FEATURES: Stealth Trigger (Cantos da tela) e Botão Explícito.
 */
"use client";
import React, { useState, useEffect } from "react";
import { Maximize, Minimize, RefreshCw } from "lucide-react";
import { useKiosk } from "@/context/KioskContext";

export default function KioskFullscreenToggle() {
  const { state, isFullscreen, toggleLock, isOffline } = useKiosk();
  const [sequence, setSequence] = useState<number[]>([]);

  // --- LÓGICA: SEQUÊNCIA SECRETA (Stealth Trigger) ---
  // Tocar nos 4 cantos em sentido horário (TopLeft -> TopRight -> BottomRight -> BottomLeft)
  useEffect(() => {
    if (sequence.length === 0) return;
    const timer = setTimeout(() => setSequence([]), 3000); // Reset após 3s
    if (sequence.length === 4) {
      if (sequence.join('') === '1234') toggleLock();
      setSequence([]);
    }
    return () => clearTimeout(timer);
  }, [sequence, toggleLock]);

  // Se estiver em modo de contingência ou violado, não mostra o botão padrão
  if (state === "BREACHED" || state === "CONTINGENCY") return null;

  // Mostra o botão se estiver em IDLE OU se estiver em LOCKED mas o navegador bloqueou o Fullscreen
  const showActivationButton = state === "IDLE" || (state === "LOCKED" && !isFullscreen);

  return (
    <>
      {/* Zonas de Manutenção (Invisíveis) */}
      <div className="fixed top-0 left-0 w-24 h-24 z-[10000]" onClick={() => setSequence(p => [...p, 1])} />
      <div className="fixed top-0 right-0 w-24 h-24 z-[10000]" onClick={() => setSequence(p => [...p, 2])} />
      <div className="fixed bottom-0 right-0 w-24 h-24 z-[10000]" onClick={() => setSequence(p => [...p, 3])} />
      <div className="fixed bottom-0 left-0 w-24 h-24 z-[10000]" onClick={() => setSequence(p => [...p, 4])} />

      {showActivationButton && (
        <div className="fixed inset-0 flex items-center justify-center bg-slate-950/80 backdrop-blur-md z-[9990] animate-in fade-in duration-500">
          <div className="text-center space-y-6">
            <div className="bg-orange-500/10 p-6 rounded-full w-24 h-24 mx-auto flex items-center justify-center border border-orange-500/20">
              <Maximize size={48} className="text-orange-500" />
            </div>
            <div className="space-y-2">
              <h2 className="text-2xl font-black text-white uppercase tracking-tighter">
                {state === "LOCKED" ? "Sessão Interrompida" : "Modo Totem"}
              </h2>
              <p className="text-slate-400 text-sm max-w-xs mx-auto">
                {state === "LOCKED" 
                  ? "O navegador saiu do modo tela cheia. Clique abaixo para restaurar a segurança." 
                  : "Clique para travar a interface e iniciar o autoatendimento."}
              </p>
            </div>
            <button 
              onClick={toggleLock}
              className="bg-orange-600 hover:bg-orange-700 text-white px-12 py-6 rounded-[2rem] font-black text-xl shadow-2xl shadow-orange-900/40 transition-all active:scale-95 flex items-center gap-4 mx-auto border-4 border-white/10"
            >
              {state === "LOCKED" ? <RefreshCw size={28} /> : <Maximize size={28} />}
              {state === "LOCKED" ? "RESTAURAR TOTEM" : "ATIVAR MODO TOTEM"}
            </button>
          </div>
        </div>
      )}

      {/* Botão de Manutenção (Visível apenas para admin em fullscreen) */}
      {state !== "IDLE" && isFullscreen && (
        <button
          onClick={toggleLock}
          className="fixed top-4 right-4 z-[100] p-4 rounded-2xl bg-slate-900/20 text-slate-500 opacity-0 hover:opacity-100 transition-opacity"
        >
          <Minimize size={24} />
        </button>
      )}
    </>
  );
}
