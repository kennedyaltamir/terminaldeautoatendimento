"use client";

import Link from "next/link";
import { ArrowRight, PlayCircle, CheckCircle2, Sparkles } from "lucide-react";
import Typewriter from "@/components/ui/Typewriter";
import { useLanguage } from "@/context/LanguageContext";
import { useState } from "react";
import DemoModal from "./DemoModal";
import { motion } from "framer-motion";

export default function Hero() {
  const { t } = useLanguage();
  const [isDemoOpen, setIsDemoOpen] = useState(false);

  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden min-h-[95vh] flex items-center">
      {/* VÍDEO BACKGROUND COM OVERLAY GRADIENTE */}
      <div className="absolute inset-0 w-full h-full z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/90 via-slate-900/80 to-slate-950 z-10"></div>
        <video 
          autoPlay 
          loop 
          muted 
          playsInline 
          className="w-full h-full object-cover opacity-60"
          poster="https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        >
          <source src="/hero-video.mp4" type="video/mp4" />
        </video>
      </div>

      <div className="max-w-7xl mx-auto px-6 text-center relative z-20">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-xl border border-white/20 rounded-full px-4 py-2 mb-8 shadow-2xl"
        >
          <Sparkles size={16} className="text-orange-400 animate-pulse" />
          <span className="text-sm font-bold text-orange-100 tracking-wide uppercase">
            Onde a tecnologia encontra a hospitalidade
          </span>
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="heading-hero text-white mb-8"
        >
          {t.hero.title_prefix} <br className="hidden md:block" />
          <Typewriter words={t.hero.typewriter} />
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
          className="text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed mb-12 font-medium"
        >
          {t.hero.subtitle}
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4, delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-6"
        >
          <Link 
            href="/admin/register" 
            className="btn-primary text-xl px-10 py-5"
          >
            {t.hero.cta_primary} <ArrowRight size={24} />
          </Link>
          <button 
            onClick={() => setIsDemoOpen(true)}
            className="w-full sm:w-auto px-10 py-5 bg-white/5 backdrop-blur-md text-white border border-white/10 rounded-2xl font-bold text-xl hover:bg-white/10 transition-all flex items-center justify-center gap-3"
          >
            <PlayCircle size={24} className="text-orange-400" /> {t.hero.cta_secondary}
          </button>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-20 flex flex-wrap items-center justify-center gap-8 text-sm font-bold text-slate-400 uppercase tracking-widest"
        >
          {t.hero.stats.map((stat, i) => (
            <span key={i} className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5">
              <CheckCircle2 size={18} className="text-emerald-500"/> {stat}
            </span>
          ))}
        </motion.div>
      </div>

      <DemoModal isOpen={isDemoOpen} onClose={() => setIsDemoOpen(false)} />
    </section>
  );
}
