/**
 * Author: MESAFLOW_AI
 * Version: 11.2 (i18n & Accessibility)
 * Objective: Universal Header for Kiosk with Language Switcher.
 */
"use client";

import React from "react";
import { ArrowLeft, ChefHat, Info, Globe } from "lucide-react";
import { useRouter } from "next/navigation";
import { useLanguage } from "@/context/LanguageContext";
import { Locale } from "@/lib/dictionaries";
import { cn } from "@/lib/utils";

interface KioskHeaderProps {
  companyName: string;
  primaryColor: string;
  logoUrl?: string | null;
}

export default function KioskHeader({ companyName, primaryColor, logoUrl }: KioskHeaderProps) {
  const router = useRouter();
  const { t, locale, setLocale } = useLanguage();

  return (
    <header className="bg-slate-900 border-b border-slate-800 p-6 flex justify-between items-center sticky top-0 z-40 shadow-2xl">
      {/* Botão Voltar Gigante */}
      <button 
        onClick={() => router.back()}
        className="bg-slate-800 text-white p-5 rounded-2xl flex items-center gap-3 font-bold hover:bg-slate-700 transition-all active:scale-95 border border-slate-700"
      >
        <ArrowLeft size={32} />
        <span className="text-lg uppercase tracking-wider">{t.kiosk.back}</span>
      </button>

      {/* Identidade Visual */}
      <div className="flex items-center gap-5">
        <div 
          className="p-3 rounded-2xl shadow-lg border border-white/10"
          style={{ backgroundColor: primaryColor }}
        >
          {logoUrl ? (
            <img src={logoUrl} alt="Logo" className="w-10 h-10 object-contain" />
          ) : (
            <ChefHat size={40} className="text-white" />
          )}
        </div>
        <div className="flex flex-col">
          <h2 className="text-3xl font-black text-white tracking-tight uppercase leading-none">
            {companyName}
          </h2>
          <div className="flex items-center gap-2 mt-1">
             <span className="relative flex h-3 w-3">
               <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
               <span className="relative inline-flex rounded-full h-3 w-3 bg-orange-500"></span>
             </span>
             <span className="text-orange-500 text-xs font-black tracking-[0.2em] uppercase">
                {locale === 'pt' ? 'Autoatendimento Ativo' : locale === 'en' ? 'Self-Service Active' : 'Autoservicio Activo'}
             </span>
          </div>
        </div>
      </div>

      {/* Seletor de Idioma & Acessibilidade */}
      <div className="flex items-center gap-4">
        <div className="flex bg-slate-800 p-1.5 rounded-2xl border border-slate-700">
          {(['pt', 'en', 'es'] as Locale[]).map((lang) => (
            <button
              key={lang}
              onClick={() => setLocale(lang)}
              className={cn(
                "px-4 py-2 rounded-xl text-sm font-black uppercase transition-all",
                locale === lang ? "bg-orange-600 text-white shadow-lg" : "text-slate-500 hover:text-slate-300"
              )}
            >
              {lang}
            </button>
          ))}
        </div>
        
        <button className="bg-slate-800 text-blue-400 p-4 rounded-2xl border border-slate-700 hover:bg-slate-700 transition-all">
          <Info size={28} />
        </button>
      </div>
    </header>
  );
}