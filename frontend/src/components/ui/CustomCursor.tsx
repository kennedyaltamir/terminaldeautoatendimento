/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.0.1 (Import Fix & Performance Edition)
 * DNA_ID: MF-UI-CURSOR-V2-FIX
 * Objective: Ultra-high performance cursor with contextual intelligence and GPU acceleration.
 * Fix: Added missing imports for framer-motion.
 */
"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion"; // 🛡️ FIX: Imports restaurados
import { cn } from "@/lib/utils";
import { ExternalLink, Move, Type, Play, Loader2 } from "lucide-react";

export default function CustomCursor() {
  // Refs para evitar re-renders e garantir 120fps (Otimização 1 e 3)
  const cursorRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);
  const mousePos = useRef({ x: 0, y: 0 });
  const cursorPos = useRef({ x: 0, y: 0 });
  const requestRef = useRef<number>();

  // Estados de Contexto (Otimização 5)
  const [mode, setMode] = useState<"default" | "pointer" | "text" | "drag" | "external" | "play" | "loading">("default");
  const [label, setLabel] = useState("");
  const [isMagnetic, setIsMagnetic] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [isTouch, setIsTouch] = useState(false);

  // 1. LERP (Linear Interpolation) para suavização premium (Otimização 2)
  const lerp = (start: number, end: number, factor: number) => start + (end - start) * factor;

  const animate = useCallback(() => {
    if (!cursorRef.current || !ringRef.current) return;

    // Fator de suavização (0.15 = fluidez orgânica)
    const factor = 0.15;
    
    cursorPos.current.x = lerp(cursorPos.current.x, mousePos.current.x, factor);
    cursorPos.current.y = lerp(cursorPos.current.y, mousePos.current.y, factor);

    // 🛡️ Otimização 1: Transform 3D para GPU Acceleration
    const transform = `translate3d(${cursorPos.current.x}px, ${cursorPos.current.y}px, 0)`;
    cursorRef.current.style.transform = transform;
    ringRef.current.style.transform = transform;

    requestRef.current = requestAnimationFrame(animate);
  }, []);

  useEffect(() => {
    // 🛡️ Otimização 10: Touch-Absolute Bypass
    const checkTouch = () => {
      setIsTouch(true);
      document.body.style.cursor = 'auto';
    };
    
    if (typeof window !== 'undefined') {
      window.addEventListener("touchstart", checkTouch, { once: true });
    }

    // 🛡️ Otimização 9: Respeitar prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion || isTouch) return;

    document.body.style.cursor = 'none';

    const onMouseMove = (e: MouseEvent) => {
      mousePos.current = { x: e.clientX, y: e.clientY };
      if (!isVisible) setIsVisible(true);
    };

    const onMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const interactive = target.closest('button, a, [role="button"]');
      const textInput = target.closest('input, textarea, [contenteditable="true"]');
      const dragZone = target.closest('[data-cursor="drag"]');
      const playZone = target.closest('[data-cursor="play"]');
      
      // 🛡️ Otimização 4: Magnetic Snapping
      const magnetic = target.closest('[data-magnetic="true"]');
      if (magnetic) {
        const rect = magnetic.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        mousePos.current = { x: centerX, y: centerY };
        setIsMagnetic(true);
      } else {
        setIsMagnetic(false);
      }

      // 🛡️ Otimização 5 & 7: Contextual Shapes & Text Reveal
      if (playZone) { setMode("play"); setLabel("PLAY"); }
      else if (dragZone) { setMode("drag"); setLabel(""); }
      else if (textInput) { setMode("text"); setLabel(""); }
      else if (interactive) {
        const isExternal = interactive.getAttribute('target') === '_blank';
        setMode(isExternal ? "external" : "pointer");
        setLabel("");
      } else {
        setMode("default");
        setLabel("");
      }
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseover", onMouseOver);
    requestRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseover", onMouseOver);
      window.removeEventListener("touchstart", checkTouch);
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
      document.body.style.cursor = 'auto';
    };
  }, [animate, isVisible, isTouch]);

  if (isTouch || !isVisible) return null;

  return (
    <div className="pointer-events-none fixed inset-0 z-[999999] overflow-hidden">
      {/* Ponto Central (GPU Accelerated) */}
      <div
        ref={cursorRef}
        className={cn(
          "fixed top-0 left-0 w-2 h-2 bg-orange-500 rounded-full will-change-transform z-50 transition-transform duration-300",
          mode !== "default" && "scale-0"
        )}
        style={{ mixBlendMode: 'difference' }} // 🛡️ Otimização 8: Adaptive Blend
      />

      {/* Anel Externo (Smooth Ring with RAF) */}
      <div
        ref={ringRef}
        className={cn(
          "fixed top-0 left-0 flex items-center justify-center rounded-full border border-orange-500/50 will-change-transform transition-all duration-500 ease-out",
          mode === "default" ? "w-8 h-8 -ml-4 -mt-4" : "w-16 h-16 -ml-8 -mt-8 bg-white/10 backdrop-blur-[2px] border-white",
          isMagnetic && "scale-125 border-orange-400 bg-orange-500/20",
          mode === "loading" && "border-dashed animate-spin" // 🛡️ Otimização 6: Progress Ring
        )}
        style={{ mixBlendMode: 'difference' }}
      >
        <AnimatePresence mode="wait">
          {mode === "external" && (
            <motion.div 
              key="external"
              initial={{ opacity: 0, scale: 0 }} 
              animate={{ opacity: 1, scale: 1 }} 
              exit={{ opacity: 0, scale: 0 }}
            >
              <ExternalLink size={12} className="text-white" />
            </motion.div>
          )}
          {mode === "drag" && (
            <motion.div key="drag" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Move size={16} className="text-white" />
            </motion.div>
          )}
          {mode === "text" && (
            <motion.div key="text" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="w-[1px] h-4 bg-white animate-pulse" />
            </motion.div>
          )}
          {mode === "play" && (
            <motion.div key="play" initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.5 }}>
              <Play size={16} className="text-white fill-current" />
            </motion.div>
          )}
          {label && (
            <motion.span 
              key="label"
              initial={{ opacity: 0, y: 5 }} 
              animate={{ opacity: 1, y: 0 }} 
              exit={{ opacity: 0, y: -5 }}
              className="text-[8px] font-black tracking-tighter text-white uppercase"
            >
              {label}
            </motion.span>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}