"use client";

import { useState } from "react";
import { FileText, Download, Loader2, CheckCircle2, ArrowRight, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function LeadMagnet() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulação de processamento e registro de lead
    await new Promise(r => setTimeout(r, 2000));
    
    setLoading(false);
    setSuccess(true);
    toast.success("Guia enviado com sucesso!");
  };

  return (
    <section className="py-24 bg-slate-50 dark:bg-slate-950 relative overflow-hidden">
      {/* Elementos Decorativos de Fundo */}
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-orange-500/20 to-transparent"></div>
      
      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <div className="bg-white dark:bg-slate-900 rounded-[3rem] p-8 md:p-16 shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col lg:flex-row items-center gap-16">
          
          {/* Representação Visual do Guia */}
          <motion.div 
            whileHover={{ rotate: -2, scale: 1.05 }}
            className="relative shrink-0"
          >
            <div className="w-56 h-72 bg-orange-600 rounded-r-2xl shadow-[20px_20px_60px_rgba(0,0,0,0.2)] flex flex-col justify-between p-6 relative overflow-hidden border-l-8 border-orange-700">
              <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
              <FileText size={40} className="text-white/90" />
              <div>
                <p className="text-white font-black text-xl leading-tight">GUIA DE <br/>EFICIÊNCIA <br/>2026</p>
                <div className="w-12 h-1 bg-orange-400 mt-4"></div>
              </div>
            </div>
            {/* Badge de "Novo" */}
            <div className="absolute -top-4 -right-4 bg-emerald-500 text-white text-[10px] font-black px-3 py-1 rounded-full shadow-lg">
              GRÁTIS
            </div>
          </motion.div>

          <div className="flex-1 text-center lg:text-left">
            <h2 className="text-4xl md:text-5xl font-black text-slate-900 dark:text-white mb-6 leading-tight tracking-tighter">
              A Bíblia do <br />
              <span className="text-orange-600">Atendimento em Escala</span>
            </h2>
            <p className="text-slate-500 dark:text-slate-400 text-lg mb-8 max-w-xl">
              Aprenda as 7 estratégias que as redes de fast-food usam para <b>eliminar filas</b> e aumentar o lucro por mesa em até 25%.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
              {[
                "Engenharia de Cardápio",
                "Psicologia do Preço",
                "Automação de Cozinha",
                "Fidelidade Invisível"
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                  <CheckCircle2 size={18} className="text-orange-500" /> {item}
                </div>
              ))}
            </div>

            {success ? (
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 p-6 rounded-2xl flex items-center gap-4"
              >
                <div className="bg-emerald-500 text-white p-2 rounded-full">
                  <CheckCircle2 size={24} />
                </div>
                <div>
                  <p className="text-emerald-900 dark:text-emerald-400 font-black">O Guia está a caminho!</p>
                  <p className="text-emerald-700 dark:text-emerald-500 text-sm">Enviamos o link de download para o seu e-mail.</p>
                </div>
              </motion.div>
            ) : (
              <form onSubmit={handleDownload} className="flex flex-col sm:flex-row gap-3">
                <input 
                  type="email" 
                  required
                  placeholder="Seu e-mail corporativo"
                  className="flex-1 px-6 py-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-2 border-transparent focus:border-orange-500 dark:text-white outline-none transition-all font-bold"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <button 
                  type="submit"
                  disabled={loading}
                  className="bg-orange-600 hover:bg-orange-700 text-white px-10 py-4 rounded-2xl font-black flex items-center justify-center gap-2 transition-all shadow-xl shadow-orange-500/20 active:scale-95 disabled:opacity-50"
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : <>Baixar Agora <ArrowRight size={20} /></>}
                </button>
              </form>
            )}
            
            <div className="mt-6 flex items-center justify-center lg:justify-start gap-4 text-slate-400">
              <div className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-widest">
                <ShieldCheck size={14} /> Privacidade Garantida
              </div>
              <div className="w-1 h-1 bg-slate-300 rounded-full"></div>
              <div className="text-[10px] font-bold uppercase tracking-widest">
                PDF • 4.2 MB • Versão 2026
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
