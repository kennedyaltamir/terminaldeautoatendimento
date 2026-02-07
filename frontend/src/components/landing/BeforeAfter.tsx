"use client";
import { useState, useRef } from "react";
import { MoveHorizontal } from "lucide-react";

export default function BeforeAfter() {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
    const percentage = (x / rect.width) * 100;
    setSliderPosition(percentage);
  };

  return (
    <section className="py-24 bg-gray-900 text-white overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 text-center mb-12">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">A diferença é brutal.</h2>
        <p className="text-gray-400">Veja como sua operação muda com o MesaFlow.</p>
      </div>

      <div className="max-w-5xl mx-auto px-6">
        <div 
          ref={containerRef}
          onMouseMove={handleMouseMove}
          className="relative w-full h-[400px] md:h-[600px] rounded-3xl overflow-hidden cursor-col-resize border-4 border-gray-800 shadow-2xl"
        >
          {/* Imagem DEPOIS (MesaFlow) - Fundo */}
          <div className="absolute inset-0 bg-gradient-to-br from-green-900 to-gray-900 flex items-center justify-center">
            <div className="text-center">
              <h3 className="text-4xl font-bold text-green-400 mb-2">Com MesaFlow</h3>
              <p className="text-green-200">Pedidos digitais, cozinha silenciosa, clientes felizes.</p>
              {/* Aqui entraria uma imagem real de um restaurante moderno */}
              <div className="mt-8 grid grid-cols-2 gap-4 opacity-50">
                <div className="bg-green-500/20 p-4 rounded-lg">KDS Ativo</div>
                <div className="bg-green-500/20 p-4 rounded-lg">Zero Filas</div>
              </div>
            </div>
          </div>

          {/* Imagem ANTES (Caos) - Sobreposta com Clip Path */}
          <div 
            className="absolute inset-0 bg-gradient-to-br from-red-900 to-gray-800 flex items-center justify-center border-r-4 border-white"
            style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
          >
            <div className="text-center">
              <h3 className="text-4xl font-bold text-red-400 mb-2">Sem Sistema</h3>
              <p className="text-red-200">Garçons correndo, pedidos errados, clientes esperando.</p>
              {/* Aqui entraria uma imagem real de caos */}
              <div className="mt-8 grid grid-cols-2 gap-4 opacity-50">
                <div className="bg-red-500/20 p-4 rounded-lg">Papelada</div>
                <div className="bg-red-500/20 p-4 rounded-lg">Gritos</div>
              </div>
            </div>
          </div>

          {/* Slider Handle */}
          <div 
            className="absolute top-0 bottom-0 w-1 bg-white cursor-col-resize z-20 flex items-center justify-center"
            style={{ left: `${sliderPosition}%` }}
          >
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg text-gray-900">
              <MoveHorizontal size={20} />
            </div>
          </div>
        </div>
        <p className="text-center text-xs text-gray-500 mt-4">Arraste para comparar</p>
      </div>
    </section>
  );
}