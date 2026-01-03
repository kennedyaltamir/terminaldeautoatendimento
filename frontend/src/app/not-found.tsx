"use client";

import Link from "next/link";
import { ChefHat, Home, ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6 text-center font-sans">
      <div className="bg-white p-8 md:p-12 rounded-3xl shadow-xl border border-gray-100 max-w-lg w-full relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-orange-500 to-red-600"></div>
        
        <div className="w-20 h-20 bg-orange-50 rounded-full flex items-center justify-center mx-auto mb-6 text-orange-600">
          <ChefHat size={40} />
        </div>
        
        <h1 className="text-6xl font-black text-gray-900 mb-2">404</h1>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Ops! Pedido não encontrado.</h2>
        <p className="text-gray-500 mb-8 leading-relaxed">
          Parece que a página que você está procurando foi removida do cardápio ou nunca existiu.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <button 
            onClick={() => window.history.back()}
            className="flex-1 py-3 px-6 rounded-xl border border-gray-200 text-gray-700 font-bold hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
          >
            <ArrowLeft size={18} /> Voltar
          </button>
          <Link 
            href="/" 
            className="flex-1 py-3 px-6 rounded-xl bg-orange-600 text-white font-bold hover:bg-orange-700 transition-colors flex items-center justify-center gap-2 shadow-lg shadow-orange-200"
          >
            <Home size={18} /> Ir para Home
          </Link>
        </div>
      </div>
      
      <p className="mt-8 text-xs text-gray-400 font-mono">ERROR_CODE: PAGE_NOT_FOUND_IN_KITCHEN</p>
    </div>
  );
}