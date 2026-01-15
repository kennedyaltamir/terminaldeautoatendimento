"use client";

import Link from "next/link";
import { ArrowRight, Globe, Moon, Sun } from "lucide-react";
import { useState, useEffect } from "react";
import { useLanguage } from "@/context/LanguageContext";
import { Locale } from "@/lib/dictionaries";
import { motion, AnimatePresence } from "framer-motion";
import Logo from "@/components/ui/Logo";

export default function Navbar() {
  const [isDark, setIsDark] = useState(false);
  const { locale, setLocale, t } = useLanguage();
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

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
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? "py-4" : "py-6"}`}>
      <div className={`max-w-7xl mx-auto px-6 transition-all duration-500 ${scrolled ? "glass-panel py-3" : ""}`}>
        <div className="flex justify-between items-center">
          <Link href="/">
            <Logo size="md" animated={true} variant={scrolled ? "color" : "light"} />
          </Link>

          <div className={`hidden md:flex items-center gap-10 text-sm font-bold uppercase tracking-widest ${scrolled ? "text-slate-600 dark:text-slate-300" : "text-slate-300"}`}>
            <a href="#solucoes" className="hover:text-orange-600 transition-colors">{t.navbar.solutions}</a>
            <a href="#recursos" className="hover:text-orange-600 transition-colors">{t.navbar.features}</a>
            <a href="#precos" className="hover:text-orange-600 transition-colors">{t.navbar.pricing}</a>
          </div>

          <div className="flex items-center gap-6">
            {/* Language Selector */}
            <div className="relative">
              <button 
                onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
                className={`hidden md:flex items-center gap-1 text-xs font-bold uppercase ${scrolled ? "text-slate-500 dark:text-slate-400 hover:text-orange-600" : "text-slate-300 hover:text-white"}`}
              >
                <Globe size={14} /> {locale}
              </button>
              <AnimatePresence>
                {isLangMenuOpen && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="absolute top-full right-0 mt-4 w-32 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl overflow-hidden"
                  >
                    <button onClick={() => toggleLanguage('pt')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200">Português</button>
                    <button onClick={() => toggleLanguage('en')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200">English</button>
                    <button onClick={() => toggleLanguage('es')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200">Español</button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <button 
              onClick={() => setIsDark(!isDark)}
              className={`p-2.5 rounded-xl transition-colors ${scrolled ? "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800" : "text-slate-300 hover:bg-white/10"}`}
            >
              {isDark ? <Sun size={20} /> : <Moon size={20} />}
            </button>

            <Link 
              href="/admin/login" 
              className={`hidden md:block text-sm font-bold uppercase tracking-widest transition-colors ${scrolled ? "text-slate-700 dark:text-slate-200 hover:text-orange-600" : "text-white hover:text-orange-400"}`}
            >
              {t.navbar.login}
            </Link>

            <Link 
              href="/admin/register" 
              className="bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-6 py-3 rounded-2xl font-black text-sm hover:scale-105 transition-all shadow-xl flex items-center gap-2 group uppercase tracking-wider"
            >
              {t.navbar.start}
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
