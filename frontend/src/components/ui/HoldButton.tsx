"use client";
import React, { useState, useRef } from "react";
import { motion, useAnimation } from "framer-motion";
import { cn } from "@/lib/utils";

interface HoldButtonProps {
  onComplete: () => void;
  label: string;
  icon?: React.ReactNode;
  color?: string;
  duration?: number;
  className?: string;
  "data-testid"?: string;
}

export default function HoldButton({ 
  onComplete, 
  label, 
  icon, 
  color = "bg-orange-600", 
  duration = 800,
  className,
  "data-testid": testId
}: HoldButtonProps) {
  const [isHolding, setIsHolding] = useState(false);
  const controls = useAnimation();
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const startHold = () => {
    setIsHolding(true);
    controls.start({ 
      width: "100%", 
      transition: { duration: duration / 1000, ease: "linear" } 
    });

    timeoutRef.current = setTimeout(() => {
      // 🛡️ FIX: console.log -> console.info para manter sinalização de teste mas limpar debug
      console.info(`[HOLD_COMPLETE] ${label}`); 
      if (navigator.vibrate) navigator.vibrate(50);
      onComplete();
      setIsHolding(false);
      controls.set({ width: "0%" });
    }, duration + 50); // Margem de segurança de 50ms
  };

  const endHold = () => {
    setIsHolding(false);
    controls.stop();
    controls.set({ width: "0%" });
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  };

  return (
    <div 
      className={cn("relative overflow-hidden rounded-2xl select-none touch-none cursor-pointer", className)}
      onMouseDown={startHold}
      onMouseUp={endHold}
      onMouseLeave={endHold}
      onTouchStart={startHold}
      onTouchEnd={endHold}
      data-testid={testId}
    >
      <div className="absolute inset-0 bg-slate-800" />
      <motion.div className={cn("absolute inset-0 z-10", color)} initial={{ width: "0%" }} animate={controls} />
      <div className="relative z-20 flex items-center justify-center gap-3 w-full h-full py-4 px-6 pointer-events-none">
        {icon}
        <span className="font-black uppercase tracking-widest text-xs text-white">
          {isHolding ? "SEGURE..." : label}
        </span>
      </div>
    </div>
  );
}
