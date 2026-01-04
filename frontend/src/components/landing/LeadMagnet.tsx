"use client";

import { useState } from "react";
import { FileText, Download, Loader2, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function LeadMagnet() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source: "footer_magnet" })
      });

      if (res.ok) {
        setSuccess(true);
        toast.success("E-mail cadastrado com sucesso!");
        // Simula download
        setTimeout(() => {
            window.open("https://mesaflow.com/assets/guia-eficiencia-2026.pdf", "_blank");
        }, 1500);
      } else {
        toast.error("Erro ao cadastrar. Tente novamente.");
      }
    } catch (error) {
      console.error(error);
      toast.error("Erro de conexão.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="py-24 bg-orange-50 border-t border-orange-100">
      <div className="max-w-4xl mx-auto px-6 flex flex-col md:flex-row items-center gap-8">
        <div className="bg-white p-6 rounded-2xl shadow-xl rotate-3 border border-gray-100">
          <div className="w-48 h-64 bg-gray-100 rounded-lg flex items-center justify-center flex-col gap-4 border-2 border-dashed border-gray-300 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-100 to-white opacity-50"></div>
            <FileText size={48} className="text-orange-500 relative z-10" />
            <span className="text-xs font-bold text-gray-500 relative z-10 text-center px-4">GUIA DE EFICIÊNCIA 2026</span>
          </div>
        </div>
        
        <div className="flex-1 text-center md:text-left">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Ainda não tem certeza?</h2>
          <p className="text-gray-600 mb-6 text-lg">
            Baixe nosso guia gratuito: <b>"Como reduzir custos operacionais em 30% automatizando o atendimento"</b> e aprenda as estratégias das grandes redes.
          </p>
          
          {success ? (
            <div className="bg-green-100 text-green-800 p-4 rounded-xl flex items-center gap-3 font-bold animate-in fade-in">
                <CheckCircle2 size={24} />
                <div>
                    <p>Sucesso! O download iniciará em instantes.</p>
                    <p className="text-xs font-normal">Verifique também seu e-mail.</p>
                </div>
            </div>
          ) : (
            <form className="flex flex-col sm:flex-row gap-3" onSubmit={handleSubmit}>
                <input 
                type="email" 
                required
                placeholder="Seu melhor e-mail profissional" 
                className="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-orange-500 outline-none"
                value={email}
                onChange={e => setEmail(e.target.value)}
                />
                <button 
                disabled={loading}
                className="bg-gray-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
                >
                {loading ? <Loader2 className="animate-spin" /> : <Download size={18} />} 
                Baixar PDF
                </button>
            </form>
          )}
          <p className="text-xs text-gray-400 mt-3">Prometemos zero spam. Apenas conteúdo de alto nível.</p>
        </div>
      </div>
    </section>
  );
}