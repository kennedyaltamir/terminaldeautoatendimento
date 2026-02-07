"use client";
import { useState } from "react";
import { Smartphone, Tablet, CheckCircle2, Loader2, ChefHat } from "lucide-react";

export default function Simulator() {
  const [step, setStep] = useState<"idle" | "processing" | "done">("idle");

  const handleOrder = () => {
    if (step !== "idle") return;
    setStep("processing");
    setTimeout(() => setStep("done"), 1500);
    setTimeout(() => setStep("idle"), 4000);
  };

  return (
    <section className="py-24 bg-gray-50 dark:bg-gray-950 overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Velocidade Real. Sem Atrito.</h2>
        <p className="text-gray-500 mt-2">Teste a sincronia entre o Cliente e a Cozinha.</p>
      </div>

      <div className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-20">
        
        {/* CLIENTE (CELULAR) */}
        <div className="relative w-64 h-[500px] bg-gray-900 rounded-[3rem] border-8 border-gray-800 shadow-2xl overflow-hidden">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-gray-800 rounded-b-xl z-20"></div>
          <div className="h-full bg-white flex flex-col">
            <div className="bg-orange-600 h-32 p-4 pt-10 text-white">
              <p className="text-xs opacity-80">Mesa 12</p>
              <h3 className="font-bold text-lg">Hamburgueria Zé</h3>
            </div>
            <div className="p-4 flex-1">
              <div className="flex gap-3 mb-4">
                <div className="w-16 h-16 bg-gray-200 rounded-lg"></div>
                <div>
                  <div className="w-24 h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="w-12 h-4 bg-orange-100 rounded"></div>
                </div>
              </div>
              <button 
                onClick={handleOrder}
                disabled={step !== "idle"}
                className={`w-full py-3 rounded-xl font-bold text-white transition-all ${step === "idle" ? "bg-orange-600 hover:bg-orange-700" : "bg-green-500"}`}
              >
                {step === "idle" ? "Fazer Pedido" : step === "processing" ? "Enviando..." : "Enviado!"}
              </button>
            </div>
          </div>
        </div>

        {/* CONEXÃO (Seta Animada) */}
        <div className="hidden md:flex flex-col items-center gap-2">
          <div className={`w-32 h-1 rounded-full transition-all duration-1000 ${step !== "idle" ? "bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.8)]" : "bg-gray-200"}`}></div>
          <span className="text-xs font-mono text-gray-400">WebSocket <br/> &lt; 100ms</span>
        </div>

        {/* COZINHA (TABLET KDS) */}
        <div className="relative w-80 h-56 md:w-96 md:h-64 bg-gray-900 rounded-xl border-8 border-gray-800 shadow-2xl overflow-hidden flex flex-col">
          <div className="bg-gray-800 p-2 flex justify-between items-center border-b border-gray-700">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <span className="text-gray-400 text-xs font-mono">KDS SYSTEM</span>
          </div>
          <div className="bg-gray-900 p-4 flex-1 relative">
            {step === "done" && (
              <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-10 animate-in fade-in zoom-in">
                <div className="bg-white text-gray-900 px-6 py-3 rounded-full font-bold shadow-xl flex items-center gap-2">
                  <ChefHat className="text-orange-600"/> Novo Pedido!
                </div>
              </div>
            )}
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-gray-800 p-2 rounded border-l-4 border-green-500 h-24"></div>
              <div className={`bg-gray-800 p-2 rounded border-l-4 border-yellow-500 h-24 transition-all duration-500 ${step === "done" ? "opacity-100 scale-100" : "opacity-0 scale-95"}`}>
                <div className="w-10 h-3 bg-gray-700 rounded mb-2"></div>
                <div className="w-20 h-2 bg-gray-700 rounded"></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}