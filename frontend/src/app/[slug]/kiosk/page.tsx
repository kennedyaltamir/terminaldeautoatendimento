"use client";

import { useRouter } from "next/navigation";
import { ChefHat, Touchpad, Utensils, Zap, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import Logo from "@/components/ui/Logo";

/**
 * KioskAttractScreen (v5.0 - Gold Master)
 * Tela de proteção e atração para Totens de Autoatendimento.
 * 
 * REGRAS DE NEGÓCIO:
 * 1. Bloqueio de Gestos: Impede scroll e navegação acidental.
 * 2. Gatilho de Início: Qualquer toque na tela redireciona para o cardápio em modo kiosk.
 * 3. Branding Dinâmico: Utiliza o sistema de cores do Tenant.
 */
export default function KioskAttractScreen({ params }: { params: { slug: string } }) {
  const router = useRouter();

  const handleStart = () => {
    // Redireciona com flag kiosk=true para ajustar comportamento do carrinho e pagamentos
    router.push(`/${params.slug}/menu?kiosk=true`);
  };

  return (
    <div 
      onClick={handleStart}
      role="button"
      aria-label="Toque na tela para iniciar o pedido"
      className="relative h-screen w-screen flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-slate-950"
    >
      {/* Background Cinematográfico */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent z-10" />
        <motion.img 
          initial={{ scale: 1.1 }}
          animate={{ scale: 1 }}
          transition={{ duration: 20, repeat: Infinity, repeatType: "reverse" }}
          src="https://images.pexels.com/photos/1639562/pexels-photo-1639562.jpeg?auto=compress&cs=tinysrgb&w=1920" 
          className="w-full h-full object-cover opacity-30"
          alt="Branding Background"
        />
      </div>

      {/* Floating Particles (Decorativo) */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute bg-orange-500/20 rounded-full blur-xl"
            animate={{
              x: [Math.random() * 100, Math.random() * 500, Math.random() * 100],
              y: [Math.random() * 100, Math.random() * 800, Math.random() * 100],
            }}
            transition={{ duration: 15 + i, repeat: Infinity }}
            style={{ width: 200 + i * 50, height: 200 + i * 50 }}
          />
        ))}
      </div>

      <div className="relative z-20 text-center px-10">
        {/* Logo de Alta Visibilidade */}
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="mb-12 flex justify-center"
        >
          <Logo size="xl" variant="light" animated={true} />
        </motion.div>

        {/* Chamada Principal (Hero Title) */}
        <div className="space-y-6 mb-20">
          <motion.h1 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-7xl md:text-9xl font-black text-white tracking-tighter drop-shadow-2xl"
          >
            PEÇA <span className="text-orange-600">AQUI</span>
          </motion.h1>
          <p className="text-2xl md:text-4xl text-slate-300 font-light tracking-wide uppercase">
            Rápido • Digital • Sem Filas
          </p>
        </div>

        {/* Call to Action (CTA) Pulsante */}
        <motion.div 
          animate={{ y: [0, 15, 0], scale: [1, 1.05, 1] }}
          transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
          className="flex flex-col items-center gap-6"
        >
          <div className="bg-white text-slate-950 px-16 py-8 rounded-[3rem] text-3xl font-black shadow-[0_20px_50px_rgba(234,88,12,0.3)] flex items-center gap-6">
            <Touchpad size={48} className="text-orange-600" />
            TOQUE PARA COMEÇAR
          </div>
          
          <div className="flex gap-8 text-slate-500 font-black text-sm uppercase tracking-[0.3em]">
            <span className="flex items-center gap-2"><Utensils size={16} /> Consumo Local</span>
            <span className="flex items-center gap-2"><Zap size={16} /> Retirada</span>
          </div>
        </motion.div>
      </div>

      {/* Footer / Badge de Segurança */}
      <div className="absolute bottom-12 left-0 w-full text-center opacity-30">
        <div className="flex items-center justify-center gap-2 text-white font-mono text-xs uppercase tracking-widest">
          <Sparkles size={14} className="text-orange-500" /> MesaFlow Totem Intelligence v5.0
        </div>
      </div>
    </div>
  );
}

