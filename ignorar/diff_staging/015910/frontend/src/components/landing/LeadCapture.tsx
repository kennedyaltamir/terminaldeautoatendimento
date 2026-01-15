"use client";

import { useState, useEffect } from "react";
import { X, Mail, ArrowRight, CheckCircle2, Sparkles, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";

export default function LeadCapture() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    // Trigger: Aparece após 12 segundos de navegação
    const timer = setTimeout(() => {
      const hasSeen = sessionStorage.getItem("mesaflow_lead_popup");
      if (!hasSeen) setIsOpen(true);
    }, 12000);

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsOpen(false);
    sessionStorage.setItem("mesaflow_lead_popup", "true");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulação de integração com CRM (RD Station/Hubspot)
    await new Promise(r => setTimeout(r, 1500));
    
    setLoading(false);
    setSubmitted(true);
    toast.success("Acesso liberado! Verifique seu e-mail.");
    
    setTimeout(() => {
      handleClose();
    }, 4000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
          <motion.div 
            initial={{ opacity: 0, y: 50, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.95 }}
            className="bg-white dark:bg-slate-900 w-full max-w-2xl rounded-[2rem] shadow-2xl overflow-hidden relative border border-white/10"
          >
            <button 
              onClick={handleClose} 
              className="absolute top-6 right-6 text-slate-400 hover:text-slate-600 dark:hover:text-white z-20 bg-slate-100 dark:bg-slate-800 p-1 rounded-full transition-colors"
            >
              <X size={20} />
            </button>

            <div className="flex flex-col md:flex-row min-h-[400px]">
              {/* Lado Visual */}
              <div className="hidden md:block w-2/5 relative">
                <div className="absolute inset-0 bg-orange-600">
                  <img 
                    src="https://images.pexels.com/photos/3184183/pexels-photo-3184183.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" 
                    className="w-full h-full object-cover opacity-40 mix-blend-luminosity"
                    alt="Gestão de Restaurante"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-orange-700 via-transparent to-transparent"></div>
                <div className="absolute bottom-8 left-8 right-8">
                  <div className="bg-white/20 backdrop-blur-md p-4 rounded-2xl border border-white/20">
                    <p className="text-white font-bold text-sm leading-tight">
                      "Essa técnica mudou nosso faturamento em 3 semanas."
                    </p>
                    <p className="text-orange-200 text-xs mt-2">— Ricardo, CEO do Grupo FoodX</p>
                  </div>
                </div>
              </div>

              {/* Lado do Formulário */}
              <div className="flex-1 p-10 flex flex-col justify-center">
                {submitted ? (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center space-y-4"
                  >
                    <div className="w-20 h-20 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-lg">
                      <CheckCircle2 size={40} />
                    </div>
                    <h3 className="text-2xl font-black text-slate-900 dark:text-white">Material Enviado!</h3>
                    <p className="text-slate-500 dark:text-slate-400">
                      O link para o <b>Guia de Engenharia de Cardápio</b> já está na sua caixa de entrada.
                    </p>
                  </motion.div>
                ) : (
                  <>
                    <div className="inline-flex items-center gap-2 bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-3 py-1 rounded-full text-xs font-black uppercase tracking-widest mb-4">
                      <Sparkles size={14} /> Conteúdo Exclusivo
                    </div>
                    <h3 className="text-3xl font-black text-slate-900 dark:text-white leading-tight mb-4">
                      Venda <span className="text-orange-600">30% mais</span> sem contratar ninguém.
                    </h3>
                    <p className="text-slate-500 dark:text-slate-400 text-sm mb-8 leading-relaxed">
                      Descubra como as maiores redes de fast-food organizam o cardápio para induzir o cliente ao maior ticket.
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="relative">
                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <input 
                          type="email" 
                          required
                          placeholder="Seu melhor e-mail profissional" 
                          className="w-full pl-12 pr-4 py-4 rounded-2xl border-2 border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-slate-900 dark:text-white outline-none focus:border-orange-500 transition-all font-medium"
                          value={email}
                          onChange={e => setEmail(e.target.value)}
                        />
                      </div>
                      <button 
                        disabled={loading}
                        className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-black py-4 rounded-2xl hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2 shadow-xl disabled:opacity-70"
                      >
                        {loading ? <Loader2 className="animate-spin" /> : <>Receber Guia Grátis <ArrowRight size={20} /></>}
                      </button>
                    </form>
                    <p className="text-[10px] text-center text-slate-400 mt-6 uppercase font-bold tracking-tighter">
                      🔒 Seus dados estão seguros. Zero Spam.
                    </p>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
