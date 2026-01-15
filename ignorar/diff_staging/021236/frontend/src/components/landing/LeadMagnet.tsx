"use client";

import { useState } from "react";
import { FileText, Download, Loader2, CheckCircle2, ArrowRight, ShieldCheck, Star } from "lucide-react";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function LeadMagnet() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setLoading(true);
    
    // Simulação de registro de Lead e disparo de e-mail
    await new Promise(r => setTimeout(r, 2000));
    
    setLoading(false);
    setSuccess(true);
    toast.success("Guia enviado com sucesso!");
  };

  return (
    <section id="lead-magnet" className="py-24 bg-slate-50 dark:bg-slate-950 relative overflow-hidden">
      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <div className="bg-white dark:bg-slate-900 rounded-[3.5rem] p-8 md:p-20 shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col lg:flex-row items-center gap-20">
          
          {/* Visual do Guia (3D-ish) */}
          <motion.div 
            whileHover={{ rotateY: -15, rotateX: 5, scale: 1.05 }}
            style={{ perspective: 1000 }}
            className="relative shrink-0 hidden sm:block"
          >
            <div className="w-64 h-80 bg-orange-600 rounded-r-3xl shadow-[25px_25px_60px_rgba(0,0,0,0.25)] flex flex-col justify-between p-8 relative overflow-hidden border-l-[12px] border-orange-700">
              <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -mr-20 -mt-20"></div>
              <div className="space-y-2">
                <Star size={24} className="text-orange-300 fill-orange-300" />
                <p className="text-white/60 text-[10px] font-black uppercase tracking-widest">MesaFlow Academy</p>
              </div>
              <div>
                <p className="text-white font-black text-3xl leading-tight tracking-tighter">GUIA DE <br/>EFICIÊNCIA <br/>OPERACIONAL</p>
                <div className="w-16 h-1.5 bg-orange-400 mt-6 rounded-full"></div>
              </div>
            </div>
            <div className="absolute -top-6 -right-6 bg-emerald-500 text-white text-xs font-black px-4 py-2 rounded-full shadow-xl border-4 border-white dark:border-slate-900">
              GRÁTIS
            </div>
          </motion.div>

          <div className="flex-1 text-center lg:text-left">
            <h2 className="text-4xl md:text-6xl font-black text-slate-900 dark:text-white mb-8 leading-[1.05] tracking-tighter">
              A Bíblia do <br />
              <span className="text-orange-600 text-gradient">Atendimento em Escala</span>
            </h2>
            <p className="text-slate-500 dark:text-slate-400 text-xl mb-10 max-w-2xl leading-relaxed">
              Aprenda as estratégias que as maiores arenas e redes de fast-food do mundo usam para <b>eliminar filas</b> e maximizar o lucro por metro quadrado.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-12">
              {[
                { t: "Engenharia de Cardápio", d: "Induza o cliente ao maior ticket." },
                { t: "Psicologia do Preço", d: "Como ancorar valor corretamente." },
                { t: "Automação de Cozinha", d: "Reduza o tempo de preparo em 40%." },
                { t: "Fidelidade Invisível", d: "Cashback que gera recorrência real." }
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-3 text-left">
                  <div className="bg-orange-100 dark:bg-orange-900/30 p-1 rounded-lg mt-1">
                    <CheckCircle2 size={18} className="text-orange-600 dark:text-orange-400" />
                  </div>
                  <div>
                    <p className="font-black text-slate-800 dark:text-slate-200 text-sm uppercase tracking-tight">{item.t}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-500">{item.d}</p>
                  </div>
                </div>
              ))}
            </div>

            {success ? (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-emerald-50 dark:bg-emerald-900/20 border-2 border-emerald-200 dark:border-emerald-800 p-8 rounded-[2rem] flex items-center gap-6"
              >
                <div className="bg-emerald-500 text-white p-3 rounded-2xl shadow-lg shadow-emerald-500/20">
                  <CheckCircle2 size={32} />
                </div>
                <div>
                  <p className="text-emerald-900 dark:text-emerald-400 text-xl font-black">O Guia está a caminho!</p>
                  <p className="text-emerald-700 dark:text-emerald-600 font-medium">Enviamos o link de download para o seu e-mail profissional.</p>
                </div>
              </motion.div>
            ) : (
              <form onSubmit={handleDownload} className="flex flex-col sm:flex-row gap-4">
                <input 
                  type="email" 
                  required
                  placeholder="Seu e-mail corporativo"
                  className="flex-1 px-8 py-5 rounded-2xl bg-slate-100 dark:bg-slate-800 border-2 border-transparent focus:border-orange-500 dark:text-white outline-none transition-all font-bold text-lg shadow-inner"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <button 
                  type="submit"
                  disabled={loading}
                  className="bg-orange-600 hover:bg-orange-700 text-white px-12 py-5 rounded-2xl font-black text-lg flex items-center justify-center gap-3 transition-all shadow-2xl shadow-orange-500/30 active:scale-95 disabled:opacity-50"
                >
                  {loading ? <Loader2 className="animate-spin" size={24} /> : <>Baixar Agora <ArrowRight size={24} /></>}
                </button>
              </form>
            )}
            
            <div className="mt-8 flex items-center justify-center lg:justify-start gap-6 text-slate-400">
              <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.2em]">
                <ShieldCheck size={16} className="text-emerald-500" /> Privacidade Garantida
              </div>
              <div className="w-1.5 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-full"></div>
              <div className="text-[10px] font-black uppercase tracking-[0.2em]">
                PDF • 4.2 MB • Edição 2026
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
