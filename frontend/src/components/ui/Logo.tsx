"use client";

import { ChefHat } from "lucide-react";
import { motion } from "framer-motion";

interface LogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "light" | "dark" | "color";
  animated?: boolean;
}

export default function Logo({ size = "md", variant = "color", animated = false }: LogoProps) {
  const sizes = {
    sm: { icon: 20, text: "text-lg" },
    md: { icon: 28, text: "text-2xl" },
    lg: { icon: 40, text: "text-4xl" },
    xl: { icon: 64, text: "text-6xl" },
  };

  const colors = {
    light: "text-white",
    dark: "text-slate-900 dark:text-white",
    color: "text-slate-900 dark:text-white",
  };

  const iconBg = variant === "color" ? "bg-orange-600 text-white" : "bg-transparent border-2 border-current";

  return (
    <div className={`flex items-center gap-3 font-black tracking-tighter ${colors[variant]} group`}>
      <motion.div
        whileHover={animated ? { rotate: 12, scale: 1.1 } : {}}
        className={`${iconBg} p-2 rounded-2xl shadow-lg shadow-orange-600/20 transition-all`}
      >
        <ChefHat size={sizes[size].icon} strokeWidth={2.5} />
      </motion.div>
      <span className={sizes[size].text}>
        MesaFlow
        {variant === "color" && <span className="text-orange-600">.</span>}
      </span>
    </div>
  );
}
