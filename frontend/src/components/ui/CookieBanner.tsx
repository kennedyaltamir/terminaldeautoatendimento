"use client";

import { useState, useEffect } from "react";
import { Cookie, X } from "lucide-react";

export default function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Verifica se já houve consentimento
    const consent = localStorage.getItem("mesaflow_cookie_consent");
    if (!consent) {
      // Pequeno delay para a animação ficar suave
      const timer = setTimeout(() => setIsVisible(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem("mesaflow_cookie_consent", "true");
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm z-[100] animate-in slide-in-from-bottom-4 fade-in duration-700">
      <div className="bg-gray-900/95 backdrop-blur-md text-white p-6 rounded-2xl shadow-2xl border border-gray-800">
        <div className="flex items-start justify-between gap-4">
          <div className="bg-orange-600/20 p-2 rounded-full text-orange-500">
            <Cookie size={24} />
          </div>
          <button onClick={() => setIsVisible(false)} className="text-gray-500 hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>
        
        <h4 className="font-bold text-lg mt-4 mb-2">Nós usamos cookies 🍪</h4>
        <p className="text-sm text-gray-400 leading-relaxed mb-6">
          Utilizamos cookies para melhorar sua experiência, analisar o tráfego e personalizar o conteúdo. Ao continuar, você concorda com nossa Política de Privacidade.
        </p>
        
        <div className="flex gap-3">
          <button 
            onClick={() => setIsVisible(false)}
            className="flex-1 py-2.5 rounded-xl border border-gray-700 text-sm font-bold hover:bg-gray-800 transition-colors"
          >
            Recusar
          </button>
          <button 
            onClick={handleAccept}
            className="flex-1 py-2.5 rounded-xl bg-orange-600 text-sm font-bold hover:bg-orange-700 transition-colors shadow-lg shadow-orange-900/20"
          >
            Aceitar
          </button>
        </div>
      </div>
    </div>
  );
}