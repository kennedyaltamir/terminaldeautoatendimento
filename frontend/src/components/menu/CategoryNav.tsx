/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Navegação "Scroll Spy" com animação fluida (Apple-style).
 * FEATURES: Indicador deslizante (LayoutId), Sticky Header e Haptics.
 */
"use client";
import { useEffect, useRef } from "react";
import { Category } from "@/types";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface CategoryNavProps {
  categories: Category[];
  activeId: number;
  onSelect: (id: number) => void;
  primaryColor: string;
}

export default function CategoryNav({ categories, activeId, onSelect, primaryColor }: CategoryNavProps) {
  const navRef = useRef<HTMLDivElement>(null);

  // Auto-scroll para manter a categoria ativa visível
  useEffect(() => {
    if (navRef.current) {
      const activeBtn = navRef.current.querySelector(`[data-active="true"]`) as HTMLElement;
      if (activeBtn) {
        const containerLeft = navRef.current.getBoundingClientRect().left;
        const activeLeft = activeBtn.getBoundingClientRect().left;
        const scrollOffset = activeLeft - containerLeft - (navRef.current.offsetWidth / 2) + (activeBtn.offsetWidth / 2);
        navRef.current.scrollBy({ left: scrollOffset, behavior: "smooth" });
      }
    }
  }, [activeId]);

  return (
    <div className="bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-gray-100 dark:border-slate-800 shadow-sm sticky top-[88px] z-20">
      <div 
        ref={navRef}
        className="flex overflow-x-auto no-scrollbar py-4 px-4 gap-2 scroll-smooth"
      >
        {categories.map((cat) => {
          const isActive = activeId === cat.id;
          return (
            <button
              key={cat.id}
              data-active={isActive}
              onClick={() => onSelect(cat.id)}
              className={cn(
                "relative px-6 py-3 rounded-full text-sm font-black uppercase tracking-wide transition-colors z-10 shrink-0",
                isActive ? "text-white" : "text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="activeCategory"
                  className="absolute inset-0 rounded-full -z-10 shadow-lg"
                  style={{ backgroundColor: primaryColor }}
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              {cat.name}
            </button>
          );
        })}
      </div>
    </div>
  );
}
