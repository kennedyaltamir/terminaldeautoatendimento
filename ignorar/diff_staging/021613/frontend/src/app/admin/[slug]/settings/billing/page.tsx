"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getCompanySettings } from "@/lib/api";
import { Check, Zap, ArrowRight, Loader2, AlertCircle } from "lucide-react";
import { toast, Toaster } from "sonner";
import { Company } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function BillingPage() {
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    if (searchParams.get("billing") === "success") {
      toast.success("Assinatura ativada com sucesso! 🎉");
      router.replace(window.location.pathname);
    } else if (searchParams.get("billing") === "cancel") {
      toast.error("Pagamento cancelado.");
    }
    getCompanySettings()
      .then(setCompany)
      .finally(() => setLoading(false));
  }, [searchParams, router]);

  const handleUpgrade = async () => {
    setProcessing(true);
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${API_URL}/admin/billing/upgrade`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Falha ao iniciar checkout");
      const data = await res.json();
      if (data.url) window.location.href = data.url;
    } catch (e) {
      toast.error("Erro ao conectar com Stripe");
    } finally {
      setProcessing(false);
    }
  };

  const handlePortal = async () => {
    setProcessing(true);
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${API_URL}/admin/billing/portal`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Falha ao abrir portal");
      const data = await res.json();
      if (data.url) window.location.href = data.url;
    } catch (e) {
      toast.error("Erro ao abrir portal");
    } finally {
      setProcessing(false);
    }
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-white"><Loader2 className="animate-spin" /></div>;
  if (!company) return null;

  const isPro = company.plan_tier === "pro" || company.plan_tier === "enterprise";

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 font-sans">
      <Toaster position="top-center" richColors />
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Planos & Assinatura</h1>
          <p className="text-gray-400 text-lg">Escolha o plano ideal para escalar sua operação.</p>
        </div>
        <div className="grid md:grid-cols-2 gap-8">
          <div className={`bg-gray-800 rounded-3xl p-8 border-2 ${!isPro ? 'border-gray-600' : 'border-gray-700 opacity-60'}`}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-2xl font-bold">Start</h3>
                <p className="text-gray-400">Para validar a ideia.</p>
              </div>
              <span className="bg-gray-700 px-3 py-1 rounded-full text-xs font-bold uppercase">Grátis</span>
            </div>
            <div className="text-4xl font-bold mb-8">R$ 0<span className="text-lg text-gray-500 font-normal">/mês</span></div>
            <ul className="space-y-4 mb-8 text-gray-300">
              <li className="flex gap-3"><Check className="text-gray-500" /> Até 50 pedidos/mês</li>
              <li className="flex gap-3"><Check className="text-gray-500" /> Cardápio Digital Básico</li>
              <li className="flex gap-3"><Check className="text-gray-500" /> 1 Usuário Admin</li>
            </ul>
            <button type="button" disabled className="w-full py-4 rounded-xl border border-gray-600 text-gray-500 font-bold cursor-not-allowed">
              {isPro ? "Plano Anterior" : "Plano Atual"}
            </button>
          </div>
          <div className={`bg-gray-800 rounded-3xl p-8 border-2 relative overflow-hidden ${isPro ? 'border-green-500' : 'border-orange-500 shadow-[0_0_40px_rgba(234,88,12,0.2)]'}`}>
            {!isPro && (
              <div className="absolute top-0 right-0 bg-orange-600 text-white text-xs font-bold px-4 py-1 rounded-bl-xl">
                RECOMENDADO
              </div>
            )}
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-2xl font-bold flex items-center gap-2">
                  Pro <Zap className="text-orange-500 fill-orange-500" size={20} />
                </h3>
                <p className="text-gray-400">Para operações reais.</p>
              </div>
              {isPro && <span className="bg-green-900 text-green-400 px-3 py-1 rounded-full text-xs font-bold uppercase border border-green-700">Ativo</span>}
            </div>
            <div className="text-4xl font-bold mb-8">R$ 149<span className="text-lg text-gray-500 font-normal">/mês</span></div>
            <ul className="space-y-4 mb-8 text-white">
              <li className="flex gap-3"><Check className="text-green-500" /> <b>Pedidos Ilimitados</b></li>
              <li className="flex gap-3"><Check className="text-green-500" /> KDS (Monitor de Cozinha)</li>
              <li className="flex gap-3"><Check className="text-green-500" /> Gestão de Estoque</li>
            </ul>
            <button 
              type="button"
              onClick={isPro ? handlePortal : handleUpgrade}
              disabled={processing}
              className="w-full py-4 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-bold transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95"
            >
              {processing ? <Loader2 className="animate-spin" /> : isPro ? "Gerenciar Assinatura" : <>Assinar Agora <ArrowRight size={20} /></>}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
