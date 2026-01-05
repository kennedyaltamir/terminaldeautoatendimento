"use client";

import { useRouter } from "next/navigation";
import { ChefHat, Touchpad } from "lucide-react";
import { motion } from "framer-motion";

export default function KioskAttractScreen({ params }: { params: { slug: string } }) {
  const router = useRouter();

  const handleStart = () => {
    // Redireciona para o menu com flag de kiosk para esconder elementos desnecessários
    router.push(`/${params.slug}/menu?kiosk=true`);
  };

  return (
    <div 
      onClick={handleStart}
      className="relative min-h-screen flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-black"
    >
      {/* Background Video/Image */}
      <div className="absolute inset-0 opacity-40">
        <img 
          src="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" 
          className="w-full h-full object-cover animate-pulse duration-[10s]"
          alt="Background"
        />
      </div>
      
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/50"></div>

      <div className="relative z-10 text-center space-y-8 p-6">
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="bg-orange-600 w-32 h-32 rounded-full flex items-center justify-center mx-auto shadow-[0_0_60px_rgba(234,88,12,0.6)]"
        >
          <ChefHat size={64} className="text-white" />
        </motion.div>

        <div className="space-y-2">
          <h1 className="text-6xl md:text-8xl font-black text-white tracking-tight drop-shadow-2xl">
            Fome de quê?
          </h1>
          <p className="text-2xl md:text-3xl text-gray-200 font-light">
            Peça aqui e retire no balcão.
          </p>
        </div>

        <motion.div 
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="pt-12"
        >
          <div className="bg-white text-black px-12 py-6 rounded-full text-2xl font-bold shadow-xl flex items-center gap-4 mx-auto w-fit">
            <Touchpad size={32} />
            TOQUE PARA COMEÇAR
          </div>
        </motion.div>
      </div>

      <div className="absolute bottom-8 text-gray-500 text-sm font-mono">
        MesaFlow Kiosk v2.0 • {params.slug}
      </div>
    </div>
  );
}
