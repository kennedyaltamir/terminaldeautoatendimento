"use client";

import { useState, useEffect } from "react";
import { MessageCircle, X, FileText, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function FloatingWidget() {
  const [showExitIntent, setShowExitIntent] = useState(false);
  const [hasShownExit, setHasShownExit] = useState(false);

  useEffect(() => {
    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 0 && !hasShownExit && !sessionStorage.getItem("exit_intent_shown")) {
        setShowExitIntent(true);
        setHasShownExit(true);
        sessionStorage.setItem("exit_intent_shown", "true");
      }
    };
    document.addEventListener("mouseleave", handleMouseLeave);
    return () => document.removeEventListener("mouseleave", handleMouseLeave);
  }, [hasShownExit]);

  const handleWhatsAppClick = () => {
    window.open("https://wa.me/5511999999999", "_blank");
  };

  const handleDownloadGuide = () => {
    setShowExitIntent(false);
    // Redireciona para a seção de Lead Magnet ou abre o modal
    const element = document.getElementById("lead-magnet");
    if (element) element.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      {/* WhatsApp Button */}
      <button 
        type="button"
        onClick={handleWhatsAppClick}
        className="fixed bottom-6 right-6 bg-green-500 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition-transform z-40 flex items-center justify-center hover:bg-green-600"
        aria-label="Falar com Vendas"
      >
        <MessageCircle size={28} />
      </button>

      {/* Exit Intent Modal */}
      <AnimatePresence>
        {showExitIntent && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm">
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="bg-white dark:bg-slate-900 rounded-[2rem] p-8 max-w-md text-center shadow-2xl relative border border-white/10"
            >
              <button 
                type="button"
                onClick={() => setShowExitIntent(false)} 
                className="absolute top-6 right-6 text-slate-400 hover:text-slate-600 dark:hover:text-white p-1"
                aria-label="Fechar"
              >
                <X size={24}/>
              </button>
              
              <div className="w-20 h-20 bg-orange-100 dark:bg-orange-900/30 rounded-3xl flex items-center justify-center mx-auto mb-6 text-orange-600">
                <FileText size={40} />
              </div>
              
              <h3 className="text-2xl font-black text-slate-900 dark:text-white mb-3 tracking-tight">Espere! Não vá ainda.</h3>
              <p className="text-slate-500 dark:text-slate-400 mb-8 leading-relaxed">
                Baixe nosso <b>Guia de Gestão de Filas para Grandes Eventos</b> gratuitamente e otimize sua operação.
              </p>
              
              <button 
                type="button"
                onClick={handleDownloadGuide}
                className="w-full bg-orange-600 text-white py-4 rounded-2xl font-black text-lg hover:bg-orange-700 transition-all shadow-lg shadow-orange-500/20 flex items-center justify-center gap-2 group"
              >
                Baixar PDF Grátis <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button 
                type="button"
                onClick={() => setShowExitIntent(false)} 
                className="mt-6 text-sm font-bold text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
              >
                Não, obrigado.
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}

