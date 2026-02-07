/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Minimalist weather/road condition display.
 */
"use client";

import { CloudRain, Sun, Wind, Thermometer } from "lucide-react";

export default function TacticalWeather() {
  // Mock Data (L8: Connect to OpenWeatherMap)
  const weather = { temp: "24°C", condition: "Seco", wind: "12km/h" };

  return (
    <div className="flex items-center gap-4 bg-slate-900/50 border border-slate-800 rounded-2xl px-4 py-2 backdrop-blur-md">
      <div className="flex items-center gap-2 text-orange-500">
        <Sun size={16} />
        <span className="text-xs font-black">{weather.temp}</span>
      </div>
      <div className="w-px h-4 bg-slate-800" />
      <div className="flex items-center gap-2 text-slate-400">
        <Wind size={14} />
        <span className="text-[10px] font-bold uppercase">{weather.wind}</span>
      </div>
      <div className="w-px h-4 bg-slate-800" />
      <span className="text-[10px] font-black uppercase text-emerald-500 tracking-wider">
        Pista {weather.condition}
      </span>
    </div>
  );
}

