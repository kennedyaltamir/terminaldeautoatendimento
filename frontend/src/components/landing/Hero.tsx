"use client";
import Link from "next/link";
import { ArrowRight, PlayCircle, CheckCircle2 } from "lucide-react";
import Typewriter from "@/components/ui/Typewriter";
import { useLanguage } from "@/context/LanguageContext";

export default function Hero() {
  const { t } = useLanguage();

  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden min-h-[90vh] flex items-center">
      
      {/* VÍDEO BACKGROUND LOCAL */}
      <div className="absolute inset-0 w-full h-full z-0">
        <div className="absolute inset-0 bg-gray-900/80 z-10"></div> {/* Overlay Escuro */}
        <video 
          autoPlay 
          loop 
          muted 
          playsInline 
          className="w-full h-full object-cover"
          // Poster: Imagem que aparece enquanto o vídeo carrega
          poster="https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        >
          {/* Aponta para o arquivo local na pasta public */}
          <source src="/hero-video.mp4" type="video/mp4" />
        </video>
      </div>

      <div className="max-w-7xl mx-auto px-6 text-center relative z-20">
        <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-full px-4 py-1.5 mb-8 shadow-lg animate-in fade-in slide-in-from-bottom-4 duration-700">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span className="text-sm font-medium text-white">{t.hero.badge}</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-black text-white tracking-tight leading-[1.1] mb-6 drop-shadow-xl">
          {t.hero.title_prefix} <br className="hidden md:block" />
          <Typewriter words={t.hero.typewriter} />
        </h1>
        
        <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed mb-10 drop-shadow-md">
          {t.hero.subtitle}
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link 
            href="/admin/register" 
            className="w-full sm:w-auto px-8 py-4 bg-orange-600 text-white rounded-xl font-bold text-lg hover:bg-orange-700 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1 flex items-center justify-center gap-2"
          >
            {t.hero.cta_primary} <ArrowRight size={20} />
          </Link>
          <Link 
            href="/hamburgueria-ze/menu?mesa=1&token=token-seguro-mesa-1" 
            className="w-full sm:w-auto px-8 py-4 bg-white/10 backdrop-blur-md text-white border border-white/20 rounded-xl font-bold text-lg hover:bg-white/20 transition-all flex items-center justify-center gap-2 shadow-sm"
          >
            <PlayCircle size={20} className="text-orange-400" /> {t.hero.cta_secondary}
          </Link>
        </div>

        <div className="mt-12 flex flex-wrap items-center justify-center gap-4 md:gap-8 text-sm font-medium text-gray-300">
          {t.hero.stats.map((stat, i) => (
            <span key={i} className="flex items-center gap-2 bg-black/30 backdrop-blur-sm px-3 py-1 rounded-full border border-white/10">
              <CheckCircle2 size={16} className="text-green-400"/> {stat}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}