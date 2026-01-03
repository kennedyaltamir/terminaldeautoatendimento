"use client";

import { useEffect, useRef } from "react";
import { Category } from "@/types";

interface CategoryNavProps {
  categories: Category[];
  activeId: number;
  onSelect: (id: number) => void;
  primaryColor: string;
}

export default function CategoryNav({ categories, activeId, onSelect, primaryColor }: CategoryNavProps) {
  const navRef = useRef<HTMLDivElement>(null);

  // Auto-scroll horizontal da barra de navegação para manter a aba ativa visível
  useEffect(() => {
    if (navRef.current) {
      const activeBtn = navRef.current.querySelector(`[data-id="${activeId}"]`) as HTMLElement;
      if (activeBtn) {
        const containerLeft = navRef.current.getBoundingClientRect().left;
        const activeLeft = activeBtn.getBoundingClientRect().left;
        const scrollOffset = activeLeft - containerLeft - (navRef.current.offsetWidth / 2) + (activeBtn.offsetWidth / 2);
        
        navRef.current.scrollBy({ left: scrollOffset, behavior: "smooth" });
      }
    }
  }, [activeId]);

  return (
    <div className="bg-white border-b border-gray-100 shadow-sm">
      <div 
        ref={navRef}
        className="flex overflow-x-auto no-scrollbar py-3 px-4 gap-3 scroll-smooth"
      >
        {categories.map((cat) => {
          const isActive = activeId === cat.id;
          return (
            <button
              key={cat.id}
              data-id={cat.id}
              onClick={() => onSelect(cat.id)}
              className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-bold transition-all duration-300 ${
                isActive 
                  ? "text-white shadow-md scale-105" 
                  : "bg-gray-100 text-gray-500 hover:bg-gray-200"
              }`}
              style={{ 
                backgroundColor: isActive ? primaryColor : undefined,
              }}
            >
              {cat.name}
            </button>
          );
        })}
      </div>
    </div>
  );
}