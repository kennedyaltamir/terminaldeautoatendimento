"use client";

import { FileText, Download } from "lucide-react";

export default function LeadMagnet() {
  return (
    <section className="py-24 bg-orange-50 border-t border-orange-100">
      <div className="max-w-4xl mx-auto px-6 flex flex-col md:flex-row items-center gap-8">
        <div className="bg-white p-6 rounded-2xl shadow-xl rotate-3 border border-gray-100">
          <div className="w-48 h-64 bg-gray-100 rounded-lg flex items-center justify-center flex-col gap-4 border-2 border-dashed border-gray-300">
            <FileText size={48} className="text-orange-500" />
            <span className="text-xs font-bold text-gray-400">CAPA DO EBOOK</span>
          </div>
        </div>
        
        <div className="flex-1 text-center md:text-left">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Não está pronto para comprar?</h2>
          <p className="text-gray-600 mb-6 text-lg">
            Baixe nosso guia gratuito: <b>"O Guia Definitivo da Automação de Atendimento 2026"</b> e aprenda como grandes redes estão eliminando filas.
          </p>
          
          <form className="flex flex-col sm:flex-row gap-3" onSubmit={(e) => e.preventDefault()}>
            <input 
              type="email" 
              placeholder="Seu melhor e-mail profissional" 
              className="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <button className="bg-gray-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition-colors flex items-center justify-center gap-2">
              <Download size={18} /> Baixar PDF
            </button>
          </form>
          <p className="text-xs text-gray-400 mt-3">Prometemos zero spam. Apenas conteúdo de alto nível.</p>
        </div>
      </div>
    </section>
  );
}