"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send, CheckCircle2, Loader2, Sparkles } from "lucide-react";
import { toast } from "sonner";

export default function LeadCapture() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      const dismissed = sessionStorage.getItem("lead_dismissed");
      if (!dismissed) setIsOpen(true);
    }, 12000);
    return () => clearTimeout(timer);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setLoading(true);
    await new Promise((r) => setTimeout(r, 1500));
    
    setLoading(false);
    setSent(true);
    toast.success("Inscrição realizada com sucesso!");
    
    setTimeout(() => {
      setIsOpen(false);
      sessionStorage.setItem("lead_dismissed", "true");
    }, 3000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="fixed bottom-6 left-6 z-[60] max-w-sm w-full"
        >
          <div className="bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 p-6 relative overflow-hidden">
            <button 
              type="button"
              onClick={() => { setIsOpen(false); sessionStorage.setItem("lead_dismissed", "true"); }}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors p-1"
              aria-label="Fechar"
            >
              <X size={20} />
            </button>

            {sent ? (
              <div className="text-center py-4 animate-in zoom-in">
                <div className="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 size={28} />
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Tudo pronto!</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Você receberá nossas novidades em breve.</p>
              </div>
            ) : (
              <>
                <div className="inline-flex items-center gap-2 bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-4">
                  <Sparkles size={12} /> Conteúdo Grátis
                </div>
                <h3 className="text-xl font-black text-slate-900 dark:text-white leading-tight mb-2">
                  Dicas de Gestão.
                </h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
                  Receba estratégias para aumentar o faturamento do seu restaurante.
                </p>

                <form onSubmit={handleSubmit} className="space-y-3">
                  <input
                    type="email"
                    required
                    placeholder="Seu melhor e-mail"
                    className="w-full px-4 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 border-none outline-none focus:ring-2 focus:ring-orange-500 transition-all text-sm"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-50"
                  >
                    {loading ? <Loader2 className="animate-spin" size={18} /> : <><Send size={18} /> Quero receber</>}
                  </button>
                </form>
              </>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
