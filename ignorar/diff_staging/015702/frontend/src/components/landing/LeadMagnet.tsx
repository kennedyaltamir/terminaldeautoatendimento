"use client";

import { useState } from "react";
import { FileText, Download, Loader2, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function LeadMagnet() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setLoading(true);
    // Simula processamento
    await new Promise(r => setTimeout(r, 2000));
    
    setLoading(false);
    setSuccess(true);
    toast.success("Guia enviado para seu e-mail!");
    
    // Simula o download do arquivo
    const link = document.createElement('a');
    link.href = '#'; // Link fictício
    link.setAttribute('download', 'guia-mesaflow.pdf');
    document.body.appendChild(link);
    // link.click(); // Comentado para não disparar download real no teste
    document.body.removeChild(link);
  };

  return (
    <section className="py-24 bg-orange-600 relative overflow-hidden">
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full -translate-x-1/2 -translate-y-1/2"></div>
      </div>

      <div className="max-w-5xl mx-auto px-6 relative z-10">
        <div className="bg-white rounded-[2.5rem] p-8 md:p-16 shadow-2xl flex flex-col md:flex-row items-center gap-12">
          <div className="bg-orange-100 p-8 rounded-3xl text-orange-600 shrink-0">
            <FileText size={80} strokeWidth={1.5} />
          </div>

          <div className="flex-1 text-center md:text-left">
            <h2 className="text-3xl md:text-4xl font-black text-slate-900 mb-4 leading-tight">
              Baixe o Guia: <br />
              <span className="text-orange-600">Atendimento em Escala</span>
            </h2>
            <p className="text-slate-500 text-lg mb-8">
              Aprenda como grandes arenas e redes de fast-food eliminam filas usando tecnologia de autoatendimento.
            </p>

            {success ? (
              <div className="flex items-center gap-3 text-emerald-600 font-bold animate-in fade-in slide-in-from-left-2">
                <CheckCircle2 size={24} />
                <span>Verifique sua caixa de entrada! O PDF foi enviado.</span>
              </div>
            ) : (
              <form onSubmit={handleDownload} className="flex flex-col sm:flex-row gap-3">
                <input 
                  type="email" 
                  required
                  placeholder="Seu e-mail profissional"
                  className="flex-1 px-6 py-4 rounded-2xl bg-slate-100 border-none outline-none focus:ring-2 focus:ring-orange-500 transition-all font-medium"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <button 
                  type="submit"
                  disabled={loading}
                  className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-2xl font-black flex items-center justify-center gap-2 transition-all shadow-lg shadow-orange-200 active:scale-95 disabled:opacity-50"
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : <><Download size={20} /> Baixar Grátis</>}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
