"use client";

import { useState } from "react";
import { CreditCard, Zap, Check, ExternalLink, Loader2, AlertCircle } from "lucide-react";
import { toast } from "sonner";
import { Company } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function BillingSection({ company }: { company: Company }) {
  const [loading, setLoading] = useState(false);

  const handleUpgrade = async () => {
    setLoading(true);
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
      setLoading(false);
    }
  };

  const handlePortal = async () => {
    setLoading(true);
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
      toast.error("Erro ao abrir portal de cobrança");
    } finally {
      setLoading(false);
    }
  };

  const isPro = company.plan_tier === "pro" || company.plan_tier === "enterprise";
  const statusLabel = company.subscription_status === 'active' ? 'Ativo' : 
                      company.subscription_status === 'past_due' ? 'Pagamento Pendente' : 
                      company.subscription_status === 'canceled' ? 'Cancelado' : 'Gratuito';

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 space-y-6 animate-in fade-in">
      <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
        <div>
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <CreditCard className="text-orange-500" /> Plano & Assinatura
          </h3>
          <p className="text-gray-400 text-sm mt-1">Status atual: <span className="text-white font-bold uppercase">{statusLabel}</span></p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${isPro ? 'bg-green-900 text-green-400 border border-green-700' : 'bg-gray-700 text-gray-300 border border-gray-600'}`}>
          {company.plan_tier}
        </span>
      </div>

      {!isPro ? (
        <div className="bg-gradient-to-br from-orange-900/40 to-gray-900 border border-orange-500/30 rounded-xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-orange-600/10 rounded-full blur-2xl -mr-16 -mt-16"></div>
          
          <div className="relative z-10">
            <h4 className="text-orange-500 font-bold text-lg mb-2 flex items-center gap-2">
              <Zap size={20} className="fill-orange-500" /> Desbloqueie o MesaFlow Pro
            </h4>
            <p className="text-gray-300 text-sm mb-6">Remova todos os limites e leve sua operação para o próximo nível.</p>
            
            <div className="grid sm:grid-cols-2 gap-3 mb-8">
              {["Pedidos Ilimitados", "KDS de Cozinha em Tempo Real", "Gestão de Estoque (Ficha Técnica)", "Múltiplos Usuários (Garçom/Cozinha)", "Suporte Prioritário WhatsApp", "Sem taxas sobre vendas"].map(f => (
                <li key={f} className="flex items-center gap-2 text-gray-300 text-xs font-medium">
                  <Check size={14} className="text-green-500 shrink-0" /> {f}
                </li>
              ))}
            </div>

            <button 
              onClick={handleUpgrade}
              disabled={loading}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-orange-500/20 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Zap size={18} className="fill-white"/>}
              Assinar Agora - R$ 149/mês
            </button>
            <p className="text-center text-xs text-gray-500 mt-3">Cancelamento a qualquer momento. 7 dias grátis.</p>
          </div>
        </div>
      ) : (
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-4">
            <div className="bg-green-900/30 p-3 rounded-full text-green-500">
              <Check size={24} />
            </div>
            <div>
              <p className="text-white font-bold">Assinatura Ativa</p>
              <p className="text-xs text-gray-500">Próxima cobrança automática no cartão.</p>
            </div>
          </div>
          <button 
            onClick={handlePortal}
            disabled={loading}
            className="text-gray-300 hover:text-white text-sm font-bold flex items-center gap-2 bg-gray-800 hover:bg-gray-700 px-6 py-3 rounded-xl transition-all border border-gray-600"
          >
            {loading ? <Loader2 className="animate-spin" size={16} /> : <ExternalLink size={16} />}
            Gerenciar Pagamento
          </button>
        </div>
      )}

      {company.subscription_status === 'past_due' && (
        <div className="bg-red-900/20 border border-red-800 text-red-200 p-4 rounded-xl flex items-center gap-3">
          <AlertCircle className="shrink-0" />
          <div className="text-sm">
            <p className="font-bold">Pagamento Pendente</p>
            <p>Houve um problema com seu cartão. Atualize seus dados no portal para evitar bloqueio.</p>
          </div>
        </div>
      )}
    </div>
  );
}