"use client";
import { Smartphone, Cloud, Server, Database } from "lucide-react";

export default function Workflow() {
  return (
    <section className="py-24 bg-gray-900 text-white overflow-hidden relative">
      {/* Background Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:4rem_4rem]"></div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-20">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Arquitetura de Baixa Latência</h2>
          <p className="text-gray-400">Como processamos milhares de pedidos simultâneos em milissegundos.</p>
        </div>

        <div className="flex flex-col md:flex-row justify-center items-center gap-12 md:gap-24">
          
          {/* Step 1: Cliente */}
          <div className="relative group">
            <div className="w-24 h-24 bg-gray-800 rounded-2xl border border-gray-700 flex items-center justify-center z-10 relative group-hover:border-orange-500 transition-colors">
              <Smartphone size={40} className="text-gray-400 group-hover:text-orange-500 transition-colors" />
            </div>
            <p className="text-center mt-4 font-bold text-sm text-gray-400">Cliente</p>
            
            {/* Particle Animation */}
            <div className="absolute top-1/2 left-full w-24 h-[2px] bg-gray-800 hidden md:block overflow-hidden">
              <div className="w-8 h-full bg-orange-500 animate-[shimmer_2s_infinite]"></div>
            </div>
          </div>

          {/* Step 2: Cloud */}
          <div className="relative group">
            <div className="w-32 h-32 bg-gray-800 rounded-full border-2 border-dashed border-gray-700 flex items-center justify-center z-10 relative animate-[spin_10s_linear_infinite]">
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
               <Cloud size={48} className="text-blue-500" />
            </div>
            <p className="text-center mt-4 font-bold text-sm text-gray-400">MesaFlow Cloud</p>

             {/* Particle Animation */}
             <div className="absolute top-1/2 left-full w-24 h-[2px] bg-gray-800 hidden md:block overflow-hidden">
              <div className="w-8 h-full bg-green-500 animate-[shimmer_2s_infinite_0.5s]"></div>
            </div>
          </div>

          {/* Step 3: Cozinha */}
          <div className="relative group">
            <div className="w-24 h-24 bg-gray-800 rounded-2xl border border-gray-700 flex items-center justify-center z-10 relative group-hover:border-green-500 transition-colors">
              <Server size={40} className="text-gray-400 group-hover:text-green-500 transition-colors" />
            </div>
            <p className="text-center mt-4 font-bold text-sm text-gray-400">KDS Cozinha</p>
          </div>

        </div>
      </div>
    </section>
  );
}