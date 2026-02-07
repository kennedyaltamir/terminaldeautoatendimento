"use client";
import React from "react";
import { motion } from "framer-motion";
import { ArrowUpRight, ArrowDownRight, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

interface KPICardProps {
  title: string;
  value: string | number;
  trend: number;
  variant?: "default" | "hero";
  isSimulated?: boolean;
}

export default function KPICard({ title, value, trend, variant = "default", isSimulated }: KPICardProps) {
  const isPositive = trend > 0;

  return (
    <motion.div 
      whileHover={{ y: -5, scale: 1.01 }}
      className={cn(
        "border p-8 rounded-[2.5rem] shadow-2xl transition-all relative overflow-hidden",
        variant === "hero" 
          ? "bg-gradient-to-br from-orange-600 to-orange-700 border-orange-500" 
          : "bg-slate-900/50 border-slate-800",
        isSimulated && "ring-2 ring-orange-500/50 ring-offset-4 ring-offset-black"
      )}
    >
      <div className="flex justify-between items-start mb-6">
        <p className={cn(
          "text-[10px] font-black uppercase tracking-[0.2em]",
          variant === "hero" ? "text-orange-100" : "text-slate-500"
        )}>
          {title}
        </p>
        <div className={cn(
          "px-3 py-1 rounded-full text-[11px] font-black flex items-center gap-1 backdrop-blur-md",
          variant === "hero" 
            ? "bg-white/20 text-white" 
            : isPositive ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"
        )}>
          {isPositive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          {Math.abs(trend)}%
        </div>
      </div>

      <div className="flex items-baseline gap-3">
        <h3 className={cn(
          "font-black tracking-tighter leading-none",
          variant === "hero" ? "text-5xl md:text-6xl text-white" : "text-4xl text-white"
        )}>
          {value}
        </h3>
        {isSimulated && <Zap size={20} className="text-orange-300 fill-orange-300 animate-pulse" />}
      </div>
    </motion.div>
  );
}
