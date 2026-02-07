/**
 * DOMAIN: FRONTEND / SECURITY
 * OBJECTIVE: Sentinela de Eventos (Trap Mode Enforcer).
 * FEATURES: Bloqueio de atalhos, menu de contexto, seleção e navegação.
 */
"use client";
import { useEffect } from "react";
import { useKiosk } from "@/context/KioskContext";
import { useCart } from "@/context/CartContext";

export default function KioskGuard() {
  const { state, triggerBreach } = useKiosk();
  const { clearCart } = useCart();

  // Limpeza de dados em caso de violação
  useEffect(() => {
    if (state === "BREACHED") {
      clearCart();
    }
  }, [state, clearCart]);

  useEffect(() => {
    if (state === "IDLE") return;

    // 1. Bloqueio de Saída (BeforeUnload) - Impede fechar a aba
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      return (e.returnValue = "Acesso restrito. Insira a senha administrativa.");
    };

    // 2. Detecção de Perda de Foco (Alt+Tab / Mudança de App)
    const handleBlur = () => {
      if (state === "LOCKED") {
          console.warn("🚨 [KioskGuard] Perda de foco detectada.");
          triggerBreach();
      }
    };

    // 3. Detecção de Saída de Fullscreen (ESC ou F11)
    const handleFullscreenChange = () => {
      if (!document.fullscreenElement && state === "LOCKED") {
        console.error("🚨 [KioskGuard] Violação de Fullscreen detectada.");
        triggerBreach();
      }
    };

    // 4. Bloqueio de Multitouch (Gestos de SO como 'swipe to switch app')
    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length > 2) { // 3 ou mais dedos
        e.preventDefault();
        e.stopPropagation();
      }
    };

    // 5. Bloqueio de Teclas de Atalho (F5, F11, Ctrl+R, Alt+F4, etc)
    const handleKeyDown = (e: KeyboardEvent) => {
      const blockedKeys = ["f5", "f11", "f12", "r", "l", "w", "t", "n", "j", "p", "s", "tab"];
      const isCtrlOrMeta = e.ctrlKey || e.metaKey || e.altKey;
      
      if (
        (blockedKeys.includes(e.key.toLowerCase()) && isCtrlOrMeta) || 
        e.key === "F5" || 
        e.key === "F11" ||
        e.key === "Escape" ||
        e.key === "ContextMenu"
      ) {
        e.preventDefault();
        e.stopPropagation();
        console.warn(`🚫 [KioskGuard] Tecla bloqueada: ${e.key}`);
      }
    };

    // 6. Bloqueio de Botão Direito (Context Menu)
    const handleContextMenu = (e: MouseEvent) => e.preventDefault();

    // Aplicação de Estilos CSS de Bloqueio (Hardening Visual)
    document.body.style.userSelect = "none";
    document.body.style.webkitUserSelect = "none";
    document.body.style.touchAction = "pan-y"; // Permite scroll vertical, bloqueia zoom/pan lateral
    document.body.style.overflow = "hidden"; // Evita scroll da página inteira (app deve gerenciar scroll interno)

    // Listeners
    window.addEventListener("beforeunload", handleBeforeUnload);
    window.addEventListener("blur", handleBlur);
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("contextmenu", handleContextMenu);
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    document.addEventListener("touchstart", handleTouchStart, { passive: false });

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      window.removeEventListener("blur", handleBlur);
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("contextmenu", handleContextMenu);
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
      document.removeEventListener("touchstart", handleTouchStart);
      
      // Cleanup CSS
      document.body.style.userSelect = "";
      document.body.style.webkitUserSelect = "";
      document.body.style.touchAction = "";
      document.body.style.overflow = "";
    };
  }, [state, triggerBreach]);

  return null;
}
