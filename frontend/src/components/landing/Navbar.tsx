"use client";
import Link from "next/link";
import { ChefHat, ArrowRight, ChevronDown, Moon, Sun, Globe } from "lucide-react";
import { useState, useEffect } from "react";
import { useLanguage } from "@/context/LanguageContext";
import { Locale } from "@/lib/dictionaries";

export default function Navbar() {
  const [isDark, setIsDark] = useState(false);
  const { locale, setLocale, t } = useLanguage();
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleLanguage = (lang: Locale) => {
    setLocale(lang);
    setIsLangMenuOpen(false);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
        
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="bg-orange-600 p-2 rounded-xl group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-orange-500/20">
            <ChefHat className="text-white w-6 h-6" />
          </div>
          <span className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight transition-colors">MesaFlow</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600 dark:text-gray-300">
          <a href="#solucoes" className="hover:text-orange-600 transition-colors">{t.navbar.solutions}</a>
          <a href="#recursos" className="hover:text-orange-600 transition-colors">{t.navbar.features}</a>
          <a href="#precos" className="hover:text-orange-600 transition-colors">{t.navbar.pricing}</a>
        </div>

        <div className="flex items-center gap-4">
          {/* Language Selector */}
          <div className="relative">
            <button 
              onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
              className="hidden md:flex items-center gap-1 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white text-xs font-bold uppercase"
            >
              <Globe size={14} /> {locale}
            </button>
            
            {isLangMenuOpen && (
              <div className="absolute top-full right-0 mt-2 w-24 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl overflow-hidden">
                <button onClick={() => toggleLanguage('pt')} className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-200">Português</button>
                <button onClick={() => toggleLanguage('en')} className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-200">English</button>
                <button onClick={() => toggleLanguage('es')} className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-200">Español</button>
              </div>
            )}
          </div>

          <button 
            onClick={() => setIsDark(!isDark)}
            className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>

          <Link 
            href="/admin/login" 
            className="hidden md:block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors"
          >
            {t.navbar.login}
          </Link>
          <Link 
            href="/admin/register" 
            className="bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-5 py-2.5 rounded-xl font-semibold hover:bg-gray-800 dark:hover:bg-gray-100 transition-all shadow-lg hover:shadow-xl flex items-center gap-2 group"
          >
            {t.navbar.start}
            <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    </nav>
  );
}