"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useKiosk } from "@/context/KioskContext";
import { Touchpad, Utensils } from "lucide-react";
import Logo from "@/components/ui/Logo";

export default function KioskScreensaver() {
  const { isIdle, resetIdleTimer } = useKiosk();

  return (
    <AnimatePresence>
      {isIdle && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={resetIdleTimer}
          className="fixed inset-0 z-[9999] bg-black flex flex-col items-center justify-center cursor-pointer"
        >
          {/* Vídeo ou Imagem de Fundo */}
          <div className="absolute inset-0 opacity-40">
            <video
              autoPlay
              loop
              muted
              playsInline
              className="w-full h-full object-cover"
            >
              <source src="/hero-video.mp4" type="video/mp4" />
            </video>
          </div>

          {/* Conteúdo de Atração */}
          <div className="relative z-10 text-center space-y-8">
            <motion.div
              animate={{ y: [0, -20, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            >
              <Logo size="xl" variant="light" />
            </motion.div>
            
            <h1 className="text-6xl md:text-8xl font-black text-white tracking-tighter">
              BATEU AQUELA <br />
              <span className="text-orange-500">FOME?</span>
            </h1>

            <div className="flex flex-col items-center gap-4">
              <div className="bg-white/10 backdrop-blur-md border border-white/20 px-8 py-4 rounded-full flex items-center gap-3 text-white animate-pulse">
                <Touchpad size={32} />
                <span className="text-2xl font-bold uppercase tracking-widest">Toque para começar</span>
              </div>
            </div>
          </div>

          {/* Badge de Segurança */}
          <div className="absolute bottom-10 text-white/20 font-mono text-xs uppercase tracking-[0.5em]">
            MesaFlow OS v13.2 • Secure Kiosk Mode
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

