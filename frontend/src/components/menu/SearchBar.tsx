"use client";

import { Search } from "lucide-react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  primaryColor: string;
  placeholder?: string;
}

export default function SearchBar({ 
  value, 
  onChange, 
  primaryColor, 
  placeholder = "Buscar produtos..." 
}: SearchBarProps) {
  return (
    <div className="relative">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-4 py-3 rounded-xl bg-gray-100 dark:bg-gray-800 border-none outline-none focus:ring-2 transition-all text-gray-900 dark:text-white"
        style={{ 
          // @ts-ignore - Custom CSS property for dynamic color
          "--tw-ring-color": primaryColor 
        }}
      />
      <Search 
        className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" 
        size={20} 
      />
    </div>
  );
}