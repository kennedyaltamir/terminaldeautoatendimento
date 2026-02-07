"use client";
import Link from "next/link";
import { ArrowRight, Globe, Moon, Sun, Menu, X } from "lucide-react";
import { useState, useEffect } from "react";
import { useLanguage } from "@/context/LanguageContext";
import { Locale } from "@/lib/dictionaries";
import { motion, AnimatePresence } from "framer-motion";
import Logo from "@/components/ui/Logo";

export default function Navbar() {
  const [isDark, setIsDark] = useState(false);
  const { locale, setLocale, t } = useLanguage();
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
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
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? "py-4 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md shadow-sm" : "py-6"}`}>
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center">
          <Link href="/" className="relative z-50">
            <Logo size="md" animated={true} variant={scrolled || isDark ? "color" : "light"} />
          </Link>

          {/* Desktop Menu */}
          <div className={`hidden md:flex items-center gap-10 text-sm font-bold uppercase tracking-widest ${scrolled ? "text-slate-600 dark:text-slate-300" : "text-slate-300"}`}>
            <a href="#solucoes" className="hover:text-orange-600 transition-colors">Soluções</a>
            <a href="#recursos" className="hover:text-orange-600 transition-colors">Recursos</a>
            <a href="#precos" className="hover:text-orange-600 transition-colors">Planos</a>
          </div>

          <div className="hidden md:flex items-center gap-6">
            {/* Language Selector */}
            <div className="relative">
              <button 
                data-magnetic="true"
                onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
                className={`flex items-center gap-1 text-xs font-bold uppercase ${scrolled ? "text-slate-500 dark:text-slate-400 hover:text-orange-600" : "text-slate-300 hover:text-white"}`}
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
              className={`text-sm font-bold uppercase tracking-widest transition-colors ${scrolled ? "text-slate-700 dark:text-slate-200 hover:text-orange-600" : "text-white hover:text-orange-400"}`}
            >
              Login
            </Link>

            <Link 
              href="/admin/register" 
              className="bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-6 py-3 rounded-2xl font-black text-sm hover:scale-105 transition-all shadow-xl flex items-center gap-2 group uppercase tracking-wider"
            >
              Começar
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden p-2 text-slate-400 hover:text-white z-50 relative"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 bg-slate-950 z-40 flex flex-col pt-24 px-6 md:hidden"
          >
            <div className="flex flex-col gap-6 text-center">
              <a href="#solucoes" onClick={() => setIsMobileMenuOpen(false)} className="text-2xl font-bold text-white py-4 border-b border-slate-800">Soluções</a>
              <a href="#recursos" onClick={() => setIsMobileMenuOpen(false)} className="text-2xl font-bold text-white py-4 border-b border-slate-800">Recursos</a>
              <a href="#precos" onClick={() => setIsMobileMenuOpen(false)} className="text-2xl font-bold text-white py-4 border-b border-slate-800">Planos</a>
              
              <div className="flex justify-center gap-6 mt-4">
                <Link 
                  href="/admin/login" 
                  className="text-lg font-bold text-slate-400 uppercase tracking-widest"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Login
                </Link>
              </div>
              
              <Link 
                href="/admin/register" 
                className="bg-orange-600 text-white px-6 py-4 rounded-2xl font-black text-lg uppercase tracking-wider mt-4"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Começar Agora
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}

 