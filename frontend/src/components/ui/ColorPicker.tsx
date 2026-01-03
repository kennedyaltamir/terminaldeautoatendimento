"use client";

import { Check } from "lucide-react";

interface ColorPickerProps {
  value: string;
  onChange: (color: string) => void;
  label?: string;
  error?: string;
}

const PRESET_COLORS = [
  "#ea580c", // Laranja Padrão
  "#dc2626", // Vermelho
  "#2563eb", // Azul
  "#16a34a", // Verde
  "#9333ea", // Roxo
  "#db2777", // Rosa
  "#000000", // Preto
];

export default function ColorPicker({ value, onChange, label, error }: ColorPickerProps) {
  return (
    <div className="space-y-2">
      {label && <label className="block text-sm font-bold text-gray-700 dark:text-gray-300">{label}</label>}
      
      <div className="flex flex-wrap gap-3 items-center">
        {PRESET_COLORS.map((color) => (
          <button
            key={color}
            type="button"
            onClick={() => onChange(color)}
            className={`w-8 h-8 rounded-full border-2 flex items-center justify-center transition-transform hover:scale-110 ${
              value === color ? "border-gray-900 dark:border-white" : "border-transparent"
            }`}
            style={{ backgroundColor: color }}
          >
            {value === color && <Check size={14} className="text-white drop-shadow-md" />}
          </button>
        ))}
        
        <div className="relative group">
          <input
            type="color"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="w-10 h-10 rounded-lg cursor-pointer border-0 p-0 overflow-hidden bg-transparent"
          />
          <div className="absolute inset-0 border border-gray-200 dark:border-gray-700 rounded-lg pointer-events-none group-hover:border-gray-400"></div>
        </div>
        
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-24 px-3 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white uppercase"
          placeholder="#000000"
          maxLength={7}
        />
      </div>
      
      {error && <p className="text-xs text-red-500 font-medium">{error}</p>}
    </div>
  );
}