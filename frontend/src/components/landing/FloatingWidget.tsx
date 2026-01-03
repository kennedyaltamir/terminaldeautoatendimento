"use client";
import { useState, useEffect } from "react";
import { MessageCircle, X, FileText } from "lucide-react";

export default function FloatingWidget() {
  const [showExitIntent, setShowExitIntent] = useState(false);
  const [hasShownExit, setHasShownExit] = useState(false);

  useEffect(() => {
    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 0 && !hasShownExit && !sessionStorage.getItem("exit_intent_shown")) {
        setShowExitIntent(true);
        setHasShownExit(true);
        sessionStorage.setItem("exit_intent_shown", "true");
      }
    };

    document.addEventListener("mouseleave", handleMouseLeave);
    return () => document.removeEventListener("mouseleave", handleMouseLeave);
  }, [hasShownExit]);

  return (
    <>
      {/* WhatsApp Button */}
      <a 
        href="https://wa.me/5511999999999" 
        target="_blank"
        className="fixed bottom-6 right-6 bg-green-500 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition-transform z-40 flex items-center justify-center"
        title="Falar com Vendas"
      >
        <MessageCircle size={28} />
      </a>

      {/* Exit Intent Modal */}
      {showExitIntent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl p-8 max-w-md text-center shadow-2xl relative">
            <button onClick={() => setShowExitIntent(false)} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"><X size={24}/></button>
            <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="text-orange-600" size={32} />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Espere! Não vá ainda.</h3>
            <p className="text-gray-600 mb-6">Baixe nosso <b>Guia de Gestão de Filas para Grandes Eventos</b> gratuitamente.</p>
            <button className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors">
              Baixar PDF Grátis
            </button>
            <button onClick={() => setShowExitIntent(false)} className="mt-4 text-sm text-gray-400 hover:text-gray-600 underline">
              Não, obrigado.
            </button>
          </div>
        </div>
      )}
    </>
  );
}