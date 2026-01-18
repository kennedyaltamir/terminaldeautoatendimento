// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 15:10:00
"use client";
import { Search } from "lucide-react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string; // Adicionado suporte a placeholder opcional
}

export default function SearchBar({ value, onChange, placeholder = "Buscar produtos..." }: SearchBarProps) {
  return (
    <div className="relative mb-6">
      <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-4 py-4 rounded-2xl border border-gray-200 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 outline-none transition-all shadow-sm text-gray-900 placeholder:text-gray-400"
      />
    </div>
  );
}

