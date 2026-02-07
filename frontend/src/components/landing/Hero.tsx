/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 11.12 (UI Alignment Fix)
 * DNA_ID: MF-HERO-V11-12
 * Objective: Fix CTA button layout and visual hierarchy.
 */
"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ArrowRight, PlayCircle, CheckCircle2, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import Typewriter from "@/components/ui/Typewriter";
import { useLanguage } from "@/context/LanguageContext";
import DemoModal from "./DemoModal";

export default function Hero() {
  const { t } = useLanguage();
  const [isDemoOpen, setIsDemoOpen] = useState(false);

  if (!t || !t.hero) return null;

  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden min-h-[95vh] flex items-center">
      {/* VÍDEO BACKGROUND */}
      <div className="absolute inset-0 w-full h-full z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-black/90 via-black/60 to-black z-10"></div>
        <video 
          autoPlay 
          loop 
          muted 
          playsInline 
          className="w-full h-full object-cover opacity-40"
        >
          <source src="/hero-video.mp4" type="video/mp4" />
        </video>
      </div>

      <div className="max-w-7xl mx-auto px-6 text-center relative z-20">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 bg-orange-600/10 backdrop-blur-xl border border-orange-500/20 rounded-full px-4 py-2 mb-8"
        >
          <Sparkles size={16} className="text-orange-500 animate-pulse" />
          <span className="text-[10px] font-black text-orange-500 tracking-[0.2em] uppercase">
            {t.hero.badge}
          </span>
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="heading-hero text-white mb-8"
        >
          {t.hero.title_prefix} <br />
          <Typewriter words={t.hero.typewriter} />
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed mb-12 font-medium"
        >
          {t.hero.subtitle}
        </motion.p>

        {/* 🛡️ FIX: Container de botões com alinhamento e classes corrigidas */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <Link 
            href="/admin/register" 
            className="btn-primary w-full sm:w-auto px-10 py-6 text-lg"
          >
            {t.hero.cta_primary} 
            <ArrowRight size={22} strokeWidth={3} />
          </Link>

          <button 
            onClick={() => setIsDemoOpen(true)}
            className="btn-secondary w-full sm:w-auto px-10 py-6 text-lg"
          >
            <PlayCircle size={22} className="text-orange-500" /> 
            {t.hero.cta_secondary}
          </button>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-20 flex flex-wrap items-center justify-center gap-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]"
        >
          {t.hero.stats.map((stat: string, i: number) => (
            <span key={i} className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5">
              <CheckCircle2 size={14} className="text-emerald-500"/> {stat}
            </span>
          ))}
        </motion.div>
      </div>

      <DemoModal isOpen={isDemoOpen} onClose={() => setIsDemoOpen(false)} />
    </section>
  );
}