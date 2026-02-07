/**
 * DOMAIN: FRONTEND / KIOSK
 * LAST_MODIFIED: 2026-01-27 23:30:00
 * DESCRIPTION: Kiosk Page - FIX: Hydration Mismatch resolvido.
 */
"use client";
import React, { useEffect, useState, useMemo, use } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Touchpad, Sparkles, WifiOff, Globe } from "lucide-react";
import { useKiosk } from "@/context/KioskContext";
import { useLanguage } from "@/context/LanguageContext";
import Logo from "@/components/ui/Logo";
import KioskStealthTrigger from "@/components/kiosk/KioskStealthTrigger";

export default function KioskAttractScreen({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  const router = useRouter();
  const { state, isOffline } = useKiosk();
  const { t, locale } = useLanguage();
  const [mounted, setMounted] = useState(false);
  const [particleData, setParticleData] = useState<any[]>([]);

  useEffect(() => {
    setMounted(true);
    const data = [...Array(6)].map((_, i) => ({
      id: i,
      size: Math.random() * 400 + 100,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      duration: Math.random() * 15 + 10,
      xMove: Math.random() * 150 - 75,
      yMove: Math.random() * 150 - 75,
    }));
    setParticleData(data);
  }, []);

  const handleStart = () => {
    if (state === "BREACHED" || state === "UNLOCKING") return;
    router.push(`/${slug}/menu?kiosk=true`);
  };

  if (!mounted) return <div className="h-screen w-screen bg-slate-950" />;

  return (
    <div onClick={handleStart} className="relative h-screen w-screen flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-slate-950 select-none touch-none">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent z-10" />
        <motion.img initial={{ scale: 1.0 }} animate={{ scale: 1.15 }} transition={{ duration: 30, repeat: Infinity, repeatType: "reverse" }} src="https://images.pexels.com/photos/1639562/pexels-photo-1639562.jpeg?auto=compress&cs=tinysrgb&w=1920" className="w-full h-full object-cover opacity-40" alt="Background" />
      </div>
      <div className="absolute inset-0 z-1 overflow-hidden pointer-events-none">
        {particleData.map((p) => (
          <div key={p.id} className="absolute" style={{ left: p.left, top: p.top }}>
            <motion.div className="bg-orange-500/10 rounded-full blur-[100px]" animate={{ width: p.size, height: p.size, x: [0, p.xMove, 0], y: [0, p.yMove, 0], opacity: [0.2, 0.4, 0.2] }} transition={{ duration: p.duration, repeat: Infinity, ease: "easeInOut" }} />
          </div>
        ))}
      </div>
      <div className="relative z-10 text-center px-10 flex flex-col items-center">
        <motion.div initial={{ y: -50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="mb-16">
          <Logo size="xl" variant="light" animated={true} />
        </motion.div>
        <div className="space-y-6 mb-24">
          <motion.h1 className="text-8xl md:text-[10rem] font-black text-white tracking-tighter leading-none">
            {t.kiosk.attract_title} <br />
            <span className="text-orange-600">{t.kiosk.attract_highlight}</span>
          </motion.h1>
        </div>
        <motion.div animate={{ scale: [1, 1.03, 1] }} transition={{ repeat: Infinity, duration: 2.5 }}>
          <div className="bg-white text-slate-950 px-20 py-10 rounded-[4rem] text-4xl font-black shadow-2xl flex items-center gap-8 hover:bg-gray-50 transition-all active:scale-95">
            <Touchpad size={56} className="text-orange-600" /> {t.kiosk.tap_to_start}
          </div>
        </motion.div>
      </div>
      <KioskStealthTrigger />
    </div> 
  );
}
