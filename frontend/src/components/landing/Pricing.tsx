"use client";
import { useState } from "react";
import { Check, Calendar } from "lucide-react";
import Link from "next/link";
import ScrollReveal from "@/components/ui/ScrollReveal";

export default function Pricing() {
  const [isAnnual, setIsAnnual] = useState(true);

  return (
    <section id="precos" className="py-24 bg-gray-900 text-white relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-orange-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <ScrollReveal>
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Preços transparentes.</h2>
            <p className="text-gray-400 mb-8">Comece grátis e escale conforme seu faturamento cresce.</p>
            
            {/* Toggle */}
            <div className="flex items-center justify-center gap-4 cursor-pointer" onClick={() => setIsAnnual(!isAnnual)}>
              <span className={`text-sm font-bold transition-colors ${!isAnnual ? 'text-white' : 'text-gray-500'}`}>Mensal</span>
              <div className="w-14 h-8 bg-gray-700 rounded-full p-1 relative transition-colors hover:bg-gray-600">
                <div className={`w-6 h-6 bg-orange-500 rounded-full shadow-md transition-transform duration-300 ${isAnnual ? 'translate-x-6' : 'translate-x-0'}`}></div>
              </div>
              <span className={`text-sm font-bold transition-colors ${isAnnual ? 'text-white' : 'text-gray-500'}`}>
                Anual <span className="text-green-400 text-xs ml-1 bg-green-400/10 px-2 py-0.5 rounded-full">-20%</span>
              </span>
            </div>
          </div>
        </ScrollReveal>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Plano Start */}
          <ScrollReveal delay={100} className="h-full">
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700 hover:border-gray-600 transition-all h-full flex flex-col">
              <h3 className="text-xl font-bold text-gray-300">Start</h3>
              <div className="my-4">
                <span className="text-4xl font-bold">Grátis</span>
              </div>
              <p className="text-sm text-gray-400 mb-8">Para quem está validando a operação.</p>
              <ul className="space-y-4 mb-8 text-sm text-gray-300 flex-1">
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> Até 50 pedidos/mês</li>
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> Cardápio Digital</li>
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> Pagamento Pix Manual</li>
              </ul>
              <Link href="/admin/register?plan=free" className="block w-full py-3 rounded-xl border border-gray-600 text-center font-bold hover:bg-gray-700 transition-colors">Começar Grátis</Link>
            </div>
          </ScrollReveal>

          {/* Plano Pro */}
          <ScrollReveal delay={200} className="h-full">
            <div className="bg-orange-600 rounded-2xl p-8 border border-orange-500 shadow-2xl transform md:-translate-y-4 relative h-full flex flex-col">
              <div className="absolute top-0 right-0 bg-white text-orange-600 text-xs font-bold px-3 py-1 rounded-bl-xl rounded-tr-xl">MAIS POPULAR</div>
              <h3 className="text-xl font-bold text-white">Pro</h3>
              <div className="my-4">
                <span className="text-4xl font-bold">R$ {isAnnual ? '119' : '149'}</span>
                <span className="text-orange-200">/mês</span>
              </div>
              <p className="text-sm text-orange-100 mb-8">Para operações em crescimento.</p>
              <ul className="space-y-4 mb-8 text-sm text-white flex-1">
                <li className="flex gap-3"><Check size={18} className="text-white"/> Pedidos Ilimitados</li>
                <li className="flex gap-3"><Check size={18} className="text-white"/> KDS de Cozinha</li>
                <li className="flex gap-3"><Check size={18} className="text-white"/> Pix Automático & Cartão</li>
                <li className="flex gap-3"><Check size={18} className="text-white"/> Programa de Fidelidade</li>
              </ul>
              <Link href="/admin/register?plan=pro" className="block w-full py-3 rounded-xl bg-white text-orange-600 text-center font-bold hover:bg-gray-100 transition-colors">Assinar Pro</Link>
            </div>
          </ScrollReveal>

          {/* Plano Enterprise */}
          <ScrollReveal delay={300} className="h-full">
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700 hover:border-gray-600 transition-all h-full flex flex-col">
              <h3 className="text-xl font-bold text-gray-300">Enterprise</h3>
              <div className="my-4">
                <span className="text-4xl font-bold">Sob Consulta</span>
              </div>
              <p className="text-sm text-gray-400 mb-8">Para redes, estádios e grandes eventos.</p>
              <ul className="space-y-4 mb-8 text-sm text-gray-300 flex-1">
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> API Dedicada</li>
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> White Label (Seu Domínio)</li>
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> Gerente de Conta</li>
                <li className="flex gap-3"><Check size={18} className="text-green-500"/> Integração Fiscal (NFC-e)</li>
              </ul>
              <button onClick={() => alert("Abrindo Calendly...")} className="w-full py-3 rounded-xl border border-gray-600 text-center font-bold hover:bg-gray-700 transition-colors flex items-center justify-center gap-2">
                <Calendar size={18} /> Agendar Demo
              </button>
            </div>
          </ScrollReveal>
        </div>
        
        <ScrollReveal delay={400}>
          <div className="mt-16 text-center">
            <div className="inline-flex items-center gap-2 bg-green-900/30 border border-green-800 px-4 py-2 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-green-400 text-xs font-mono font-bold">LGPD COMPLIANT • PCI-DSS SECURE • 99.99% UPTIME</span>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}