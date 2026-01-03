"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { dictionaries, Locale } from '@/lib/dictionaries';

interface LanguageContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: typeof dictionaries['pt']; // Tipo inferido do dicionário PT
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>('pt');

  // Detectar idioma do navegador na primeira carga
  useEffect(() => {
    const browserLang = navigator.language.split('-')[0];
    if (browserLang === 'en' || browserLang === 'es') {
      setLocale(browserLang as Locale);
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