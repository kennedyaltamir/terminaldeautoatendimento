"use client";

import { useState } from "react";
import { ChefHat, Instagram, Linkedin, Twitter, ArrowRight, ShieldCheck, Globe, Activity } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

export default function Footer() {
  const [email, setEmail] = useState("");
  const currentYear = new Date().getFullYear();

  const handleNewsletterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    toast.success("Inscrição realizada! Você receberá nossas atualizações.");
    setEmail("");
  };

  return (
    <footer className="bg-slate-950 text-slate-400 py-20 border-t border-slate-900 relative overflow-hidden">
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-orange-600/5 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-16 lg:gap-8">
          
          <div className="lg:col-span-4 space-y-8">
            <div className="flex items-center gap-3 text-white">
              <div className="bg-orange-600 p-2 rounded-xl">
                <ChefHat className="text-white" size={24} />
              </div>
              <span className="text-2xl font-black tracking-tighter">MesaFlow<span className="text-orange-600">.</span></span>
            </div>
            <p className="text-base leading-relaxed max-w-sm">
              A infraestrutura operacional definitiva para restaurantes, arenas e eventos de alto tráfego. Tecnologia invisível, resultados exponenciais.
            </p>
            <div className="flex gap-5">
              {[
                { icon: Instagram, href: "https://instagram.com/mesaflow", label: "Instagram" },
                { icon: Twitter, href: "https://twitter.com/mesaflow", label: "Twitter" },
                { icon: Linkedin, href: "https://linkedin.com/company/mesaflow", label: "Linkedin" }
              ].map((social) => (
                <a 
                  key={social.label}
                  href={social.href} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center hover:text-white hover:border-orange-500 hover:bg-orange-500/10 transition-all group"
                  aria-label={social.label}
                >
                  <social.icon size={20} className="group-hover:scale-110 transition-transform" />
                </a>
              ))}
            </div>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <h4 className="text-white font-black uppercase text-xs tracking-[0.2em]">Produto</h4>
            <ul className="space-y-4 text-sm font-bold">
              <li><Link href="/#recursos" className="hover:text-orange-500 transition-colors">Cardápio Digital</Link></li>
              <li><Link href="/#recursos" className="hover:text-orange-500 transition-colors">KDS (Cozinha)</Link></li>
              <li><Link href="/#recursos" className="hover:text-orange-500 transition-colors">Fidelidade & Cashback</Link></li>
              <li><Link href="/#solucoes" className="hover:text-orange-500 transition-colors">Integrações Hub</Link></li>
              <li><Link href="/admin/register" className="text-orange-500 hover:text-orange-400">Criar Conta Grátis</Link></li>
            </ul>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <h4 className="text-white font-black uppercase text-xs tracking-[0.2em]">Empresa</h4>
            <ul className="space-y-4 text-sm font-bold">
              <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Sobre Nós</Link></li>
              <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Carreiras</Link></li>
              <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Blog Técnico</Link></li>
              <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Contato</Link></li>
              <li>
                <Link href="/trust/status" className="flex items-center gap-2 hover:text-orange-500 transition-colors">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                  Status do Sistema
                </Link>
              </li>
            </ul>
          </div>

          <div className="lg:col-span-4 space-y-8">
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-[2rem] space-y-4">
              <h4 className="text-white font-bold text-sm">Fique por dentro</h4>
              <p className="text-xs leading-relaxed">Receba atualizações sobre novas funcionalidades e dicas de gestão.</p>
              <form onSubmit={handleNewsletterSubmit} className="flex gap-2">
                <input 
                  type="email" 
                  required
                  placeholder="Seu e-mail" 
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs outline-none focus:border-orange-500 transition-colors text-white"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <button 
                  type="submit"
                  className="bg-white text-slate-950 p-2 rounded-xl hover:bg-orange-500 hover:text-white transition-all"
                  aria-label="Inscrever-se"
                >
                  <ArrowRight size={18} />
                </button>
              </form>
            </div>
            
            <div className="flex items-center gap-6 px-2">
              <div className="flex flex-col items-center gap-1 opacity-50 hover:opacity-100 transition-opacity">
                <ShieldCheck size={24} className="text-emerald-500" />
                <span className="text-[8px] font-black uppercase tracking-tighter">LGPD Ready</span>
              </div>
              <div className="flex flex-col items-center gap-1 opacity-50 hover:opacity-100 transition-opacity">
                <Globe size={24} className="text-blue-500" />
                <span className="text-[8px] font-black uppercase tracking-tighter">Global Scale</span>
              </div>
              <div className="flex flex-col items-center gap-1 opacity-50 hover:opacity-100 transition-opacity">
                <Activity size={24} className="text-orange-500" />
                <span className="text-[8px] font-black uppercase tracking-tighter">99.9% Uptime</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-20 pt-8 border-t border-slate-900 flex flex-col md:flex-row justify-between items-center gap-6 text-[10px] font-bold uppercase tracking-widest">
          <p>© {currentYear} MesaFlow Tecnologia Ltda. Todos os direitos reservados.</p>
          <div className="flex gap-8">
            <Link href="/trust/security" className="hover:text-white transition-colors">Termos de Uso</Link>
            <Link href="/trust/security" className="hover:text-white transition-colors">Privacidade</Link>
            <Link href="/trust/security" className="hover:text-white transition-colors">Segurança</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
