"use client";

import { useState, useEffect } from "react";
import { X, Mail, ArrowRight, CheckCircle2, Sparkles, Loader2, TrendingUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";

export default function LeadCapture() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      const hasSeen = sessionStorage.getItem("mesaflow_lead_popup");
      if (!hasSeen) setIsOpen(true);
    }, 15000);
    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsOpen(false);
    sessionStorage.setItem("mesaflow_lead_popup", "true");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setLoading(true);
    
    // Simulação de processamento de Lead
    await new Promise(r => setTimeout(r, 1800));
    
    setLoading(false);
    setSubmitted(true);
    toast.success("Guia enviado com sucesso!");
    
    setTimeout(handleClose, 5000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-950/90 backdrop-blur-md">
          <motion.div 
            initial={{ opacity: 0, y: 100, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 100, scale: 0.9 }}
            className="bg-white dark:bg-slate-900 w-full max-w-3xl rounded-[2.5rem] shadow-2xl overflow-hidden relative border border-white/10"
          >
            <button 
              type="button"
              onClick={handleClose} 
              className="absolute top-6 right-6 text-slate-400 hover:text-orange-500 dark:hover:text-white z-20 bg-slate-100 dark:bg-slate-800 p-2 rounded-full transition-all hover:rotate-90"
              aria-label="Fechar"
            >
              <X size={20} />
            </button>

            <div className="flex flex-col md:flex-row min-h-[450px]">
              {/* Lado Visual: Autoridade */}
              <div className="hidden md:block w-5/12 relative">
                <div className="absolute inset-0 bg-orange-600">
                  <img 
                    src="https://images.pexels.com/photos/3184183/pexels-photo-3184183.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" 
                    className="w-full h-full object-cover opacity-30 mix-blend-overlay"
                    alt="MesaFlow Efficiency"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-orange-700 via-transparent to-transparent"></div>
                <div className="absolute bottom-10 left-8 right-8 space-y-4">
                  <div className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl border border-white/20 shadow-xl">
                    <div className="flex gap-1 mb-2">
                      {[1,2,3,4,5].map(i => <Sparkles key={i} size={10} className="text-orange-300 fill-orange-300" />)}
                    </div>
                    <p className="text-white font-medium text-sm italic leading-relaxed">
                      "O guia de engenharia de cardápio nos ajudou a aumentar o ticket médio em 18% em apenas 3 semanas."
                    </p>
                    <div className="mt-4 flex items-center gap-3">
                      <div className="w-8 h-8 bg-orange-400 rounded-full flex items-center justify-center text-[10px] font-bold text-orange-900">RA</div>
                      <p className="text-orange-100 text-xs font-bold">Ricardo A. <span className="font-normal opacity-70">| CEO FoodX</span></p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Lado do Conteúdo: Conversão */}
              <div className="flex-1 p-10 md:p-14 flex flex-col justify-center">
                {submitted ? (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center space-y-6"
                  >
                    <div className="w-24 h-24 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
                      <CheckCircle2 size={48} />
                    </div>
                    <div>
                      <h3 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">Acesso Liberado!</h3>
                      <p className="text-slate-500 dark:text-slate-400 mt-2">
                        O link para o <b>Guia de Eficiência 2026</b> foi enviado para seu e-mail. Prepare-se para escalar.
                      </p>
                    </div>
                  </motion.div>
                ) : (
                  <>
                    <div className="inline-flex items-center gap-2 bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.2em] mb-6">
                      <TrendingUp size={14} /> Estratégia de Crescimento
                    </div>
                    <h3 className="text-4xl font-black text-slate-900 dark:text-white leading-[1.1] mb-4 tracking-tighter">
                      Venda mais com <br/><span className="text-orange-600">menos staff.</span>
                    </h3>
                    <p className="text-slate-500 dark:text-slate-400 text-base mb-10 leading-relaxed">
                      Baixe nosso guia exclusivo e aprenda a técnica de <b>Engenharia de Cardápio</b> usada pelas redes que faturam milhões.
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="relative group">
                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-orange-500 transition-colors" size={20} />
                        <input 
                          type="email" 
                          required
                          placeholder="Seu melhor e-mail profissional" 
                          className="w-full pl-12 pr-4 py-4 rounded-2xl border-2 border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-slate-900 dark:text-white outline-none focus:border-orange-500 focus:ring-4 focus:ring-orange-500/10 transition-all font-bold"
                          value={email}
                          onChange={e => setEmail(e.target.value)}
                        />
                      </div>
                      <button 
                        type="submit"
                        disabled={loading}
                        className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-black py-5 rounded-2xl hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-3 shadow-2xl disabled:opacity-70"
                      >
                        {loading ? <Loader2 className="animate-spin" /> : <>Baixar Guia Gratuitamente <ArrowRight size={20} /></>}
                      </button>
                    </form>
                    <p className="text-[10px] text-center text-slate-400 mt-8 uppercase font-bold tracking-widest">
                      🔒 Seus dados estão protegidos. Versão 2026.
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

