"use client";
/**
 * DOMAIN: FRONTEND
 * FILE: src/context/LanguageContext.tsx
 * OBJECTIVE: Gerenciamento de internacionalização com inicialização segura (Render Safe).
 * FIX: Deferral de atualização de estado para evitar conflitos de renderização.
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { dictionaries, Locale } from '@/lib/dictionaries';

interface LanguageContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: typeof dictionaries['pt'];
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>('pt');

  useEffect(() => {
    if (typeof window !== "undefined") {
      const browserLang = navigator.language.split('-')[0];
      if (['en', 'es', 'pt'].includes(browserLang)) {
        // 🛡️ FIX: Deferral (Adiamento) da atualização de estado.
        // Move a atualização para o próximo tick do Event Loop, evitando
        // conflitos de renderização com outros Context Providers.
        setTimeout(() => {
          setLocale(browserLang as Locale);
        }, 0);
      }
    }
  }, []);

  const value = {
    locale,
    setLocale,
    t: dictionaries[locale]
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}