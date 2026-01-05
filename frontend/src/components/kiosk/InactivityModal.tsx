"use client";

import { useState, useEffect } from "react";
import { Clock, AlertCircle } from "lucide-react";

interface InactivityModalProps {
  isOpen: boolean;
  onStay: () => void;
  onTimeout: () => void;
  countdownDuration?: number; // Segundos
}

export default function InactivityModal({ isOpen, onStay, onTimeout, countdownDuration = 10 }: InactivityModalProps) {
  const [timeLeft, setTimeLeft] = useState(countdownDuration);

  useEffect(() => {
    if (isOpen) {
      setTimeLeft(countdownDuration);
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            onTimeout();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [isOpen, countdownDuration, onTimeout]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="bg-white rounded-3xl p-8 max-w-md w-full text-center shadow-2xl border-4 border-orange-500">
        <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse">
          <Clock size={40} className="text-orange-600" />
        </div>
        
        <h2 className="text-3xl font-black text-gray-900 mb-2">Ainda está aí?</h2>
        <p className="text-gray-500 text-lg mb-8">Sua sessão será encerrada em <span className="font-bold text-orange-600 text-2xl">{timeLeft}</span> segundos para segurança.</p>
        
        <button 
          onClick={onStay}
          className="w-full bg-orange-600 text-white py-5 rounded-2xl font-bold text-xl shadow-lg hover:bg-orange-700 transition-transform active:scale-95"
        >
          Continuar Pedindo
        </button>
      </div>
    </div>
  );
}
