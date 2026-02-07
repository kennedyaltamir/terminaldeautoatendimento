"use client";
import { useState } from "react";
import { X, ArrowRight, Building2, Users, CheckCircle2 } from "lucide-react";
import { useRouter } from "next/navigation";

export default function QualifyModal({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  const [step, setStep] = useState(1);
  const [segment, setSegment] = useState("");
  const router = useRouter();

  if (!isOpen) return null;

  const handleSegment = (seg: string) => {
    setSegment(seg);
    setStep(2);
  };

  const handleFinish = (volume: string) => {
    if (volume === "high") {
      // Cliente Grande -> WhatsApp Vendas
      window.open("https://wa.me/5511999999999?text=Ola,%20sou%20uma%20grande%20operacao%20e%20quero%20conhecer%20o%20MesaFlow", "_blank");
    } else {
      // Cliente Pequeno -> Self Service
      router.push("/admin/register");
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-lg rounded-2xl p-8 shadow-2xl relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"><X size={24}/></button>
        
        {/* Barra de Progresso */}
        <div className="w-full bg-gray-100 h-1 rounded-full mb-8">
          <div className="bg-orange-600 h-1 rounded-full transition-all duration-500" style={{ width: step === 1 ? '50%' : '100%' }}></div>
        </div>

        {step === 1 ? (
          <div className="animate-in slide-in-from-right-4 fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Qual o seu negócio?</h2>
            <p className="text-gray-500 mb-6">Vamos personalizar sua experiência.</p>
            <div className="grid gap-3">
              {['Restaurante / Bar', 'Estádio / Eventos', 'Hotel / Resort', 'Outro'].map((item) => (
                <button key={item} onClick={() => handleSegment(item)} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl hover:border-orange-500 hover:bg-orange-50 transition-all text-left group">
                  <span className="font-medium text-gray-700 group-hover:text-orange-700">{item}</span>
                  <ArrowRight size={18} className="text-gray-300 group-hover:text-orange-500"/>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="animate-in slide-in-from-right-4 fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Qual seu volume mensal?</h2>
            <p className="text-gray-500 mb-6">Para {segment}.</p>
            <div className="grid gap-3">
              <button onClick={() => handleFinish("low")} className="p-4 border border-gray-200 rounded-xl hover:border-green-500 hover:bg-green-50 transition-all text-left">
                <span className="block font-bold text-gray-900">Estou começando</span>
                <span className="text-sm text-gray-500">Menos de 1.000 pedidos/mês</span>
              </button>
              <button onClick={() => handleFinish("high")} className="p-4 border border-gray-200 rounded-xl hover:border-purple-500 hover:bg-purple-50 transition-all text-left">
                <span className="block font-bold text-gray-900">Operação em Escala</span>
                <span className="text-sm text-gray-500">Mais de 1.000 pedidos/mês</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}